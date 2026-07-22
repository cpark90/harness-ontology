# Verify: techdoc technical-documentation harness assembly

**Verdict: pass-with-notes.** All 6 verification items pass. The techdoc recipe
is a faithful demonstration that a complete, buildable `ho:Harness` assembles
from the neutral central parts library by IRI with minimal local specialization
(5 local nodes, 0 core redefinitions, central untouched). Notes are curation
observations, not defects.

Role: vnv (judgment only — no ontology/tools/docs edits, no git). Interpreter:
`/usr/bin/python3` (has rdflib/pyshacl/owlrl). Recipe under test:
`staging/harness-recipes/recipes/techdoc/techdoc.ttl`.

## Reproduction (commands run)

Central (unchanged repo):
```
git status --short ontology/            # empty
grep -rin techdoc ontology/abox/core/   # no output (0 hits)
/usr/bin/python3 tools/validate.py       # PASS
```
Composed union (temp symlink `./central` -> this repo, created then removed):
```
ln -s "$(pwd)" staging/harness-recipes/central
cd staging/harness-recipes
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/techdoc \
  /usr/bin/python3 central/tools/validate.py            # PASS
# graph inspection via central/tools/ontology_lib.load_graph()
# retrieve over the same union + central-only retrieve
rm staging/harness-recipes/central                      # symlink removed
```
At-rest symlinks after cleanup: none (`find staging -type l` empty).

