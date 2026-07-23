# SystemPrompt decomposition — PromptSection + 4th hasComponent propertyChain (Stage b)

finer-harness-decomposition-assembly Stage (b): decompose a blob `ho:SystemPrompt`
into ordered composable `ho:PromptSection`s; materialize composes the Persona from
them in order. Exact analogue of Stage (a) WorkflowStep.

## TBox vocab (central, neutral)
- `ho:PromptSection ⊑ HarnessComponent`.
- `ho:hasSection` SystemPrompt→PromptSection, **plain object prop (NOT ⊑ hasComponent)**.
- `ho:sectionOrder` PromptSection→xsd:integer (1-based; total order for determinism).
- section text via `ho:promptText` (REUSE, no new datatype prop).

## ★ Reachability = 4th propertyChainAxiom on hasComponent (2-link, like hasStep)
Add `ho:hasComponent owl:propertyChainAxiom ( ho:hasComponent ho:hasSection )`.
→ harness hasComponent systemPrompt (holds because `ho:hasSystemPrompt` IS already
  `⊑ ho:hasComponent`) ∧ systemPrompt hasSection section ⟹ harness hasComponent section.
  So it's the SAME 2-link chain shape as hasStep (NOT the 3-link Contract chain) —
  the first link is already inferred by the hasSystemPrompt sub-property. Subject stays
  Harness → section orphan-free, no bespoke shape. **Do NOT make hasSection ⊑ hasComponent**
  (hasComponent domain=Harness would mistype the SystemPrompt subject as Harness → HarnessShape trip).
- FOUR propertyChainAxiom now coexist on hasComponent (implementationCandidate, contract,
  hasStep, hasSection); owlrl prp-spo2 applies each independently (verified: all 4 roll up).
- ontology_lib: `HO.PromptSection`→INSTANCE_CLASSES; `HO.hasSection`→INSTANCE_LINK_PREDICATES.
- probe: each section (h hasComponent section)==True, typed PromptSection, sp NOT typed Harness.

## ABox (central core/system-prompts.ttl)
3 sections decomposing `sp-methodical` (ps-methodical-decisions/error/escalate), sectionOrder
1/2/3, each prefLabel+definition+promptText fragment+tokenEstimate+maturity "reviewed". Wire
`sp-methodical ho:hasSection …` (predicate order: assembly edge BEFORE data promptText).
**KEEP sp-methodical's blob promptText** — sections refine/compose it; section-less SystemPrompt
must still render from its blob. prefLabels unique within PromptSection class.

## materialize Persona (tools/materialize.py)
`_prompt_sections(g,sp)` = sorted by (sectionOrder, IRI), mirroring `_workflow_steps`. In the
build_claude_md Persona loop: if sp has sections, `fallback = "\n\n".join(fragment promptTexts
in order)` (paragraph per section); else blob promptText as before. Then render_component (so
artifactTemplate still overrides if present — unchanged mechanism). Deterministic; two runs
diff -r IDENTICAL. Section-less prompt (sp-research/h-research) Persona UNCHANGED (no regression).
Do NOT touch fixed section ORDER of CLAUDE.md doc (that's Stage c). individuals 99→102.
