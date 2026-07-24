# Dispatch brief — Phase 0.7: 기존 recipe coverage-audit 보정 (대량 임포트 前 차단요소)

> 작성: orchestrator (2026-07-25, 자율 루프). 상위: `docs/plans/harness-100-scaleup-plan.md` §5c **M2**.
> 근거: `docs/plans/harness-100-attribute-inventory.md` §1F·1G·1K.
> 실행: **developer dispatch (opus)**. ★**선행: Phase 0.6(중앙 어휘 GAP) land 완료 후** — 이번 작업은
> 거기서 저작되는 중앙 `fp-*` 원형을 **바인딩**하는 것이라 순서가 뒤집히면 로컬 중복이 생긴다.

## 왜 지금 (대량 임포트 前에 해야 하는 이유)
전수 인벤토리가 드러낸 사실: **land된 8 recipe 전부 `hasExecutionMode` 0 · `TestScenario` 0 · `FailurePolicy` 0**
(orchestrator 재확인 완료). 그런데 코퍼스 소스는 셋 다 거의 전수 제공한다 — topology **100/100**,
test scenario **90/100**(정확히 3개씩), failure policy **95/100**.

즉 **어휘 GAP이 아니라 반영 누락**이며, CLAUDE.md step-7의 **coverage-audit 게이트가 잡았어야 할 것**이다.
지금 고치지 않고 30~40개를 임포트하면 **같은 누락을 35× 복제**한다. 그래서 이것이 임포트의 차단요소다.

## 소스가 다른 두 그룹 — 섞지 말 것

### 그룹 A — 코퍼스 유래 파일럿 5 (`03-newsletter-engine`·`16-fullstack-webapp`·`21-code-reviewer`·`31-ml-experiment`·`46-product-manager`)
소스: `/home/cpark/git/harness-100/en/<name>/.claude/` (읽기 전용).
- **실행 topology**: 코퍼스 전량이 `Agent Team`이다(§1F, 변이 0) → `ho:hasExecutionMode core:mode-agent-teams`.
  **소스에서 실제로 확인한 뒤** 바인딩하라. 확인 없이 일괄 부여 금지.
- **TestScenario**: 소스의 시나리오 표에서 추출. 값 종류는 `ho:scenarioKind`의 `normal`/`existing-input`/`error`와
  **1:1 대응**한다(§1K). prompt·expected는 **하네스별 내용이므로 recipe-local**이 옳다(중앙 금지).
- **FailurePolicy**: **중앙 원형을 재사용하라** — Phase 0.6이 `fp-agent-failure-retry`·`fp-insufficient-input`·
  `fp-review-critical-rework`·`fp-source-unavailable`·`fp-conflict-contradiction`를 중앙에 저작한다.
  소스의 error-handling 표를 그 원형에 **매핑**하고, 원형으로 안 덮이는 것만 recipe-local로 저작하라.
  **로컬에 원형 복제본을 만들지 말 것**(그게 이 repo가 막는 drift다).

### 그룹 B — 자체 recipe 3 (`lpranging`·`techdoc`·`contract-demo`)
코퍼스 유래가 **아니다**. 소스가 다르므로 **같은 잣대를 기계적으로 적용하지 마라**.
- 각각의 원 소스·설계 의도를 확인해 **실제로 해당하는 축만** 채워라.
- 해당 정보가 원 소스에 **없으면 지어내지 말고**, "표현하지 않음 + 명시적 수용 사유"로 보고하라
  (CLAUDE.md step-7이 인정하는 결론이다). **날조가 미반영보다 나쁘다.**

## 배선 주의
- `ho:hasTestScenario`·`ho:hasFailurePolicy`는 **Harness 직결**(⊑hasComponent)이라 각 recipe의 harness 노드에 문다.
- `ho:hasExecutionMode`는 Harness→ExecutionMode. 중앙 `core:mode-*`를 **IRI로 참조**한다(recipe에 모드 복제 금지).
- recipe TTL의 prefix 규약(§2a): 자기 도메인은 `id:`, 중앙 참조는 `core:`. 기존 recipe 파일의 지역 컨벤션을 따르라.

## 완료 게이트 (recipe별)
```bash
# per-recipe closure 1개씩 — ★all-recipes union 금지
HARNESS_CATALOG=$PWD/staging/harness-recipes/catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<name> /usr/bin/python3 tools/validate.py   # PASS
/usr/bin/python3 tools/materialize.py <recipe harness> ...   # 신규 섹션 렌더 확인 + 2회 결정성
```
- **중앙 무회귀**: 중앙 하네스 7종 산출물 **byte-identical**(이번 작업은 recipe만 건드린다).
- 보정 후 8 recipe의 3축 카운트를 **표로 제시**하라(0이던 것이 무엇으로 채워졌는지, 그룹 B의 미표현 사유 포함).

## 금지
- **중앙 `ontology/**` 편집 금지** — 이번 범위는 `staging/harness-recipes/recipes/**`뿐이다.
  중앙에 부족한 어휘를 발견하면 저작하지 말고 **GAP 보고**(Phase 0.6의 잔여일 수 있다).
- 코퍼스 `/home/cpark/git/harness-100` **쓰기 금지**(읽기 전용).
- `docs/**` 편집 금지 · **git 조작 금지**(inspection 전담).

## 반환 보고
① recipe별 추가 노드·edge 표(3축) ② 중앙 원형 재사용 내역과 **로컬로 갈 수밖에 없던 것의 이유**
③ 그룹 B의 축별 판정(표현/미표현+사유) ④ 게이트 로그(8 federate + materialize) ⑤ 중앙 byte-identity 증명 ⑥ GAP.
