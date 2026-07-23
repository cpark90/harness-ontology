# Authoring a corpus recipe (harness-100 inc3 pilot: 21-code-reviewer)

Recipe-local blueprint (0 new central nodes) mirroring an external multi-agent harness.
Format template = lpranging.ttl. 15 local nodes: harness1 + role4 + persona5 (sp-<name> +
sp-role×4) + concept2 + instruction3. Reused ~24 core: IRIs by binding only.

## Load-bearing facts confirmed by materialize round-trip
- **Worker persona = short promptText INLINE + full body via `ho:artifactTemplate`.**
  materialize P4 role emitter (`_render_roles`→`render_component`) FETCHES the persona's
  artifactTemplate source and renders `.claude/agents/<role>.md` = graph-authored
  frontmatter/heading + fetched source body. So the file is NOT byte-identical to the raw
  corpus agent md (it prepends graph frontmatter) but the source body IS faithfully present.
  Set persona `ho:tokenEstimate` to the INLINE promptText size (retrieve budget), not the
  fetched body — matches lpranging convention. Skills (`ins-*` artifactTemplate) emit a
  BYTE-IDENTICAL `.claude/skills/<name>/SKILL.md` copy; tokenEstimate = skill body `wc -w`.
- **promote-once via reused role satisfies a required capability.** Bind the corpus QA/gate
  agent (review-synthesizer) as `core:role-synthesizer` on `hasRole` (NOT a local role) →
  it provides `core:cap-synthesis`, satisfying harness `requiresCapability cap-synthesis`
  (Role rolls up under hasComponent). It emits `.claude/agents/synthesizer.md` rendered from
  graph (no artifactTemplate). Proven: 5 agents emitted = 4 local + 1 reused synthesizer.
- **Both coordination topologies co-declared.** `appliesPattern pat-orchestrator-workers,
  pat-peer-mesh` + `hasChannel chan-workspace, chan-peer, chan-agent-user` — orchestrator/
  dispatch doctrine AND analysts' SendMessage mesh both present, no conflict.
- **Extending skill → target agent in `skos:definition`** ("TARGET AGENT: <name>") since
  GAP-5 `augmentsRole` not yet in TBox; bound at harness level via `hasInstruction`.

## Validation GOTCHA (staging recipe)
- Staging `catalog-v001.xml` uri paths are `central/ontology/...` RELATIVE TO THE CATALOG
  DIR. Running `validate.py` from repo root with `HARNESS_CATALOG=staging/.../catalog.xml`
  FAILS (central/ unresolved → tools/roles look untyped, cap unsatisfied). Correct: create
  `staging/harness-recipes/central` symlink → repo root, `cd` into staging dir, run
  `central/tools/validate.py`. Symlink + whole `/staging/` is gitignored (leave symlink for vnv).
- Self-check gate: working-tree union (central @126 + recipe 15 = 141 individuals) PASS;
  materialize 2 runs `diff -r` IDENTICAL (deterministic); stub test = repoint one ref to
  nonexistent abs path → `.ref` stub emitted, exit 0, other refs still resolved.
- retrieve "⚠ <cap> required but no provider retrieved" for cap-synthesis is a BUDGET
  artifact (provider role not pulled into the small pack), NOT a validation gap — validate.py
  already confirms capability satisfaction. New harness surfaces as TOP base candidate.

## Flag carried to orchestrator
- artifactTemplate/dct:source use TEMPORARY scratchpad abs paths (528b6512.../scratchpad/
  harness-100/en/21-code-reviewer). Ephemeral — persistent corpus path must be confirmed and
  substituted before finalize/push. Flagged in recipe header comment + README top warning.
