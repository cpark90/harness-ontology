# Recurrence-prevention 반영: coverage 갭을 guardrail+process gate 쌍으로

**상황**: 실 harness 반영 시 특정 구조 요소(communication channel, `.claude/skills`/commands)가
누락됨. root cause = 반영이 **assembly-driven**(알려진 part-type 고정집합에서 조립)이라
**source-driven 완전열거**가 없었고, 어휘 없는 요소는 슬롯이 없어 보이지 않았으며, coverage가
게이트가 아니었다(`validate.py`는 그래프 정합성만, source-fidelity 아님).

**패턴 = 예방을 두 축에 동시 반영**:
1. 중립 ontology guardrail `id:gr-structural-coverage`(guardrails.ttl, maturity reviewed,
   tagged `id:c-traceability`). promptText = "반영 시 소스 구조 요소 완전열거→각각 매핑, 어휘
   없는 요소는 schema EXTEND 신호이지 skip 아님, done 전 커버리지 검증." h-multiagent
   `hasGuardrail`에 배선(anti-orphan). **near-dup 구분 필수**: gr-traceability(기록 불변/
   provenance)·gr-no-arbitrary-decision(미결 에스컬레이션)과 다른 "반영 완전성" 축.
2. CLAUDE.md §"Composing a new harness" 워크플로에 step 7 coverage-audit gate 추가(vnv
   dispatch, validate 초록≠done). 스타일=기존 번호목록·한글산문/영어용어.
3. lessons doc `docs/lessons/coverage-gap-channels.md`(dir 신규).

**함정 회피**: guardrail은 TBox 무수정으로 됨(기존 ho:Guardrail+promptText/tokenEstimate/
tagged 재사용). 76→77 개체 1증가. 두 로더 parity(HARNESS_CATALOG=/nonexistent glob vs 기본).
일반 원칙: **어휘 없는 소스 요소 = schema 확장 신호, silent skip 아님.**
