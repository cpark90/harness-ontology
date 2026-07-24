# Dispatch brief — revfactory-harness-reflection P1 잔여 개체 (ExecutionMode·TestScenario·FailurePolicy·2 workflow)

> 작성: orchestrator (2026-07-24). 상위(승인): `docs/feedback/revfactory-harness-reflection.md`(status: approved) +
> `docs/feedback/revfactory-harness/delta-inventory.md`(소스 진실). 검증 보고: `docs/feedback/verified/methodology-round-finalize.md`.
> 실행: **developer dispatch (opus)**. orchestrator는 이 brief 작성·assemble·`validate.py` 확인만.

## ★선행 게이트 — **해소됨 (2026-07-24 orchestrator 확인)**
이 증분은 **신규 개체를 추가**한다(개체 수 185→증가). DA-4/REORG("185 불변" 순수 구조 refactor)가 먼저 land돼야 했고,
**land 완료 확인**: `af31594`(Taxonomy DA-4 + reorg) → `f6a5317`(finalize) → `81740f5`. **tree clean**(미커밋 온톨로지
변경 0), 평면 abox 잔재 0, `validate.py` **PASS @185**. ⇒ 커밋 경계가 깨끗하므로 **착수 가능**.

## 배경 — 이미 land된 것 (재저작 금지)
`revfactory-harness-reflection`의 delta 다수는 96→185 통합에서 이미 land: **TBox 클래스/속성 전부**(ExecutionMode·
TestScenario·FailurePolicy·WorkflowStep·Deliverable·assemblyOrder·step* edges·augmentsRole·agentType·
integrationMode·reinvocationKeywords 등), **sectionKind 4종**(execution-mode/data-flow/error-handling/test-scenarios),
**6 named 패턴**(pipeline·fanout-fanin·expert-pool·producer-reviewer·supervisor·hierarchical-delegation), **chan-task-board**,
**cap-skill**, **복잡도/반복 guardrail**(depth-limit·no-nested-teams·single-active-team·bottleneck-avoidance·
flatten-hierarchy·bounded-iteration·integration-coherence·discriminating-eval·single-responsibility·generalize-not-overfit·
absolute-paths·well-formed-skill). ⇒ **P2(중립 라이브러리) 완료**. **클래스는 있으나 개체(individual)가 0개인 P1 잔여만** 이 brief 범위.

## 범위 — 저작할 개체 (delta-inventory §A1–A3, §G 기준)

### 1. ExecutionMode 개체 3 (`substrate/` 또는 신규 unit — 아래 파일 결정 참조)
클래스 `ho:ExecutionMode` 존재, 개체 0. DesignPattern과 **직교**하는 실행 topology 축.
- `id:mode-agent-teams` — "peer agent-teams: 대등한 협업 팀."
- `id:mode-sub-agents` — "경량 sub-agents: 오케가 짧은-생애 워커를 소환."
- `id:mode-hybrid` — "phase별 hybrid: 단계마다 topology 전환."
- 연결(anti-orphan): 각 개체는 `ho:tagged id:c-multiagent`. **harness에 `ho:hasExecutionMode`로 물린다** — 최소
  `core:h-multiagent`(agent-teams) 하나는 `ho:hasExecutionMode id:mode-agent-teams`로 연결해 reachability 확보.
  `hasExecutionMode`가 `EdgeTypingShape`(range=ExecutionMode)에 있는지 developer가 `retrieve.py`/shapes로 확인,
  없으면 **shapes는 건드리지 말고 orchestrator에 GAP 보고**(TBox/shape 확장은 이 brief 밖).
- 데이터: `skos:prefLabel`·`skos:definition`(왜 이 mode를 고르나)·`ho:tokenEstimate`·`ho:maturity "draft"`.

### 2. TestScenario 개체 (delta §A2 — 행위 수용 fixture)
클래스 `ho:TestScenario` ⊑HarnessComponent 존재, 개체 0. 대표 요청+기대 결과 fixture(빌드트리 `Contract`·few-shot `Example`와 구별).
- 중립 fixture **1–2개**만 저작(seed 최소). 예: `id:scn-compose-smoke` — "대표 compose 요청 → HarnessShape 최소 충족 + validate PASS 기대."
- 연결: harness가 `ho:hasTestScenario`(⊑hasComponent, orphan-free 직접)로 참조 — `core:h-multiagent`에 물린다.
  `ho:scenarioKind`·`ho:scenarioPrompt`·`ho:scenarioExpected`(반복)·옵션 `ho:scenarioReferences`(→WorkflowStep) 사용.
  속성 present 여부 `retrieve.py`로 확인, 없는 속성은 GAP 보고(발명 금지).
- 데이터: prefLabel·definition·tokenEstimate·maturity "draft". **도메인 content 금지**(중립 fixture).

