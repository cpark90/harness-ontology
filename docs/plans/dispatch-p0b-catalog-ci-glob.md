# Dispatch brief — P0-b: catalog·CI matrix를 glob에서 생성 (임포트 前 차단요소)

> 작성: orchestrator (2026-07-25, 자율 루프). 상위: `docs/plans/harness-100-scaleup-plan.md` §6 · §1 P0-b.
> 실행: **developer dispatch (opus)**. ★**선행: Phase 0.7 land 완료 후**(같은 `staging/harness-recipes/` 트리라
> recipe TTL 저작과 겹치면 충돌). 이번 범위는 catalog·CI·생성 스크립트 — recipe TTL 본문은 안 건드린다.

## 왜 (차단요소인 이유)
현재 recipe 나열이 **세 곳에 손으로** 중복돼 있다:
- `staging/harness-recipes/catalog-v001.xml` — 30 uri(중앙 per-type units + recipe roots)
- published `harness-recipes/.github/workflows/validate.yml` — CI matrix 8 entry
- 중앙 `docs/ci/data-repo-validate.yml`(참조)

8개일 때도 이 세 곳이 **이미 한 번 어긋났다**(REORG 때 전용 catalog 4개 누락 → 41 individuals만 로드되고
에러 없이 통과). 35~40개로 늘리면서 손 유지하면 이 **조용한 부분 closure**가 반복된다. 이 세션에서 확인된
"레지스트리 표류"(§B16)의 recipe판이다. → **`recipes/*/`에서 생성**해 단일 진실 공급원으로 만든다.

## 설계 (orchestrator 확정)
**생성 스크립트 1개 + CI가 그것으로 검증.** recipe 목록의 진실은 **디스크의 `recipes/*/` 디렉토리**다.

### 1. 생성 스크립트 `tools/gen_recipe_catalog.py` (또는 staging repo 내 적절한 위치)
- `recipes/*/` 를 walk → 각 recipe의 **root 문서 IRI**를 결정론적으로 수집.
  - recipe root IRI는 관례상 `https://harness-ontology.dev/recipes/<dirname>`. 각 recipe TTL의 `owl:Ontology`
    헤더에서 **실제로 읽어** 확인하라(디렉토리명 가정이 틀릴 수 있다 — 검증 후 사용).
- 출력 둘: **(a) catalog-v001.xml**(중앙 per-type unit 매핑 + recipe root 매핑), **(b) CI matrix 목록**.
- **결정적**(정렬) · **idempotent**(재실행 시 diff 0).

### 2. "생성물 == 현재 수기 파일" 게이트 (핵심 — §B16 대책의 recipe판)
스크립트가 만든 것이 **현재 8개 손 파일과 동등**함을 먼저 증명하라(회귀 0). 그 다음에야 자동 생성으로 전환한다.
- 동등 확인: 생성 catalog로 8 recipe federate가 **전과 동일하게 PASS**(개체 수도 동일).
- 이 "생성물==원본" 체크 자체를 **CI step**으로 넣어라 — 누가 recipe를 추가하고 catalog를 재생성하지 않으면 CI가 잡는다.

### 3. CI 스케일 (35~40, 나아가 100 대비)
- published `validate.yml`의 matrix를 **생성 목록에서** 채운다(스크립트 출력 또는 `fromJSON`).
- **path-filtered 또는 shard**: 40개 recipe × 매 push는 과금·시간이 크다. 변경된 recipe만 검증하거나 shard로 나눠라.
  중앙이 바뀐 라운드는 전 recipe 게이트가 필요하다(D4 불변) — 이 두 경로를 구분해 설계하라.
- **★B19 동반 수정**: published `validate.yml`에 `workflow_dispatch` 트리거가 **없어** 중앙만 바뀐 라운드에서
  연합 CI를 못 돌린다(`gh workflow run` → 422). 트리거 1줄을 이번에 함께 추가하라.

## 완료 게이트 (로그 첨부)
```bash
/usr/bin/python3 tools/gen_recipe_catalog.py --check    # 생성물 == 현재 수기 파일 (diff 0)
# 생성 catalog로 8 recipe federate
for r in 03-newsletter-engine 16-fullstack-webapp 21-code-reviewer 31-ml-experiment 46-product-manager \
         lpranging techdoc contract-demo; do
  HARNESS_CATALOG=<generated> HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/$r \
    /usr/bin/python3 tools/validate.py; done    # 8/8 PASS, 개체 수 전과 동일
/usr/bin/python3 tools/validate.py              # 중앙 PASS @223 (이번 작업은 중앙 그래프 무변경)
```
- **위조 시나리오 검증**: recipe 하나를 catalog에서 일부러 빼고 `--check`가 **실패하는지** 확인하라
  (가드가 실효인지 — determinism guard의 negative control과 같은 성격).

## 금지
- 중앙 `ontology/**` 편집 금지(중앙 그래프 무변경) · recipe TTL **본문** 편집 금지(Phase 0.7 소관, 이미 land됨).
- `docs/plans/**` 편집 금지. **git 조작 금지**(inspection 전담).

## 반환 보고
① 생성 스크립트 위치·로직 ② "생성물==수기" 동등 증명 + 위조 시나리오 실패 확인 ③ CI matrix 생성·shard/path-filter
방식 ④ B19 트리거 추가 ⑤ 8 federate 로그 ⑥ GAP(특히 100 스케일에서 남는 문제).

종료 전 `.claude/agent-memory/developer/`에 재사용 지식을 남겨라(기존 줄 보존).
