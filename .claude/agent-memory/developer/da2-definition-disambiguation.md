# DA-2 — TBox skos:definition disambiguation (B~F) + DA-1 residue cleanup

Definition-only clarification of confusable class pairs. **Graph structure UNCHANGED**
(no predicate/domain/cardinality edits) → zero-risk: validate PASS 185 individuals invariant,
materialize byte-identity holds (class-level skos:definition is NOT rendered into any harness
CLAUDE.md — emitters read per-NODE prose like promptText, never TBox class definitions).
File-exclusive = `tbox/harness.ttl` + `abox/core/domains-tasks.ttl` + `ONTOLOGYSTYLE.md`.
Design: `docs/plans/disambiguation-audit.md` §B~F.

## Disambiguation pattern (each confusable pair)
De-conflate by (1) removing self-reference / cross-term, (2) adding an explicit
"Distinguished from ho:X (...): A=<this>, X=<that>" clause. Pairs fixed:
- **Workflow vs DesignPattern**: Workflow=concrete instantiated control flow, decomposed by
  ho:hasStep (describe as FLOW SHAPES — "sense-act-observe loop", "plan-then-dispatch-then-integrate",
  "branch-and-merge" — NOT pattern names). DesignPattern=abstract named tag via ho:appliesPattern,
  never instantiated, multiply-applicable (orchestrator-workers/peer-mesh/pipeline/fan-out-fan-in/reflection).
  Removed the shared ReAct/plan-execute examples that caused conflation.
- **Guardrail vs Constraint**: dropped "constraint" from Guardrail (imperative behavioural policy);
  Constraint=declarative NFR on the harness.
- **SystemPrompt vs Instruction**: dropped "instruction" from SystemPrompt (always-on persona framing,
  every inference); Instruction=on-demand skill/slash-command, triggered.
- **Tool vs Capability**: stopped calling Tool a "capability" (concrete invokable that PROVIDES via
  ho:providesCapability); Capability=abstract ability.
- **Role vs Agent**: Role tightened to "mandate + policy pi_i" (rolePersona/guardrail/tool-scope);
  Agent already said "Role (mandate + policy)" → NO edit needed (structure-preserving confirm only).

## ★ Gotcha — brief referenced a non-existent property
Brief said Instruction uses "ho:notation/ho:triggerPhrase". **ho:notation does not exist.** Real
Instruction props = `ho:integrationMode` (invoke/inline/reference-load) + `ho:triggerPhrase`. Used the
REAL props, did not invent ho:notation. Always grep the property before citing it in a definition.

## DA-1 residue cleanup (finishing the DA-1 flag)
- `domains-tasks.ttl` 3 spots: chain comment "-> ObservationArea" → "-> ObservationSpace"; "each
  ObservationArea ho:projectsFrom" → "ObservationSpace"; global-state def "each agent's ObservationArea
  partially projects from" → "ObservationSpace" (projectsFrom moved onto ObservationSpace in DA-1).
- `ONTOLOGYSTYLE.md` naming table: replaced 1 `ObservationArea | oa-` row with 3 rows —
  `ObservationSpace os-` / `AreaOfInterest aoi-` / `AreaOfObservation oa-` (oa- meaning fixed to AoO).
- Verify with `grep -rn ObservationArea ontology/ tools/ ONTOLOGYSTYLE.md` → must be 0.
