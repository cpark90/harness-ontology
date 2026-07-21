# V&V verdict — neutral-parts rework (domain-independent decomposition)

- **Scope**: verify the rework that replaced domain-coupled `lpranging` modeling with
  generalized, neutral, reusable governance PARTS appended to `ontology/abox/seed.ttl`
  (core id-namespace), reverting the physical split (federation D1/D3 infra kept, no
  `lpranging` data unit).
- **Interpreter**: `/usr/bin/python3` (has rdflib/pyshacl/owlrl). Ran from repo root.
- **Verdict**: **pass-with-notes** — every structural, neutrality, buildability,
  anti-orphan/drift, discoverability and split-revert check passes on the graph; notes
  are review-before-promote items, not blockers.

---

## 1. Structural gate — PASS

`/usr/bin/python3 tools/validate.py`:

```
loaded graph: 1364 triples (post-reasoning)
=== SHACL structural invariants ===      ✓ conforms — no orphaned/under-specified nodes
=== Global reachability (orphan islands)=== ✓ all 63 individuals reachable from a Harness
=== Capability satisfaction ===          ✓ every harness's required capabilities are provided internally
=== Duplicate / drift detection ===      ✓ no duplicate labels within a class
=== Summary ===  ✓ SHACL  ✓ reachability  ✓ capabilities
PASS
```

**Loader equivalence** (catalog vs glob fallback via `HARNESS_CATALOG=/nonexistent`,
`ontology_lib` reloaded): both **1364 triples**, raw triple-set symmetric difference
**0**. `instance_nodes` = **63** individuals. Both loader paths agree. Count matches the
claim (63 core individuals = 41 prior + 22 new).

## 2. Neutrality — PASS (core of the rework)

Grep `uwb|rtls|ranging|low-power|lpranging|sysdesign|embedded|docgraph|simulator`
(case-insensitive) across all of `ontology/`:

- Only **one** match anywhere: `ontology/harness-ontology.ttl:22` — inside a `#` comment
  documenting the retirement. **Zero matches inside any node** (id/label/definition/
  promptText). Grep excluding comment lines returns **NO NON-COMMENT MATCHES**.
- All **12 claimed-dropped ids** (`h-lpranging-sysdesign`, `dom-sysdesign`, `task-sysarch`,
  `cap-designgraph`, `cap-simulation`, `tool-docgraph`, `tool-simulator`, `sp-sysdesign`,
  `c-sysdesign`, `c-embedded`, `c-lowpower`, `c-rtls`) resolve to **0 occurrences** in the
  loaded union.

**Semantic judgment of the new guardrails' promptText** (sampled all 10, judged for
domain-independence):

- `gr-verify-proceed`, `gr-traceability`, `gr-grounding`, `gr-no-arbitrary-decision`,
  `gr-least-privilege`, `gr-report-over-prompt`, `gr-controlled-vocabulary`,
  `gr-root-cause`, `gr-simplicity` — genuinely domain-independent governance/design
  principles; each names no technology and reads as reusable across engineering domains.
