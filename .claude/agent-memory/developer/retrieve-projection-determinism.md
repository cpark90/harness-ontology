# retrieve.py 투영 결정성 (read-projection determinism)

`tools/retrieve.py`가 같은 질의에 실행마다 다른 pack을 내던 결함 수정에서 얻은 재사용 지식.
**tools 소스 결함이라 온톨로지 무접촉** — 이런 항목은 `ontology/**` 한 줄도 건드리지 않는다.

## 이 repo의 비결정성 발생원 지도 (tools 공통)

| 지점 | 결정적? | 이유 |
|---|---|---|
| `lib.instance_nodes(g)` | ✗ **set 반환** | 이걸 그대로 순회해 만든 리스트는 순서가 매 프로세스 다름 |
| `lib.instance_edges(g)` | ✗ | `for s,p,o in g` 그래프 순회. **owlrl reasoning이 추론 트리플을 set 순서로 insert**해서 파싱순서 보장이 깨짐 (원본 트리플만이면 rdflib Memory store는 insertion=parse 순서라 안정) |
| `lib.most_specific_types` | ✓ | 내부에서 `sorted()` |
| `g.objects(n, ...)`(asserted only) | 사실상 ✓ | parse 순서. provides/requires 리스트는 실측상 seed 0~9에서 불변 |
| `g.value(...)` | ✓(단일값이면) | prefLabel은 클래스 내 유일 |

→ **set/그래프 순회가 "동점 정렬"에 새면 내용까지 바뀌고, 순위에 안 새면 표시순만 바뀐다.** 둘을 구분해서 진단할 것.

## 수정 패턴 — 총순서(total) 키

```python
def _rank_key(item):            # (node, score)
    node, score = item
    return (-score, str(node))  # 점수만 음수화 → IRI는 오름차순 유지
```
- ★`sorted(..., key=..., reverse=True)` + 2차 문자열 키는 **금물**: 문자열까지 역순이 된다. **점수만 음수화**한다.
- 정렬 키가 IRI까지 포함해 total이면 **입력 리스트 구성 순서(set 순회)는 무해**해진다 → `instance_nodes` 자체를 sorted로 감쌀 필요 없음.
- `traverse`의 heap은 이미 `(-s, str(n), n)`로 총순서였다(3-튜플의 `str(n)`은 tie-break 겸
  **URIRef 비교 예외 회피**). 이미 결정적인 곳은 손대지 말 것 — 랭킹 의미가 바뀐다.
- 엣지 리스트처럼 점수가 없는 목록은 **표시 키(label) 우선 + IRI 튜플 tie-break**로 sorted.

## 의미 보존 증명 방법 (semantic-preservation evidence)

`--format json`으로 **의미 코어**만 뽑아 대조한다: `{budget_used, sorted(node id→relevance),
set(edges), set(candidates), sorted(gaps)}`. 수정 전은 `PYTHONHASHSEED=0..9`로 10변종을 만들어
**모든 변종 vs 수정 후**를 비교하면 "무엇이 원래 흔들렸는지"까지 드러난다.
- 관찰: 공통 노드의 `relevance` 값은 어떤 경우에도 불변(랭킹 함수는 안 건드렸으므로). 바뀔 수 있는 건 **seed 컷 경계의 tie 멤버**뿐.
- **tie 그룹은 클 수 있다**: `"workflow steps and deliverables"`는 컷 점수 1.35에 17개가 동점,
  남은 슬롯 5개 → 수정 전 pack membership이 실제로 6변종. 반면 다른 질의는 seed 목록만
  흔들리고 admitted 노드·budget은 동일했다. **"tie=표시순만" 이라고 가정하지 말고 실측**할 것.

## 회귀 가드

- `tools/check_determinism.py` — 질의별로 **fresh 프로세스 N회**(`PYTHONHASHSEED`를 None/0/1/2로
  **서로 다르게**) 실행해 md5 동일 요구. `make determinism`, CI는 `.github/workflows/validate.yml`
  step 1줄. md는 pack dict의 순수 함수라 json만 봐도 되지만 렌더러까지 both로 검사.
- ★**PYTHONHASHSEED를 고정해서 "고쳤다"고 하면 결함이 숨는다.** 가드는 반드시 시드를 흔든 채 비교.
- 실행비용: retrieve 1회 ≈ 1.8s(그래프 로드+owlrl) → 4질의×4런×2포맷 ≈ 60s.
- **negative control 방법(git 조작 없이)**: `git show HEAD:tools/retrieve.py > scratch/orig.py`(read-only)
  후 `importlib.util.spec_from_file_location`로 가드 모듈을 로드해 `m.RETRIEVE`만 orig로 갈아끼우고
  `m.check(...)` 호출 → 수정 전 코드가 4/4 probe에서 FAIL함을 증명. 가드가 진짜 잡는지 확인 필수.
