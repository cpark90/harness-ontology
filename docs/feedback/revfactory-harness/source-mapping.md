# revfactory/harness 전 개념 → 온톨로지 귀속 (traceability)

> 출처: inspection dispatch 3-에이전트 전수 정독(2026-07-23). 목적: 소스의 **모든 개념이 하나의 귀속을
> 갖게** 함 — EXISTING(기존 요소) / NEW-TBox / NEW-central(ABox) / CONVENTION(materialize·저작) / NO-MODEL(사유).
> delta 상세: `./delta-inventory.md`. 상위: `../revfactory-harness-reflection.md`.

## 문서 지도 (`skills/harness/`)
`SKILL.md`(생성 메타스킬) + `references/`: `agent-design-patterns` · `orchestrator-template` · `qa-agent-guide` ·
`skill-writing-guide` · `skill-testing-guide` · `team-examples`. (+ README/CONTRIBUTING = repo 운영, 온톨로지 대상 아님.)

## 1. agent-design-patterns.md
- **실행모드**: Agent-Teams / Sub-agents / Hybrid → **NEW-TBox `ho:ExecutionMode`**(+step별). 프리미티브
  TeamCreate/SendMessage(to:name)/TaskCreate/Agent-spawn → EXISTING channel medium(chan-peer/workspace/dispatch).
  broadcast(to:all) 비용 → PARTIAL(medium 문자열). 유휴알림·리더고정 → NO-MODEL(런타임).
- **6 아키텍처 패턴**: Pipeline·Fan-out/Fan-in·Expert-Pool·Producer-Reviewer·Hierarchical-Delegation → **NEW-central
  `pat-*`**; Supervisor → EXISTING `pat-orchestrator-workers`(동적 vs 정적 구별 note). depth≤2·중첩불가·병목·무한루프
  → **NEW-central guardrail**(gr-depth-limit/flatten/bottleneck/bounded-iteration). 복합패턴 → EXISTING(다중 appliesPattern).
- **agent-type**: general-purpose/Explore/Plan → **NEW-TBox `ho:agentType`**(+read-only=roleTool 제한); custom →
  EXISTING Role. 선택기준표 → NO-MODEL(wf-compose prose). model:opus → EXISTING mc-opus(+옵션 gr-opus-required).
- **정의구조/분리/재사용**: 필수섹션(핵심역할=definition/rolePersona·작업원칙=roleGuardrail·I/O=stepConsumes/
  Produces·팀통신=channelParticipant·에러=gr-graceful-fallback·협업=Channel) 대부분 EXISTING; 템플릿 레이아웃=
  CONVENTION. 분리4축 → `gr-single-responsibility`(NEW)+`gr-simplicity`. 재사용 매트릭스 → EXISTING `gr-reuse-first`.
- **스킬↔에이전트**: 스킬=Instruction/에이전트=Role(EXISTING doctrine 일치). 3연결(invoke/inline/reference-load) →
  **NEW-TBox `ho:integrationMode` + `ho:augmentsRole`**.

## 2. orchestrator-template.md (= materialize emit 스펙)
섹션→온톨로지-소스(materialize가 읽어 emit):
- frontmatter name/description + **재실행 키워드** → prefLabel + **NEW `ho:reinvocationKeywords`**.
- `## 실행 모드` → **NEW-TBox ExecutionMode**(sectionKind `execution-mode` 신규).
- `## 에이전트 구성`(roster) → Role×N(hasRole)+definition; 타입열 → **NEW agentType**; 스킬열 → hasInstruction; 출력열 → Deliverable.
- `## 워크플로우` Phase 0(context 감사·재실행 분기) → WorkflowStep + `gr-scale-modes`; Phase1-5 → WorkflowStep(hasStep/
  stepOrder/stepByRole/stepUsesTool/stepGuardedBy) **EXISTING**.
- **task-DAG 표**(Order/Task/Owner/Depends-On/Deliverable) → **FULLY EXISTING**: stepOrder/prefLabel/stepByRole/
  stepDependsOn/stepProduces→Deliverable (inc1에서 land). **gap 아님.**
