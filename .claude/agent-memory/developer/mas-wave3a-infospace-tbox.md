# MAS Wave 3a — information-space hierarchy TBox/shapes/tools

Schema base layer for the 4-stage observation projection chain (Environment -> Domain ->
GlobalState -> LocalObservation). File-exclusive = `tbox/harness.ttl` + `shapes/harness-shapes.ttl`
+ `tools/ontology_lib.py` ONLY. No ABox/harnesses/roles/git (that is W3b). Design source:
`docs/plans/mas-observation-refinement.md` §3e + §6 MAS-W3.

## Authored delta (additive, validate PASS 173 INVARIANT)
- Classes 2, NON-HarnessComponent (ho:Domain form — NO rdfs:subClassOf, so NO
  ComponentConnectivityShape wiring pressure): `ho:EnvironmentSpace` (top anchor, infinite source)
  and `ho:GlobalState` (S of Dec-POMDP). Placed right after `ho:Domain` in the "Non-component
  concepts" block (they are the projection-chain neighbors of Domain).
- 4 ObjectProperties, NONE sub of hasComponent (projection chain, not component wiring):
  `scopedFrom`(Domain->EnvironmentSpace), `describesDomain`(GlobalState->Domain),
  `hasGlobalState`(Harness->GlobalState), `projectsFrom`(ObservationArea->GlobalState). New group
  "information-space projection chain" after the observesMemory group, before hasStep.
  ★ hasGlobalState is Harness->GlobalState but MUST NOT be ⊑hasComponent (GlobalState is not a
  HarnessComponent — mirrors ho:targetsDomain which is also Harness->non-component, not a
  hasComponent sub). This is the key mistype trap.
- shape 1: `ho:GlobalStateShape` (targetClass GlobalState): describesDomain min1 + prefLabel min1
  + maturity min1. EnvironmentSpace stays shape-free (bare anchor, like Domain).
- tools: added the 4 predicates to `INSTANCE_LINK_PREDICATES` (so projection chain counts as
  weak-connectivity links — else W3b env-space/global-state orphan) and `EnvironmentSpace`/
  `GlobalState` to `INSTANCE_CLASSES` (so they count as individuals + reachability targets).

## Why PASS held (additive-TBox invariant)
Zero new instances (W3b authors them) -> 0 shape violations -> 173 individuals unchanged.
INSTANCE_CLASSES/LINK additions have no effect on a graph with no such instances yet.
reachability chain for W3b: ObservationArea is already reachable via W1's 6th hasComponent chain;
env-space reached via Domain scopedFrom, global-state via harness hasGlobalState — all now
weak-connectivity links so W3b instances won't orphan.

## Flags (none blocking)
- projection edges are directional data links (scopedFrom Domain->Env, describesDomain
  GlobalState->Domain, projectsFrom Area->GlobalState); reachability closure in validate.py is
  undirected (weak connectivity) so direction does not affect orphan check — env-space at the
  "top" is still reachable because Domain points UP to it via scopedFrom. Confirmed fine.
- No ABox/host wiring here (W3b: harness hasGlobalState on h-multiagent + ObservationArea
  projectsFrom links in roles.ttl).
