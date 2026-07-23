# agent-design-patterns.md 커버리지 판정 (내 제안이 다 반영하나?)

> 출처: inspection(2026-07-23). 대상: `revfactory/harness`(harness-100과 **다른 repo**)의
> `skills/harness/references/agent-design-patterns.md` — 코퍼스를 만든 **설계 방법론 레퍼런스**.
> 상위 제안: `../harness-100-augmentation.md`.

## 결론: **부분 반영. "다"는 아니다.**
내 제안은 harness-100 **인스턴스 100개 실측**에서 도출돼 **지배적 구조(orchestrator-workers) + role/skill/
guardrail 원형 + coordination/DAG 메커니즘**을 담았다. 그러나 이 레퍼런스는 그 **위층 방법론** —
**named 패턴 taxonomy(6종)·agent-type taxonomy·설계 거버넌스 원칙**을 정의하며, 상당 부분이 아직
first-class로 반영되지 않았다. (좋은 소식: orchestrator가 이미 확정한 **"pluggable coordination pattern"**
방향이 이걸 흡수할 정확한 프레임이다.)

## 커버리지 표
| 레퍼런스 개념 | 반영? | 비고 |
|---|---|---|
| Agent Teams(peer) vs **Sub-agents(경량 순차)** 실행모드 | 부분 | 열린결정1 확정=pluggable(pat-peer-mesh+chan-peer). **Sub-agents 모드는 미반영** |
| **Supervisor** 패턴 | ✅ | ≈ orchestrator-workers |
| **Producer-Reviewer** | 부분 | reviewer role·cross-validation·bounded-iteration은 있으나 **named pattern 아님** |
| **Pipeline**(순차의존) | 구조만 | GAP-1 `stepDependsOn`이 mechanism, **named pattern 아님** |
| **Fan-out/Fan-in** | 구조만 | GAP-1 병렬분기 mechanism, **named pattern 아님** |
| **Expert Pool**(router→specialist) | ❌ 미반영 | |
| **Hierarchical Delegation**(2-level, depth≤2) | ❌ 미반영 | + depth-limit 규칙 |
| **Agent-type taxonomy**(general-purpose/Explore/Plan/custom) + tool-access scope | ❌ 미반영 | 내 분석은 "all general-purpose" 관찰만. built-in read-only 타입 미모델 |
| **`model: "opus"` 필수** | ⚠️ 불일치 | 내 분석은 "코퍼스 agent가 model 미선언"이라 했는데 **레퍼런스는 opus 필수**라 규정 → 재확인 필요 |
| Agent 정의 템플릿 + 필수 섹션(핵심역할/작업원칙/**I/O 프로토콜**/팀통신/에러핸들링/협업) | 부분 | role 템플릿은 있으나 I/O 프로토콜·섹션 규격 미반영(GAP-1 Deliverable과 연결 가능) |
| **설계 거버넌스**: 분리기준·재사용/일반화 매트릭스·역할범위 | ❌ 미반영 | composition-methodology와 일부 겹치나 이 규칙들은 미포착 |
| **Skill↔Agent 연결 3방식**(explicit invoke / inline / reference-load) | 부분 | GAP-5 `augmentsRole`는 관계만, 3방식 구분 없음 |
| **복잡도 guardrail**: no-nested-teams·single-active-team·flattening·depth-limit·**bottleneck 회피** | ❌ 미반영 | 신규 중립 guardrail 후보 |
| _workspace / I/O·팀통신·에러 프로토콜 / reference-load | ✅ | chan-workspace·GAP-1·guardrail·artifactTemplate |
| TaskCreate/TaskUpdate·SendMessage(to:name / to:all) | 부분 | channel medium으로 있으나 broadcast-cost 등 뉘앙스 미포착 |

## 반영 권고 (roadmap 보강분 — 대부분 **중앙 중립 라이브러리** 강화)
이 레퍼런스는 recipe가 아니라 **중앙 neutral parts(패턴·원칙)**를 강화한다:
1. **패턴 taxonomy를 중앙 `ho:DesignPattern`으로 승격**: `pat-pipeline`·`pat-fanout-fanin`·`pat-expert-pool`·
   `pat-producer-reviewer`·`pat-supervisor`(≈기존 orchestrator-workers)·`pat-hierarchical-delegation`.
   → orchestrator의 "pluggable coordination" 결정과 정합. recipe가 `appliesPattern`으로 골라 씀.
2. **실행모드 축**: Agent-Teams(peer) vs Sub-agents(순차) — `ExecutionMode`(GAP-2)와 별개의 coordination
   모드. `pat-*`와 어떻게 관계 지을지 설계 필요.
3. **agent-type taxonomy**: general-purpose/Explore/Plan을 Role의 tool-access 프로파일로(우리 `roleTool`
   least-privilege와 자연 연결). built-in read-only 타입 = roleTool 제한으로 표현.
4. **복잡도/거버넌스 guardrail(중립)**: `gr-depth-limit`(≤2)·`gr-no-nested-teams`·`gr-bottleneck-avoidance`·
   `gr-bounded-iteration`(명시화). 분리/재사용 기준은 composition-methodology(`wf-compose-harness`/
   `gr-reuse-first`) 보강으로.
5. **불일치 해소**: `model:opus 필수`(레퍼런스) vs 코퍼스 agent model 미선언(실측) — 어느 쪽을 SPEC으로
   삼을지 확인(레퍼런스=규범, 인스턴스=실태).
6. **Skill 연결 3방식**을 GAP-5(`augmentsRole`) 설계에 반영(explicit/inline/reference-load).

## 성격
이건 **인스턴스가 아니라 방법론 반영**이라 대부분 **중앙 TBox/부품 강화**(패턴·guardrail·agent-type)이고,
harness-100 인스턴스 임포트(recipe-side)와 **직교**한다. → augmentation 로드맵에 **"패턴·거버넌스 축"을
추가**하는 것을 권고(별도 inc로). 저작은 orchestrator→developer.
