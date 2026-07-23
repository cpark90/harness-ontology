# Authoring a corpus recipe (harness-100 inc3 pilot: 16-fullstack-webapp)

Recipe-local blueprint (0 new central nodes) mirroring an external 5-agent harness.
Format template = 21-code-reviewer.ttl. 18 local nodes: harness1 + role5 + persona6
(sp-<name> + sp-role×5) + concept3 + instruction3. Reused core: IRIs by binding only.
Union = central 126 + 18 = 144 individuals, validate PASS.

## qa-engineer = LOCAL role (deviated from promote-once reuse) — DECISION CRITERION
- 21's review-synthesizer was a PURE terminal gate → reused core:role-synthesizer.
- 16's qa-engineer is a HYBRID: primarily a test-ENGINEERING worker (writes+runs
  Vitest/Playwright test code → needs tool-shell, rich distinct persona) that ALSO
  produces the convergence review report (06_review_report.md verdict + consistency
  matrix). Reusing role-synthesizer (roleTool editor-only, pure-convergence identity)
  would ERASE its shell scope + test-authoring identity + undercut the tool-scope test.
- So authored LOCAL `id:role-qa-engineer` (roleTool editor+shell, persona artifactTemplate
  → qa-engineer.md) and satisfied harness `requiresCapability core:cap-synthesis` via
  `ho:providesCapability core:cap-synthesis` on the LOCAL role — REUSE the capability
  IRI, invent no new cap (Golden Rule #2 intact). A local Role providing a core cap is
  legit + anti-orphan (cap already central/connected).
- RULE OF THUMB: corpus QA/gate agent → reuse role-synthesizer only if it's a PURE
  convergence gate (no distinct worker tooling/identity). If it's a worker+gate hybrid
  with a distinct tool scope, author local role + providesCapability core:cap-synthesis.
  Flag either way.

## Tool-scope variation (this recipe's test point) — DIFFERENT roleTool slices
- architect=editor; frontend=editor; backend=editor,shell; devops=shell,editor
  (shell-forward); qa=editor,shell. harness usesTool = union (editor,shell).
- Renders per-agent: materialized .claude/agents/<role>.md frontmatter/## Tools shows
  each slice (architect/frontend editor-only; backend/devops/qa editor+shell). Verified.
- Note: brief grouped frontend/backend as "editor 위주"; backend faithfully needs shell
  (ORM migrations/seed/dev server) so I gave it editor+shell (documented, minor deviation).

## ★ REF-RESOLUTION ASYMMETRY (crucial, corrects the recipe-references note)
- SKILL / implementationRef / scaffold artifactTemplate absent → `.ref` STUB, build exit 0
  (`_resolve_ref_path` + `_ref_stub`). Proven: skill ref → NO-SUCH → SKILL.md.ref, exit 0.
- **PERSONA (SystemPrompt) artifactTemplate absent → HARD-RAISES FileNotFoundError**
  (P2 render_component → render_from_template → resolve_template; UNCHANGED, does NOT stub).
  Proven: persona ref → DOES-NOT-EXIST → exit 1, no tree.
- Consequence for the ephemeral-scratchpad flag: re-pointing PERSONA refs to a persistent
  source is a BLOCKING build prerequisite (not graceful) — the ephemeral-path issue is
  more severe for personas than for skills. Flag this to orchestrator as cross-recipe.

## Self-check gate (shared-catalog write-race avoidance)
- Used DEDICATED `catalog-16-fullstack-webapp.xml` (copy of catalog-v001 + my recipe line
  only) + `staging/harness-recipes/central` symlink → repo root; ran `central/tools/validate.py`
  from staging dir with HARNESS_CATALOG/HARNESS_ROOT_ONTOLOGY env. Do NOT edit shared
  catalog-v001.xml — return the recipe <uri> line as a string for orchestrator to merge.
- GOTCHA: `--out` under session scratchpad got polluted mid-run by a concurrent parallel
  dispatch (newsletter agents appeared in my mat1). Redo determinism with FRESH back-to-back
  dirs (fs_a/fs_b) → diff -r IDENTICAL. Skills byte-identical to corpus (cmp), agent bodies
  contain fetched corpus content, 0 .ref stubs when source present.

## Flag carried to orchestrator
- Shared catalog line to add: `<uri id="recipe-16-fullstack-webapp" name=".../recipes/16-fullstack-webapp" uri="recipes/16-fullstack-webapp/16-fullstack-webapp.ttl"/>`.
- artifactTemplate/dct:source use TEMP scratchpad abs paths (528b6512.../en/16-fullstack-webapp);
  persistent path must be confirmed+substituted before finalize/push (BLOCKING for personas).
- qa-engineer local-role decision (above) — needs orchestrator ack on promote-once deviation.
