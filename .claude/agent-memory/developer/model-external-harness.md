# Modeling an EXTERNAL agent harness into the ABox

Pattern for turning a real-world multi-agent/design harness (a repo's CLAUDE.md +
`.claude/agents/*` + tools) into `ontology/abox/*.ttl` individuals.

## What maps to what
- persona / CLAUDE.md governance voice → **1 SystemPrompt** (`sp-`, needs promptText + tokenEstimate).
- `.claude/agents/*` role split (orchestrator/dev/vnv/inspection) → the harness's
  **control-flow character**: a `Workflow` (`wf-`, derivedFrom `wf-planexec`) + a
  `DesignPattern`. `orchestrator-workers` is a canonical DesignPattern named in the
  TBox class definition, so authoring `pat-orchestrator-workers` is reuse, not drift.
- `.claude/agents/*` frontmatter `model:` → pick the matching `ModelConfig` (source
  declared `sonnet` → reuse `mc-sonnet`). Be faithful to the source, not to our own
  dispatch tier.
- each real tool/script → a `Tool` (`tool-`) with `providesCapability`. Domain tools
  with no existing capability get a NEW `cap-` (e.g. design-graph mgmt, simulation).
- CLAUDE.md design rules → distinct **Guardrails** (one policy each): verify-then-proceed,
  design-for-loss, traceability/no-delete, no-arbitrary-decision. REUSE `gr-lang` for
  the Korean/English policy (same policy as our repo's `id:gr-lang`).

## Gotchas / gates (all enforced by validate.py)
- Every harness `requiresCapability` X MUST have one of ITS components `providesCapability` X
  (`check_capability_satisfaction`). Only require caps you also wire a provider for.
- Reachability BFS is from Harness nodes, undirected, over `INSTANCE_LINK_PREDICATES`
  (incl. skos:broader/related, NOT topConceptOf — scheme isn't an instance). Make every
  new Concept the object of at least one `ho:tagged` OR chain it via `skos:broader` to a
  concept that is tagged. topConceptOf alone does NOT make a concept reachable.
- ConceptConnectivityShape: a top concept with no broader needs a narrower (something
  `skos:broader` it) or a tag or `skos:related` — otherwise SHACL flags it.
- prefLabel must be unique per class (case-folded) — `check_duplicates`. Diff against seed labels.
- Text-bearing nodes (SystemPrompt/Guardrail promptText, Tool/Workflow) need `ho:tokenEstimate`.
- Avoid apostrophes-as-quote issues: write plain ASCII in promptText; `--` reads fine.
- Write a NEW file under `ontology/abox/` (validate globs `ontology/**`); never rewrite seed.ttl.
