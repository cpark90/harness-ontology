# disambiguation audit(관측 3분할 + 정의 정리) 검증 재현 절차

DA-1(구조): `ho:ObservationArea` 삭제 → 3분할 `ho:ObservationSpace`(Ω_i)/`ho:AreaOfInterest`(intent)/
`ho:AreaOfObservation`(realized). DA-2(정의): B~F 5쌍 skos:definition 자기지칭·중복 제거.
판정: docs/verify/disambiguation.md → **PASS + 3 non-blocking(N1 내부AoO무AoI/N2 STYLE예시오탈/N3 capacity대표값)**.

## 핵심 검증 포인트 (재사용)
- **3분할 rollup = Agent/WorkflowStep 동형 확장**: agentObservation(Agent→Space, range=Space,
  NOT⊑hasComponent) + propertyChain **6/7/8**: `(hasComponent agentObservation)` / `(… hasAreaOfInterest)`
  / `(… hasAreaOfObservation)`. 7/8은 **Deliverable 5번째 3-link(hasComponent hasStep stepProduces)와
  동형** — hasComponent 접두로 inferred subject=Harness. 3클래스 전부 ⊑HarnessComponent라
  subsumption 계수(INSTANCE_CLASSES 등록 불요). hasAreaOf*/coversInterest 전부 NOT⊑hasComponent
  (중간노드/양끝비Harness mistype 방지). validate PASS+orphan0이 rollup 완결 실증.
- **ABox 배선**: 각 agent Agent→agentObservation→os-(1)→{aoi-(≥1), oa-×2(ext/int)}, ext-oa가
  coversInterest aoi-. capacity fit Σ(oa tokenEstimate)≤cognitiveCapacity(150000) **눈 합산**(SHACL
  미강제). observationKind sh:in{internal,external} 문자대조. 신규 20=os5+aoi5+oa10.
- **잔재 grep 필수**: `grep -rn ObservationArea ontology/ tools/ ONTOLOGYSTYLE.md`=0. domains-tasks
  투영사슬 서술·ONTOLOGYSTYLE 명명표(os-/aoi-/oa-)까지 치환 확인.

## DA-2 정의 비중복 판정법 (B~F)
각 쌍이 **① genus 자기지칭 제거 ② 양방향 "Distinguished from" 절 ③ 예시 비중복**인지 3점 확인.
- B Workflow(hasStep 구체)↔DesignPattern(appliesPattern tag): 과거 겹친 ReAct/plan-execute 예시가
  양쪽에서 제거됐는지(→single-pass/branch-merge vs orchestrator-workers/pipeline)가 핵심 신호.
- C Guardrail 정의문에서 "constraint" genus 제거 / D SystemPrompt에서 "instruction" 제거 /
  E Tool에서 "capability" genus→"operation that PROVIDES capabilities". grep로 definiens 잔재 확인.
- **flag(ho:notation 미존재)**: Instruction이 notation 대신 triggerPhrase(759)+integrationMode(734)
  참조 — 이 둘이 datatype prop로 **실재**하면 정의 정합 OK(notation 불요). grep ho:notation=0 확인.

## byte-identity (관측+class정의 둘 다 미emit)
관측술어 grep tools/materialize.py=0 + h-multiagent build exit0 산출물 관측참조=0(N1 방식).
**추가**: DA-2가 바꾼 건 **class-level skos:definition** → materialize는 individual 텍스트만 emit,
class 정의 미참조. class-def 특유 문구("imperative rule that disciplines"/"always-on persona framing"
/"classification tag"/"concrete means")를 CLAUDE.md에 grep=0으로 **class 정의 미emit** 확증(원시 HEAD
diff 대신 구조적 격리). recipe(21 catalog-v001/46 전용카탈로그)는 additive 상속, 200/205 reachable PASS.
