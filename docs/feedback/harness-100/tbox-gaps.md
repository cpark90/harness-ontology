# harness-100 코퍼스 — TBox 스키마 gap 분석

> 출처: inspection dispatch 분석(2026-07-23). 우리 TBox(`ontology/tbox/harness.ttl`) vs 코퍼스가
> 표현하는 개념. 상위 제안: `../harness-100-augmentation.md`. 관련: 승인된 `../finer-harness-decomposition-assembly.md`.

## 요지
코퍼스는 균일해서 대부분 기존 어휘로 매핑되나, **5개 실질 gap**이 있다. 전부 기존 `hasComponent`
sub-property/propertyChain 관용구로 **orphan 없이** 연결 가능(신규 SHACL shape 불필요). GAP-1이 모델
형태를 바꾸는 최대 건이며, **이미 승인된 finer-decomposition(WorkflowStep)의 직접 확장**이다.

## 매핑 요약 (MAPS)
Agent-Team mode → `Workflow`+`DesignPattern`(orchestrator-workers) · 5-agent 팀 → `Role`+`hasRole`
(reviewer는 Concept 태그, 새 클래스 아님) · 좌표 프로토콜/review-loop → `Channel`+`channelMedium`/
`channelParticipant` · error-handling → `Guardrail` · 구조화출력 템플릿 → `artifactTemplate`(GAP-D 이후).

## GAP + 권고 스키마 delta (중요도순)

### GAP-1 (Deliverable + step-간 데이터흐름 DAG) — 최우선
코퍼스 중심 메커니즘. 현 `WorkflowStep`은 `stepOrder`(총 정수순)+`stepByRole`만 → **병렬 분기·
데이터흐름·산출물**을 못 담음.
- **`ho:Deliverable`** ⊑HarnessComponent — "워크플로 step/역할이 생산하고(`_workspace/*`) 하류 step이
  소비하는 명명 아티팩트". `artifactTemplate`(출력 스키마)·`tokenEstimate` 보유.
- **`ho:stepProduces`**(WorkflowStep→Deliverable)·**`ho:stepConsumes`**(WorkflowStep→Deliverable) —
  데이터흐름 명시(DAG = produces/consumes 조인으로 복원).
- **`ho:stepDependsOn`**(WorkflowStep→WorkflowStep, `owl:TransitiveProperty`) — 순서 DAG(2a·2b가 1에
  동시 의존=병렬, `stepOrder`로 불가능).
- **anti-orphan**: `hasComponent`에 propertyChain `(hasComponent hasStep stepProduces)` 추가 →
  Deliverable이 바인딩 harness로 rollup(기존 `implementationCandidate`/`capabilityContract`/`hasStep`
  체인과 동일 관용구, 별도 shape 불필요).

### GAP-2 (ExecutionMode / scale modes) — 高
- **`ho:ExecutionMode`** ⊑HarnessComponent — "요청범위 tier별 role/workflow 부분집합 활성화 프로파일
  (Full/Backend/MVP)". **`ho:hasMode`**(Harness→, ⊑hasComponent) · **`ho:modeActivatesRole`**
  (ExecutionMode→Role, 이미 hasRole된 role 지시) · datatype **`ho:modeTrigger`**(요청 패턴).

### GAP-3 (trigger boundaries) — 中高 (datatype only, orphan 위험 0)
- **`ho:triggerPhrase`**(Harness, xsd:string, 반복) — in-scope 활성화 cue.
- **`ho:outOfScope`**(Harness, xsd:string, 반복) — 명시적 배제(237파일에 존재하나 현재 담을 곳 없음).

### GAP-4 (TestScenario) — 中
- **`ho:TestScenario`** ⊑HarnessComponent — "행위 수용 fixture: 샘플 요청+기대 결과, kind별".
  **`ho:hasTestScenario`**(⊑hasComponent) · datatype `ho:scenarioKind`(normal|existing-input|error)·
  `ho:scenarioPrompt`·`ho:scenarioExpected`. `Contract`(빌드트리 검사)·`Example`(few-shot)와 구별.

### GAP-5 (skill→agent 확장) — 中
- **재사용 우선**: extending 스킬 = `ho:Instruction` + 신규 **`ho:augmentsRole`**(Instruction→Role)
  "이 지시번들이 특정 역할의 도메인 전문성을 확장". (대안: 전용 `ho:Skill` 서브클래스.)

## 모델하지 말 것 (의도적)
- per-agent tool/model least-privilege: 우리 `roleTool`/`roleGuardrail`/`usesModel`이 **더 표현적**
  (코퍼스는 agent를 name+description만으로 선언, 0파일이 tools/model 지정) → delta 불필요.
- concrete 기술스택 표·severity 마커(🔴🟡🟢)·`_workspace` 넘버링 = ABox free-text/materialize 관례, 어휘 아님.

## 우선순위
**GAP-1(Deliverable+DAG) ≫ GAP-2(ExecutionMode) > GAP-3(trigger) > GAP-4(TestScenario) > GAP-5(augmentsRole).**
GAP-1만 모델 형태를 바꾸고 나머지는 additive leaf. 전부 기존 관용구로 연결 → orphan/신규 shape 없음.
