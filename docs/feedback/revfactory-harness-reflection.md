---
status: approved            # 사용자만 approved로 바꾼다
targets: [core:h-multiagent, core:wf-compose-harness, core:pat-orchestrator-workers]
kind: proposal
related: [docs/feedback/harness-100-augmentation.md, docs/feedback/finer-harness-decomposition-assembly.md]
---
# revfactory/harness 방법론 전체를 온톨로지에 반영 (결정 앵커)

## 요청 (사용자)
`revfactory/harness`(방법론 repo)의 내용을 **상세 분석해 다 온톨로지에 반영할 수 있게 문서 작성**.
→ inspection이 **3개 opus 에이전트 dispatch**로 SKILL.md + 레퍼런스 6종을 전수 정독, 아래 문서 세트로 합성.

## 산출 문서 세트 (companion)
- **`revfactory-harness/source-mapping.md`** — 소스 전 개념의 온톨로지 귀속(EXISTING/NEW-TBox/NEW-central/
  CONVENTION/NO-MODEL). "모든 개념이 하나의 home을 갖는다"는 traceability.
- **`revfactory-harness/delta-inventory.md`** — 반영에 필요한 통합 delta(TBox 클래스/속성 + 중앙 패턴/채널/
  guardrail/workflow/capability), 각 orphan-free 연결 + 우선순위.
- **`revfactory-harness/verification-and-doctrine.md`** — 3검증개념 정리 + doctrine 불일치(결정 필요) + 모델하지 말 것.

## 한 문장 결론
소스 방법론의 **거의 모든 개념이 귀속 가능**하다. 다수는 **이미 존재**(강한 적합 — role/channel/capability/
**task-DAG(inc1 완비)**/guardrail 21개/Contract 평가축/skill=Instruction·agent=Role). 신규는 **중앙 중립
라이브러리 강화 + TBox 소폭 확장**이며, **harness-100 인스턴스 임포트와 직교**(방법론 축 vs 인스턴스 축).

## 반영 delta 요약 (상세 = delta-inventory.md)
- **TBox 클래스**: `ExecutionMode`(agent-teams/sub/hybrid) · `TestScenario` · `FailurePolicy` · `sectionKind`
  4종 확장(execution-mode/data-flow/error-handling/test-scenarios ← **materialize를 orchestrator-template
  스펙에 맞추는 핵심**).
- **TBox 속성**: `augmentsRole`+`integrationMode`(skill↔role) · `agentType`(Role) · `reinvocationKeywords` ·
  `triggerPhrase`/`outOfScope`.
- **중앙 패턴 6**: pipeline·fanout-fanin·expert-pool·producer-reviewer·supervisor(동적)·hierarchical-delegation.
- **중앙 채널**: `chan-task-board`(4번째 전달매체).
- **중앙 guardrail**: 복잡도(depth-limit/no-nested/single-active/bottleneck/flatten) · bounded-iteration ·
  integration-coherence · discriminating-eval · single-responsibility · generalize-not-overfit · absolute-paths ·
  well-formed-skill(+`cap-skill` 구조 Contract).
- **중앙 workflow**: `wf-harness-evolution`(생애주기) · `wf-verify-harness`(구조/트리거/baseline/dryrun).
- **옵션**: `role-qa`(대개 role-vnv+guardrail로 대체).

## 기존 방향과의 관계
- **harness-100-augmentation(approved)의 방법론 상위층**이다. 그 로드맵에 **"방법론 반영 축"을 별도 inc**로 추가 권고.
- **finer-harness-decomposition(approved, 범위 c)**과 수렴: WorkflowStep/조립축 위에 이 delta들이 얹힌다
  (task-DAG는 이미 land, sectionKind 확장·ExecutionMode가 그 조립축의 연장).

## 열린 결정 (승인 시 지정 — verification-and-doctrine.md §2)
1. **기본 실행모드 (핵심)**: 소스는 peer Agent-Teams 기본, 우리 repo는 central-dispatch 기본. → **양쪽 selectable
   저장 + repo의 central-dispatch 기본 명시 유지**(저장≡운영 harness 일치 원칙). 이대로면 승인만. **[결정]**
2. **ExecutionMode 모델링**: 별도 클래스(권장, 축 직교) vs DesignPattern로 경량화. 추천=별도 클래스.
3. **반영 범위/순서**: P1(materialize↔orchestrator-template: sectionKind+ExecutionMode+TestScenario+FailurePolicy)
   → P2(패턴6+chan-task-board+복잡도/QA guardrail) → P3(augmentsRole/agentType/skill 거버넌스/생애주기 workflow)
   → P4(옵션 role-qa). 추천=P1 선행.
4. **role-qa**: 신설 vs `role-vnv`+`gr-integration-coherence`로 대체. 추천=대체(anti-drift).
5. **model:opus**: 옵션 `gr-opus-required`로 명시화? (소스=repo 일치, 불일치 아님.) 추천=명시화.

## 범위 / 핸드오프
inspection은 **조사·문서화까지 완료**(3 에이전트 dispatch + 4문서). TBox 확장·중앙부품·workflow 저작은
orchestrator가 노드단위 dispatch brief로 계획해 **developer** 수행(schema 변경=coverage-audit gate +
"Adding vocabulary" 규율; 각 land마다 validate + federate + materialize round-trip). 승인 = 이 항목
`status: open`→`approved` + 열린결정 1~5 지정.

> 소스 로컬 클론: scratchpad `harness-src/`(임시). 반영 저작 시 소스 §/line을 근거로(source-mapping.md 참조).
