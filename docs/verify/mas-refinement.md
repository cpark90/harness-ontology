# VERIFY — MAS 이론 재정리 (W1~W3b) 독립 검증

- 판정: **PASS** (blocking 결함 0) + 3 non-blocking note/REC
- 대상 설계: `docs/plans/mas-observation-refinement.md` (§3 Agent composite·ObservationArea
  internal/external·§3d 인지능력≠identity·§3e 정보공간 계층·§4 델타)
- 검증자: vnv (dispatch), 2026-07-23. developer self-check 불신뢰, 전 항목 직접 재실행.
- 인터프리터: `/usr/bin/python3` (rdflib/pyshacl/owlrl 보유).

---

## (1) 중앙 validate — PASS, 175, 4체크 green

```
/usr/bin/python3 tools/validate.py
  loaded graph: 4509 triples (post-reasoning)
  ✓ SHACL         — conforms, no orphaned/under-specified nodes
  ✓ reachability  — all 175 individuals reachable from a Harness
  ✓ capabilities  — every harness's required capabilities provided internally
  ✓ assemblyOrder — 1 harness total order; default holder resolves (8 sections)
  PASS
```

individual 수 = **175** (주장 일치). Agent 5 + ObservationArea 10 + env-space 1 +
global-state 1 이 모두 reachable 집합에 포함(orphan 0). 재현 메커니즘은 (2)(3)에서 확증.

## (2) TBox 패턴 정합 — 정합, propertyChain 동형

증거: `ontology/tbox/harness.ttl`, `ontology/shapes/harness-shapes.ttl` 직접 판독.

- `ho:Agent rdfs:subClassOf ho:HarnessComponent` (127-128) · `ho:ObservationArea
  rdfs:subClassOf ho:HarnessComponent` (132-133) ✓.
- `ho:hasAgent rdfs:subPropertyOf ho:hasComponent` (domain Harness, range Agent, 276-281)
  — subject가 Harness이므로 **direct subProperty**가 옳다(hasRole/hasMemory 관례와 동형). ✓
- **6번째 propertyChainAxiom** `( ho:hasComponent ho:agentObservation )` (188) —
  기존 WorkflowStep(hasStep)·PromptSection(hasSection) rollup과 **구조 동형**. 첫 링크가
  hasComponent라 추론 subject가 항상 Harness. `agentObservation`/`agentRole`/`agentFunction`은
  hasComponent의 direct subProperty가 **아님**(각 316-332) → Agent subject를 Harness로
  mistype하지 않는 anti-mistype 패턴 정확. ✓ (reasoned graph에서 Agent가 Harness로 오타입
  안 됨은 SHACL PASS·assemblyOrder=1로 확증.)
- `ho:EnvironmentSpace`·`ho:GlobalState`: `rdfs:subClassOf ho:HarnessComponent` **없음**
  (147-153) = 비-component(Domain 꼴). `ho:hasGlobalState`는 hasComponent의 subProperty가
  **아님**(366-370) → GlobalState가 HarnessComponent로 mistype되지 않음. ✓
- shape ↔ 개체 오타 대조(0 위반):
  - `AgentShape`(239-263): agentRole min1(sh:class Role)·**agentObservation min1**(sh:class
    ObservationArea)·**cognitiveCapacity min1**(sh:datatype xsd:integer)·prefLabel·maturity.
  - `ObservationAreaShape`(271-292): observationKind **sh:in ("internal" "external")**
    min1/max1·tokenEstimate min1(xsd:integer)·prefLabel·maturity. observes* soft(정상).
  - `GlobalStateShape`(300-306): describesDomain min1(sh:class Domain). EnvironmentSpace는
    shape-free anchor(정상).
  - 개체값 대조: observationKind = **5 "external" + 5 "internal"** (전부 closed set 내).
    cognitiveCapacity·tokenEstimate 전부 bare integer(=xsd:integer). SHACL PASS와 일치.

## (3) 정보공간 사슬 — 그래프에서 연결

증거: `roles.ttl`·`harnesses.ttl`·`domains-tasks.ttl` 판독.

