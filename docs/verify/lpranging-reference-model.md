# V&V verdict — lpranging "reference-model" rework (store references + explanation, not concrete build documents)

- **Verdict: `pass-with-notes`**
- Agent: vnv. Date: 2026-07-23. All tools run with `/usr/bin/python3`.
- Principle under test: the ontology/recipe stores ONLY **generalized parts + methodology
  + an explanation of the composition** — NOT the concrete build documents; `materialize.py`
  **fetches** external references at build (or emits a fail-safe `.ref` stub if absent).
- Scope of edit: `docs/verify/**` only. No ontology/tools/docs edits; no git. All temp
  symlinks/scratch created for reproduction were removed (staging has no at-rest symlink;
  verified `find staging -type l` empty).

---

## 1. Central neutral/structural (verification gate) — PASS

Command (repo root):
```
/usr/bin/python3 tools/validate.py
```
Output: `PASS` — 2220 triples, SHACL conforms, **all 96 individuals** reachable from a
Harness, capabilities satisfied, no duplicate labels. Both loader observations agree:
default `lib.load_graph(reason=True)` reports `instances 96`; validate reports 96.
`retrieve.py "design a low power ranging embedded system"` returns a bounded pack (898/900
tokens, 27 nodes) with `h-multiagent` as the base candidate — retrieve smoke intact.

## 2. No stored concrete artifacts — PASS (proof)

`staging/harness-recipes/recipes/lpranging/` contains **exactly two files**:
```
lpranging.ttl
README.md
```
`find` shows no `.py`, no `SKILL.md`, no `scaffold/*.md` bodies, no `impl/` dir. The vendored
build documents are gone.

All build refs in `lpranging.ttl` are **external absolute paths** under
`/home/cpark/git/agrtls/device_harvest_lp/lpranging/...`:
- `ho:implementationRef` (lines 130, 141) → `tools/docgraph.py`, `reference/sim_grid_reservation.py`
- `ho:artifactTemplate` (lines 210, 215, 220) → the 3 real source `.claude/skills/*/SKILL.md`
- `ho:scaffold` (line 252) → `DESIGN_HARNESS_STANDARD.md`, `CODESTYLE.md`, `docs/ONTOLOGY.md`

`grep -nE '"recipes/'` on the TTL → **NONE**: no repo-relative in-recipe refs remain.

Recipe union composes and validates (symlink dance: `ln -sfn <repo-root>
staging/harness-recipes/central`, then):
```
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
/usr/bin/python3 central/tools/validate.py
```
Output: `PASS` — **all 119 individuals** reachable, SHACL conforms, capabilities satisfied
(the ~119 the brief expected; individuals unchanged by the rework — refs are build-only
literals and do not add/remove nodes). Also verified every `ho:promptText` node in the union
carries `ho:tokenEstimate` (missing = NONE), so future projections stay budget-accurate.

## 3. materialize fetch-or-stub — PASS (evidence)

### 3a. Source PRESENT → byte-identical fetch, status resolved, deterministic
```
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=.../recipes/lpranging \
/usr/bin/python3 central/tools/materialize.py h-lpranging --out <scratch>/lpr1
```
Exit 0. Emitted tree: `CLAUDE.md`, `MANIFEST.json`, `harness.lock.json`,
`.claude/agents/{developer,vnv,inspection}.md`, `.claude/skills/{check-docs,new-design-doc,resolve-issue}/SKILL.md`,
`tools/{docgraph.py,sim_grid_reservation.py}`, `DESIGN_HARNESS_STANDARD.md`, `CODESTYLE.md`,
`ONTOLOGY.md`.

`cmp` emitted vs the real source — **all 8 byte-identical**:

| emitted | source | cmp |
|---|---|---|
| tools/docgraph.py | tools/docgraph.py (32560B) | identical |
| tools/sim_grid_reservation.py | reference/sim_grid_reservation.py (11309B) | identical |
| DESIGN_HARNESS_STANDARD.md | DESIGN_HARNESS_STANDARD.md | identical |
| CODESTYLE.md | CODESTYLE.md | identical |
| ONTOLOGY.md | docs/ONTOLOGY.md | identical |
| .claude/skills/check-docs/SKILL.md | .claude/skills/check-docs/SKILL.md | identical |
| .claude/skills/new-design-doc/SKILL.md | .claude/skills/new-design-doc/SKILL.md | identical |
| .claude/skills/resolve-issue/SKILL.md | .claude/skills/resolve-issue/SKILL.md | identical |

MANIFEST records `status: resolved` for all 8 (2 impl + 3 scaffold + 3 skill). Determinism:
a second run to `lpr2` and `diff -r lpr1 lpr2` → **IDENTICAL** (lock/manifest carry no timestamps).

### 3b. Source ABSENT → exit 0, `.ref` stubs, no crash, resolved refs still fetched
Made a scratch copy of the whole recipe repo (did NOT touch the real recipe) and repointed
**one ref of each kind** at a nonexistent path (`NOPE_sim.py`, `NOPE_CODESTYLE.md`,
`resolve-issue/NOPE_SKILL.md`). The scratch union still validates PASS (refs are build-only).
Materialize exit 0, emitted exactly three stubs:
```
tools/NOPE_sim.py.ref
NOPE_CODESTYLE.md.ref
.claude/skills/resolve-issue/SKILL.md.ref
```
MANIFEST marks those three `status: stub`; the remaining resolved refs still fetch
byte-identical (`cmp` docgraph, check-docs → OK). Stub body is a deterministic placeholder
naming the owner IRI and the unresolved ref — the build "names exactly what did not travel"
rather than failing. `_resolve_ref_path` (repo→recipe→absolute→None) is the single shared
resolver for impl/scaffold/skill, so the fetch-or-stub behaviour is uniform across all three.