- `## 데이터 흐름`(ASCII) → Deliverable produce/consume join에서 렌더(sectionKind `data-flow` 신규, emit).
- Data Transfer Protocol(file/message/task) → chan-workspace/chan-peer/**NEW chan-task-board**.
- `## 에러 핸들링`(상황→전략 표) → **NEW-TBox `ho:FailurePolicy`**(sectionKind `error-handling` 신규).
- `## 테스트 시나리오`(정상/에러) → **NEW-TBox `ho:TestScenario`**(sectionKind `test-scenarios` 신규).
- Template C phase-mode 표 + hybrid 전이 → **NEW `ho:stepExecutionMode`**; "세션당 1팀" → `gr-single-active-team`(또는 Constraint).
- 작성원칙(절대경로/의존성명시/에러현실/테스트필수) → `gr-absolute-paths`(NEW)+기존 guardrail.
- `_workspace` 보존·파일명 스킴·CLAUDE.md 포인터 → CONVENTION(gr-traceability 의미).

## 3. team-examples.md (예제 5 → recipe)
전부 중앙 archetype을 `derivedFrom`으로 재사용(role taxonomy 완비 확인). 드러난 신규:
- Ex1 리서치(fan-out/fan-in) → `pat-orchestrator-workers`+`pat-peer-mesh`; **NEW chan-task-board**.
- Ex2 소설(pipeline+fan-out, hybrid) → **NEW pat-pipeline**; `stepExecutionMode` phase별; 역할=role-design/synthesizer/vnv derived.
- Ex3 웹툰(generate-verify) → **pat-producer-reviewer**(또는 pat-reflection); **NEW gr-bounded-iteration**; verdict=gr-structured-output.
- Ex4 코드리뷰(fan-out+토론) → 순수 재사용(pat-orchestrator-workers+pat-peer-mesh) — **신규 0**(peer-mesh+workers 조합 검증).
- Ex5 마이그레이션(supervisor 동적) → **NEW pat-supervisor**(동적 claim); **chan-task-board**.

## 4. qa-agent-guide.md
- QA=first-class sub-agent → EXISTING Role(role-vnv/synthesizer 사이 → **새 클래스 X, gr-integration-coherence 태그**).
- 경계 교차비교·강/약 체크리스트 → **NEW `gr-integration-coherence`**. severity 🔴🟡🟢 → CONVENTION. bounded 루프 →
  **`gr-bounded-iteration`**. 검증우선순위 → salience/stepOrder. verdict/checklist → artifactTemplate. general-purpose
  요구 → roleTool 실행 scope. incremental QA → stepDependsOn 스케줄(EXISTING).

## 5. skill-writing-guide.md
- 스킬=주입 절차 → EXISTING Instruction. 역할 확장 → **NEW `ho:augmentsRole`**. description=트리거 → **NEW
  triggerPhrase**; 트리거 경계/유사배제 → **NEW outOfScope**. §8 미포함 파일(README 등) → **cap-skill 구조 Contract**(부재검사)+
  `gr-well-formed-skill`. well-formed(frontmatter/명령형/허용섹션) → **구조 Contract on cap-skill**. why-first/명령형/
  context경제 → CONVENTION(+gr-simplicity). 일반화/anti-overfit → `gr-generalize-not-overfit`. progressive disclosure/
  번들링 스크립트 → CONVENTION(scaffold/implementationRef). §9 재사용설계 → EXISTING `gr-reuse-first`(1:1).
- data schema(eval_metadata/grading/timing.json) → artifactTemplate 내용(NO-MODEL 필드명).

## 6. skill-testing-guide.md
- 테스트 프롬프트=현실 요청 → **NEW `scenarioPrompt`**. 3 coverage(핵심/엣지/복합)+normal/error → **NEW `scenarioKind`**.
- assertion=객관 기대 → **NEW `scenarioExpected`/acceptanceCriterion**; 프로그램검사 가능 → EXISTING executable `Contract`.
- With/Without baseline 차등 → **NEW `gr-discriminating-eval`**; 비변별 assertion 폐기 → 동. Grader/Comparator/Analyzer →
  EXISTING role-vnv/synthesizer(옵션 신규 role, 파일럿 시). 반복+종료조건 → `gr-bounded-iteration`. 트리거 eval(10 should
  +10 should-NOT, near-miss) → **`scenarioKind` trigger-positive/negative**. 교차 트리거 충돌 → triggerPhrase/outOfScope.
- `_workspace`/iteration-N/삭제금지·timing 즉시저장 → CONVENTION(gr-traceability/tokenEstimate). auto-opt(claude -p) → NO-MODEL(외부도구).

## 7. SKILL.md (생성 메타스킬, Phase 0~7)
전체 ≈ EXISTING `wf-compose-harness`+`pat-ontology-composition`. Phase별:
- P0 감사/drift/모드분기 → **NEW `wf-harness-evolution` step `wfs-audit`** + gr-structural-coverage/traceability/scale-modes.
- P1 도메인분석/코드탐색 → EXISTING Domain/Task + role-inspection/research. 유저숙련감지 → NO-MODEL.
- P2 팀아키텍처설계 → EXISTING wf-compose + ExecutionMode(D1)/패턴(D2).
- P3 에이전트생성/중복검토/파일필수/opus/QA필수 → EXISTING Role authoring+gr-reuse-first+mc-opus; QA → role-vnv+gr-integration-coherence(옵션 role-qa/cap-integration-verification).
- P4 스킬생성/구조/트리거/본문/progressive/연결 → EXISTING Instruction+gr-reuse-first; 연결 → augmentsRole/integrationMode; 500줄/트리거문구 → NO-MODEL/CONVENTION.
- P5 오케스트레이션/데이터전달4종/에러/팀크기/포인터등록 → EXISTING role-orchestrator+channel 4종(chan-task-board 포함)+gr-graceful-fallback/design-for-loss; 팀크기 2~7 → NO-MODEL(옵션 Constraint); 파일명 → CONVENTION.
- P6 검증(구조/모드별/baseline/트리거/dryrun/시나리오섹션) → **NEW `wf-verify-harness`**; assertion 평가 → **EXISTING `ho:Contract`**(강한 재사용); dead-link → stepConsumes/produces join(EXISTING); 시나리오섹션 → TestScenario(D)/Example.
- P7 진화(피드백수집/반영경로/변경이력/진화트리거/유지보수) → **`wf-harness-evolution`**(라우팅 step)+chan-agent-user+gr-traceability/maturity/derivedFrom.
- 산출물 체크리스트 → EXISTING `ho:HarnessShape`(최소구성 SHACL) + 위 delta들.

## 요약
소스의 **거의 모든 개념이 귀속**됨: 다수 EXISTING(강한 적합), 신규는 delta-inventory의 A~H(패턴 6·ExecutionMode·
TestScenario·FailurePolicy·복잡도/QA guardrail·생애주기 workflow·augmentsRole/agentType·skill 거버넌스), 그리고
명시적 NO-MODEL/CONVENTION(verification-and-doctrine §3). **task-DAG는 이미 완비**(재제안 금지).
