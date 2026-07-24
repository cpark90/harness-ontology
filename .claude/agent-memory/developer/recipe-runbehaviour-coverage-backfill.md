# Recipe run-behaviour coverage backfill (execMode / TestScenario / FailurePolicy)

Backfilled 8 staging recipes that had 0 of the three run-behaviour axes while sources
provided them (coverage-audit miss, not a vocab GAP). Reusable facts:

## Wiring (all recipe-local nodes are `id:`, central reuse is `core:`)
- Bind on the **harness node** (all three are Harness-direct): `ho:hasExecutionMode`
  (→ExecutionMode, NOT ⊑hasComponent), `ho:hasTestScenario`/`ho:hasFailurePolicy`
  (⊑hasComponent, so bound scenarios/policies are auto reachable — no host/rollup needed).
- Recipe harnesses declare no `hasAssemblySection`, so materialize uses the central
  DEFAULT_ASSEMBLY_HOLDER order which already carries execution-mode/data-flow/
  error-handling/test-scenarios sections → the 3 sections render automatically once
  data is present. Renderers early-return empty when the harness has no such parts,
  so a recipe with 0 fixtures emits nothing (no error).

## Shape minimums (harness-shapes.ttl)
- TestScenario: exactly one `ho:scenarioKind` from closed set
  {normal, existing-input, error, trigger-positive, trigger-negative}, ≥1
  `ho:scenarioPrompt`. `scenarioExpected`/`scenarioReferences` optional. +prefLabel
  (unique in-class **within the per-recipe closure only** — different recipes never
  share a closure, so scenario prefLabels may repeat across recipes).
- FailurePolicy: ≥1 `ho:failureCondition` + ≥1 `ho:recoveryStrategy`. +prefLabel.
- Both carry text → add `ho:tokenEstimate` (style).

## Corpus source extraction (harness-100 en/<n>/.claude)
- The rich axes live in the **orchestrator skill.md** (`skills/<name-without-number>/`),
  NOT in the thin CLAUDE.md. Sections: `## Execution Mode` (always "Agent Team" →
  `core:mode-agent-teams`), `## Test Scenarios` (3 headings Normal/Existing-File/Error
  → scenarioKind normal/existing-input/error **by heading position**, prompt+expected
  recipe-local), `## Error Handling` (condition→strategy table).
- FailurePolicy mapping: reuse central `core:fp-*` archetypes by IRI, author id:fp-*
  LOCALLY only for genuinely domain-specific rows (code: language-detect, large-codebase,
  build-error; ML: no-dataset, no-gpu, training-divergence). NEVER duplicate a central
  row locally (that is the drift). Central archetype coverage of corpus error tables:
  agent-failure→fp-agent-failure-retry, insufficient/ambiguous-input & default-fallback→
  fp-insufficient-input (often 2 source rows→1 archetype), review-🔴→fp-review-critical-rework,
  external-source-fail→fp-source-unavailable, contradiction→fp-conflict-contradiction.

## Group B (self recipes) — do NOT mechanically apply corpus yardstick
- lpranging = cold-start dispatch design harness (orchestrator + short-lived
  developer/vnv, inspection separate session) → `core:mode-sub-agents` (the mode its
  lineage h-multiagent runs in), NOT agent-teams. Its explicit verify-then-proceed +
  validation-gate discipline == central methodology archetype `core:fp-validation-fail`
  (reuse by IRI). No behaviour TestScenario: acceptance is structural (validate.py),
  nearer ho:Contract → explicit accepted coverage-audit reason.
- techdoc/contract-demo = synthetic single-agent plan-execute, no real source → declare
  NO run-behaviour axes; record the accepted reason as an in-recipe comment. Fabrication
  is worse than under-reflection.

## Gate
- per-recipe closure: `HARNESS_CATALOG=staging/harness-recipes/catalog-v001.xml
  HARNESS_ROOT_ONTOLOGY=.../recipes/<n>` (recipe IRI, not dir). Central materialize
  (unset those env) stays byte-identical since only recipe files change — 44 files
  across 7 central harnesses unchanged, proving central no-regression.
