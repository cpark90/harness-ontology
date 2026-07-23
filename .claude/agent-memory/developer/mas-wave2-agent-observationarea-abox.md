# MAS Wave 2 — Agent + ObservationArea ABox instances + h-multiagent wiring

Wave 2 of the MAS refinement (ABox, after W1 TBox/shapes). File-exclusive =
`roles.ttl` + `harnesses.ttl` only. Models this repo's 5 operating agents as
partially-observed distributed nodes. Design source: `docs/plans/mas-observation-refinement.md`.

## Authored delta (validate PASS 173 = 158 + 15)
- 5 `ho:Agent` in roles.ttl (prefix `agent-`, brief-mandated): agent-{orchestrator,
  developer,vnv,inspection,synthesizer}. Each satisfies AgentShape: agentRole→existing
  Role (role-orchestrator ALREADY EXISTED, reused — NOT minted), agentObservation→2 areas
  (external+internal), agentFunction→EXISTING caps (orch=cap-orchestration, dev=cap-fileedit
  +cap-codeexec, vnv=cap-codeexec, inspection=cap-traceability, synth=cap-synthesis),
  cognitiveCapacity 150000 (uniform, mc-opus-derived "modeled loss-free capacity"),
  tagged c-multiagent, maturity draft.
- 10 `ho:ObservationArea` (prefix `oa-`): per agent one external + one internal.
  external: observesChannel + observedFileScope + observesMemory(mem-firmware,mem-longterm)
  + unobserved; internal: observesComponent(own Role) + observesMemory(mem-cache) + unobserved.
  Each has observationKind sh:in{internal,external}, tokenEstimate (ext 5k–12k, int 1.5k–2k;
  per-agent sum << 150000 capacity fit), maturity draft. ObservationAreaShape satisfied.
- harnesses.ttl: `id:h-multiagent ho:hasAgent` the 5 agents (2-line, indented continuation).

## ★ Key correctness points
- **role-orchestrator EXISTS** in roles.ttl (userFacing true, reviewed) — brief said
  "신설 if absent"; it was present → REUSED, no new Role. Verify before minting.
- **agentFunction is SOFT** (not in AgentShape) and points at EXISTING Capabilities.
  cap-synthesis is fine for agent-synthesizer even though role-synthesizer is bound to
  h-workspace-synthesis (not h-multiagent) — agentRole/agentFunction/observes* are plain
  reference edges, they don't require the target to be in the SAME harness; the target only
  needs to be an already-connected component (it is). No new orphan.
- **Anti-orphan = the 6th hasComponent propertyChain (hasComponent o agentObservation)**
  from W1: hasAgent⊑hasComponent gives harness→agent, chain rolls each area up. So wiring
  ONLY hasAgent on h-multiagent makes all 15 nodes reachable + ComponentConnectivityShape-clean.
  No host harness needed here (contrast B1 Channel/Guardrail which have NO such rollup and
  needed hasChannel/hasGuardrail direct wiring). Agent itself reachable via hasAgent directly.

## ★ Byte-identity: hasAgent has NO materialize emitter → CLAUDE.md unchanged
Proved WITHOUT git (brief forbids git): materialize h-multiagent post-change → save; then
temporarily REVERT both edits via Edit (harnesses hasAgent removed) + `head -n 161 roles.ttl`
(drop appended block) → materialize baseline; `cmp` CLAUDE.md = BYTE-IDENTICAL; then restore
full roles.ttl from a scratch copy + re-Edit hasAgent. Memory-tier precedent held: adding a
non-emitted hasComponent-family edge to h-multiagent leaves its projected CLAUDE.md identical.
(MANIFEST/lock DO change with node count — expected, not a regression.)

## Recipe propagation spot-check
staging/harness-recipes `central` = symlink → working tree, so recipe closure sees live
changes. 21-code-reviewer per-recipe validate (HARNESS_CATALOG=catalog-v001.xml,
HARNESS_ROOT_ONTOLOGY=.../21-code-reviewer, cd staging + central/tools/validate.py) →
PASS 188 (= core 173 propagated + 15 recipe-local). New core Agent/ObservationArea nodes
flow into the recipe import closure cleanly, no breakage.

## Flags for orchestrator
- **Prefix table**: ONTOLOGYSTYLE.md §naming table has no row for Agent/ObservationArea
  (new W1 kinds). Used `agent-` (brief) + `oa-` (observation-area, compact like mc-/sp-).
  Recommend registering both rows. `oa-` is an abbreviation vs the "full word" [지킴] rule —
  chose compactness for a repeated per-agent×kind axis; orchestrator may prefer a full-word
  prefix. Not blocking (validate is prefix-agnostic).
- cognitiveCapacity 150000 uniform is a MODELED representative value (loss-free session
  size), not a measured mc-opus field; consistent per plan §3d. Adjust if a real budget lands.
- agent-vnv agentFunction=cap-codeexec (no dedicated verification capability exists);
  agent-inspection=cap-traceability (git/single-source-of-truth fit). Both reuse, no new cap.