- `gr-design-for-loss` — the **narrowest** of the set: a reliable-messaging /
  distributed-systems principle ("treat message and data loss as normal… judge completion
  by the final receiver's confirmation… report cumulative absolute state… make every loss
  observable via counters"). It was clearly generalized from the lossy-wireless origin but
  now **names no domain tech**, so it passes neutrality. Its *applicability* is narrower
  (messaging/pipelines/telemetry) than the others — see Note B.

## 3. Buildability / HarnessShape — PASS (with Note A)

`h-multiagent` slots read from the graph:

| slot | bound components |
|---|---|
| SystemPrompt (≥1) | `sp-methodical` ✓ |
| Workflow (≥1) | `wf-multiagent` ✓ |
| Guardrail | `gr-lang`, `gr-verify-proceed`, `gr-design-for-loss`, `gr-traceability`, `gr-grounding`, `gr-no-arbitrary-decision`, `gr-least-privilege`, `gr-report-over-prompt`, `gr-controlled-vocabulary`, `gr-root-cause`, `gr-simplicity` (11) ✓ |
| ModelConfig | `mc-opus` ✓ |
| Tool | **[] — none** (see Note A) |
| Domain / Task / Pattern | `dom-design` / `task-architecture`,`task-designdecision` / `pat-orchestrator-workers` |

**requires → provides (internally bound):**

- `cap-orchestration` → `wf-multiagent` (bound via `hasWorkflow`) ✓
- `cap-traceability` → `gr-traceability` (bound via `hasGuardrail`) ✓

Both required capabilities are satisfied by a component bound to the harness (not merely
existing in the graph). Reuse confirmed: `gr-lang`, `mc-opus`, `wf-planexec`
(`wf-multiagent ho:derivedFrom wf-planexec`), `c-autonomy` (`c-multiagent skos:related`),
`c-safety`/`c-communication` (guardrail tags), `id:scheme`.

## 4. Anti-orphan / anti-drift — PASS

- **Reachability**: all 63 individuals reachable from a Harness (validate §reachability).
- **No TBox drift**: `ho:` predicates used in `seed.ttl` NOT declared in
  `ontology/tbox/harness.ttl` = **[]**; `ho:` rdf:types used but not declared = **[]**.
  No new `ho:` class or property was introduced.
- **New Concepts connected**: `c-design` (topConceptOf; tags `wf-multiagent`,`h-multiagent`),
  `c-multiagent` (topConceptOf; `skos:related c-autonomy`; tags 2), `c-traceability`
  (topConceptOf; tags `gr-traceability`,`gr-grounding`,`h-multiagent`).
- **New Capabilities**: both `cap-orchestration` and `cap-traceability` are provided AND
  required (not orphaned).

## 5. Discoverability (anti-rot) — PASS

`tools/retrieve.py "<q>" --format json` (seeds, score):

- **"verify then proceed traceability guardrail"** → `Verify then proceed` 9.45 (#1),
  `Multi-agent orchestration harness` 4.5, `Traceability` 2.7 ×2, `Traceable single
  source of truth` 1.89, `Multi-agent orchestration loop` 1.8, `Fix root cause` 1.35.
- **"orchestrator workers multi-agent"** → `Multi-agent orchestration harness` 7.2 (#1),
  `Orchestrator-workers` 5.4 (#2), `Multi-agent orchestration loop` 3.6,
  `Multi-agent orchestration` 2.7 ×2, `Low latency` 0.9.
- **No domain-term leak** in either pack (scanned the full JSON blob for the 9 terms).
- **tokenEstimate**: every node with `ho:promptText` carries `ho:tokenEstimate` (0
  missing); all 11 new text-bearing guardrails/persona + `wf-multiagent` (definition +
  tokenEstimate 74) carry it. Definition-only Task/Capability/Domain/Concept nodes are
  outside the [지킴] tokenEstimate scope (ONTOLOGYSTYLE §1c), correctly not flagged.

## 6. Split-revert — PASS

- `catalog-v001.xml`: root/schema/data-core/data-authored only; **no** `data/lpranging`
  entry (only a `<!-- -->` comment documenting retirement).
- `ontology/harness-ontology.ttl`: `owl:imports` = schema, data/core, data/authored; no
  lpranging data unit (only a `#` NOTE).
- `docs/federation-design.md`: lines 173–188 explicitly document the lpranging modeling as
  **RETIRED** and state `…/data/lpranging` appears in no catalog entry or root import; no
  longer claims an active pilot. (Lines 120/131 use `lpranging` only as an illustrative
  domain-segment *naming* example — see Note D.)
- `staging/` directory is **gone**.

---

## Notes (review-before-promote, not blockers)

- **A — `h-multiagent` has no Tool.** The brief and CLAUDE.md's composition workflow list
  "tools + ModelConfig" as minimum config, but the actual `ho:HarnessShape` requires only
  prefLabel + targetsDomain + addressesTask + hasSystemPrompt(≥1) + hasWorkflow(≥1) — so a
  tool-less harness passes SHACL, and validate is green. **Judgment**: for a genuinely
  *neutral* template this is defensible — the seed's tools (shell/editor/retriever/
  websearch) are all domain-coupled, and binding one would reintroduce coupling. So the
  omission is consistent with the rework's purpose, but it means `h-multiagent` is not a
  fully "buildable" agent per the prose minimum. A reviewer should decide before promoting
  past `draft` whether the template should ship with a neutral tool (e.g. a generic
  file/search tool) or stay tool-agnostic by design.
- **B — `gr-design-for-loss` is the narrowest neutral part.** Passes neutrality (no domain
  tech named) but is a distributed-systems/messaging principle rather than a
  universal-engineering one; acceptable as a reusable part, flagged for awareness.
- **C — Missed reusable principle.** The source docs' single most central governance rule —
  *"never load the whole knowledge base into context; work from a bounded retrieved
  projection"* (CLAUDE.md golden rule #1, the context-rot/budget defense) — was **not**
  decomposed into a guardrail, though it is genuinely domain-independent and reusable by
  any large-context agent. Candidate addition (e.g. `gr-context-budget`). Anti-orphan
  ("connect every new node in the same commit") is likewise only implicitly present.
- **D — Cosmetic.** `docs/federation-design.md` lines 120/131 still use `lpranging` as an
  illustrative domain-segment naming example. Not a pilot claim and not inside the
  ontology; could be swapped for a neutral example but is not a defect.
- **E — Composition-workflow deviation.** `h-multiagent` carries no `ho:derivedFrom`
  (CLAUDE.md step 5 suggests deriving from a base template). Correct here because this is a
  *decomposition* of governance docs, not composition from a base harness; `h-multiagent`
  is itself declared the neutral template. `wf-multiagent ho:derivedFrom wf-planexec` is
  present. Both `h-multiagent` and `sp-methodical` are `maturity "draft"` (correct;
  promote after review).

## Routing

- Notes A and C are **authoring** judgments (add a neutral tool / add a context-budget
  guardrail) → orchestrator via developer dispatch if the reviewer wants them.
- Note D is a docs cosmetic → inspection (docs are outside developer's abox scope).
- No structural blocker; nothing to re-author for correctness. Reproduce via the commands
  quoted in each section above (all `/usr/bin/python3`).