## 4. README-as-explanation — PASS (assessment)

`recipes/lpranging/README.md` genuinely reads as *an explanation of a composition*, not a
store of artifacts. It has the four required movements:
- **§1 Which parts** — the reused central neutral parts named by `core:` IRI (template,
  workflow/pattern, 9 guardrails, generic tools+model, 3 channels, tasks/concepts) vs. the
  locally-declared domain bindings (domain+concept sub-tree, 2 domain tools+capabilities, 3
  contracts, 3 worker roles, domain persona). It is explicit that the recipe *references*,
  does not define, the central parts.
- **§2 Which methodology** — the composition methodology (bind every `requiresCapability` to
  a provider, satisfy `HarnessShape` minimums) with the 6 concrete capability→provider
  bindings listed, plus the ODR SPEC/BIND/EMIT/VERIFY axes.
- **§3 How applied** — the load-bearing statement that the recipe stores spec + explanation
  + references and NOT the build documents, with an explicit, honest **tradeoff** callout
  (absolute external paths → not portable; a deliberate reversal of the earlier vendoring).
- **§4 What result** + a reproduce block (compose→validate→materialize).

It states which parts, which methodology, how, and what result — the explanation objective is met.

## 5. Regression — PASS

`techdoc` and `contract-demo` unions both validate PASS and materialize exit 0:
- `h-techdoc` → CLAUDE.md + MANIFEST + lock (1 template source: the central
  `tools/materialize_templates/persona.md.tmpl`).
- `h-contract-demo` → CLAUDE.md + MANIFEST + lock + `tools/greeter.py`
  (`cand-greeter-stable`, latest-stable). The `.ref` mechanism did not perturb either.

## 6. Principle judgment (V&V opinion)

**Does the reworked lpranging embody the principle?** Yes. Its recipe dir now carries only
the spec TTL (part IRIs + external references) and an explanatory README; every concrete
build document (tool code, scaffold, skill body) lives at its authoritative external source
and is fetched at build. This is a clean instance of "store generalized parts + methodology
+ explanation, not the concrete artifacts." The only cost is portability, which the README
discloses as an explicit user choice — acceptable and correctly documented, not a defect.

**techdoc — aligned.** Its recipe dir is `README.md` + `techdoc.ttl` only; it stores no
build document. Its single `ho:artifactTemplate` points at `tools/materialize_templates/
persona.md.tmpl`, a **reusable central tool asset** (resolves under the central repo root,
not inside the recipe). Referencing a generalized central template — rather than vendoring a
persona copy — is exactly the principle. No action needed.

**contract-demo — acceptable, noted tension (my recommendation: keep, document as fixture).**
It still stores concrete build documents in-recipe (`impl/greeter_v1.py`, `impl/greeter_v2.py`,
referenced by repo-relative `recipes/contract-demo/impl/...`), which is literally the
vendoring pattern the principle removes. However this is defensible and I do **not** flag it
as a defect:
- These are **synthetic demo fixtures** with **no external source** — purpose-built as two
  deliberately divergent candidates to exercise the ODR VERIFY / INV-4 candidate-rebind
  machinery. The recipe *is* their authoritative home; there is no elsewhere to reference.
- The principle's intent (per the rework) is: do not vendor **copies of documents that live
  authoritatively elsewhere** (a real source harness). greeter_v* are not copies and are not
  a "generalized part" drawn from a library — they are the demo's own subject matter.
- Converting them to an external ref would mean inventing an external home for throwaway
  demo code — relocation for purity with zero generalization benefit, and it would make the
  demo non-self-contained.

**Recommendation (non-blocking):** to remove the surface tension without harming the demo,
either (a) explicitly document contract-demo's `impl/` as an accepted *test-fixture*
exception to the store-references principle (a one-line note in its README / `docs/recipes-
design.md`), or (b) if strict uniformity is wanted, relocate them under a `fixtures/` marker
so they read as fixtures, not vendored build artifacts. Neither is required for this
increment to pass.

---

## Notes (bounds, not defects)

- **N1 — portability tradeoff (lpranging).** External absolute refs resolve only on a box
  where the real source harness is present; off that box, materialize fail-safes to `.ref`
  stubs. Disclosed in the README as a deliberate user choice ("설명서 중심 + 참조 fetch").
  Correct and honest; portability, if ever wanted, is a separate concern.
- **N2 — contract-demo in-recipe fixtures.** See §6; accepted as a demo fixture, with a
  documentation/relocation recommendation.
- **N3 — recipe ≠ full project.** The materialized tree covers the harness (persona,
  guardrails, workflow, pattern, model, 3 roles, 3 channels, 2 tools, 3 scaffold, 3 skills);
  the source project's domain design docs / exports / agent-memory content remain
  out-of-model, which is correct (only the harness is modeled) but noted to avoid overclaim.

## Reproduce (commands actually run)

```
# central gate
/usr/bin/python3 tools/validate.py                      # PASS 96

# recipe union (symlink dance; removed after)
cd staging/harness-recipes && ln -sfn <repo-root> central
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=.../recipes/lpranging \
  /usr/bin/python3 central/tools/validate.py            # PASS 119
  ... materialize.py h-lpranging --out lpr1             # exit 0, 8 fetched
  ... materialize.py h-lpranging --out lpr2 ; diff -r lpr1 lpr2   # IDENTICAL
cmp <emitted> <source>                                  # all 8 identical
# absent-source: scratch recipe copy, 3 bogus refs -> materialize exit 0, 3 .ref stubs
# regression: materialize.py h-techdoc / h-contract-demo -> exit 0
rm -f central                                           # cleanup (verified no staging symlink)
```