```
env-space (EnvironmentSpace)
   ↑ scopedFrom          dom-design (Domain, domains-tasks.ttl:19)
   dom-design ho:scopedFrom id:env-space
global-state (GlobalState) ho:describesDomain id:dom-design   (domains-tasks.ttl:39)
h-multiagent ho:hasGlobalState id:global-state                 (harnesses.ttl:104)
10 × ObservationArea ho:projectsFrom id:global-state           (roles.ttl, 10 triples)
```

- 사슬: ObservationArea →projectsFrom→ global-state →describesDomain→ dom-design
  →scopedFrom→ env-space. **끊긴 링크 없음** (projectsFrom 실triple=10, area당 1개 확인).
- tools 등록: `ontology_lib.py:58` `INSTANCE_LINK_PREDICATES += {scopedFrom, describesDomain,
  hasGlobalState, projectsFrom}`. reachability는 이 술어를 weak(무향) 연결로 순회
  (`validate.py check_reachability`, adj[o].add(s)) → env-space·global-state가 Harness에서
  **실제로 도달**(단순 카운트 아님). instance_nodes는 INSTANCE_CLASSES 기반이며
  `EnvironmentSpace`·`GlobalState`가 `INSTANCE_CLASSES`(`ontology_lib.py:71`)에 등록되어
  노드로 계수됨 → 175에 포함되고 orphan 0.

## (4) materialize 무크래시 + prose byte-identity

```
/usr/bin/python3 tools/materialize.py h-multiagent --out <tmp>
  ✓ materialized Multi-agent orchestration harness   EXIT=0
  CLAUDE.md (68 components, ~49794 tokens) · MANIFEST.json · .claude/agents/(7) · channels(3) · lock
```

- `grep -c "hasAgent|agentObservation|projectsFrom|hasGlobalState|ObservationArea|HO.Agent|
  GlobalState|EnvironmentSpace|observesChannel|cognitiveCapacity" tools/materialize.py` = **0**
  → MAS 레이어 emitter/렌더러 분기 **부재**.
- 산출 `CLAUDE.md`에 MAS 노드 참조(agent-*/oa-*/global-state/env-space/hasAgent/
  cognitiveCapacity/observationArea/observesChannel) grep = **0**.
- ⇒ 렌더러에 MAS 분기가 없으므로 MAS 어떤 델타도 prose로 진입할 수 없음 = **prose 0바이트
  추가**를 구조적으로 확증(Memory 선례 방식; working-tree 원시 diff는 무관 변경 혼입으로 신뢰
  불가하여 구조적 격리로 증명). 임시 out dir는 검증 후 삭제.
- MANIFEST 정합: 컴포넌트 타입 히스토그램에서 **HarnessComponent 18 = Agent 5 + ObservationArea
  10 + Memory 3** (아래 N1 참조). global-state/env-space는 MANIFEST에 **부재**(비-component,
  hasComponent 미배선) = 올바름.

## (5) recipe 무영향 — 2개 per-recipe closure PASS

```
cd staging/harness-recipes
# 21-code-reviewer (catalog-v001.xml)
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=.../recipes/21-code-reviewer
  → ✓ all 190 individuals reachable · assembly order 1 · PASS   (= 중앙175 + 로컬15)
# 46-product-manager (catalog-46-product-manager.xml)
HARNESS_CATALOG=catalog-46-product-manager.xml HARNESS_ROOT_ONTOLOGY=.../recipes/46-product-manager
  → ✓ all 195 individuals reachable · assembly order 1 · PASS   (= 중앙175 + 로컬20)
```

- 중앙 175 전파가 두 recipe union을 깨지 않음. capabilities/SHACL/assemblyOrder 전부 green.
- **함정 기록**: 46은 `catalog-v001.xml`에 IRI 매핑이 **없어**(grep=0) 그 카탈로그로 돌리면
  로더가 중앙만 로드(175)해 조용히 통과한다 — 반드시 `catalog-46-product-manager.xml` 사용.
  각 recipe README(§Reproduce)가 자기 카탈로그를 명시하므로 그대로 따를 것.

## (6) coverage audit — MAS 이론 ↔ 표현

