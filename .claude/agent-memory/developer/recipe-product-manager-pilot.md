# Recipe 46-product-manager (harness-100 inc3 pilot) — variation notes

Second corpus recipe after 21-code-reviewer; same lpranging/code-reviewer template.
20 local nodes: harness1 + domain1 + task1 + concept5(1 root+4 framework) + persona5
(sp-<name> + sp-role×4) + role4 + instruction3. Reused ~18 core: IRIs by binding only.
Validate PASS (union 146 individuals working-tree), materialize 2 runs IDENTICAL,
5 agents (4 local + reused synthesizer) · 3 skills(SKILL.md) · CLAUDE.md · MANIFEST · lock.

## New/confirmed load-bearing facts (delta vs code-reviewer)
- **NEW LOCAL DOMAIN + LOCAL TASK.** No core Task fits PM planning (task-architecture=
  system structure, task-codereview=change assessment) → authored id:task-productplanning
  locally + FLAG (promote to core only if reused). id:dom-product new local Domain
  (ho:salience). Golden Rule #2: both recipe-local, not core.
- **Framework concepts = variation point.** RICE / story-point are domain-methodology
  terms → recipe-local ho:Concept, NEVER neutral core. Anchored as 1 root
  c-product-management (skos:topConceptOf core:scheme) + 4 children skos:broader it
  (roadmap/prd/rice/story-point). Root-concept anchor mirrors lpranging c-sysdesign
  (brief said "3~4"; a clean SKOS tree needs the umbrella root, so 5 total — reported).
- **Least-privilege tool-scope variation (honest).** PM workers only author markdown →
  bind core:tool-editor ONLY (no tool-shell), requiresCapability cap-fileedit +
  cap-orchestration + cap-synthesis, DROP cap-codeexec. HarnessShape does NOT require
  codeexec → validate PASS. Every roleTool = tool-editor. This is the tool axis the
  pilot exercises (vs code-reviewer's editor+shell).
- **⚠ PERSONA artifactTemplate HARD-FAILS on absent; only skill/impl/scaffold STUB.**
  Persona (rolePersona→SystemPrompt) renders via render_component→resolve_template
  (materialize.py:529-532,124-130) which RAISES FileNotFoundError if source missing.
  Skill/tool-impl/scaffold refs use _resolve_ref_path+_ref_stub → .ref stub, exit 0.
  So stub-test a recipe by repointing a SKILL ref (not a persona ref). Consequence for
  the ephemeral-path flag: after scratchpad clears, materialize FAILS at persona step,
  not just stubs — re-pointing to persistent source is a hard build prerequisite.
- gr-scale-modes bound: the product-manager skill's "Execution Modes by Request Scope"
  table (Full/Strategy/PRD/Story/Sprint/Review) is textbook scale-modes; also tagged
  core:c-scale-modes. Both coordination topologies (pat-orchestrator-workers+peer-mesh,
  chan-workspace+peer+agent-user) since every agent has "Team Communication Protocol".

## Self-check gate (dedicated catalog, no shared-catalog edit)
- cp catalog-v001.xml catalog-46-product-manager.xml + add ONLY this recipe's <uri>
  line before </catalog>; symlink staging/harness-recipes/central → repo root; run
  central/tools/validate.py with HARNESS_CATALOG=that + HARNESS_ROOT_ONTOLOGY=.../46-product-manager.
- Shared catalog line to hand to inspection (NOT edited by developer):
  <uri id="recipe-46-product-manager" name="https://harness-ontology.dev/recipes/46-product-manager" uri="recipes/46-product-manager/46-product-manager.ttl"/>
