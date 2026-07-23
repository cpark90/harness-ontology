# vnv verdict — finer harness decomposition + assembly (scope c) + role-model refinement

**Feature**: `docs/feedback/finer-harness-decomposition-assembly.md` (status: approved, scope **(c)**) —
(a) WorkflowStep, (b) PromptSection, (c) graph-driven assembly order — plus the role-model refinement
(present-only `userFacing`, per-role guardrail/tool/memory scope, redefinable channels).

**Verdict: `pass-with-notes`.** (a)/(b)/(c) and the role-model are correct, byte-identical-preserving
(at the document section-ORDER level — see N2), deterministic, and the graph-driven assembly is guarded
by a total-order enforcement (SHACL per-node + validate.py set-level + materialize hard-fail). All notes
are precision/clarification or pre-existing, none is a defect.

Reproduction interpreter: `/usr/bin/python3` throughout. Commands run from repo root unless noted.

---

## 1. Structural (PASS)

`/usr/bin/python3 tools/validate.py` → **PASS**, all 4 hard checks green:
```
SHACL ✓  |  reachability ✓ (110/110 individuals from a Harness)
capabilities ✓  |  assemblyOrder ✓ (1 harness declares total order; default holder resolves 8 sections)
```
- **individuals = 110** (matches expected).
- **Both loader paths agree**: catalog (default) vs glob fallback (`HARNESS_CATALOG=/nonexistent` +
  module reload) → **URI-individual symdiff = 0** (110==110). Raw-triple symdiff = 44, all of which are
  blank-node RDF-list triples of the 4 `owl:propertyChainAxiom` structures (`rdf:first`/`rdf:rest`/BNode) —
  blank-node relabeling across two independent parses, **not a content divergence** (see N1).
- **retrieve.py within budget**: `retrieve.py "multi-agent orchestration workflow steps"` →
  `budget 897/900 tokens · 29 nodes`. New nodes surface (AssemblySection section shown in-pack;
  WorkflowStep/PromptSection surface on targeted queries).
- **tokenEstimate on every new node**: all 3 WorkflowStep + 3 PromptSection + 8 AssemblySection carry
  `ho:tokenEstimate` (checked programmatically; missing list = empty).

## 2. Reachability / anti-mistype (PASS)

On the reasoned graph (`load_graph(reason=True)`):

| node class | sample | hasComponent-reachable from | typed correctly | typed `ho:Harness`? |
|---|---|---|---|---|
| WorkflowStep | wfs-{plan-dispatch,author-verify,integrate-gate} | h-multiagent | yes | **no** ✓ |
| PromptSection | ps-methodical-{decisions,error,escalate} | h-multiagent | yes | **no** ✓ |
| AssemblySection | as-{overview,persona,…,skills} | h-multiagent | yes | **no** ✓ |

Anti-mistype (the crux of the modeling choice) — all correct:
- `wf-multiagent` (Workflow) typed Harness = **False**; `sp-methodical` (SystemPrompt) typed Harness = **False**;
  each `as-*` typed Harness = **False**; `h-multiagent` typed Harness = **True** (subject genuinely IS the Harness).
- **(c) uses a DIRECT sub-property** — `ho:hasAssemblySection rdfs:subPropertyOf ho:hasComponent` = **True**.
  Correct: the subject of `hasAssemblySection` IS the Harness (mirrors `hasRole`/`hasChannel`), so no mistype.
