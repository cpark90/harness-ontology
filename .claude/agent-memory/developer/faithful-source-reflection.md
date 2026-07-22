# Faithful reflection of a REAL source harness into a recipe

When a recipe must FAITHFULLY mirror an actual source harness (not showcase
mechanisms), audit every artifact against source and strip synthetic demo
content. "Faithfulness to source > showcasing mechanisms — use a mechanism only
where the source genuinely has it."

## Audit method (lpranging worked example)
- **Provenance-check every impl/scaffold file**: `cmp` vendored files to source;
  `find <source> -name '<file>'` to prove a candidate is synthetic (docgraph_v2.py
  existed nowhere in source → synthetic demo → removed with its `ho:Candidate`).
- **BIND candidates collapse to a single direct ref when source has ONE impl**:
  drop `ho:Candidate`/`implementationCandidate`/`selectionPolicy`/`candidateVersion`,
  put `ho:implementationRef "recipes/<n>/impl/<file>.py"` directly on the Tool.
  Direct-ref tool → materialize keeps source basename (docgraph.py). Removing 2
  candidates dropped union 83→81 (candidates are ⊑HarnessComponent, counted).
- **Scaffold: templated `{{prefLabel}}` stubs are NOT faithful**. The demo shipped
  a `DESIGN_HARNESS_STANDARD.md` stub with `{{prefLabel}}`/`{{definition}}` +
  a synthetic `docs/README.md` (referenced `docs/decisions/` the source lacked;
  source has no top-level `docs/README.md`). Fix = vendor the REAL standard docs
  byte-identical. materialize `render_from_template` only replaces the 3 `{{}}`
  tokens then `rstrip("\n")`+re-add one `\n`; real docs with exactly one trailing
  newline emit **byte-identical** (verify with `od -An -c | tail -c1`).
  Chosen scaffold = real DESIGN_HARNESS_STANDARD.md + CODESTYLE.md + docs/ONTOLOGY.md
  (methodology docs the harness ships), all `cmp`-identical post-materialize.
- **Tool location ≠ tools/**: a real "tool" may live in `reference/` (source's
  `sim_grid_reservation.py` is graph-external reference code, not `tools/`). Point
  `implementationRef` at what you vendor; `cmp` the vendored copy to the REAL path
  (reference/…), not an assumed tools/ path.
- **Roles = one per REAL `.claude/agents/*` entry** (here developer/vnv/inspection;
  orchestrator = main agent = top-level CLAUDE.md persona, no agent file). Verify
  materialized `.claude/agents/` == source `ls`, and persona/roleTool/roleGuardrail/
  roleMemoryPolicy reflect each real agent file.

## Lock decision (ODR §4-③) — remove when no candidates remain
A vendored `harness.lock.json` exists to reproduce a *candidate selection*. With
every tool a single direct-ref impl, the vendored `impl/` file already IS the
pinned content → lock adds no reproducibility value → **remove the vendored lock**
(keeping a stale one referencing removed candidates/old individualCount is
unfaithful). Determinism is still proved by two no-lock materialize runs
(`diff -r` identical). materialize still WRITES a fresh lock into the *output*
tree (build artifact in scratch) — that's central-tool behavior, not vendored.

## Gate recipe (consolidation dispatch, no git, central untouched)
central `validate.py` PASS at 64 unchanged + `grep ontology/abox/core/` for
domain/role terms = 0 (never edit core); temp `central` symlink→repo root at
staging catalog root → env-catalog `validate.py` (union PASS 81) + `materialize.py
h-lpranging --out <scratch>` → `cmp` tools/scaffold to source + `diff -r` two runs
→ `rm` symlink. grep `"/` on implementationRef/scaffold lines = 0 (repo-relative).
