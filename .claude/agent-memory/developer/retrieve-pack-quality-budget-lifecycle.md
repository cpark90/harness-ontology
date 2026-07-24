# retrieve 팩 품질: 예산 의미 분리 + lifecycle 랭킹

`tools/retrieve.py`의 **품질** 결함 2건(조기 절단 / 폐기 노드 상위) 수정에서 얻은 지식.
결정성(`retrieve-projection-determinism.md`)과 달리 이쪽은 **어휘(TBox)까지 손대야 풀린다**.

## 1. 한 프로퍼티에 두 의미 = 조용한 팩 절단 (진단 패턴)

증상: 어떤 질의가 `nodes=3, budget_used=125/900`처럼 **예산을 남기고** 끝난다(에러 없음).

- 원인 A(뿌리): `ho:tokenEstimate`가 (i) *이 노드 텍스트를 팩에 실을 비용* 과
  (ii) *이 노드가 서술하는 런타임 관측량* 두 뜻으로 쓰였다. `AreaOfObservation`이 (ii)로
  12000·9000…을 달고 있어 **기본 예산 900을 단독 초과** → seed가 아니면 어떤 팩에도 못 들어가고,
  프론티어에 뜨는 순간 그 팩을 잘라 먹었다.
- 원인 B(증폭): `traverse()`가 예산 초과 노드에서 `break` → 뒤따르는 작은 후보 전부가 함께 죽음.
- **진단 한 줄**: `tokenEstimate > DEFAULT_BUDGET`인 노드를 세어라. **0이어야 정상**이다
  (수정 후 0 유지 = 회귀 가드로 쓸 수 있는 불변식).

### 수정: 프로퍼티 분리(`ho:observedTokenVolume`)
- `ho:tokenEstimate` = **노드 자신의 텍스트 비용**(projector·materialize MANIFEST 소비자),
  `ho:observedTokenVolume` = **런타임 관측량**(cognitiveCapacity 적합성 리뷰 소비자).
  domain `ho:AreaOfObservation`(단일 클래스라 domain 명시 가능), range xsd:integer.
- 값 **이관**만 하면 SHACL이 옛 술어를 요구해 FAIL → `AreaOfObservationShape`의 `sh:path`도
  같이 갈아야 한다(minCount/datatype/message 그대로 **repoint**, 제약 추가 금지).
- 재산정 기준: 이 repo의 tokenEstimate 관례 ≈ **노드가 지닌 리터럴 전부의 단어 수 × 1.3**
  (실측: 최근 노드 median 1.27, `mode-*`/`wf-*`/`gr-*` 모두 1.3대). 5단위 반올림.
- 파급 grep 대상: 클래스 definition(AoO·AoI)·`cognitiveCapacity` definition·shape **주석**·
  ABox 배너 주석. "tokenEstimate"를 관측량 의미로 서술한 문장이 남으면 다시 과부하된다.
- ★**materialize 회귀**: MANIFEST의 `tokenEstimate`는 컴포넌트 tokenEstimate **합**이라
  이관하면 값이 바뀐다(49888→2383). CLAUDE.md·role md·lock은 byte-identical(관측 술어를
  emitter가 안 읽음). lock의 `individualCount`는 값 이관이라 불변 → **개체 수 불변 증거**로 쓸 수 있다.

### `break` → `continue`
```python
if used + cost > budget and admitted:
    continue        # was: break
```
- 무한루프 없음: 스킵된 노드는 `done`에 안 넣지만 재푸시 불가 — 이후 pop의 score ≤ 현재 score이고
  `cand = score*HOP_DECAY*w < score ≤ best[node]`라 `cand > best` 조건이 절대 성립 안 한다.
- 스킵 노드의 이웃은 **확장하지 않는다**(팩에 없는 노드가 relevance를 나르면 안 되므로).
- 앵커 보장(`and admitted`)·heap 키 `(-s,str(n),n)`는 무접촉 → 결정성 유지.
- 기여도 실측(A-1 이후): 8질의 중 3개가 +1 노드(861→895 등). **A-1이 본체, A-2는 방어선**.
  isolation 방법 = 새 코드 위에 옛 `traverse`(break판)를 스크래치에서 monkeypatch해 같은 그래프로 대조.

## 2. deprecated 랭킹 강등 — 배수 크기는 "실측으로" 고른다

`retrieve.py`엔 `ho:maturity`를 읽는 코드가 원래 0줄이었다 → 폐기 노드가 후계보다 위(8.1 vs 6.3).

- 구현: `lifecycle_factor()`를 **score가 정해지는 모든 지점**에 곱한다 —
  `lexical_score`(seed)와 `traverse`의 `cand`(전파, 노드별 캐시). 한쪽만 하면 이웃 전파로
  다시 올라올 수 있다. 미선언 maturity는 **1.0**(부재 ≠ 폐기; 여기선 58노드가 미선언).
- `ho:maturity`는 `sh:maxCount`가 없다 → `g.value()` 대신 `sorted(g.objects(...))`로 읽어야
  다중값일 때 순회 순서가 팩에 새지 않는다(결정성 규율).
- ★**배수는 감이 아니라 스윕으로**: factor∈{0.2,0.3,1/3,0.35,0.4,0.5}×질의 4개×예산 3종을
  한 스크립트로 돌려 (a) 후계가 항상 위인가 (b) 폐기 노드가 **자기 얘기 질의에서도 사라지지 않는가**를 본다.
  - 0.2는 너무 세다 — 폐기 노드가 자기 질의에서도 **완전 소멸**(seed 컷 MAX_SEEDS=8에서 잘림).
  - 0.5는 너무 약하다 — 후계와 마진 6%(3.375 vs 3.6)로 순서 보장이 부서지기 쉽다.
  - 채택 **0.35**("살아있는 대안보다 약 3배의 어휘 근거가 있어야 위로 온다") — 후계 대비 2배 이상
    마진 + 관련 질의에 여전히 등장.
- 숨기지 않는다는 요구는 **필터 금지 + 배지**로 만족: 팩 노드 dict에 `"maturity"` 구조화 필드,
  md 렌더에 `⚠ DEPRECATED` 배지(폐기 사실이 definition 산문에만 있으면 팩 독자는 못 본다).
- 남는 한계: md는 **타입 그룹 알파벳 순**이라 `DesignPattern`(폐기) 섹션이 `ExecutionMode`(후계)보다
  문서상 먼저 나올 수 있다. relevance 순위는 뒤집혔으므로 배지로 방어. 그룹을 max-relevance로
  정렬하려면 전 팩 레이아웃이 바뀌므로 별도 결정 사항.
- 근본 해법 후보(미구현·GAP): 후계 관계가 `DEPRECATED: superseded by id:x` **산문**으로만 존재한다.
  `ho:supersededBy` 같은 edge가 있으면 폐기 노드를 뽑을 때 후계를 같이 끌어올 수 있다.
