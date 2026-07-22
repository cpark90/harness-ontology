# lpranging recipe — coverage / completeness audit (vnv)

**Question**: does the ontology recipe `staging/harness-recipes/recipes/lpranging/`
reflect the REAL source harness `~/git/agrtls/device_harvest_lp/lpranging/`
*without missing parts*? Enumerate the source, map each artifact to its ontology
representation (or a GAP), classify each gap, and give an honest verdict.

**Interpreter**: `/usr/bin/python3` (has rdflib/pyshacl/owlrl). All commands below
run from the recipe repo `staging/harness-recipes/` with a temp `central` symlink
→ repo root (removed at the end). Base every claim on files + materialized output.

---

## 0. Headline finding (BLOCKER — read first)

**As shipped, the lpranging recipe does NOT validate and `materialize.py h-lpranging`
emits NOTHING.** This is a composition/import regression, independent of the
coverage mapping below.

Reproduction (real files, no patching):
```
cd staging/harness-recipes && ln -sfn /home/cpark/git/harness_ontology central
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
/usr/bin/python3 central/tools/validate.py      # → FAIL (7 SHACL violations)
… central/tools/materialize.py h-lpranging --out /tmp/build
# → "✗ REFUSING to materialize: the composed union does not validate", out dir not created
```

The 7 violations are `id2:role-{orchestrator,inspection,developer,research,
inspection-worker,vnv,design}` — *"Component must have a skos:prefLabel."*

**Root cause** (not a coverage gap — a stale import list):
- The central store gained a new unit `ontology/abox/core/roles.ttl` (7 neutral
  roles, all WITH prefLabel), and central `h-multiagent` (`ontology/abox/core/
  harnesses.ttl:98-99`) now `ho:hasRole` those 7 roles.
- The lpranging recipe imports `core-harnesses` (for `derivedFrom core:h-multiagent`
  lineage), so `h-multiagent` and its 7 `hasRole` bindings enter the union — but
  neither the **recipe catalog** `staging/harness-recipes/catalog-v001.xml` nor
  `lpranging.ttl`'s `owl:imports` (lines 50-61) includes the new `core-roles` unit.
- Result: the 7 role IRIs land in the union as bare component nodes (no triples
  from `roles.ttl` loaded) → each fails the Component `prefLabel` shape → union
  FAIL → materialize refuses.
- Central's own `tools/validate.py` (repo-root catalog, which *does* map `core-roles`
  at line 24) still prints **PASS** — so the defect is purely the recipe closure.

**Fix, verified**: add `core-roles` to the recipe catalog and to `lpranging.ttl`'s
`owl:imports`. With that one unit added to a scratch copy, the union validates
(`✓ SHACL / ✓ reachability / ✓ capabilities → PASS`) and materialize succeeds
(22 components, ~1086 tokens, 3 roles, 2/2 impls). The coverage mapping below was
produced from that scratch materialization (`build-lpr`), byte-diffed against source.

---

## 1. Source inventory (concrete counts)

`find . -path ./.git -prune -o -type f -print | wc -l` = **385 files**. Breakdown:

| area | count | notes |
|---|---|---|
| top-level `CLAUDE.md` / `CODESTYLE.md` / `DESIGN_HARNESS_STANDARD.md` | 3 | 20257 / 8707 / 16697 bytes |
| top-level docs `ARCHITECTURE/CONCEPT/ONTOLOGY/SYSTEM_DESIGN.md` | 4 | domain + doc-graph vocab |
| `.claude/agents/*` | 3 | developer, vnv, inspection |
| `.claude/skills/*/SKILL.md` | 3 | check-docs, new-design-doc, resolve-issue |
| `.claude/agent-memory/**` | 19 | per-role accumulated memory |
| `.claude/settings.local.json` | 1 | 3161 B permission allow-list |
| `tools/docgraph.py` | 1 | 32560 B |
| `reference/sim_grid_reservation.py` | 1 | 11309 B |
| `reference/**` (bitcraze_analysis, normal_ranging, ranging_v1, design_suggestions, …) | 128 | domain reference/research |
| `docs/terminology` / `issues` / `requirements` / `lessons` / `software` / `hardware` / `research` / `feedback` | 73/47/46/14/17/7/6/11 | project design-graph content |
| `exports/*.manifest` | 2 | ranging_module, weight_device |

`.claude/commands/` : **absent** in source (skills are the only slash-invocables).

---

## 2. Coverage table (source artifact class → representation / GAP)

