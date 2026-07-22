# Verdict — lpranging recipe: faithful re-reflection of the real source

- **Verdict**: `pass-with-notes`
- **Primary axis**: faithfulness of `staging/harness-recipes/recipes/lpranging/` to the
  real source harness `~/git/agrtls/device_harvest_lp/lpranging/`.
- **Agent**: vnv. **Interpreter**: `/usr/bin/python3` (rdflib/pyshacl/owlrl).
- **Scope**: judgment only. No `ontology/` / `tools/` / source edits; no git. Temp compose
  symlink and scratch trees created for evidence were removed after use.

Bottom line: the re-authoring claims all hold. Synthetic/demo content is gone, the recipe
now binds one faithful vendored implementation per tool via a direct `ho:implementationRef`,
and the materialized tree is a **byte-identical** reproduction of the source's code +
scaffold docs and a **semantically faithful** reflection of its roles and operating rules.
The notes are honest boundary limitations (language shift + source artifacts a harness
recipe does not model), not defects.

---

## 1. Central neutrality & structural (verification)

Command (repo root):
```
/usr/bin/python3 tools/validate.py
```
Result: **PASS**, `all 64 individuals reachable from a Harness`, SHACL conforms, capabilities
satisfied, no duplicate labels. Post-reasoning graph 1630 triples.

- `grep -rniE "lpranging|hasRole|implementationCandidate|selectionPolicy|docgraph|sim_grid" ontology/abox/core/` → **0 hits**. The recipe/role/candidate terms did not leak into central abox.
- retrieve smoke `/usr/bin/python3 tools/retrieve.py "multi-agent orchestration"` → intact
  (base candidate "Multi-agent orchestration harness", 29 nodes, 894/900 budget).
- Central TBox `ontology/tbox/harness.ttl` **still carries** the BIND/lock vocab
  (`ho:Candidate` L77, `ho:implementationCandidate` L170, `ho:selectionPolicy` L295,
  `hasComponent owl:propertyChainAxiom` L120, `ho:implementationRef` L278). It is retained
  but unused by this faithful recipe — and the `ho:implementationRef` definition itself
  sanctions the path taken here: "Carried by a ho:Candidate ... **OR directly by a ho:Tool
  as a degenerate single-candidate**." Claim confirmed.

## 2. No synthetic residue (the removal claims)

In `staging/harness-recipes/recipes/lpranging/`:
- `find -iname '*_v2*' -o -iname '*lock*' -o -iname '*.lock.json'` → **none**. `impl/docgraph_v2.py` and the vendored `harness.lock.json` are ABSENT.
- `grep -nE "Candidate|implementationCandidate|selectionPolicy|harness.lock" lpranging.ttl`
  → the **only** hit is a lone `#` comment (L90) stating the ODR BIND axis is intentionally
  not used. No `ho:Candidate` / `ho:implementationCandidate` / `ho:selectionPolicy` node exists.
- `impl/` holds exactly two files: `docgraph.py` (32560 B) and `sim_grid_reservation.py` (11309 B).
- Each tool carries a **single direct, repo-relative** `ho:implementationRef`:
  - `id:tool-docgraph` → `"recipes/lpranging/impl/docgraph.py"`
  - `id:tool-simulator` → `"recipes/lpranging/impl/sim_grid_reservation.py"`

## 3. Compose validity (union)

Commands (`staging/harness-recipes/`, temp `central` symlink → repo root):
```
ln -sfn /home/cpark/git/harness_ontology central
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
/usr/bin/python3 central/tools/validate.py
```
Result: **PASS**, `all 81 individuals reachable from a Harness`, SHACL conforms, capabilities
satisfied internally, no duplicate labels. Post-reasoning 1939 triples. Both central (64) and
union (81) consistent. Symlink removed afterward; `find staging -type l` → none.

## 4. Faithful materialize + cmp against the REAL source (core check)

Command:
```
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
/usr/bin/python3 central/tools/materialize.py h-lpranging --out <scratch>
```
Emitted tree: `CLAUDE.md`, `MANIFEST.json`, `.claude/agents/{developer,vnv,inspection}.md`,
`tools/{docgraph.py,sim_grid_reservation.py}`, `DESIGN_HARNESS_STANDARD.md`, `CODESTYLE.md`,
`docs/ONTOLOGY.md`, `harness.lock.json` (a fresh **build** lock — an output artifact, not the
removed vendored recipe file).

