# V&V report — lpranging system-design harness

- **subject**: `ontology/abox/lpranging-sysdesign.ttl`, central individual `id:h-lpranging-sysdesign`
- **verdict**: **pass-with-notes**
- **agent**: vnv
- **interpreter**: `/usr/bin/python3` (has rdflib/pyshacl/owlrl; shell default `python3` lacks them)
- **date**: 2026-07-21

The composition is structurally green, satisfies `ho:HarnessShape`, is fully reachable
(no orphans), introduces no TBox drift, and is discoverable at rank #1 for its own request.
"pass-with-notes" (not plain pass) only because of three reviewer-facing judgment calls that
are validation/completeness observations, not defects — enumerated at the end. Buildable and
correct as a `draft`; the notes should be weighed before promotion beyond `draft`.

---

## 1. Structural gate — `validate.py` (PASS)

Command: `/usr/bin/python3 tools/validate.py`

```
Loading ontology and applying OWL RL reasoning...
  loaded graph: 1320 triples (post-reasoning)

=== SHACL structural invariants ===
✓ conforms — no orphaned/under-specified nodes

=== Global reachability (orphan islands) ===
✓ all 62 individuals reachable from a Harness

=== Capability satisfaction ===
✓ every harness's required capabilities are provided internally

=== Duplicate / drift detection (warning only) ===
✓ no duplicate labels within a class

=== Summary ===
  ✓ SHACL   ✓ reachability   ✓ capabilities
PASS
```

All four sections green. SHACL connectivity/under-specification, global reachability
(62/62 individuals reach a Harness), capability satisfaction, and duplicate-label all pass.

## 2. HarnessShape minimums (PASS) — read from the graph, not from claims

`id:h-lpranging-sysdesign` bindings (queried via rdflib over tbox+seed+new file):

| slot | count | members |
|---|---|---|
| `hasSystemPrompt` | 1 | `sp-sysdesign` |
| `hasWorkflow` | ≥1 (1) | `wf-multiagent-design` |
| `usesTool` | ≥1 (5) | `tool-editor`, `tool-shell`, `tool-docgraph`, `tool-simulator`, `tool-websearch` |
| `hasGuardrail` | ≥1 (5) | `gr-lang`, `gr-verify-proceed`, `gr-design-for-loss`, `gr-traceability`, `gr-no-arbitrary-decision` |
| `usesModel` | 1 | `mc-sonnet` |
| `appliesPattern` | (1) | `pat-orchestrator-workers` |

Exactly 1 SystemPrompt and 1 ModelConfig; ≥1 Workflow/Tool/Guardrail. Minimums met.

**requires → internal provider** (edges read from the graph; every requirement satisfied by a
component actually bound to this harness):

| `requiresCapability` | provided by (internal component) |
|---|---|
| `cap-fileedit` | `tool-editor` |
| `cap-codeexec` | `tool-shell` |
| `cap-designgraph` | `tool-docgraph` (new) |
| `cap-simulation` | `tool-simulator` (new) |
| `cap-websearch` | `tool-websearch` |

No unsatisfied capability. Matches the developer's claimed bindings.

## 3. Anti-orphan / anti-drift (PASS)

- **Reachability**: validate.py confirms all 62 individuals reach a Harness — the new harness
  and every new vocab node included.
- **No TBox drift**: every `ho:` predicate/type used in the new file is already declared in
  `ontology/tbox/harness.ttl`. Programmatic diff of `ho:` terms used vs. TBox-declared →
  **NONE undeclared**. No new class or property was invented.
- **Reused nodes all exist** in `seed.ttl`: `tool-editor`, `tool-shell`, `tool-websearch`,
  `gr-lang`, `mc-sonnet`, `wf-planexec`, `h-coding`, `cap-fileedit`, `cap-codeexec`,
  `cap-websearch`, `c-autonomy`, `c-safety`, `scheme` — all present; the three reused caps are
  provided by seed tools (`tool-shell`→cap-codeexec, `tool-editor`→cap-fileedit,
  `tool-websearch`→cap-websearch).
- **New Concepts connected** (no floating SKOS): `c-sysdesign` (topConceptOf scheme),
  `c-embedded`/`c-lowpower`/`c-rtls`/`c-traceability` (skos:broader chain to c-sysdesign),
  `c-multiagent` (topConceptOf scheme + related c-autonomy).
- **New Capabilities provided**: `cap-designgraph`←`tool-docgraph`, `cap-simulation`←`tool-simulator`.
- **No near-synonym drift**: new `gr-traceability` ("Traceable single source of truth" —
  decision/record lifecycle) vs. seed `gr-nodestruct` ("No destructive actions" — shell
  command safety) are distinct scopes with distinct prefLabels; duplicate-label check passes.

## 4. Discoverability / anti-rot (PASS)

