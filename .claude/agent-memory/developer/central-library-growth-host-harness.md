# Promoting recurring neutral parts to central library + anti-orphan host harness

harness-100 augmentation inc2 (central-library growth, before recipe import). Promote-once the
parts that recur across the corpus so recipes REUSE by IRI instead of 100x duplication.

## What was promoted (roadmap §2)
- Capability `core:cap-synthesis` (capabilities.ttl).
- Role `core:role-synthesizer` (roles.ttl): terminal convergence gate — cross-checks every worker
  deliverable AND compiles integrated final result. Broader than role-vnv (which only judges).
  `ho:providesCapability cap-synthesis` (Role ⊑ HarnessComponent, so providesCapability domain OK).
  roleTool tool-editor, roleGuardrail reuse + gr-structured-output, tagged c-multiagent + c-synthesis.
- Channel `core:chan-workspace` (channels.ttl): shared file workspace hand-off; participants = worker
  roles + synthesizer; involvesUser false; channelMedium string. No tokenEstimate (Channel has only
  definition, no promptText — same as other chan-*).
- Guardrails (guardrails.ttl) `gr-structured-output` / `gr-scale-modes` / `gr-graceful-fallback`:
  each promptText + tokenEstimate + maturity reviewed + tagged its paired new concept.
- Concepts (concepts.ttl): c-synthesis + c-scale-modes broader c-multiagent; c-structured-output
  broader c-communication; c-graceful-fallback broader c-agent-methodology. Each guardrail tags its own
  fine concept (convention: gr-* tags c-* one-to-one, not the top concept).

## Anti-orphan WITHOUT breaking h-multiagent byte-identical (the key move)
- New Role/Channel/Guardrail ⊑ HarnessComponent → MUST be reachable from a Harness or SHACL orphan-FAIL.
- DO NOT wire them into `h-multiagent` — that changes its emitted CLAUDE.md (inc1 lesson).
- Author a dedicated NEUTRAL library host harness `core:h-workspace-synthesis` (derivedFrom h-multiagent,
  maturity draft) that binds all the new parts, mirroring how `h-peer-mesh` hosts chan-peer. Chose a
  dedicated host over reusing h-peer-mesh (keeps h-peer-mesh's peer-mesh focus clean; the new parts are a
  distinct neutral bundle = the corpus template neutralized).
- **Capability satisfaction via a Role**: host `requiresCapability cap-synthesis`; bound `role-synthesizer`
  `providesCapability cap-synthesis`. validate.check_capability_satisfaction iterates reasoned
  `hasComponent` (hasRole rolls up under OWL RL), so a hasRole-bound role's providesCapability satisfies the
  host. cap must also be required OR provided (CapabilityConnectivityShape) → both ends present. GREEN.
- Host binds all chan-workspace channelParticipant roles via hasRole (mirrors h-peer-mesh binding chan-peer
  participants) and usesTool tool-editor (because role-synthesizer roleTool tool-editor — convention:
  roleTool/roleGuardrail point at parts the harness binds via usesTool/hasGuardrail).

## Gotchas / confirmations
- Added ZERO new files (appended to existing core/*.ttl) → no catalog/root wiring needed; both loaders
  (catalog vs HARNESS_CATALOG=/nonexistent glob) auto-parity: 126 individuals / 1333 triples identical.
- Byte-identical: baseline-materialize h-multiagent BEFORE edits, diff after → CLAUDE.md IDENTICAL (only
  NEW nodes added, no existing node's def/prefLabel touched; new parts hosted elsewhere so h-multiagent's
  hasComponent closure unchanged). Host materializes cleanly (23 comps, 6 roles, 1 chan, 1 cap binding) +
  deterministic on rebuild. Assembly: host declares no hasAssemblySection → inherits default holder.
- retrieve "synthesizer workspace structured output scale modes fallback" → host is TOP base candidate
  (6.3); all new parts surface with provides/requires Synthesis shown; distinctive (no lexical collision).
- count delta +11 (1 cap +1 role +1 chan +3 gr +4 concept +1 harness): 115→126.

## What pilot increment 3 still needs (not done here — later increment)
- GAP-2..5 leaves (e.g. GAP-5 augmentsRole for agent-targeted skills; task-DAG deliverable leaves).
- per-recipe attribution (dct:source / dct:license "Apache-2.0", NOTICE credit).
- retrieve-seed distinctiveness across ~100 near-identical orchestrator-workers (prefLabel/def + domain/task
  edges must stay distinctive; wave-by-wave retrieve spot checks).