| # | source artifact | ontology representation | verdict |
|---|---|---|---|
| 1 | `CLAUDE.md` persona | `id:sp-lpranging` (`ho:promptText`) → emitted `CLAUDE.md ## Persona` | COVERED |
| 2 | `CLAUDE.md` operating rules | 9 central `gr-*` guardrails → emitted `## Operating rules` (9 bullets) | COVERED |
| 3 | language rule (§언어 규칙) | `core:gr-lang` "Korean/English only" → emitted rule + 3 language sub-bullets (code/prose/terms) | COVERED |
| 4 | multi-agent process | `core:wf-multiagent` + `core:pat-orchestrator-workers` → emitted `## Process` | COVERED |
| 5 | model choice | `core:mc-opus` → emitted `## Model` (`claude-opus-4-8; temp 0.2`) | COVERED |
| 6 | `.claude/agents/developer.md` | `id:role-developer` + `id:sp-role-developer` → emitted `.claude/agents/developer.md` | COVERED |
| 7 | `.claude/agents/vnv.md` | `id:role-vnv` + `id:sp-role-vnv` | COVERED |
| 8 | `.claude/agents/inspection.md` | `id:role-inspection` + `id:sp-role-inspection` | COVERED |
| 9 | orchestrator (main agent, no file) | harness persona + `pat-orchestrator-workers` (no Role individual, matches source having no orchestrator file) | COVERED (consistent) |
| 10 | `DESIGN_HARNESS_STANDARD.md` | `ho:scaffold` → `scaffold/DESIGN_HARNESS_STANDARD.md` (**byte-identical**) | COVERED |
| 11 | `CODESTYLE.md` | `ho:scaffold` → `scaffold/CODESTYLE.md` (**byte-identical**) | COVERED |
| 12 | `docs/ONTOLOGY.md` (doc-graph vocab) | `ho:scaffold` → `scaffold/docs/ONTOLOGY.md` (**byte-identical**) | COVERED |
| 13 | `tools/docgraph.py` | `id:tool-docgraph` + `cap-designgraph`; `implementationRef` → `impl/docgraph.py` (**byte-identical**, emitted `tools/docgraph.py` identical to source) | COVERED |
| 14 | `reference/sim_grid_reservation.py` | `id:tool-simulator` + `cap-simulation`; `impl/sim_grid_reservation.py` (**byte-identical**) | COVERED |
| 15 | per-role memory discipline | `ho:roleMemoryPolicy` on each Role (policy text) | COVERED (policy) |
| 16 | RTLS/low-power domain vocab | `id:dom-sysdesign` + concept sub-tree `c-sysdesign/-embedded/-lowpower/-rtls` | COVERED |
| 17 | `.claude/skills/{check-docs,new-design-doc,resolve-issue}` | — none — | **GAP-B** (low) |
| 18 | `.claude/settings.local.json` | — none — | **GAP-A** |
| 19 | `.claude/agent-memory/**` (19 accumulated notes) | policy modeled (row 15); *content* not modeled | **GAP-A** |
| 20 | `exports/*.manifest` (2) | — none — | **GAP-A** |
| 21 | `docs/{terminology,issues,requirements,lessons,software,hardware,research,feedback}` (261 files) | — none — | **GAP-A** |
| 22 | `docs/{ARCHITECTURE,CONCEPT,SYSTEM_DESIGN}.md` | — none — | **GAP-A** |
| 23 | `reference/{bitcraze_analysis,normal_ranging,ranging_v1,design_suggestions}` (~126 files) | `sim_grid_reservation.py` only (row 14); rest not modeled | **GAP-A** |

Byte-fidelity checks (all `cmp` → identical): emitted `tools/docgraph.py` == source
`tools/docgraph.py`; emitted `tools/sim_grid_reservation.py` == source `reference/
sim_grid_reservation.py`; `scaffold/{DESIGN_HARNESS_STANDARD,CODESTYLE}.md` and
`scaffold/docs/ONTOLOGY.md` == source. Agent `.md` files are rendered from ontology
personas (English graph-data) so they byte-differ from the source's Korean files by
design — sanity-read confirms persona/scope match; the *set* is exactly
{developer,vnv,inspection}, matching source. Materialize is deterministic (two runs
`diff -r` identical). All 9 recipe text nodes carry `ho:tokenEstimate`; `validate.py`
reports no duplicate labels (no drift/near-synonyms).

---

## 3. What's missing

### GAP-A — legitimately out-of-model (acceptable)
The recipe models the harness's **reusable structure / bill-of-materials**, not the
project's domain-content instances or per-machine runtime state. Each of these is
correctly absent:

- **Domain design-graph content** (rows 21-22, 261+ files: terminology, issues,
  requirements, lessons, software/hardware design docs, ARCHITECTURE/CONCEPT/
  SYSTEM_DESIGN). Rationale: this is exactly the *output* the harness produces with
  `tool-docgraph` under the `docs/ONTOLOGY.md` vocabulary it ships — per-project
  instance data, not harness structure. Modeling it would re-import the whole project.
