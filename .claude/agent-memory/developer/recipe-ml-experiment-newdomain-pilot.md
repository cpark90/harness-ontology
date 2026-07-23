# Authoring corpus recipe 31-ml-experiment (inc3 pilot: NEW local domain+task)

Recipe-local blueprint (0 new central nodes) mirroring corpus harness 31-ml-experiment.
20 local nodes: harness1 + domain1 + task1 + concept4 + persona5 (sp-<name> + sp-role×4)
+ role4 + instruction4. Reuses ~24 core: IRIs by binding only. Validate PASS = 146
individuals (central 126 + local 20). Same template as 21-code-reviewer; deltas below.

## New-vocabulary decisions (Golden Rule #2: local only, connected)
- **New local Domain `id:dom-ml`** ("Machine-learning experimentation") because central
  `dom-research` = literature/citation survey, NOT a hands-on train-and-evaluate empirical
  lifecycle. Distinct. Flagged for central promotion if corpus batch recurs.
- **New local Task `id:task-mlexperiment`** — no central task fits an empirical
  measure-and-compare workflow (`task-architecture` = define system structure/interfaces).
  Flagged. Both dom+task are ho:maturity "draft", recipe-local.
- **Concept sub-tree = 4 not 3**: brief said "3 (feature/model/eval)" but a rooted tree
  needs a local TOP (no central ML concept to hang under, unlike 21 which used core:c-softeng).
  So `id:c-mlexperiment` topConceptOf core:scheme + 3 leaves (c-feature-engineering,
  c-model-development, c-model-evaluation) skos:broader it. lpranging c-* pattern. Defensible.
- **experiment-reviewer = core:role-synthesizer REUSE** (promote-once): QA gate that
  cross-validates all stages + compiles final report + bounded rework = clean synthesizer fit,
  NOT ambiguous. Satisfies requiresCapability cap-synthesis. Emits synthesizer.md from graph.

## Skill extension targets (4 skills; recorded in skos:definition, GAP-5 not in TBox)
Read the ORCHESTRATOR skill's "Agent Extension Skills" table for authoritative targets:
feature-engineering-cookbook→data-engineer; model-selection-guide→model-designer+evaluation-analyst;
experiment-tracking-setup→training-manager. ins-ml-experiment=orchestrator entry.
gr-scale-modes ADDED (skill has explicit "Scale-Based Modes" table full/data/model/eval/review).
pat-peer-mesh+chan-peer included (skill: "5 members communicate directly via SendMessage").

## ★ NEW load-bearing finding: persona artifactTemplate does NOT stub — it HARD-FAILS
Confirmed by stub test on THIS recipe: skill artifactTemplate absent → graceful `.ref` stub,
exit 0 (emit_instructions uses `_resolve_ref_path`). But PERSONA artifactTemplate absent →
`materialize.py` RAISES FileNotFoundError (render_component → resolve_template path, line ~129),
exit 2, whole build aborts. So the two ref kinds are ASYMMETRIC: skills degrade, personas block.
Consequence: once scratchpad clears, `materialize h-<name>` HARD-FAILS on first unresolved
persona (not merely fidelity loss). This strengthens the "substitute persistent source path"
flag into a BUILD BLOCKER. Existing central materialize behavior (out of recipe scope) — flag,
don't fix. (My earlier recipe-authoring memory only claimed impl/scaffold/skill stub — never
persona; consistent, now proven.)

## Validation setup (dedicated catalog to avoid shared-catalog race)
Brief mandated a PER-RECIPE catalog copy `catalog-31-ml-experiment.xml` (= catalog-v001.xml +
one <uri> line) so parallel sibling recipes don't collide on shared catalog-v001.xml.
`ln -sfn <repo-root> staging/harness-recipes/central`, cd into staging, run
`central/tools/validate.py` with HARNESS_CATALOG=catalog-31-ml-experiment.xml. materialize
--out is REQUIRED (no default -o). 2 runs diff -r IDENTICAL. staging/ + symlink + dedicated
catalog all gitignored (leave for vnv). Shared catalog line reported as string, NOT edited.

## Shared catalog line to add at finalize (string only, inspection applies)
    <uri id="recipe-31-ml-experiment" name="https://harness-ontology.dev/recipes/31-ml-experiment" uri="recipes/31-ml-experiment/31-ml-experiment.ttl"/>