### 3. FailurePolicy 개체 (delta §A3 — error-handling 표의 한 행)
클래스 `ho:FailurePolicy` ⊑HarnessComponent 존재, 개체 0. 실패조건→복구전략 1행.
- 중립 policy **1–2개**. 예: `id:fp-dispatch-timeout` — "worker dispatch 무응답 → 재dispatch 또는 축소-후-보고."
- 연결: `ho:hasFailurePolicy`(⊑hasComponent) 또는 step의 `ho:stepFailurePolicy`(WorkflowStep→) 중 present한 것으로
  harness/step에 물린다(chain `hasComponent o hasStep o stepFailurePolicy`). `core:h-multiagent` 또는 신규 워크플로 step에 연결.
- 데이터: prefLabel·definition(실패조건+복구전략)·tokenEstimate·maturity "draft".

### 4. Workflow 2 + 그 WorkflowStep (delta §G — 생애주기·검증)
`ontology/abox/core/process/workflows.ttl`에 저작(기존 `wf-multiagent`+`wfs-*` 블록의 predicate template 그대로 따름 — §참고).
- **`id:wf-harness-evolution`** (생애주기): steps
  - `id:wfs-audit`(status/drift 감사) — `stepByRole id:role-inspection`, `stepOrder 1`.
  - `id:wfs-feedback-route`(피드백 → 품질/스킬·역할/에이전트·순서/오케·트리거/description 라우팅) — `stepByRole id:role-orchestrator`, `stepOrder 2`, `stepDependsOn wfs-audit`.
  - `id:wfs-change-log`(변경 기록) — `stepByRole id:role-inspection`, `stepOrder 3`, `stepDependsOn wfs-feedback-route`.
- **`id:wf-verify-harness`** (구조/트리거/baseline/dryrun): steps
  - `id:wfs-structure-check` — `stepByRole id:role-vnv`, `stepOrder 1`.
  - `id:wfs-trigger-validation`(should 8~10 + should-NOT near-miss) — `stepByRole id:role-vnv`, `stepOrder 2`, `stepDependsOn wfs-structure-check`.
  - `id:wfs-baseline-compare`(with/without skill) — `stepByRole id:role-vnv`, `stepOrder 3`, `stepDependsOn wfs-trigger-validation`.
  - `id:wfs-dryrun` — `stepByRole id:role-vnv`, `stepOrder 4`, `stepDependsOn wfs-baseline-compare`.
- 연결: 두 workflow는 harness에 `ho:hasWorkflow`로 물린다 — `core:h-multiagent`에 `ho:hasWorkflow id:wf-harness-evolution, id:wf-verify-harness` 추가(기존 `id:wf-multiagent, id:wf-compose-harness` 리스트에 append). step은 `hasComponent o hasStep` chain으로 롤업.
- **Phase6-3 assertion 평가는 신규 개체 없이 기존 `ho:Contract`(executable/structural) 재사용**(delta §G 명시).
- 각 step/workflow: prefLabel·definition(왜/언제)·기존 role·guardrail·tool을 **IRI 재사용**(gr-verify-proceed·gr-structural-coverage 등 present한 것)·tokenEstimate·maturity "draft".

## 파일 배치 (DA-4 그룹 디렉토리, ONTOLOGYSTYLE §4)
- workflow/step: `ontology/abox/core/process/workflows.ttl`(기존 unit에 append).
- ExecutionMode: 담을 그룹 판단 — `substrate/`(실행 기저) 또는 전용. **기존에 ExecutionMode 개체가 없으므로 신규 unit이면
  root `owl:imports`·`catalog-v001.xml`·recipe catalog 동기화까지 필요** → 이 경우 orchestrator에 먼저 보고(federation 배선은 REORG류 작업). **가능하면 기존 unit에 수용**해 신규 유닛/catalog 변경을 피한다(TestScenario·FailurePolicy도 동일 판단).
- 신규 unit이 불가피하면 그 사실 + 필요한 catalog/import 델타를 브리핑백으로 보고(직접 catalog 편집은 developer 범위 밖일 수 있음 — orchestrator 확인).