## 1. Central untouched & neutral — PASS
- `git status --short ontology/` = empty (no core change).
- `grep -rin techdoc ontology/abox/core/` = 0 hits.
- Central-only `tools/validate.py` = **PASS**; central individuals = 64.
- Central-only `retrieve.py "technical documentation writing citations
  accuracy review"`: no techdoc node in the pack (the sole "technical
  documentation" string is the query-echo header line, excluded); top base
  candidate is the neutral **Research synthesis agent** (rel 2.16). Central
  neutrality intact — the recipe adds nothing to core.

## 2. techdoc composes + buildable — PASS
- Union validate = **PASS** (SHACL, reachability, capabilities, no dup labels).
- Union individuals = **69** = 64 central + 5 local.
- `id:h-techdoc` satisfies `ho:HarnessShape` (actual edges from the graph):
  - hasSystemPrompt: `sp-techdoc` (1)
  - hasWorkflow: `wf-planexec` (>=1)
  - usesTool: `tool-retriever`, `tool-websearch`, `tool-editor` (>=1)
  - hasGuardrail: `gr-cite`, `gr-lang`, `gr-grounding`, `gr-traceability`,
    `gr-report-over-prompt` (>=1)
  - usesModel: `mc-opus` (1); appliesPattern: `pat-planexec`
- **requires -> provides, resolved over bound components (from the graph):**
  | requiresCapability | provided by (bound component) |
  |---|---|
  | `cap-retrieval` | `tool-retriever` |
  | `cap-websearch` | `tool-websearch` |
  | `cap-citation`  | `gr-cite` (guardrail provider) |
  | `cap-fileedit`  | `tool-editor` |
  Every `requiresCapability` of h-techdoc is met internally by a component it
  binds — **no gap** for the target harness.

## 3. Reuse-by-IRI (not redefinition) — PASS
- Parsing `techdoc.ttl` standalone (rdflib subject set, not grep):
  - `core:` IRIs appearing as **subject = 0** (no core individual redefined).
  - Local subjects = exactly **5**: `dom-techdoc` (Domain), `c-techdoc`
    (Concept), `task-techdoc` (Task), `sp-techdoc` (SystemPrompt),
    `h-techdoc` (Harness).
- `id:c-techdoc` carries `skos:broader core:c-communication` → connected to the
  central Communication concept, not an orphan.
- All reused parts (workflow, pattern, model, tools, guardrails, litreview task,
  neutral concepts) are referenced by `core:` IRI only.

## 4. Anti-drift — PASS
- No new `ho:` class/property defined in the recipe (schema-namespace subjects
  in `techdoc.ttl` = 0).
- Text nodes carry `ho:tokenEstimate`: `sp-techdoc` has `ho:promptText` +
  `ho:tokenEstimate 95`. `task-techdoc`/`c-techdoc`/`dom-techdoc` are
  definition/label-only and outside the tokenEstimate **[지킴]** scope
  (`ONTOLOGYSTYLE.md:75-76` scopes it to promptText-bearing nodes +
  Tool/Workflow), consistent with central precedent (`core:task-litreview`
  carries a definition, no tokenEstimate). Compliant.
- Labels/definitions/promptText are English; `ho:maturity "draft"` on
  `h-techdoc` and `sp-techdoc`. No near-synonym class, no untyped edge, no
  duplicate prefLabel (validate's dup-label gate = clean over the union).

## 5. Discoverability — PASS
- Composed-union `retrieve.py "technical documentation writing citations
  accuracy review"` (JSON): base-harness candidates ranked, **#1 =
  "Technical documentation agent" (h-techdoc) rel 8.1**, above all central
  siblings (each 3.691). h-techdoc is surfaced as the top base candidate.
- (The markdown candidate label is "Technical documentation agent"; an earlier
  grep on the literal "techdoc" hid it — the JSON pack confirms it is #1.)
- Central-only retrieve unaffected (item 1): no techdoc node leaks into core.

## 6. No regressions — PASS
- lpranging recipe still composes: union validate = **PASS**, union
  individuals = **75** (64 central + 11 local).
- Recipe-repo CI (`staging/harness-recipes/.github/workflows/validate.yml`) is a
  real gate, not a no-op: matrix has **both** recipe roots
  (`.../recipes/lpranging`, `.../recipes/techdoc`); each job checks out the
  central library into `./central`, installs `central/requirements.txt`, and
  runs `python3 central/tools/validate.py` with `HARNESS_CATALOG` +
  `HARNESS_ROOT_ONTOLOGY` set so central validate runs over each composed union
  and a non-zero exit fails the check. `catalog-v001.xml` maps
  `recipe-techdoc` → `recipes/techdoc/techdoc.ttl`.

## Judgment — faithful demonstration, with curation notes

This is a faithful demonstration: a working harness assembles from the neutral
library with minimal local specialization. Central stays a neutral parts
library (0 techdoc references, unchanged, PASS); the recipe reuses 15+ core
parts by IRI and adds only 5 local nodes — a Domain, a Concept hung under
central Communication, a domain Task, a domain persona SystemPrompt, and the
Harness assembly. HarnessShape is satisfied, every capability is met
internally, and h-techdoc is the #1 discoverable base candidate. No drift, no
orphan, no redefinition.

Notes (for orchestrator/curation; none block acceptance):

- **N1 — `task-techdoc` is borderline general.** Its definition ("research
  sources and author technical documentation with per-claim citations, then
  review the draft for factual accuracy against those sources") describes a
  generic *cited-authoring + accuracy-review* pattern that could plausibly be a
  neutral reusable core Task (reusable by any authoring domain), rather than a
  technical-documentation-scoped local task. It is defensible as local because
  the label/scope names the technical-documentation domain and the demo's point
  is domain specialization; but if similar recipes recur, promoting a neutral
  "cited authoring + accuracy review" task to core would reduce duplication.
  `sp-techdoc` (a three-phase technical-writing persona with concrete
  promptText) and `dom-techdoc`/`c-techdoc` are correctly domain-specific and
  belong local — no concern there.
- **N2 — union pulls all 12 imported core units (64 individuals).** As with the
  lpranging recipe, `derivedFrom core:h-research` drags in the single
  `core/harnesses` document, whose seed harnesses reference every other unit, so
  the full core is imported to close the union (EdgeTypingShape). This is not a
  defect: anti-rot is enforced at the retrieve/projection (budget-cap) layer,
  not at union size, so runtime cost is unaffected. Minimizing the union would
  require finer central-side splitting of `harnesses` — a central change,
  outside recipe scope.
- **N3 — reading the retrieve gap list.** The composed-union pack reports
  capability gaps `[Code execution, Multi-agent orchestration]`; these belong to
  sibling harnesses pulled into scope (coding / multiagent), **not** to
  h-techdoc, whose four capabilities are all met (item 2). Noted so the gap list
  is not misread as a techdoc gap.

Routing: N1 (whether `task-techdoc` should become a neutral core part) is a
design/curation question → orchestrator (developer dispatch if promoted) or
inspection. N2/N3 are informational.
