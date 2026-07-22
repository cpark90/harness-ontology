# Verify: materialization layer (increment 1) + language-condition guardrail

**Verdict: `pass-with-notes`** — both changes are correct against the graph and by
execution; the single note is a latent central bug in `ontology_lib.most_specific_types`
that the materialize developer correctly worked around locally (not a defect of this increment).

Agent: vnv. Interpreter: `/usr/bin/python3` (has rdflib/pyshacl/owlrl). Reproduction commands below.

---

## 1. Structural (verification)

`/usr/bin/python3 tools/validate.py` → **PASS**:
```
✓ SHACL (conforms — no orphaned/under-specified nodes)
✓ reachability (all 64 individuals reachable from a Harness)
✓ capabilities (every harness's required capabilities provided internally)
PASS
```
- Both loader paths agree. Catalog vs glob-fallback (`HARNESS_CATALOG=/nonexistent`,
  `importlib.reload`): pre-reasoning triples 575 == 575, **symmetric diff 0**. `validate.py`
  PASSes under both loaders.
- `retrieve.py` unaffected — smoke `retrieve.py "cited technical documentation" --format json`
  returns candidates (top: Research synthesis agent). The read projection ignores the two new
  build-only datatype properties.

## 2. Anti-drift on the two TBox adds

- `grep -rn "languageCondition|artifactTemplate" ontology/` → **exactly two** new schema terms,
  both in `ontology/tbox/harness.ttl` (`ho:languageCondition` DatatypeProperty domain
  `ho:Guardrail`; `ho:artifactTemplate` DatatypeProperty domain `ho:HarnessComponent`, range
  string). No near-synonym class, no untyped edge.
- Each is used by ≥1 node → connected, not orphan vocabulary:
  - `ho:languageCondition` on `core:gr-lang` (central `ontology/abox/core/guardrails.ttl`).
  - `ho:artifactTemplate` on `id:sp-techdoc` (techdoc **recipe**, `staging/harness-recipes/recipes/techdoc/techdoc.ttl`).
- `grep -rln artifactTemplate ontology/abox/core/` = **0** — central stays neutral; the template
  ref lives in the recipe only, as designed.
- `core:gr-lang` carries **exactly 3** `languageCondition` items (queried via rdflib):
  prose(documentation/comments/harness .md)=Korean; technical terms(incl. answers)=English;
  code/identifiers/commits=English. Matches the operating language policy in CLAUDE.md / §1d.
- Shapes not weakened: `grep -rn sh:closed ontology/ tools/` = **none** (no closed-shape to
  break); SHACL still `conforms`. Only shape file is `ontology/shapes/harness-shapes.ttl`.

## 3. materialize runs + is correct (validation — BUILD dual)

Built the techdoc **recipe** union (temporary `staging/harness-recipes/central` symlink → repo
root; catalog `catalog-v001.xml`; `HARNESS_ROOT_ONTOLOGY=…/recipes/techdoc`) and ran
`central/tools/materialize.py h-techdoc --out <scratch>`. **Symlink removed and scratch cleaned
after** (staging at-rest symlink count = 0). Exit 0, emitted `CLAUDE.md` + `MANIFEST.json`.

(a) **CLAUDE.md** non-empty, all sections present in fixed order: `# Technical documentation
agent` (overview←definition) / `## Persona` / `## Operating rules` / `## Process` (Workflow +
Pattern) / `## Model` (`mc-opus` with `model=claude-opus-4-8; temperature=0.2`). The
`languageCondition` bullets render as three sub-bullets under **Korean/English only**:
```
- **Korean/English only** — Use only Korean and English, unless another language …
    - Code, identifiers, commit messages: English
    - Prose (documentation, comments, harness .md): Korean
    - Technical terms, including in answers: English
```

(b) **MANIFEST.json** lists 11 components (5 Guardrail, 3 Tool, 1 Workflow, 1 ModelConfig,
1 SystemPrompt) with **correct concrete types** (not the abstract HarnessComponent), plus the
**4 capability bindings** matching the graph's requires→provides:
`cap-citation←gr-cite` (guardrail provider), `cap-fileedit←tool-editor`,
`cap-retrieval←tool-retriever`, `cap-websearch←tool-websearch`. `derivedFrom` = `core:h-research`.
`tokenEstimate` = 479 (summed).

(c) **templateSources** = `["tools/materialize_templates/persona.md.tmpl"]`, and the Persona
section shows **template-rendered** text — it carries the template's fixed tail line
`_Persona: … rendered from a template fragment (ho:artifactTemplate) rather than raw graph data._`
which is absent from the graph-data fallback path. Confirms render-via-template, not fallback.

