# MAS 이론 재정리(W1~W3b) 검증 재현 절차

`ho:Agent`·`ho:ObservationArea`(⊑HarnessComponent) + `ho:EnvironmentSpace`·`ho:GlobalState`
(비-component, Domain 꼴) + 투영사슬 4술어(scopedFrom/describesDomain/hasGlobalState/projectsFrom).
판정: docs/verify/mas-refinement.md → **PASS + 3 non-blocking(N1 tools/N2 대표값/N3 단일 global-state)**.

## 핵심 검증 포인트 (재사용)
- **Agent composite 패턴 = WorkflowStep/PromptSection rollup 동형**: `hasAgent ⊑ hasComponent`
  (direct subProp, subject=Harness=hasRole 관례) + **propertyChain `(hasComponent agentObservation)`**
  로 ObservationArea rollup. agentRole/agentObservation/agentFunction는 hasComponent subProp가
  **아님**(Agent를 Harness로 mistype 방지). reasoned SHACL PASS+assemblyOrder=1이 mistype 부재 실증.
- **비-component(Env/GlobalState) 처리**: subClassOf HarnessComponent **없음**, hasGlobalState는
  hasComponent subProp **아님**. → reachability에 잡히려면 반드시 **INSTANCE_CLASSES 등록 필요**
  (subsumption 못 타므로). 등록해서 175에 계수+투영사슬 link predicate로 weak-connect.
- **★INSTANCE_CLASSES 비대칭 규율(중요)**: component 하위(Agent/ObservationArea/**Memory**)는
  HarnessComponent subsumption으로 이미 계수·reachable → INSTANCE_CLASSES 등록 **불요**(등록해도
  무해). 비-component(Env/GlobalState/Domain)는 등록 **필수**. brief가 "Agent도 등록" 했다 해도
  실제 미등록이 **옳음**. 대가: MANIFEST most_specific_types가 미등록 component를 generic
  "HarnessComponent"로 fallback typing(히스토그램 HarnessComponent N = Agent+OA+Memory 합으로 확인).
  emitter 없으면 무해 → 정밀 타이핑 원할 때만 tools REC(developer 범위).
- **투영사슬 연결 확인**: env-space ←scopedFrom← dom-design ←describesDomain← global-state
  ←projectsFrom← N개 ObservationArea, harness hasGlobalState global-state. projectsFrom 실triple
  수(grep 제외 comment/definition-string)가 area 수와 일치해야 사슬 완결.
- **capacity fit(§3d 비-identity)**: Σ(area tokenEstimate) ≤ cognitiveCapacity를 눈으로 합산
  (SHACL 미강제=의도적, shape/definition 주석에 명시 확인). Role·ObservationArea가 **별개 노드**
  로 Agent에 묶임=identity 아님. observationKind는 5+5 등 sh:in{internal,external} 문자 대조.

## materialize byte-identity (prose 0바이트)
grep -c MAS술어 tools/materialize.py=0(렌더러 분기 부재) + 산출 CLAUDE.md에 MAS노드참조 grep=0
→ 구조적 확증. h-multiagent build exit0. 임시 out dir, 검증 후 rm. (Memory 선례와 동일 방식.)

## ★recipe closure 카탈로그 함정 (실수 방지)
per-recipe closure는 **recipe별 전용 카탈로그** 필요. 46은 catalog-v001.xml에 IRI 매핑 없어
그걸로 돌리면 로더가 **중앙만 로드(175)해 조용히 PASS**(오탐 통과). 반드시 recipe README
§Reproduce의 HARNESS_CATALOG(예 catalog-46-product-manager.xml) 사용. 통과 신호=individuals가
중앙+로컬(21:190=175+15, 46:195=175+20)이고 "1 harness assembly order".
