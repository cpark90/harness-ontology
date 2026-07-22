# 연합 lockstep — 중앙 core 변경 시 recipe catalog 동반 필수 (inspection)

## 교훈 (2026-07-22, ODR+faithful 라운드에서 회귀)
중앙(`harness-ontology`)에 **신규 core 유닛**(예: `roles.ttl`·`channels.ttl`)을 추가하고 그것을
`h-multiagent` 등 공유 하네스에 wire하면, **recipe repo의 `catalog-v001.xml`가 그 신규 유닛을
매핑하지 않는 한 모든 published recipe의 federate가 FAIL**한다(h-multiagent의 hasRole/hasChannel
컴포넌트 미해결 → SHACL MinCount 위반). 중앙 self-validate는 PASS라 **중앙만 보면 안 보인다.**

## 게이트 (verify-then-proceed 강화)
중앙 abox/TBox에 **개체·컴포넌트가 늘어나는** push 전에는 반드시:
1. 중앙 clone 후 **기존 published recipe들(techdoc·lpranging …)을 새 중앙에 federate validate** →
   전부 PASS 확인(회귀 조기 발견).
2. FAIL이면 push 보류 + recipe catalog(신규 core 유닛 `<uri>` 매핑) 동반 fix를 developer 핸드백.
brief가 "중앙 validate PASS"만 게이트로 걸어도, inspection은 **recipe federation 회귀축을 추가로**
확인한다. (`validate.py`는 단일 그래프만 본다.)

## 복구
이미 push된 중앙이 federation을 깼으면 **force-push revert보다 forward fix**(recipe catalog 매핑
추가)가 정석 — 공개 이력 재작성 회피. 즉시 복원 필요 시에만 사용자 판단으로 revert.

## 관련
[[federation-physical-split]] (recipes repo 구조·federate 재현 명령).
