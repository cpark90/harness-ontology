# MAS Wave 1 — Agent + ObservationArea TBox/shapes schema layer

Multi-agent-system-theory refinement of the agent-utilization structure (schema base layer only,
TBox+shapes; ABox/tools/harnesses = later waves). File-exclusive = `tbox/harness.ttl` +
`shapes/harness-shapes.ttl`. Design source: `docs/plans/mas-observation-refinement.md` §3/§4/§6.

## Authored delta (correct, additive, validate PASS 158 INVARIANT)
- Classes 2 ⊑HarnessComponent: `ho:Agent` (partially-observed distributed node the harness compiles
  from a Role; bundles agentRole=mandate/policy + agentObservation≥1=cognitive region O_i +
  agentFunction=action space A_i; bounded by cognitiveCapacity=loss-free context) and
  `ho:ObservationArea` (one area-of-interest per inference; observationKind internal|external).
  Placed after `ho:FailurePolicy` (end of HC group), before `# Non-component concepts`.
- Direct hasComponent sub 1: `ho:hasAgent` (domain Harness, range Agent — hasRole/hasMemory 꼴, subject
  IS Harness so direct sub, NOT chain). Placed before channelParticipant.
- Agent-composite object props (NOT hasComponent sub): `agentRole`(→Role), `agentObservation`
  (→ObservationArea), `agentFunction`(→Capability). ObservationArea object props (NOT sub):
  `observesComponent`(→HarnessComponent), `observesChannel`(→Channel), `observesMemory`(→Memory).
  Placed as new group before `hasStep`.
- Datatype: `cognitiveCapacity`(Agent,int), `observationKind`(ObservationArea,string; sh:in
  internal|external), `observedFileScope`(ObservationArea,string), `unobserved`(ObservationArea,string).
  Placed before `ho:userFacing`. **Area size REUSES existing `ho:tokenEstimate` — no new size prop.**
- shapes: `ho:AgentShape` (agentRole min1 · agentObservation min1[hard] · cognitiveCapacity min1 ·
  prefLabel min1 · maturity min1; agentFunction NOT required=soft). `ho:ObservationAreaShape`
  (observationKind sh:in(internal external) min1 maxCount1 · tokenEstimate min1 · prefLabel · maturity;
  observes* SOFT=not required).

## ★ propertyChainAxiom = ObservationArea rollup (orphan defense, 6th chain)
Added `owl:propertyChainAxiom ( ho:hasComponent ho:agentObservation )` as the **6th** chain on
`ho:hasComponent`, + one sentence to its skos:definition (mirroring the 5 existing chain descriptions).
Mechanism = EXACT twin of the PromptSection 4th chain: `hasAgent ⊑ hasComponent` makes
`harness hasComponent agent` inferred → +agentObservation → `harness hasComponent area`. So
ObservationArea (⊑HC) is reachable + passes ComponentConnectivityShape WITHOUT making agentObservation
a direct hasComponent sub (which would mistype the Agent subject as a Harness via rdfs:domain). 2-link
chain, prefix hasComponent MANDATORY. Agent itself is reachable directly via hasAgent⊑hasComponent.

## Why PASS held (additive-TBox invariant)
Zero new instances → 0 shape violations → 158 individuals unchanged; chains have no instances so no
inference effect. TBox additive = standard. NO ABox/harness wiring in this wave (B1 lesson: Channel/
Guardrail ⊑HC need host-harness wiring in the SAME wave to self-PASS — but Agent/ObservationArea have
0 instances here, so no orphan yet; Wave 2 authors instances + `h-multiagent hasAgent` wiring and MUST
satisfy AgentShape/ObservationAreaShape + rollup then). agentFunction→Capability: at instance time,
agentFunction alone does NOT satisfy CapabilityConnectivityShape (needs requires/provides) — Wave 2 note.

## Language
skos:definition/prefLabel = ENGLISH (brief gave Korean intent; language policy → graph data values EN).
Wrote long style-matching definitions (reachability/wiring rationale) per repo convention.

## Flags (none blocking)
- Capacity FIT (Σ area tokenEstimate ≤ cognitiveCapacity) is NOT SHACL-enforceable (no aggregation) —
  documented in shape comment + both definitions as tool/review check. Consistent with plan §3d/§4.
- No ambiguous points forced; ObservationArea sized by cognitiveCapacity (not role identity) per §3d.
