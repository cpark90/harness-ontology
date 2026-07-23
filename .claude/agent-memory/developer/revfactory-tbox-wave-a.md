# revfactory reflection Wave A — TBox + shapes schema layer

revfactory/harness 방법론 반영의 스키마 기반층(TBox+shapes만, ABox/tools 후속 wave).
파일 배타=`tbox/harness.ttl`+`shapes/harness-shapes.ttl` 딱 둘.

## 저작 델타
- 클래스 2 ⊑HarnessComponent: `ho:TestScenario`(behaviour-acceptance fixture; ho:Contract=artifact
  tree, ho:Example=few-shot와 구별 명시), `ho:FailurePolicy`(condition→strategy 한 행).
- 직접 hasComponent sub-property 2: `hasTestScenario`/`hasFailurePolicy`(domain Harness,
  Memory/Role 꼴 direct sub — subject IS Harness라 propertyChain 불요, ComponentConnectivityShape 커버).
- refinement edge 2: `augmentsRole`(Instruction→Role, reach=hasInstruction), `scenarioReferences`
  (TestScenario→WorkflowStep, reach=hasTestScenario+hasStep chain).
- datatype: scenarioKind(sh:in 5)/scenarioPrompt/scenarioExpected(반복) · failureCondition/recoveryStrategy
  · integrationMode(Instruction,invoke|inline|reference-load) · agentType(Role,general-purpose|Explore|Plan|custom)
  · reinvocationKeywords(Harness) · triggerPhrase/outOfScope.
- shapes: AssemblySectionShape sectionKind sh:in +4(execution-mode·data-flow·error-handling·test-scenarios,
  기존 8 뒤) — emitter/instance는 Wave C, 여기선 허용값만. + TestScenarioShape/FailurePolicyShape(minCount).

## ★triggerPhrase/outOfScope domain 처리 (재사용 결정)
Harness+Instruction 공용 datatype property는 **rdfs:domain 생략 + definition에 "Domain: Harness +
Instruction" 명시**가 repo 관례. `owl:unionOf` domain은 repo 전체에 0회(grep 확인). 선례=
`implementationRef`/`selectionPolicy`/`scaffold` 셋 다 domain 생략+definition 설명(단일 domain이면
prp-dom로 타 클래스 subject 오타입). integrationMode/agentType/reinvocationKeywords는 단일 클래스라
domain 명시.

## 배치/검증
- TBox 클래스는 Deliverable 다음(HC 그룹 끝), object prop은 hasMemory 다음+hasSection 다음(refinement),
  datatype은 scaffold 앞에 그룹 삽입. 기존 predicate order(subClassOf→label→definition) 미러.
- ExecutionMode 클래스·hasExecutionMode/stepExecutionMode 속성 **만들지 않음**(D2 결정: 실행 topology는
  DesignPattern+appliesPattern으로 경량화, sectionKind execution-mode는 tagged c-execution-mode 패턴 렌더).
- validate PASS, 130 individuals INVARIANT(additive라 신규 instance 0=shape 위반 0). TBox additive 정석.
