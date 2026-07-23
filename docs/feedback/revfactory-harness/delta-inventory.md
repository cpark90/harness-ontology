# revfactory/harness → 온톨로지 반영: 통합 delta 인벤토리

> 출처: inspection dispatch 3-에이전트 분석(2026-07-23), `revfactory/harness`(방법론 repo, Apache-2.0)의
> SKILL.md + 레퍼런스 6종 전수 정독. 상위: `../revfactory-harness-reflection.md`. 상세 매핑: `./source-mapping.md`.
> 검증/doctrine: `./verification-and-doctrine.md`. **저작은 orchestrator→developer**(schema=coverage-audit gate + Adding vocabulary).

각 항목 = 무엇 + 한 줄 정의 + **orphan-free 연결**. 세 에이전트 결과를 reconcile(중복명 통일)함.
게이트: 전부 기존 `hasComponent` sub-property/propertyChain 관용구로 연결 → 신규 SHACL shape 불필요(예외 명시).

## A. 신규 TBox 클래스 (4)
1. **`ho:ExecutionMode`** ⊑? (non-component, DesignPattern처럼) — "하네스가 도는 실행 topology: peer
   agent-teams / 경량 sub-agents / phase별 hybrid. 아키텍처 DesignPattern과 **직교**." + `ho:hasExecutionMode`
   (Harness→) · `ho:stepExecutionMode`(WorkflowStep→, hybrid phase별). ABox: `mode-agent-teams`/`mode-sub-agents`/
   `mode-hybrid`. 연결: `hasExecutionMode`를 `EdgeTypingShape`에 추가, `tagged c-multiagent`.
   *(경량대안: `pat-agent-teams`/`pat-sub-agents`를 DesignPattern으로 — 축을 conflate하므로 별도 클래스 권장.)*
2. **`ho:TestScenario`** ⊑HarnessComponent — "행위 수용 fixture: 대표 요청 + 기대 결과, kind별(빌드트리
   `Contract`·few-shot `Example`와 구별)." + `ho:hasTestScenario`(⊑hasComponent, Harness→ = orphan-free 직접) ·
   datatype `scenarioKind`(sh:in normal|existing-input|error|trigger-positive|trigger-negative)·`scenarioPrompt`·
   `scenarioExpected`(반복)·`scenarioReferences`(→WorkflowStep). 옵션 `TestScenarioShape`(minCount scenarioKind/prompt).
3. **`ho:FailurePolicy`** ⊑HarnessComponent — "error-handling 표의 한 행: 실패조건→복구전략." + `hasFailurePolicy`
   (⊑hasComponent) 또는 `stepFailurePolicy`(WorkflowStep→, `hasComponent o hasStep o stepFailurePolicy` chain) ·
   datatype `failureCondition`·`recoveryStrategy`. tag `c-graceful-fallback`.
4. **`sectionKind` enum 확장**(기존 닫힌 8종에 4 추가): `execution-mode`·`data-flow`·`error-handling`·
   `test-scenarios`. + 각 `ho:AssemblySection` 기본값을 `h-multiagent`에 추가해 조립 총순서 유지. **이게
   materialize가 orchestrator-template의 그 섹션들을 emit하게 하는 핵심.**

## B. 신규 TBox 속성 (Role/Instruction/Harness 위)
- **`ho:augmentsRole`**(Instruction→Role) — "이 스킬이 특정 역할의 도메인 전문성을 확장"(GAP-5). refinement
  edge라 orphan 없음(reachability는 `hasInstruction`). + **`ho:integrationMode`**(Instruction, invoke|inline|
  reference-load) — 스킬↔에이전트 3연결방식.
- **`ho:agentType`**(Role, general-purpose|Explore|Plan|custom) — subagent_type·기본 도구접근 구동. read-only
  타입은 `roleTool` 제한으로 자연 표현(least-privilege 정합). 옵션 `ho:toolAccessScope`(full|read-only).
- **`ho:reinvocationKeywords`**(Harness) — description이 담아야 할 재실행/후속 트리거 키워드(없으면 하네스가
  dead code). datatype, orphan 없음.
- **`ho:triggerPhrase`·`ho:outOfScope`**(도메인 미지정 또는 HarnessComponent → **Harness+Instruction 공용**) —
  스킬 description 트리거 + 명시적 배제(GAP-3, Instruction까지 확장). datatype, orphan 없음.

## C. 신규 중앙 DesignPattern (patterns.ttl) — 6패턴 taxonomy
`pat-pipeline`(순차 스테이지) · `pat-fanout-fanin`(병렬→통합) · `pat-expert-pool`(router→specialist, **완전
미모델**) · `pat-producer-reviewer`(생성+검증 bounded loop) · `pat-supervisor`(런타임 **동적** 할당; 기존
`pat-orchestrator-workers`는 정적 사전할당 → altLabel/정의로 구별 또는 별 노드) · `pat-hierarchical-delegation`
(2단계 재귀). 연결: `DesignPattern`은 orphan shape 없음 → 각 `tagged c-multiagent`(+`c-pattern-taxonomy`) +
데모/템플릿 harness가 `appliesPattern`으로 참조. 복합패턴 = 한 harness에 다중 `appliesPattern`(신규 클래스 불필요).

