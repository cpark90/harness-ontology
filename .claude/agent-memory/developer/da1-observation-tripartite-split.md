# DA-1 — ObservationArea → 3-class atomic split (ObservationSpace / AreaOfInterest / AreaOfObservation)

Disambiguation refactor: the old `ho:ObservationArea` conflated 3 sensing/attention concepts.
Split atomically (TBox+shapes+tools+ABox in one dispatch, no transient broken state). File-exclusive
= `tbox/harness.ttl` + `shapes/harness-shapes.ttl` + `tools/ontology_lib.py` + `roles.ttl` +
`harnesses.ttl`. Design: `docs/plans/disambiguation-audit.md` §A. validate PASS 185, recipe 21 PASS 200.

## The 3 classes (all ⊑HarnessComponent, replace ObservationArea in place)
- `ho:ObservationSpace` (Omega_i): the CAN-observe envelope, exactly 1 per Agent, projectsFrom
  GlobalState, bounded above by cognitiveCapacity. Container of AoI + AoO.
- `ho:AreaOfInterest` (AoI): what the role WANTS/NEEDS (intent), observationKind, NO tokenEstimate
  (intent isn't consumed input — shape doesn't require it).
- `ho:AreaOfObservation` (AoO): what is ACTUALLY observed (realized), observationKind + observes*/
  observedFileScope + tokenEstimate (realized size) + coversInterest.

## Property wiring (the reachability spine)
- `agentObservation` retargeted Agent→**ObservationSpace** (was →ObservationArea).
- NEW mid-node props, NONE ⊑hasComponent (subject is the intermediate, not the Harness):
  `hasAreaOfInterest`(Space→AoI), `hasAreaOfObservation`(Space→AoO), `coversInterest`(AoO→AoI).
- ★ propertyChainAxiom on hasComponent: 6th `(hasComponent agentObservation)` now rolls up the
  SPACE; ADD 7th `(hasComponent agentObservation hasAreaOfInterest)` + 8th `(... hasAreaOfObservation)`
  — 3-link chains, EXACT twin of the 5th `(hasComponent hasStep stepProduces)`. This is what keeps
  aoi/oa orphan-free without direct hasComponent subs (which would mistype Space subject as Harness).
- domain re-homing: `projectsFrom`→ObservationSpace; `observesComponent/Channel/Memory`+
  `observedFileScope`→AreaOfObservation.

## ★ Shared-domain trap (unobserved + observationKind)
`observationKind` is on BOTH AoI and AoO; `unobserved` is on BOTH ObservationSpace and AoO. OWL RL
prp-dom means a single rdfs:domain would mistype the other class → **OMIT rdfs:domain, state
applicability in skos:definition** (the triggerPhrase/observationKind precedent). ⚠ Brief literally
said "unobserved→domain ObservationSpace" BUT also "keep unobserved on AoO" — those conflict under
prp-dom; resolved by omitting domain (honors both + the repo's own no-unionOf pattern). Flag raised.

## ABox refactor pattern (per 5 agents)
- NEW `id:os-<agent>` a ObservationSpace: projectsFrom global-state + unobserved + hasAreaOfInterest
  + hasAreaOfObservation(ext+int) + prefLabel/maturity. NO tokenEstimate (container, Agent precedent
  — Agent nodes also carry definition text but no tokenEstimate, measured by cognitiveCapacity).
- NEW `id:aoi-<agent>` a AreaOfInterest (1 external info-need each; ≥1 satisfies shape). NO tokenEstimate.
- RETYPE 10 `id:oa-<agent>-{external,internal}` → AreaOfObservation: keep observationKind/observes*/
  observedFileScope/tokenEstimate/unobserved; **DROP projectsFrom** (moved to os-); external gets
  `coversInterest id:aoi-<agent>`.
- REWIRE `agent-<x> agentObservation` oa-pair → `id:os-<agent>`.
- naming: os-=observation-space, aoi-=area-of-interest, oa-=area-of-observation (oa- meaning fixed).

## tools + byte-identity + boundary
- ontology_lib INSTANCE_LINK_PREDICATES += agentObservation, hasAreaOfInterest, hasAreaOfObservation,
  coversInterest. INSTANCE_CLASSES untouched (3 classes ⊑HC → counted via HarnessComponent subsumption,
  same as Agent/old ObservationArea which were never listed there).
- ★ byte-identity: NO materialize emitter reads any observation predicate/class (grep confirms; the
  role emitter's "agent" hits = .claude/agents/ files, unrelated). h-multiagent CLAUDE.md unaffected;
  proved via 2 fresh-dir builds cmp IDENTICAL + emitter grep (git-free, W2/W3b method).
- FLAG: `domains-tasks.ttl` (OUT of my 5-file boundary) still has stale "ObservationArea" prose in
  comments + GlobalState definition → next-dispatch cleanup. ONTOLOGYSTYLE.md prefix table needs
  os-/aoi- rows + oa- semantics note (out of boundary, flagged).