| MAS 개념 | 표현 | 판정 |
|---|---|---|
| Agent(분산노드) | `ho:Agent` × 5 (orchestrator/developer/vnv/inspection/synthesizer) | ✓ |
| O_i(인지영역) | `ho:ObservationArea` internal+external, **agent당 2개(≥1 hard)** = 10 | ✓ |
| A_i(행동집합) | `ho:agentFunction` → Capability (cap-orchestration/fileedit/…) | ✓ |
| π_i(정책) | `ho:agentRole` → Role (persona+guardrail+workflow 재사용) | ✓ |
| b_i(신념) | `ho:observesMemory` → Memory tier (firmware/cache/longterm) | ✓ |
| 통신 | `ho:observesChannel` → Channel | ✓ |
| topology | `ho:appliesPattern` pat-orchestrator-workers | ✓ |
| partiality | `ho:unobserved` (모든 area에 명시) | ✓ |

- **인지능력 ≠ identity (설계 §3d 준수)**: `cognitiveCapacity`(loss-free, Agent 속성)가 Role·
  ObservationArea와 **별개 노드/속성**으로 기록됨. Role(π_i)과 ObservationArea(O_i)는 Agent를
  통해 묶이되 **병합/동일시 아님** → "인지영역 ≡ 역할"이 identity가 아니라 효율 매칭으로 표현됨.
  **용량 적합** Σ(area tokenEstimate) ≤ cognitiveCapacity(150000) 만족: orch 11000·dev 7500·
  vnv 6500·inspection 13500·synth 9500 — 전부 << 150000. (SHACL 미강제, tool/review 검사.)
- **4-space 계층 형식화**: Environment(env-space) → Domain(dom-design) → GlobalState(global-state)
  → LocalObservation(ObservationArea) 가 (3)의 사슬로 그래프에 완전 형식화됨. ✓
- **표현 밖 요소의 명시성**: 용량적합 합산이 SHACL 미강제인 점은 shape 주석(harness-shapes.ttl
  266-270)과 TBox definition(cognitiveCapacity 621-625)에 **의도적·명시**로 기록 — 수용가능.
  **누락 GAP 없음.**

---

## Notes / RECs (전부 non-blocking)

- **N1 (tools 등록 — brief 기술 부정확, 구현은 정확)**: brief는 "INSTANCE_CLASSES += Agent·
  ObservationArea·EnvironmentSpace·GlobalState" 라 했으나 실제 추가는 **EnvironmentSpace·
  GlobalState 2개뿐**(`ontology_lib.py:71`). 이는 **올바른** 구현이다 — Agent/ObservationArea는
  HarnessComponent 하위클래스라 subsumption으로 이미 계수·reachable(등록 불요)이고, 비-component는
  등록해야만 노드로 계수됨(안 하면 orphan). 관측 가능한 유일 결과: MANIFEST가 Agent 5·
  ObservationArea 10·Memory 3을 **generic "HarnessComponent"로 fallback typing**(most_specific_types
  화이트리스트 미포함). emitter 없고 그래프 영향 0이라 무해 — agent-memory 검증의 REC와 동일.
  MANIFEST 정밀 타이핑을 원하면 `HO.Agent`·`HO.ObservationArea`를 INSTANCE_CLASSES에 추가
  (tools 변경 = developer 범위). **권고(선택), 비차단.**
- **N2 (cognitiveCapacity 대표값)**: 5 agent 모두 150000 균일. 설계 §3d "mc-* 파생"에 비춰
  대표 loss-free window로 **수용가능**하되, agent별 실제 model에서 파생하는 것이 향후 refinement.
  값이 기록되어 mismatch가 inspectable하다는 목적은 충족. 비차단.
- **N3 (단일 global-state)**: global-state 1개가 dom-design만 describes. 단일 도메인 repo에
  적절하고 describesDomain min1 만족. 비차단.

## 재현 명령 요약
```
/usr/bin/python3 tools/validate.py
/usr/bin/python3 tools/materialize.py h-multiagent --out <tmp>   # then rm <tmp>
grep -c "hasAgent|agentObservation|projectsFrom|hasGlobalState|ObservationArea|cognitiveCapacity" tools/materialize.py
cd staging/harness-recipes
HARNESS_CATALOG=catalog-v001.xml            HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/21-code-reviewer  /usr/bin/python3 central/tools/validate.py
HARNESS_CATALOG=catalog-46-product-manager.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/46-product-manager /usr/bin/python3 central/tools/validate.py
```
