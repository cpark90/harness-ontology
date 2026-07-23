# Workflow decomposition — WorkflowStep + 3rd hasComponent propertyChain (Stage a)

finer-harness-decomposition-assembly Stage (a): decompose a coarse one-node
Workflow into ordered `ho:WorkflowStep`s with part-to-part assembly edges;
materialize renders the Process section from the steps in order.

## TBox vocab (central, neutral)
- `ho:WorkflowStep ⊑ HarnessComponent`.
- `ho:hasStep` Workflow→WorkflowStep, **plain object prop (NOT ⊑ hasComponent)**.
- `ho:stepOrder` WorkflowStep→xsd:integer (1-based; total order for determinism).
- assembly edges: `ho:stepUsesTool`→Tool, `ho:stepByRole`→Role, `ho:stepGuardedBy`→Guardrail
  (all domain WorkflowStep; point at parts the harness ALREADY binds — part-to-part).

## ★ Reachability = 3rd propertyChainAxiom on hasComponent (same trap as Candidate/Contract)
Add `ho:hasComponent owl:propertyChainAxiom ( ho:hasComponent ho:hasStep )`.
→ harness hasComponent workflow (via hasWorkflow⊑hasComponent) ∧ workflow hasStep step
  ⟹ harness hasComponent step. Subject stays Harness → step is orphan-free HarnessComponent,
  no bespoke shape. **Do NOT make hasStep ⊑ hasComponent** — hasComponent domain=Harness would
  (prp-dom) mistype the Workflow subject as Harness → HarnessShape trip. Must PREFIX with
  hasComponent (the chain's inferred subject is the first link's subject = harness).
- THREE propertyChainAxiom now coexist on hasComponent (implementationCandidate, contract, hasStep);
  owlrl prp-spo2 applies each independently (verified: 3 chains present, all roll up).
- ontology_lib: `HO.WorkflowStep`→INSTANCE_CLASSES; hasStep+stepUsesTool+stepByRole+stepGuardedBy
  →INSTANCE_LINK_PREDICATES (makes wf→step + step→part edges visible to retrieve/reachability views).
- probe: each step (h hasComponent step)==True, typed WorkflowStep, workflow NOT typed Harness.

## ABox (central core/workflows.ttl)
3 steps decomposing wf-multiagent (wfs-plan-dispatch/author-verify/integrate-gate), stepOrder 1/2/3,
each prefLabel+definition+tokenEstimate+maturity + 1–2 assembly edges reusing core IRIs
(role-orchestrator/developer, tool-editor, gr-delegated-orchestration/verify-proceed). Wire
`wf-multiagent ho:hasStep …` (all 3). Steps REFINE the workflow's prose definition — keep it.

## materialize Process section (tools/materialize.py)
`_workflow_steps(g,wf)` = sorted by (stepOrder, IRI) — total+deterministic. In build_claude_md
Process loop: after the one-line workflow bullet, if it has steps render each nested
`    - **N. label** — def` + `        - by role/uses tool/guarded by:` (scope IRI-sorted).
**Step-less workflow renders EXACTLY as before** (no regression); step-ful adds nested detail
(enhancement — Process content changes by design, NOT a determinism regression; two runs diff -r IDENTICAL).
Do NOT touch fixed section ORDER (that's Stage c). Stage b = SystemPrompt sections (later).
