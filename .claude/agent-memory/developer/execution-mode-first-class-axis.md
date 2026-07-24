# Execution mode as a first-class Harness property (individual-enumerated axis)

Reversal of the earlier "D2 lightening" that carried runtime topology on
`ho:appliesPattern` + `tagged c-execution-mode`. That conflated two ORTHOGONAL
axes on one property, could not be queried directly, and stayed inert (0 harness
adopted the three `pat-*`, so the execution-mode section never rendered).

## The reusable design rule: enumerate the axis as INDIVIDUALS, not as an enum
"확장성 있게" for a value axis means **a new value = one more individual**:
`ho:ExecutionMode ⊑ ho:SpecConcept` (sibling of DesignPattern/Constraint, NOT a
HarnessComponent) + `ho:hasExecutionMode` (domain Harness, range ExecutionMode,
NOT ⊑hasComponent) + `EdgeTypingShape` `sh:path`/`sh:class` pair. Deliberately
NOT `ho:sectionKind`-style `sh:in` closed strings — that variant makes every new
value a shapes edit. Self-check before finishing: "what must change to add one
more value?" — if the answer names a shape/TBox/tool file, the design is wrong.
**Proven, not asserted**: scratch overlay (absolute-path catalog copy + scratch
root importing central root + scratch data unit) with a 4th mode `mode-swarm` in
a FOREIGN domain namespace and a scratch harness declaring it → validate PASS
(207) + `## Execution mode` rendered, with zero repo edits.

## Checklist a new non-component leaf class needs (beyond TBox+shape+ABox)
1. `ho:SpecConcept`'s definition ENUMERATES its leaves — add the new class there
   or the TBox lies (same trap as sectionKind enum vs prose).
2. `lib.INSTANCE_CLASSES` must gain it, otherwise the individuals are invisible
   to `instance_nodes` → not counted, not reachability-checked, not retrievable
   (HarnessComponent fallback does NOT apply: this class is not ⊑HC). The brief
   only listed `INSTANCE_LINK_PREDICATES`; the count gate (202→205) is what
   exposes the omission.
3. `INSTANCE_LINK_PREDICATES` += the new property (edge visibility / anti-orphan
   BFS). `retrieve.PREDICATE_WEIGHT` is optional — unknown predicates default to
   0.5 and the modes already surface at rel 3.6.
4. `ONTOLOGYSTYLE §2` prefix row (`ExecutionMode | mode- |`), placed next to the
   sibling class row.
5. Any ABox node whose definition DESCRIBES the old mechanism (here
   `as-execution-mode`'s "rendered from appliesPattern picks" and
   `c-execution-mode`'s "tag the DesignPatterns…") is stale prose — grep for the
   old mechanism words, not just the old IRIs.

## Deprecation instead of deletion (IDs are never reused)
`pat-agent-teams`/`pat-sub-agents`/`pat-hybrid` kept with `ho:maturity
"deprecated"` + a trailing "DEPRECATED: superseded by id:mode-… " sentence, and
their `ho:tagged c-execution-mode` retained so they stay connected (deprecating
does NOT exempt a node from reachability). They still appear in retrieve packs —
that is fine and desirable: the pack shows the supersession sentence.
Co-location: the modes live in `spec/patterns.ttl` (banner updated) rather than a
new unit, because a new unit costs root imports + root catalog + N recipe
catalogs; co-locate whenever the superseded nodes are in the same file.

## Document impact (expected, and how to bound it)
`hasExecutionMode` on a harness ADDS `## Execution mode` to its CLAUDE.md — an
intended feature change, but prove it is *only* that: baseline copies before the
edit, then `diff | grep -c '^<'` = 0 (h-multiagent/h-peer-mesh/h-harness-factory
each +6 lines, 0 deleted; h-workspace-synthesis untouched since it declares no
mode). MANIFEST.json stays byte-identical (a mode is not a component, so
`all_components` and its tokenEstimate do not move); only the lock's global
`individualCount` shifts 202→205. `ho:tokenEstimate` edits change neither
document — they only move retrieval budget admission.

## Which harness gets which mode (evidence, not defaults)
- `h-multiagent` → `mode-sub-agents`: definition says the orchestrator dispatches
  node-scoped briefs to workers and integrates results; `chan-dispatch` is
  literally "spawn/return of the subagent invocation".
- `h-peer-mesh` → `mode-agent-teams`: peers coordinate directly over `chan-peer`,
  no central dispatcher.
- `h-harness-factory` → `mode-hybrid`: topology differs BY PHASE — authoring runs
  as dispatch (`wf-multiagent`), while verify/evolution (`wf-verify-harness`,
  `wf-harness-evolution`) run as a standing team claiming work on the shared
  board (`chan-task-board`). Rationale left as a TTL comment, not in the
  `skos:definition`, so the CLAUDE.md diff stays the section alone.
- `h-workspace-synthesis` → `mode-sub-agents`. I first held this back as
  "topology-neutral channel, no pattern ⇒ no evidence"; orchestrator corrected
  the reasoning and the correction is the lesson: **`chan-workspace` is the
  HAND-OFF MEDIUM axis, not the SPAWN TOPOLOGY axis** — those are orthogonal, so
  a neutral channel does not imply an undetermined mode. Evidence that does
  decide it: `derivedFrom h-multiagent` (parent is sub-agents), `hasWorkflow
  wf-multiagent` (dispatch/reclaim control flow) and `role-synthesizer`'s
  definition saying "dispatch-invoked only" (a summoned role, not a standing
  peer). Generalise: when a harness declares no pattern, look at derivedFrom +
  workflow + the ROLES' invocation wording before concluding "no evidence".
- Left UNDECLARED: single-agent `h-coding`/`h-research`/`h-support` (the property
  is optional and they run no second agent).