- **`reference/` research/reference subtrees** (row 23, ~126 files). Rationale: prior
  domain investigation material; not a harness capability. The one executable piece
  used as a tool (`sim_grid_reservation.py`) *is* modeled.
- **`exports/*.manifest`** (row 20). Rationale: docgraph-generated build artifacts,
  regenerable from the design graph.
- **`.claude/agent-memory/**` content** (row 19). Rationale: runtime-accumulated
  role memory; the *policy* that governs it is modeled per-role (`ho:roleMemoryPolicy`).
- **`.claude/settings.local.json`** (row 18). Rationale: per-machine permission grants
  with absolute project paths and one-off bash allow-entries; not reusable structure.

### GAP-B — should be reflected (genuine omissions)

**B1 (CRITICAL — blocker) — recipe union does not validate → materialize emits nothing.**
Not a modeling gap but a stale import closure: the recipe was not updated when the
central store added `core-roles`. Concrete fix (route to developer dispatch):
1. `staging/harness-recipes/catalog-v001.xml` — add
   `<uri id="core-roles" name="https://harness-ontology.dev/data/core/roles" uri="central/ontology/abox/core/roles.ttl"/>`.
2. `recipes/lpranging/lpranging.ttl` — add
   `https://harness-ontology.dev/data/core/roles` to the `owl:imports` list.
Verified sufficient: scratch copy with exactly these two additions → `validate.py`
PASS and `materialize.py h-lpranging` succeeds. (Any recipe that `derivedFrom`
`core:h-multiagent` needs this; techdoc likely has the same latent break.)

**B2 (LOW) — the 3 skills / slash-commands are not modeled.** `check-docs`,
`new-design-doc`, `resolve-issue` are named operating procedures the agents invoke
(referenced in source `CLAUDE.md:110-111` as `/check-docs` etc.). They are part of
the harness's operating capability, and the TBox already has classes that fit
(`ho:Instruction` = "procedure snippet injected into a harness", or `ho:Workflow`).
Suggested representation: 3 `ho:Instruction` (or `ho:Workflow`) individuals in
`lpranging.ttl`, each `ho:tagged core:c-traceability`, bound to `h-lpranging` (e.g.
via `hasWorkflow`/a new `hasInstruction`) and materialized as `.claude/skills/<name>/
SKILL.md`. **Severity is low** because the underlying capability (design-graph
management) is already fully captured by `tool-docgraph` + the `docs/ONTOLOGY.md`
scaffold — the skills are thin procedural wrappers over those. Note: materialize.py
currently has no skill-emit path, so B2 is a model+projection enhancement, not a
one-line fix.

---

## 4. Verdict

**Modeling faithfulness: COMPLETE ENOUGH.** Every reusable harness-structural element
of the source is represented: persona, all operating rules (incl. the Korean/English
language rule), the multi-agent workflow + orchestrator-workers pattern, the model
config, the exact 3 worker roles (+personas, tool/guardrail scopes, memory policy),
both operating tools with **byte-identical** vendored implementations, and all three
standard/vocabulary docs as byte-identical scaffold. No drift (no duplicate labels,
no untyped edges, tokenEstimate on every text node).

**But the harness does NOT currently reproduce a working tree.** As shipped, the
recipe union fails SHACL and `materialize.py` refuses (GAP-B1). So the honest answer
to "does materialize reproduce a working harness?" is **NO, until the `core-roles`
import is restored** — after which it reproduces a faithful, deterministic, working
harness (demonstrated on the scratch copy).

**Honest residual — what a human diffing against the real source would still miss:**
- the 3 skills/slash-commands (GAP-B2) — an operating convenience, capability already present;
- all domain design-graph content, reference subtrees, exports, memory content, and
  local settings (GAP-A) — intentionally out of model; the harness ships the *means*
  to regenerate the design graph, not the graph itself. A user materializing
  `h-lpranging` gets a working, empty-project harness skeleton, not a populated
  RTLS design repo. That is the correct scope for a harness BoM, but worth stating so
  the recipe is not over-claimed as a full project snapshot.

---

## 5. Prioritized routing for orchestrator (→ developer dispatch)

1. **[P0 / blocker] B1** — restore `core-roles` in the recipe catalog + `lpranging.ttl`
   `owl:imports` (2-line change, fix verified). Without it the recipe is unbuildable.
   Check whether `techdoc.ttl` needs the same. Re-run union `validate.py` → PASS gate.
2. **[P2 / enhancement] B2** — model the 3 skills as `ho:Instruction`/`ho:Workflow`
   individuals + a materialize.py skill-emit path, if skill parity with source is wanted.

Verification commands are in §0; scratch materialization used for §2 lives under the
session scratchpad `build-lpr/` (temp, not committed). No `ontology/`, `tools/`, or
central `docs/` files were edited; the temp `central` symlink was removed.