### `cmp` table (emitted vs real source)

| emitted artifact | source file | cmp result |
|---|---|---|
| `tools/docgraph.py` | `tools/docgraph.py` | **identical** (byte-for-byte) |
| `tools/sim_grid_reservation.py` | `reference/sim_grid_reservation.py` | **identical** |
| `DESIGN_HARNESS_STANDARD.md` | `DESIGN_HARNESS_STANDARD.md` | **identical** |
| `CODESTYLE.md` | `CODESTYLE.md` | **identical** |
| `docs/ONTOLOGY.md` | `docs/ONTOLOGY.md` | **identical** |
| `.claude/agents/developer.md` | `.claude/agents/developer.md` | differs — re-authored persona (see below) |
| `.claude/agents/vnv.md` | `.claude/agents/vnv.md` | differs — re-authored persona |
| `.claude/agents/inspection.md` | `.claude/agents/inspection.md` | differs — re-authored persona |

Vendored code and scaffold docs are exact reproductions. The three agent files differ
byte-wise **by design**: they are rendered from ontology role personas (English graph-data
values per the repo language policy §1d), not byte copies of the Korean source files.

### Agent set

Emitted `.claude/agents/` = exactly `{developer.md, vnv.md, inspection.md}` = the source's
agent set. `orchestrator` is correctly NOT a role file (it is the main agent in CLAUDE.md).

### Persona / scope faithfulness (sanity-read)

- **developer** (emitted) — "receive a complete node-scoped brief ... implement only the
  module it assigns ... do not widen scope ... stop and report [divergence] to the
  orchestrator." Matches source `developer.md` (담당 모듈만 구현, brief 밖 확장 금지, 설계
  어긋남 보고). Scope tools editor+shell, guardrails least-privilege / no-arbitrary-decision /
  verify-proceed / lang, memory `developer/` only — a faithful reflection.
- **vnv** (emitted) — "run the verification harness ... grounded verdict with reproducible
  evidence, separating verification from validation ... never edit source or design docs."
  Matches source `vnv.md` (판정만, verification/validation 구분, 소스·설계 편집 금지).
- **inspection** — investigates design graph, verifies feedback ripple via docgraph impact,
  owns version control, touches only feedback channel. Matches source persona.

### CLAUDE.md operating rules vs source

All six requested source principles are present and faithful in the emitted CLAUDE.md:

| principle | emitted rule | source |
|---|---|---|
| traceable design records | "Traceable single source of truth ... never delete a decision, deprecate with reason+replacement, increment identifiers" | CLAUDE.md L68-69, L167 |
| escalate-as-issue | "No arbitrary decisions — register each open judgment as an issue and escalate" | L189 |
| verify-then-proceed | "Verify then proceed — advance only on confirmed state; timeouts are give-up bounds" | L171, L230 |
| design-for-loss | "Design for loss — hold custody until confirmed, report cumulative absolute state, make loss observable via counters" | L175-185 |
| least-privilege | "Least-privilege role boundaries — authoring, judgment, application, version control in separate hands" | L150, roles table |
| Korean/English | "Korean/English only — prose Korean, terms/code/identifiers/commits English" | L213-215 |

## 5. Determinism

Two materialize runs → `diff -r mat_A mat_B` → **IDENTICAL**.

## 6. Faithfulness judgment

**This is a truthful re-reflection of the real harness's structure.** The materialized tree
reproduces the source's operating code (`docgraph.py`, `sim_grid_reservation.py`) and its
authoring-standard scaffold (`DESIGN_HARNESS_STANDARD.md`, `CODESTYLE.md`, `docs/ONTOLOGY.md`)
byte-for-byte, carries the exact same three sub-agents with faithfully reflected personas and
least-privilege scopes, and encodes the source's persona and operating-rule set (traceable
records, escalate-as-issue, verify-then-proceed, design-for-loss, least-privilege, K/E
language) in the emitted CLAUDE.md. No invented node, no wrong tool location (source
`reference/sim_grid_reservation.py` correctly lands at emitted `tools/sim_grid_reservation.py`
via the tool basename), no stub-vs-real-doc substitution, no missing role. No divergence
between the materialized tree and the real source was found on any checked artifact.