## D. 신규 중앙 Channel (channels.ttl)
**`chan-task-board`** — "워커가 task를 claim하고 task-update로 진행 보고, 리더가 idle 자동 통지받는 공유
작업목록; file(chan-workspace)·message(chan-peer)·spawn(chan-dispatch)에 이은 4번째 전달매체." 연결:
`channelParticipant` 워커+orchestrator, `involvesUser false`, `channelMedium`, `tagged c-multiagent`.

## E. 신규 중앙 Guardrail (guardrails.ttl) + 짝 Concept
- **복잡도**: `gr-depth-limit`(위임 ≤2) · `gr-no-nested-teams` · `gr-single-active-team` · `gr-bottleneck-avoidance`
  · `gr-flatten-hierarchy`. tag `c-complexity-governance`(broader c-multiagent).
- **반복**: `gr-bounded-iteration`(producer-reviewer 재시도 2~3회 상한; = 에이전트2의 gr-bounded-retry와 통합).
- **QA/평가**: `gr-integration-coherence`(생산자-소비자 함께 읽어 경계정합 교차검증; 존재검사보다 연결검사 우선;
  기존 `gr-grounding`과 유사하나 협의 → 별도) · `gr-discriminating-eval`(baseline 대비 차등 평가, 둘 다 통과하는
  assertion 폐기).
- **저작/거버넌스**: `gr-single-responsibility`(한 역할 한 책임) · `gr-generalize-not-overfit`(피드백을 원칙으로
  일반화) · `gr-absolute-paths`(`_workspace/` 절대경로) · `gr-well-formed-skill`(아래 F) · (옵션)`gr-opus-required`.

## F. 스킬 well-formed 거버넌스 (Contract 축 재사용, 신규 클래스 없음)
- **`cap-skill`** Capability("스킬 저작/패키징") — 스킬 `Instruction`이 `providesCapability cap-skill`(제공)
  + 스킬빌드 harness가 require(orphan-free).
- **구조 `Contract` on cap-skill**(`capabilityContract`, 기존 `hasComponent o providesCapability o
  capabilityContract` chain): `file-contains:SKILL.md::description`·`section:SKILL.md::<필수헤딩>`·금지파일 부재
  (README/CHANGELOG 등). → **`verify_contract.py`로 빌드검사 가능**(강제 가능한 절반). + `gr-well-formed-skill`
  (저작측 절반).

## G. 신규 중앙 Workflow (workflows.ttl) — 하네스 생애주기
- **`wf-harness-evolution`**: step `wfs-audit`(status/drift 감사)·`wfs-feedback-route`(피드백→품질/스킬·역할/
  에이전트·순서/오케·트리거/description 라우팅)·`wfs-change-log`.
- **`wf-verify-harness`**: step `wfs-structure-check`·`wfs-trigger-validation`(should 8~10 + should-NOT near-miss)·
  `wfs-baseline-compare`(with/without skill)·`wfs-dryrun`(dead-link은 stepConsumes/produces join이 이미 잡음).
- 연결: `hasWorkflow`(from `h-multiagent` 또는 신규 `h-harness-factory` 템플릿), step은 `hasComponent o hasStep`
  chain, `stepByRole`로 `role-vnv`/`role-inspection`/`role-orchestrator` 재사용. **Phase6-3 assertion 평가는 기존
  `ho:Contract`(executable/structural) 강한 재사용**(신규 없음).

## H. 옵션 신규 Role/Capability
- **`role-qa`**(옵션, `agentType general-purpose`) + `cap-integration-verification`("경계 교차비교, 모듈마다
  incremental") — 대부분 `role-vnv`/`role-synthesizer`와 겹침. **권고: 새 클래스 X → `role-vnv` + `gr-integration-
  coherence` scoped(roleGuardrail) + reviewer concept 태그**. 경계교차+incremental이 충분히 구별될 때만 신설.

## 우선순위 (권고)
**P1**(materialize를 orchestrator-template 스펙에 맞춤): A4 sectionKind 4종 + A1 ExecutionMode + A2 TestScenario +
A3 FailurePolicy. **P2**(중립 라이브러리 완성): C 6패턴 + D chan-task-board + E 복잡도/반복/QA guardrail.
**P3**: B augmentsRole/integrationMode + agentType + reinvocationKeywords/trigger, F skill 거버넌스, G 생애주기 workflow.
**P4**(옵션): H role-qa.

## 성격
대부분 **중앙 중립 라이브러리(패턴·guardrail·workflow·실행모드) + TBox 소폭 확장**이라 harness-100 인스턴스
임포트(recipe-side)와 **직교**. → augmentation 로드맵에 **"방법론 반영 축"으로 별도 inc**. doctrine 불일치
(기본 실행모드 등)는 `verification-and-doctrine.md` 참조 — **사용자 결정 필요**.
