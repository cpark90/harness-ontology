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
- **`most_specific_types` quirk (shared lib, do NOT edit)**: OWL RL makes
  `rdfs:subClassOf` reflexive (Tool subClassOf Tool), which defeats the
  superclass-drop in `lib.most_specific_types` → it returns BOTH the subtype and
  generic `HarnessComponent`, `sorted()` alphabetically (Guardrail<HarnessComponent<
  ModelConfig/SystemPrompt/Tool/Workflow) so `types[0]` picks HarnessComponent for
  most. Fix LOCALLY in the consumer: drop `HO.HarnessComponent` from the list when a
  concrete subtype is present. retrieve depends on current lib behavior — leave lib alone.
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