### Notes / honest limitations (why pass-**with-notes**, none are defects)

- **N1 — language shift (by design).** Emitted personas / agent files / CLAUDE.md prose are
  **English** (ontology neutral graph-data values, language policy §1d), whereas the source
  files are **Korean**. The reflection is therefore *semantically* faithful but not a byte
  copy of the source's Korean prose. This is a property of how the ontology stores persona
  text, not an error; the code and scaffold docs (which the recipe vendors verbatim) are
  byte-identical.
- **N2 — a harness recipe models the harness, not the whole project.** Source artifacts with
  **no ontology representation** and thus absent from the materialized tree: domain design
  docs (`docs/ARCHITECTURE.md`, `docs/CONCEPT.md`, `docs/SYSTEM_DESIGN.md`, and the
  `docs/{feedback,hardware,issues,lessons,requirements,research,software,terminology}` trees),
  `.claude/skills/{check-docs,new-design-doc,resolve-issue}`, `.claude/agent-memory/*`,
  `.claude/settings.local.json`, `exports/*.manifest`, and the `reference/` subtrees
  (`bitcraze_analysis`, `normal_ranging`, `ranging_v1`, `design_suggestions`). This is the
  correct boundary — the recipe captures the harness (persona, operating rules, tools, roles,
  model, authoring scaffold), not the project's full domain content — but is stated here as an
  explicit limitation so the reproduction's scope is not overclaimed.
- **N3 — vnv role gains the simulator tool** (`roleTool core:tool-shell, id:tool-simulator`)
  whereas source `vnv.md` frontmatter lists `Read, Grep, Glob, Bash, Write`. This is a
  domain-appropriate binding (vnv runs the discrete-event simulator as its verification
  harness for this design domain), consistent with least-privilege (the tool is bound to the
  harness via `usesTool`), and faithful in spirit — non-defect.

---

## Reproduction (exact commands run)

```
# 1 central
/usr/bin/python3 tools/validate.py                       # PASS, 64 reachable
grep -rniE "lpranging|hasRole|implementationCandidate|selectionPolicy|docgraph|sim_grid" ontology/abox/core/   # 0

# 2 residue (in recipe dir)
find recipes/lpranging -iname '*_v2*' -o -iname '*lock*'  # none
grep -nE "Candidate|selectionPolicy|harness.lock" recipes/lpranging/lpranging.ttl   # only a # comment

# 3 compose (staging/harness-recipes)
ln -sfn /home/cpark/git/harness_ontology central
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
  /usr/bin/python3 central/tools/validate.py             # PASS, 81 reachable

# 4 materialize + cmp
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
  /usr/bin/python3 central/tools/materialize.py h-lpranging --out <A>
cmp <A>/tools/docgraph.py             ~/git/agrtls/device_harvest_lp/lpranging/tools/docgraph.py
cmp <A>/tools/sim_grid_reservation.py ~/git/agrtls/device_harvest_lp/lpranging/reference/sim_grid_reservation.py
cmp <A>/DESIGN_HARNESS_STANDARD.md    ~/git/agrtls/device_harvest_lp/lpranging/DESIGN_HARNESS_STANDARD.md
cmp <A>/CODESTYLE.md                  ~/git/agrtls/device_harvest_lp/lpranging/CODESTYLE.md
cmp <A>/docs/ONTOLOGY.md              ~/git/agrtls/device_harvest_lp/lpranging/docs/ONTOLOGY.md

# 5 determinism
... materialize --out <B>; diff -r <A> <B>               # IDENTICAL

# cleanup
rm -f central                                            # staging at-rest symlinks: 0
```

Routing: no defect requiring developer re-authoring. The two boundary limitations (N1 language
shift, N2 unmodeled source artifacts) are recipe-scope characteristics; if broader coverage of
the source's domain-doc tree is desired, that is a recipe-authoring design decision for
orchestrator/inspection, not a correctness fix.