## 저작 규약 (ONTOLOGYSTYLE 요약)
- predicate 순서 §3, 4칸 스페이스 들여쓰기, prefLabel 1줄, definition은 "왜/언제 고르나".
- **어휘 발명 금지**(Golden Rule #2): 새 클래스/속성/Concept 만들지 않는다. 없는 속성·필요한 shape 확장은 **GAP 보고**.
- 텍스트 지닌 모든 노드에 `ho:tokenEstimate` 필수. 신규 노드 maturity `"draft"`.
- 착수 전 `python3 tools/retrieve.py "harness lifecycle verification execution mode"` 등으로 중복 재사용 확인.

## 완료 게이트 (developer 자기검증)
```bash
/usr/bin/python3 tools/validate.py     # 반드시 PASS (SHACL·reachability·capabilities·assemblyOrder)
/usr/bin/python3 tools/retrieve.py "verify harness structure and triggers"   # wf-verify-harness가 후보로 뜨는지
/usr/bin/python3 tools/retrieve.py "agent-teams vs sub-agents execution topology"  # ExecutionMode 검색
```
개체 수는 185 + (신규 개수)로 증가. git commit은 하지 않는다(inspection 소관). 산출을 orchestrator에 반환.

## 반환 시 보고 항목
저작한 개체 IRI 목록 + 연결 edge + validate PASS 로그 + retrieve 확인 + (있으면) TBox/shape/federation GAP.

---

# 실행 결과 (2026-07-24, developer dispatch 완료 · orchestrator 독립검증)

**저작 13개체 → `validate.py` PASS, 185→198.** 파일: `abox/core/process/workflows.ttl`(+117) ·
`abox/core/wholes/harnesses.ttl`(+11/−5, h-harness-factory 블록만).

- Workflow 2: `wf-harness-evolution` · `wf-verify-harness`
- WorkflowStep 7: `wfs-audit`·`wfs-feedback-route`·`wfs-change-log` / `wfs-structure-check`·`wfs-trigger-validation`·`wfs-baseline-compare`·`wfs-dryrun`
- TestScenario 2: `scn-compose-smoke`·`scn-trigger-near-miss` · FailurePolicy 2: `fp-dispatch-timeout`·`fp-validation-fail`

**orchestrator 독립검증**: 사용된 속성/클래스 전부 TBox 실재(발명 0) · abox 내 클래스/프로퍼티 선언 0 ·
신규 13노드 전부 `tokenEstimate`+`maturity "draft"` · SHACL/reachability/capabilities/assemblyOrder 전부 ✓.

## orchestrator 판정 — GAP 처리

- **GAP-1 (ExecutionMode) → 브리프 전제 오류 확정, 미저작이 옳음.** `ho:ExecutionMode`·`hasExecutionMode`·
  `stepExecutionMode`·`stepFailurePolicy`는 **TBox에 없다**(grep 0). 이 브리프 §1이 "클래스는 있고 개체만 0"이라고
  쓴 것은 오기였다. 해당 축은 Wave A의 **D2 경량화 결정**으로 `pat-agent-teams`/`pat-sub-agents`/`pat-hybrid`
  (DesignPattern, `tagged c-execution-mode`)로 이미 land돼 있고 retrieve로 검색된다. `mode-*` 저작은 클래스 발명 +
  중복(drift) 이중 위반이므로 **미저작 유지**(현행 D2 존속). ⇒ **조치 없음**.
- **GAP-2 (호스트 편차) → 승인.** 브리프는 `h-multiagent`를 지시했으나 developer가 `h-harness-factory`를 택함.
  근거 검증됨: ① 기존 주석이 정확히 이 노드들을 예약("Wave B2 will add the harness-lifecycle workflows; Wave C …
  demo test scenarios / failure policies") ② `h-harness-factory`의 `skos:definition`이 설계의도를 명시("the parts live
  here rather than on id:h-multiagent so binding them leaves that harness's materialized document byte-identical")
  ③ diff상 `h-multiagent` 트리플 **무변경**. ⇒ 브리프보다 developer 선택이 옳다. **편차 승인**.
- **GAP-3 (verification/ unit 부재) → 후속 과제.** DA-4상 TestScenario/FailurePolicy의 자리는 `core/verification/`인데
  중앙 unit이 없어 `process/workflows.ttl`에 co-locate됨. 이제 중앙 individual이 생겼으므로 ONTOLOGYSTYLE §4의
  레이아웃 규칙상 unit 신설이 맞다. 델타 = 새 파일 + root `owl:imports` 1줄 + `catalog-v001.xml` 1 uri +
  **recipe staging catalog 동기화**(recipes repo push 파급). 개체 IRI 불변 = 순수 relocation.
- **GAP-4 (미렌더) → 후속(Wave C, tools 영역).** `sectionKind` test-scenarios/error-handling/execution-mode/data-flow용
  AssemblySection 개체 + `materialize.py` 렌더러 부재 → scenario/failure-policy는 그래프 데이터로만 존재, CLAUDE.md에
  렌더되지 않음. 또 `scenarioReferences`가 `tools/ontology_lib.py:INSTANCE_LINK_PREDICATES` 미등록(도달성 무영향).
- **GAP-5 (네이밍표) → 후속.** `ONTOLOGYSTYLE §2` 표에 `scn-`·`fp-`(및 기존 `wfs-`·`dlv-`) 접두사 누락. 표 갱신 필요.

## 다음 단계
git land는 **inspection 세션** 소관(이 증분 미커밋). GAP-3/4/5는 별도 증분으로 계획한다.