## 4. Validation gate (refuse to build an unvalidated union)

The gate (`validate.run_structured()`) runs **before** load/resolve/write. Two proofs, both
non-zero exit with **no output directory created**:
- **Bogus harness id** (`h-DOES-NOT-EXIST`, union otherwise valid) → exit **2**,
  `✗ no harness matches …`, no dir written.
- **Non-validating union** (scratch root importing only `schema` + `core/harnesses`, so harness
  nodes reference components absent from the closure) → exit **1**,
  `✗ REFUSING to materialize: the composed union does not validate …`, no dir written.

## 5. Determinism

Two runs into `det1`/`det2` → `diff -r` reports **IDENTICAL**; sha256 of both `CLAUDE.md`
equal and both `MANIFEST.json` equal (fixed section order + IRI-sorted components + `sort_keys`).

## 6. Design doc

`docs/materialize-design.md` states the retrieve↔materialize symmetry (read vs build
projection, table), the template-file-reference mechanism + two-base path resolution (repo-root
then catalog/recipe-dir, first-existing wins, missing-file hard error, absent ⇒ graph-data
fallback), the section→predicate mapping table, and P3/P4/P5 as explicit **follow-ups (NOT
done)**. Confirmed **no P3/P4/P5 vocabulary silently introduced**:
`grep -rniE "toolImpl|implementationRef|firstClassRole|standardScaffold|docsScaffold"` over
`ontology/`+`tools/` = none (mentioned only as future prose in the design doc).

---

## Judgments

**Is materialize a faithful BUILD dual of retrieve?** Yes. It (i) loads the same union under the
same `HARNESS_CATALOG`/`HARNESS_ROOT_ONTOLOGY` contract as validate/retrieve (recipe union
materializes identically to the central store), (ii) is honest — it emits a file tree *only*
from a graph that passes the very same structured validation, refusing otherwise, (iii) is
deterministic (byte-identical re-runs), and (iv) its manifest mirrors
`validate.check_capability_satisfaction` as an explicit requires→provides composition proof.
`ho:artifactTemplate` is strictly build-only and leaves the read projection unchanged. This is a
sound spine (P1) + template refs (P2) increment.

**Is the `_component_type` local workaround sound, or should `ontology_lib` be fixed centrally?**
The workaround is **sound and correct for the manifest**, and choosing a local fix (touching only
`materialize.py`, per least-privilege) was the right call for this increment. But it papers over
a **real latent bug in the shared `ontology_lib.most_specific_types`** that a central fix should
eventually address. Empirically confirmed under `load_graph(reason=True)`:
- OWL RL materializes reflexive `rdfs:subClassOf` (verified: `Tool subClassOf Tool` present).
- `most_specific_types(tool-editor)` therefore returns `['HarnessComponent', 'Tool']` — the
  "drop superclasses" loop discards every type via its own reflexive self-edge, so it always
  falls back to returning **all** types. `mst[0]` = `HarnessComponent`, which is why the manifest
  would otherwise label every component with the abstract class.
- This defect is **pre-existing and not introduced by this change**, and it affects *all* callers
  under reasoning: `validate.py:131` (dup-label grouping — benign, keys stay consistent),
  `retrieve.py:77/169` and `webui/server.py:146/162` (`types` field shows the abstract class
  alongside the concrete one — noisy but not breaking).

Recommended central fix (route to orchestrator → developer, out of scope here): guard the
self-edge in `most_specific_types`, e.g. `if sup != t: specific.discard(sup)`, so superclass-drop
survives reflexive `subClassOf`. That would let `materialize._component_type` fall back to the
plain `lib.most_specific_types(...)[0]` and would also clean up retrieve/webui type reporting.
The workaround also only strips `HarnessComponent`; a future intermediate class in the hierarchy
would not be handled by it, whereas the central fix generalizes. **Not a blocker** — this
increment is correct as delivered.

---

Reproduction (from repo root unless noted):
```
/usr/bin/python3 tools/validate.py
HARNESS_CATALOG=/nonexistent /usr/bin/python3 tools/validate.py
/usr/bin/python3 tools/retrieve.py "cited technical documentation" --format json
# recipe materialize (temp symlink, removed after):
ln -sfn "$(pwd)" staging/harness-recipes/central
cd staging/harness-recipes
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/techdoc \
  /usr/bin/python3 central/tools/materialize.py h-techdoc --out <scratch> --format text
rm -f central   # hygiene: no at-rest symlink
```
