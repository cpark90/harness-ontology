# MAS Wave 3b — information-space hierarchy ABox + projection links

Completes the 4-stage observation projection chain as INSTANCES + links (after W3a
schema). File-exclusive = `domains-tasks.ttl` + `roles.ttl` + `harnesses.ttl` +
`ONTOLOGYSTYLE.md` ONLY. No tools/tbox/shapes/staging/git. Source:
`docs/plans/mas-observation-refinement.md` §3e/§6.

## Authored delta (validate PASS 175 = 173 + 2)
- domains-tasks.ttl: 2 singleton instances (own "Information-space projection chain"
  section, after Domains, before Tasks): `id:env-space a ho:EnvironmentSpace`
  (prefLabel/definition/maturity — NO tokenEstimate, it is a Domain-form non-component
  concept, not projected text; like Domain it carries neither tokenEstimate nor shape)
  and `id:global-state a ho:GlobalState` (+ `ho:describesDomain id:dom-design`,
  satisfies GlobalStateShape=describesDomain/prefLabel/maturity min1). Chain closed
  above by adding `ho:scopedFrom id:env-space` to the EXISTING `id:dom-design`
  (reused, brief-recommended = altLabel "structured design work", best fit of the 4
  domains; NO new Domain minted).
- roles.ttl: `ho:projectsFrom id:global-state` on all 10 ObservationAreas
  (oa-<5agents>-external/internal), placed right after `ho:observationKind`. Local
  observation = partial projection of the global state.
- harnesses.ttl: `ho:hasGlobalState id:global-state` on `id:h-multiagent`
  (after hasAgent block, before hasAssemblySection). NOT a hasComponent sub.
- ONTOLOGYSTYLE.md prefix table: added rows `agent-`/`oa-`/(singleton env-space,
  global-state) — resolves the W2 flag. `oa-` registered as an accepted compact
  prefix (like mc-/sp-).

## ★ Key correctness points
- env-space/global-state are NON-HarnessComponent (Domain-form) so NOT covered by
  ComponentConnectivityShape → orphan avoidance is via WEAK-CONNECTIVITY, not
  hasComponent. W3a registered the 4 projection predicates in
  `ontology_lib.INSTANCE_LINK_PREDICATES` so these edges count as connectivity links:
  global-state reachable via harness hasGlobalState; env-space via dom-design
  scopedFrom (direction is irrelevant — validate reachability is undirected).
  So NO host harness / hasComponent wiring needed here.
- Individual count +2 only (the 2 new singletons). projectsFrom×10 / hasGlobalState /
  scopedFrom add edges, not individuals; ObservationAreas/Domain already counted.

## ★ Byte-identity: hasGlobalState + projectsFrom have NO materialize emitter
`grep hasGlobalState|projectsFrom|GlobalState|scopedFrom|describesDomain tools/materialize.py`
= ZERO references → projected CLAUDE.md provably unchanged. Proved WITHOUT git
(brief forbids git): materialize h-multiagent (current) → save; python-strip the added
lines from the 3 ttl (backup first with cp to scratchpad) → materialize baseline →
`cmp` CLAUDE.md = BYTE-IDENTICAL → restore all 3 files from cp backups → re-validate
175 PASS. (MANIFEST/lock DO change with node count — expected.) Same pattern as W2 hasAgent.

## Recipe propagation spot-check
21-code-reviewer per-recipe closure (central=symlink→working tree): PASS 190
(= core 175 propagated + 15 recipe-local; was 188 at W2 with 173). New info-space
nodes flow into the import closure cleanly, no breakage.

## Flags (none blocking)
- Domain choice for global-state describesDomain = `id:dom-design` (brief-recommended,
  best of the 4). Not deeply ambiguous but noted: global-state is currently modeled as
  the state of ONE representative domain (dom-design, the domain h-multiagent targets).
  If per-domain global states are later wanted, mint one GlobalState per Domain — the
  schema (describesDomain, non-shape cardinality) already allows N.