Q1 `retrieve.py "low-power UWB ranging device system design" --format json`: seed ranking
top-3 = **`h-lpranging-sysdesign` (score 15.3, rank #1)**, `sp-sysdesign` (8.1), `c-rtls`/`dom-sysdesign` (7.2).
The new harness surfaces as the #1 base candidate for its own request.

Q2 `retrieve.py "multi-agent design orchestrator"`: `wf-multiagent-design` (6.3, #1),
**`h-lpranging-sysdesign` (4.5, #2)**, `pat-orchestrator-workers` (4.05, #3). Harness and its
components both surface near the top.

**tokenEstimate per [지킴] (ONTOLOGYSTYLE §1c:75-76)**: the rule scopes tokenEstimate to
promptText-bearing nodes (SystemPrompt/Instruction/Guardrail/Example) **and** Tool/Workflow.
All in-scope new nodes carry it: `sp-sysdesign`=100; guardrails `gr-verify-proceed`=38,
`gr-design-for-loss`=55, `gr-traceability`=42, `gr-no-arbitrary-decision`=32;
tools `tool-docgraph`=48, `tool-simulator`=42; workflow `wf-multiagent-design`=72.
Nodes carrying only `skos:definition` (Task/Capability/DesignPattern/Harness) have no
tokenEstimate — this is **outside** the [지킴] scope and **matches the seed.ttl convention**
(seed Task 0/4, DesignPattern 0/3, Harness 0/3 carry tokenEstimate). Not a defect.

## 5. Provenance / faithfulness (PASS)

- `ho:derivedFrom id:h-coding`; `h-coding` is a real `ho:Harness` in seed. Template link valid.
- `ho:maturity "draft"` on the harness and all new authored nodes (tools carry their own
  "stable"/"reviewed" maturities, acceptable for reusable components).
- prefLabels/definitions/altLabels are all English (policy / ONTOLOGYSTYLE §1d compliant).

---

## Assessment of the developer's flagged judgment calls (V&V view)

1. **Model tier `mc-sonnet` vs `mc-opus`** — *revisit before promotion (acceptable as draft)*.
   HarnessShape is satisfied (exactly 1 ModelConfig), so no structural issue. But note the
   template `h-coding` binds `mc-opus`, and the applied pattern `pat-orchestrator-workers`
   mirrors this repo's own multi-agent harness, for which CLAUDE.md mandates opus at the
   dispatch/authoring/judgment points "because 저작·판정 품질이 최종 정합성을 좌우한다." A
   design agent whose guardrails demand traceability and "no arbitrary decisions" arguably
   belongs in that same high-stakes tier. `mc-sonnet` is a deliberate downgrade from the
   template — legitimate if cost-motivated, but the rationale should be recorded (e.g. a
   `skos:note` or in review) rather than left implicit. Both models exist; either binding
   validates. Recommend reviewer either justify sonnet or align to opus.

2. **Omitted `gr-controlled-vocab`** — *acceptable as-is*. There is **no** `gr-controlled-vocab`
   node in the ontology (seed guardrails: `gr-nodestruct`, `gr-cite`, `gr-lang`). "Omitting" it
   correctly means the developer did **not invent a new near-synonym guardrail** — exactly the
   anti-drift discipline this repo enforces. The controlled-vocabulary concern here is a
   property of *this* meta-authoring harness, not obviously a runtime guardrail the modeled
   lpranging design agent needs. No V&V objection. If a future need arises, author it once as a
   shared guardrail (connected in the same commit) rather than a local variant.

3. **Feedback / lessons-learned process not modeled** — *acceptable as draft; note for
   enrichment*. No shape requires a feedback loop, so this is a completeness/validation gap, not
   a defect. The harness models authoring + verify + inspect roles via
   `wf-multiagent-design` and `pat-orchestrator-workers`, but the external harness's
   feedback/lessons cycle (analogous to this repo's `docs/feedback/` inbox→verified pipeline)
   is absent. If faithfulness to the external system's lessons loop matters, consider a future
   Workflow (e.g. a feedback-intake loop) or Instruction; not required to pass.

---

## Reproduction (commands actually run)

```
/usr/bin/python3 tools/validate.py
/usr/bin/python3 tools/retrieve.py "low-power UWB ranging device system design" --format json
/usr/bin/python3 tools/retrieve.py "multi-agent design orchestrator" --format json
# + rdflib graph queries over tbox/harness.ttl + abox/{seed,lpranging-sysdesign}.ttl for
#   HarnessShape slots, requires→provides bindings, TBox-term conformance, tokenEstimate scope
```

**Routing**: verdict pass-with-notes → no re-authoring required to be buildable. The three
notes are reviewer decisions for promotion beyond `draft` (route via orchestrator/developer if
acted on); none is a structural failure requiring inspection ripple analysis.
