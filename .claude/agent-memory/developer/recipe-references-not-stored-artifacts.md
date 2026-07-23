# Recipe stores references + explanation, NOT concrete build artifacts (fetch model)

MODELING PRINCIPLE (user directive): a recipe/ontology holds ONLY generalized
parts + methodology + **references**; the example EXPLAINS which parts +
methodology were used, how, and what result. It must NOT **store the concrete
build documents** (real tool code, standard/doc files, skill bodies). Vendoring
= storing copies = the anti-pattern. Fix = external references + materialize
FETCHES at build. "설명서 중심 + 참조 fetch". This is ODR INV-1 at the recipe layer:
implementation is referenced/regenerated, never stored in the spec.

## Applied to lpranging (staging/harness-recipes/recipes/lpranging)
- DELETED vendored `impl/*.py`, `scaffold/*.md` bodies, `skills/*/SKILL.md`
  (recipe dir now only `lpranging.ttl` + `README.md`).
- REPOINTED ref STRINGS at the REAL external source (absolute paths into
  `/home/cpark/git/agrtls/device_harvest_lp/lpranging`): `ho:implementationRef`
  (tools/docgraph.py, reference/sim_grid_reservation.py), `ho:scaffold` (3 root/docs
  .md), skill `ho:artifactTemplate` (.claude/skills/<name>/SKILL.md). These are
  REF-string edits only → ontology INDIVIDUAL COUNT UNCHANGED (union 119).
- README rewritten explanation-centric: §which parts (core: reused + id: local
  bindings), §which methodology (wf-compose-harness + ODR axes), §how (refs not
  stored + non-portability tradeoff), §what result (materialized tree).
- Tradeoff noted: absolute external refs = non-portable (resolve only where source
  present) but store NOTHING. Portability (repo-relative vendoring) is itself a
  stored copy — acceptable only for genuinely recipe-owned assets.

## materialize.py fetch-or-stub (the 3 emitters made symmetric)
- Single resolver `_resolve_ref_path(ref)` (renamed from `_resolve_implementation`,
  + `not ref` guard): repo root → recipe/catalog dir → **absolute path** → None.
  Used by ALL of implementationRef, scaffold, skill artifactTemplate.
- `_ref_stub(kind, ref, owner)` shared deterministic stub body.
- `emit_scaffold`: was `render_from_template` (placeholder subst + rstrip) → now
  **raw `shutil.copyfile`** (byte-identical) + `.ref` stub on absent. Placeholder
  subst DROPPED from scaffold (a scaffold is now a faithful byte-copy, not a
  rendered template). NOTE: component-SECTION templating via artifactTemplate on a
  SystemPrompt/Guardrail (P2, `render_component`→`resolve_template`) is UNCHANGED —
  techdoc's persona.md.tmpl still substitutes {{}}. Don't conflate the two.
- `emit_instructions` (skills): was `shutil.copyfile(resolve_template(...))`
  (raised FileNotFoundError on absent) → now `_resolve_ref_path` + `.ref` stub.
- Added per-record `status` (resolved|stub; skills also `graph`) to scaffold +
  skill manifest records (impl already had it).
- `_scaffold_dest`: external abs path has no "scaffold/" marker → **basename at
  tree root** (so `.../docs/ONTOLOGY.md` emits `ONTOLOGY.md` at root, was
  `docs/ONTOLOGY.md`). Documented in README + materialize-design.

## Gate recipe (no git, /usr/bin/python3, central untouched)
- central validate PASS 96 unchanged; py_compile materialize.py.
- lpranging compose: temp `central` symlink→repo root at staging catalog root,
  `HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=.../recipes/lpranging`
  → validate PASS, union 119 unchanged. rm symlink after.
- materialize with source PRESENT → all resolved, `cmp` each fetched file to
  source = byte-identical, 2 runs `diff -r` IDENTICAL.
- STUB test: scratch recipe copy + scratch catalog (copy catalog + `central`
  symlink + copy recipe ttl) with one ref of EACH kind repointed to a nonexistent
  abs path → materialize exit 0, emits `<dest>.ref` for impl/scaffold/skill, other
  refs still resolved, 2 runs identical.
- Regression: techdoc + contract-demo still materialize (render_component/candidate
  paths untouched).

## techdoc / contract-demo (separate-decision note)
- **techdoc**: NO vendored artifacts. artifactTemplate → central neutral tool asset
  `tools/materialize_templates/persona.md.tmpl` (reusable, not a harness build doc).
  Already principle-aligned; nothing to convert.
- **contract-demo**: stores `impl/greeter_v1.py` + `greeter_v2.py` — but these are
  SYNTHETIC demo code for the ODR VERIFY INV-4 candidate-swap; there is NO real
  external source to reference (the demo IS the artifact). The "reference the
  external source" fix doesn't cleanly apply (nothing external). Acceptable as a
  genuinely recipe-owned demo asset, OR convert via a generation step / fetchable
  source if a stricter "store nothing" line is wanted. Flag for orchestrator/user.
