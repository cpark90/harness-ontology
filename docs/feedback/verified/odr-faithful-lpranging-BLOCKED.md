---
status: reported
verdict: BLOCKED
source_brief: docs/plans/inspection-brief-odr-and-faithful-lpranging.md
---
# 블로커 보고 — ODR+faithful 라운드: Task 1 push 후 federation 회귀 발견

inspection이 brief를 verify-then-proceed로 진행하던 중 **재현 가능한 federation 회귀**를 발견해
**Task 2를 push하지 않고 중단**한다. 핸드백.

## Task 1 — 완료(push)됐으나 회귀 유발
- 중앙 commit **`91fea30`** push됨. 중앙 **자체 validate = PASS 77**(64 + guardrail 3 + role 7,
  + channel/role/coverage TBox). 단, brief 예상 73 ≠ 실제 77 — brief(17:07) 이후 channels/coverage
  후속(channels.ttl·CLAUDE.md coverage gate·gr-structural-coverage)이 트리에 folded-in돼 통합 커밋함
  (partial 커밋 불가: TBox/harnesses.ttl가 channels/roles를 참조·entangled).

## 회귀 (재현됨) — recipe federation FAIL
중앙이 64→77로 커지며 `h-multiagent`에 신규 `hasRole`·`hasChannel` 컴포넌트가 생겼는데,
**harness-recipes `catalog-v001.xml`가 신규 core 유닛을 매핑하지 않는다.**
- recipe catalog 매핑 = 11 유닛(capabilities/concepts/constraints/domains-tasks/guardrails/
  harnesses/model-configs/patterns/system-prompts/tools/workflows). **누락: `core-channels`·`core-roles`.**
- 결과: **이미 published된 recipe(`520487d`)조차 새 중앙(`91fea30`)에 federate하면 FAIL**
  (h-multiagent의 role/channel 컴포넌트 미해결 → MinCount 위반). techdoc union = 82인데 FAIL.
- faithful lpranging(staging)은 별도로 union 17 (central 미로드)로 FAIL — SHACL(usesTool/hasWorkflow
  dangling) + capability(cap-fileedit/codeexec/orchestration/traceability provider 없음). lpranging.ttl은
  techdoc와 동일하게 `.../ontology`를 import하므로 근인은 catalog 누락과 동일 계열로 판단(추가 조사 여지).

## 추가 정황 — 라운드 미정착
중앙 working tree가 blocker 조사 중에도 **계속 변경**됨(`ontology/abox/core/{concepts,guardrails}.ttl`
새로 dirty) → **developer가 이 라운드를 아직 저작 중**. 즉 push 시점이 이르다.

## 핸드백 — 필요한 fix (developer 저작, orchestrator dispatch)
1. **harness-recipes `catalog-v001.xml`에 `core-channels`·`core-roles` `<uri>` 매핑 추가**
   (central root import closure의 신규 유닛 해소) — federation 복구의 핵심.
2. faithful **lpranging.ttl이 실제로 central을 로드하는지** 재확인·수정(union이 17이 아니라 full이 되게).
3. 진행 중인 `concepts.ttl`·`guardrails.ttl` 편집 등 **라운드 마무리**.
4. **재검증**: 중앙 validate + `harness-recipes`의 techdoc·lpranging **federate PASS**를 확인한 뒤
   corrected 브리프로 inspection이 Task 2 push.

## 중앙 91fea30 처리
- 중앙 자체는 valid(77)이나 **published federation을 깨는 상태**. 되돌리려면 force-push(공개 이력
  재작성)라 권장하지 않음 — **forward fix(위 catalog 매핑)**로 복구가 정석. 즉시 복원이 필요하면
  사용자 판단으로 revert 가능.
- recipe repo는 **520487d 그대로**(내 broken faithful sync는 폐기·복원함). recipes CI는 다음 recipe
  push 전까지 red로 뜨지 않으나, 클론+federate 소비자는 현재 FAIL.

## 체크리스트
- [x] 중앙 push: `91fea30` / 중앙 self-validate 77 PASS — **단 federation 회귀 유발**
- [ ] recipes push: **BLOCKED**(catalog 누락 + faithful lpranging FAIL + 라운드 미정착)
