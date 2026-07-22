# materialize.py — build projection (recipe → harness file tree)

`tools/materialize.py` = the DUAL of `retrieve.py`. retrieve=READ projection
(request→context pack), validate=CHECK, materialize=BUILD (validated harness IRI
→ file tree: `CLAUDE.md` + `MANIFEST.json`). First increment = spine P1 + template
refs P2; P3(tool impl refs)/P4(first-class roles)/P5(scaffold) are follow-ups.
Design doc: `docs/materialize-design.md`.

## Key patterns / gotchas
- **Peer of retrieve/validate**: flat `import ontology_lib`, `import validate`,
  `/usr/bin/python3`. Loads via `lib.load_graph()` so `HARNESS_CATALOG`/
  `HARNESS_ROOT_ONTOLOGY` env overrides compose a RECIPE union identically to central.
- **Validation gate before build**: call `validate.run_structured()` (same as
  `validate.py --json`); refuse (stderr + non-zero exit, write nothing) unless
  `result["pass"]`. "Only a validated harness materializes." Test refusal by a
  catalog that omits central units → incomplete union fails SHACL/capability → refuse.
- **`most_specific_types` reflexive-subClassOf bug — NOW FIXED CENTRALLY**: OWL RL
  materialises `rdfs:subClassOf` reflexively (`Tool subClassOf Tool`); the superclass-drop
  loop discarded every type via its own self-edge → returned ALL types incl. generic
  `HarnessComponent`. The old workaround stripped `HO.HarnessComponent` locally in each
  consumer (didn't generalise to intermediate classes Role/Channel/Candidate). Central
  fix (2026-07): guard the self-edge in `lib.most_specific_types` — `if sup != t:
  specific.discard(sup)`. Now it returns the concrete subtype directly for ALL consumers
  (retrieve/webui/validate-dedup/materialize). `_component_type` simplified to
  `types[0]` (list is IRI-sorted → deterministic tie-break). Materialize tree stays
  byte-identical for Tool/Role (already correct via old strip). VERIFIED no regression.
- **Latent gap the fix EXPOSED, then RESOLVED — `HO.Channel` was absent from
  `lib.INSTANCE_CLASSES`** (ontology_lib.py ~L55-60). `most_specific_types` only considers
  types in that set, so channel nodes resolved to `HarnessComponent` (Channel type never
  collected); the reflexive fix alone did NOT make channels concrete. Fixed (orchestrator-
  authorized) by adding `HO.Channel` to `INSTANCE_CLASSES` (one line). Effect: retrieve/webui/
  materialize now show `['Channel']`. It CHANGES materialize `components[].type` for channels
  (HarnessComponent→Channel) — this is the INTENDED correction, not a regression; the
  byte-identical clause becomes "byte-identical except the 3 corrected channel type strings"
  (verified: `diff -r` vs pre-fix baseline = exactly those 3 lines; determinism 2-run identical).
  Does NOT touch validate count/reachability(96)/SHACL — channels were already counted via
  HarnessComponent membership, so INSTANCE_CLASSES membership doesn't change the reachable set.
  **Audit method to catch such gaps**: enumerate `owl:Class` in the `ho:` ns, for each check
  `in INSTANCE_CLASSES` vs `subClassOf HarnessComponent` vs instance-count; any subClassOf-HC
  class with instances not in the set is missing. As of this fix Channel was the ONLY one
  (Role/Candidate already present; abstract/zero-instance ones don't matter).
- **Determinism**: sort every multi-valued predicate by IRI (`sorted(nodes, key=str)`),
  `json.dump(..., sort_keys=True)`, no timestamps in content → run twice = byte-identical
  (`diff -r`). languageCondition bullets also sorted.

## `ho:artifactTemplate` (P2 vocab add)
- TBox datatype property, `rdfs:domain ho:HarnessComponent`, `rdfs:range xsd:string`,
  value = repo-relative template-fragment path. Style modeled on `ho:promptText`.
  No `sh:closed` in shapes → safe to add without touching shapes (verify first).
- **Fallback semantics**: property ABSENT ⇒ render section from graph data; property
  present but file missing ⇒ HARD ERROR (misconfig). Substitution is minimal string
  replace: `{{prefLabel}}`/`{{promptText}}`/`{{definition}}` from the node's graph data.
- **Path resolution** (first existing wins): (1) ontology repo root `lib.ROOT`,
  (2) `dirname(HARNESS_CATALOG)` = recipe repo root (so a recipe ships its own fragments).
- **Central stays neutral**: wire the `ho:artifactTemplate` ref onto the RECIPE node
  (techdoc.ttl `id:sp-techdoc`), pointing at a neutral reusable fragment in
  `tools/materialize_templates/` (a tool asset, not an ontology part).

## Demo compose without a central clone
The staging recipe catalog points at `central/` (needs a clone). For a quick demo,
write a scratch catalog mapping the central IRIs + recipe IRI to ABSOLUTE real repo
paths, set `HARNESS_CATALOG`/`HARNESS_ROOT_ONTOLOGY`, run. Central validate stays
64 individuals on both loader paths (glob only scans `ontology/`, not staging).
