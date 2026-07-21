# Decomposing governance docs into NEUTRAL reusable parts (not a domain harness)

Correction learned in the lpranging rework: the ontology is a **library of
generalized, domain-INDEPENDENT reusable PARTS** decomposed from harness
governance docs — NOT a store of one specific harness's description. Harness
construction happens later by assembling these neutral parts. Storing a
domain-coupled harness instance (UWB/RTLS/low-power domain, docgraph/simulator
tools, a domain persona) is the modeling error to avoid.

## How to decompose (source doc -> ho: part)
- Each distinct **design rule / policy** in CLAUDE.md / CODESTYLE / a design
  STANDARD -> one `Guardrail` (single responsibility). From these docs the
  reusable, domain-free set was: verify-then-proceed, design-for-loss,
  traceability(SSoT+increment-ids), grounding(link-to-rationale), no-arbitrary-
  decision(escalate), least-privilege role boundaries, report-over-prompt,
  controlled-vocabulary(anti-drift), root-cause-over-symptom, simplicity/YAGNI.
  REUSE existing `gr-lang` for the language policy — do not re-author it.
- role split (orchestrator/workers) -> `DesignPattern pat-orchestrator-workers`
  (canonical, named in TBox class def = reuse not drift) + a `Workflow`
  wf-multiagent (`derivedFrom wf-planexec`, `providesCapability cap-orchestration`).
  STRIP any `dependsOn` on a domain tool when neutralizing.
- methodology voice -> ONE neutral `SystemPrompt` (drop every domain noun:
  UWB/RTLS/ranging/low-power). Keep only domain-free methodology sentences.
- Capabilities: mint only when a component provides one AND the harness requires
  it (buildable pairing). Here: cap-orchestration (wf provides), cap-traceability
  (gr-traceability provides). Concept tags reused: c-safety, c-communication,
  c-autonomy; kept-neutral: c-multiagent, c-traceability; new: c-design.

## The anti-orphan tension (important)
Even a "library of parts" must satisfy the SHACL shapes: every HarnessComponent
needs `hasComponent` from >=1 Harness, and reachability BFS starts at Harness
nodes. So neutral parts CANNOT float free — wire them into ONE **neutral,
domain-independent** harness (h-multiagent) that names no problem domain/tool/
tech. This is legitimate (mirrors seed's generic h-coding/h-research examples),
not a re-introduction of a domain harness. Its `targetsDomain` needs a neutral
Domain (dom-design "Design engineering", a broad problem area like coding/
research), and >=1 Task (HarnessShape minimums).

## Placement
Append to `ontology/abox/seed.ttl` (the `core` data unit, `id: -> .../id/core/`)
under a `####` banner — no new data-unit plumbing (catalog/root/imports) needed.
Everything is `id:` (you are inside the core file); reference existing seed nodes
directly (`id:mc-opus`, `id:c-safety`, `id:scheme`). Do NOT resurrect deleted
domain files or add `core:` prefixes (that's for separate domain files only).

## Retiring a domain split (federation infra stays)
When retiring a domain pilot: catalog + root `owl:imports` keep the D1/D3 infra
but drop the domain data-unit entry; rewrite the NOTE from "split EXECUTED /
externalized" to "no active external data repo; infra available for future
domain part-collections; the domain modeling was retired per neutral-parts."
Delete `staging/<domain>-data-repo/` (durable payload). In federation-design.md,
genericize the worked-example + full-union recipe to `<domain>` placeholders.
grep-clean gate is about NODES (label/definition/id) — NOTE **comments** that
document the retirement are allowed and expected (grep `-vE '^\s*#'` to prove
nodes are clean). Both loader paths must still agree (imports == glob triples).

## V&V follow-ups on the neutral set (2 more parts)
- Missing neutral guardrail found in review: **bounded-context / anti-context-rot**
  (`gr-bounded-context`, prefLabel "Bounded context projection", altLabel
  "anti-context-rot"). It is CLAUDE.md golden-rule #1 stated domain-free: never
  ingest the whole store, retrieve only a request-scoped budget-capped projection,
  keep working context bounded. Tag `c-safety`, wire into h-multiagent hasGuardrail.
  Distinct from gr-controlled-vocabulary(anti-drift) — that is about vocabulary
  reuse, this is about context budget; do not conflate them.
- Neutral template must meet the CLAUDE.md prose harness minimum (SystemPrompt +
  Workflow + **tools** + guardrails + ModelConfig), not just SHACL. h-multiagent
  had no usesTool → bind the generic domain-neutral seed tools `id:tool-shell`,
  `id:tool-editor` (predicate order: usesTool sits between hasSystemPrompt and
  hasWorkflow). Adding matching `requiresCapability id:cap-codeexec, id:cap-fileedit`
  stays green because those tools already `providesCapability` them (mirrors
  h-coding). tool-websearch left off — not core to neutral orchestration.
