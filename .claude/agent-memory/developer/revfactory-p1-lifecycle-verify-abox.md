# revfactory P1 잔여 ABox — lifecycle/verify workflow + TestScenario/FailurePolicy

브리프가 지목한 "클래스는 있고 개체만 0"인 잔여분 저작. 결과: 185→198 individuals, validate PASS.

## ★brief의 클래스 목록을 믿지 말고 TBox를 먼저 grep
- brief는 `ho:ExecutionMode`+`hasExecutionMode`+`stepFailurePolicy`가 land됐다고 했으나 **TBox에 없음**
  (`grep -n "ExecutionMode" ontology/tbox/harness.ttl` → 0). Wave A에서 **D2 경량화 결정**으로
  일부러 만들지 않았고, 실행 topology 축은 이미 **DesignPattern 3개**(`pat-agent-teams`/`pat-sub-agents`/
  `pat-hybrid`) + `c-execution-mode` Concept로 표현돼 있었다. ⇒ `mode-*` 개체 저작은 (a) 클래스 발명이고
  (b) 같은 뜻 노드 중복(drift)이라 **양쪽으로 금지** → GAP 보고하고 나머지만 완주.
- 교훈: 브리프의 "이미 land됨" 목록은 delta-inventory의 *제안*이 섞여 있을 수 있다. 저작 전 ① TBox grep
  ② `retrieve.py "<축 이름>"`로 **기존 표현이 다른 어휘로 이미 있는지** 확인(여기선 retrieve가 pat-* 3개를
  바로 돌려줬다).

## 호스트 하네스 선택 = 파일 주석에 적힌 wave 계획을 따른다
- 브리프는 `h-multiagent`에 물리라 했지만, `harnesses.ttl`의 `h-harness-factory` 블록 주석에 이미
  "Wave B2가 harness-lifecycle workflow를, Wave C가 test scenario/failure policy를 여기에 추가"라고
  적혀 있었다 → **메타(주어가 harness 자신인) 파트는 h-harness-factory**가 정답. h-multiagent에 물리면
  그 CLAUDE.md Process 섹션이 변해 byte-identity가 깨진다(중앙 라이브러리 성장의 표준 회피책 = 전용 host).
- byte-id 증명: `materialize.py h-multiagent --out A` → `git stash` → 동일 명령 `--out B` → `git stash pop`
  → `diff -r A B`. **CLAUDE.md/MANIFEST.json 동일**, `harness.lock.json`의 전역 `individualCount`만
  185↔198로 다름(전역 필드라 어떤 증분이든 바뀜 — 이 차이는 정상, 회귀 아님).

## TestScenario / FailurePolicy 저작 실무
- 필수(SHACL): TestScenarioShape = prefLabel + `scenarioKind` **정확히 1개**(closed set: normal /
  existing-input / error / trigger-positive / trigger-negative) + `scenarioPrompt` ≥1 + maturity.
  FailurePolicyShape = prefLabel + `failureCondition` ≥1 + `recoveryStrategy` ≥1 + maturity.
  `scenarioExpected`는 반복 가능(수용기준 1개=1리터럴), `scenarioReferences`→WorkflowStep은 선택.
- 도달성: `hasTestScenario`/`hasFailurePolicy`는 **직접 ⊑hasComponent**(subject가 Harness) → 별도
  propertyChain 불요, harness에 물리기만 하면 ComponentConnectivityShape 통과.
- `ontology_lib.INSTANCE_CLASSES`에 두 클래스는 없지만 owlrl이 HarnessComponent로 추론 → 개체 카운트·
  retrieve에 정상 노출(HC fallback). 단 `scenarioReferences`는 `INSTANCE_LINK_PREDICATES`에 없어
  retrieve "Structure (edges)" 뷰에 안 보인다(도달성엔 무관, tools/ 수정은 developer 범위 밖).
- materialize에는 scenario/failure-policy **렌더러가 없다** → CLAUDE.md에 안 찍힘(Wave C: sectionKind
  test-scenarios/error-handling AssemblySection + emitter가 남은 일).

## 파일 배치 — `verification/` 유닛이 아직 없다
DA-4 그룹상 TestScenario/FailurePolicy(=VerificationComponent leaf)의 자리는 `core/verification/`이지만
중앙에 해당 data unit이 없다. 신규 unit = root `owl:imports` + `catalog-v001.xml` + recipe catalog 동기화
(=federation 3점, orchestrator 소관)라서 **기존 `process/workflows.ttl`에 배너 주석 달고 co-locate**했다
(개체 IRI는 위치 독립이라 나중 이동은 순수 relocation). 신규 unit이 필요하면 만들지 말고 델타만 보고.

## 저작한 것 (13)
Workflow 2(`wf-harness-evolution`/`wf-verify-harness`) + WorkflowStep 7(wfs-audit·feedback-route·
change-log / structure-check·trigger-validation·baseline-compare·dryrun) + TestScenario 2(scn-compose-smoke
normal · scn-trigger-near-miss trigger-negative) + FailurePolicy 2(fp-dispatch-timeout·fp-validation-fail),
전부 `h-harness-factory`에 배선. step의 role/tool/guardrail은 전부 기존 IRI 재사용 —
`gr-generalize-not-overfit`(피드백 라우팅), `gr-discriminating-eval`(baseline 비교),
`gr-well-formed-skill`(트리거 검증), `gr-integration-coherence`(구조 점검)가 의미상 정확히 맞는 짝.