- **(a)/(b) use prefixed propertyChains, NOT direct sub-properties** — `hasStep`/`hasSection` subPropertyOf
  hasComponent = **False** (both). Correct: their subject is an intermediate Workflow/SystemPrompt; a direct
  sub-property would (via `hasComponent`'s `rdfs:domain ho:Harness`) mistype that intermediate as a Harness and
  trip HarnessShape. Chains `( hasComponent hasStep )` and `( hasComponent hasSection )` roll steps/sections up
  to the harness while keeping the inferred subject = Harness. **The modeling choice is right in each case.**

## 3. Byte-identical section order + determinism (PASS)

`materialize.py h-multiagent --out run1` / `--out run2` (both exit 0). Emitted CLAUDE.md heading order:
```
# Multi-agent orchestration harness   (overview,     assemblyOrder 1)
## Persona                            (persona,       2)
## Operating rules                    (operating-rules,3)
## Process                            (process,       4)
## Model                              (model,         5)
## Roles                              (roles,         6)
## Coordination channels              (channels,      7)
[skills, order 8 → conditional, emits nothing: no hasInstruction]
```
This equals the **documented historical fixed order** (overview / Persona / Operating rules / Process /
Model / Roles / Channels / Skills, formerly hardcoded in `materialize.py`). The order is now READ from the
graph (`resolve_assembly_order`), not hardcoded.

**Determinism**: `diff -r run1 run2` → **IDENTICAL** (full tree: CLAUDE.md, MANIFEST.json, harness.lock.json,
7 `.claude/agents/*.md`).

**(a)/(b) enhancements render ordered** (intended bodies):
- Persona composes 3 `PromptSection` fragments in `sectionOrder` 1→2→3 (decision-capture → error-min → escalation).
- Process renders `wf-multiagent`'s 3 `WorkflowStep`s numbered 1→2→3, each with its `stepByRole` / `stepUsesTool` /
  `stepGuardedBy` (e.g. step 1 → role Orchestrator, guarded by Delegated-only orchestration).

## 4. Error path — total-order enforcement + atomicity (PASS)

Scratch recipe (temp `central` symlink + scratch catalog + scratch harness ttl; real files untouched;
symlink removed after). Three failure modes:

| case | mechanism | result |
|---|---|---|
| **E1** two AssemblySections share `assemblyOrder 1` | validate.py `check_assembly_order` (SET-level) | **FAIL, exit 1** ("duplicate assemblyOrder 1 … order is not total"); SHACL still ✓ (correctly a set-level, not per-node, check) |
| E1 → materialize | gate runs `validate.run_structured()` before load/write | **REFUSES, exit 1, NO output dir created** (atomic — verified `badout` absent) |
| **E2** AssemblySection missing `assemblyOrder` | SHACL `AssemblySectionShape` MinCount + `check_assembly_order` | **FAIL** (both fire) |
| **E3** `sectionKind "bogus"` | SHACL `AssemblySectionShape` `sh:in` (closed set) | **FAIL** (InConstraintComponent) |

The per-node half (presence + closed `sectionKind` enum) is SHACL; the set-level half (unique/total order) is
`validate.check_assembly_order`; `materialize.resolve_assembly_order` re-checks and raises rather than falling
back — matching approved decision 2 (undefined order = hard error, never silent code fallback).

## 5. Redefine path (PASS)

Valid scratch harness `h-redef` declaring its OWN `hasAssemblySection` set (model=1, overview=2, persona=3,
dropping the rest). Union validates (PASS). `materialize.py h-redef` (exit 0) emits heading order:
```
## Model
# Scratch redefine-order harness   (overview)
## Persona
```
The emitted order **changes accordingly** — per-harness override works and does not disturb h-multiagent's
default (still resolves the central 8-section default).

## 6. Role-model refinement (PASS)

- **`userFacing` present-only**: true only on `role-orchestrator` and `role-inspection`; the 5 worker roles
  (developer, research, inspection-worker, vnv, design) **omit** it (value None/absent). Cross-checked in the
  emitted tree: the "**User-facing role**" line appears in exactly `orchestrator.md` and `inspection.md`,
  in no worker file.
- **Emitted `.claude/agents/<role>.md`** shows each role's scope: developer.md carries Tools (editor, shell),
  Guardrails (controlled-vocabulary, dispatch-execution, least-privilege, reuse-first) and Memory policy;
  no user-facing line. orchestrator.md carries Guardrails + Memory policy + user-facing line.
- **Least-privilege**: every `roleTool`/`roleGuardrail` is a subset of h-multiagent's `usesTool`/`hasGuardrail`
  — violations = NONE.
- **Channel redefinability**: documented at the schema level — `ho:Channel` class definition ("central Channel
  individuals are reusable DEFAULTS, and a specific harness MAY redefine them") and `ho:hasChannel` property
  ("per-harness and redefinable"). (See N3.)
- **Determinism** holds (agent files identical across run1/run2, item 3).

---

## Notes (non-blocking)

- **N1 (loader residue)**: catalog-vs-glob raw-triple symdiff = 44, entirely blank-node `propertyChainAxiom`
  RDF-list triples (`rdf:first`/`rdf:rest`/BNode) — blank-node relabeling across two parses of the identical
  schema. URI-individual symdiff = 0. Benign; the standard equivalence proof is at the individual level.
- **N2 (precision on "byte-identical")**: the preserved invariant is the document's **top-level section ORDER**
  plus **full-tree determinism** — NOT the section bodies. The Persona body (blob → 3 ordered fragments) and the
  Process body (1-line workflow → 3 ordered steps) **intentionally changed** — these are the approved (a)/(b)
  enhancements. A naive byte-compare of h-multiagent's CLAUDE.md against a pre-feature emission would therefore
  DIFFER in those two bodies; that is expected, not a regression. The feature preserves ORDER + determinism, and
  the section-ORDER equals the historical fixed order.
- **N3 (channel redefinability placement)**: stated on the `ho:Channel` class and `ho:hasChannel` property
  definitions (TBox), not on each channel individual's `skos:definition`. Correct placement (a schema-wide
  semantic), noted only because the brief phrased it as "channels' definitions".
- **N4 (roleTool absence)**: `role-orchestrator` and `role-design` carry no `roleTool` (their agent files have
  no Tools section). Defensible least-privilege — the orchestrator performs no tool execution
  (gr-delegated-orchestration) and design is deliberative. Not a defect.
- **N5 (stale comment)**: `tools/materialize.py:51-53` still reads "Sections are emitted in this fixed order",
  mildly stale now that order is graph-driven via `resolve_assembly_order`. Documentation nit only (behaviour
  and the within-section IRI-sort it describes are correct). Route to developer if a cleanup pass is desired.

## Routing
No blockers. N5 (stale comment) is the only actionable item and is cosmetic → optional developer follow-up.
All ontology/tool changes for (a)/(b)/(c) + role-model are verified correct as landed.
