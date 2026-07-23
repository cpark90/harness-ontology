# revfactory reflection Wave B1 — coordination/topology + governance guardrails

Wave B1 of revfactory reflection. File-exclusive: `concepts.ttl`+`patterns.ttl`+`channels.ttl`+`guardrails.ttl`.

## 저작 델타 (authored, correct in-boundary)
- concepts.ttl +4: `c-execution-mode`·`c-pattern-taxonomy`·`c-complexity-governance`(broader c-multiagent)
  + `c-skill-authoring`(broader c-agent-methodology; for gr-well-formed-skill & Wave B2 cap-skill).
- patterns.ttl +9 (maturity draft, tokenEstimate OMITTED to match siblings=definition-only):
  exec 3 tag c-execution-mode(pat-agent-teams/pat-sub-agents/pat-hybrid) + arch 6 tag c-pattern-taxonomy
  (pat-pipeline/pat-fanout-fanin/pat-expert-pool/pat-producer-reviewer/pat-supervisor/pat-hierarchical-delegation).
  pat-supervisor(DYNAMIC runtime alloc) vs pat-orchestrator-workers(STATIC pre-alloc) distinguished in def+altLabel.
- channels.ttl +1: `chan-task-board`(tag c-multiagent, maturity draft, channelParticipant=orchestrator+4 workers,
  involvesUser false, channelMedium "shared task board...", "4th hand-off medium").
- guardrails.ttl +13 (all promptText → tokenEstimate REQUIRED+present; maturity draft): 6 tag c-complexity-governance
  (gr-depth-limit/no-nested-teams/single-active-team/bottleneck-avoidance/flatten-hierarchy/bounded-iteration),
  + gr-integration-coherence(tag c-grounding; def states distinction from gr-grounding: fit-at-boundary vs link-to-rationale),
  gr-discriminating-eval, gr-single-responsibility(c-least-privilege), gr-generalize-not-overfit(c-design),
  gr-absolute-paths(c-multiagent), gr-well-formed-skill(c-skill-authoring), gr-opus-required(c-multiagent).

## ★★ CRITICAL GOTCHA: reachability-check ≠ SHACL orphan shape (plan finding WRONG)
Master plan claimed "신규 부품은 concept에 ho:tagged만 걸면 harness 참조 없이 reachable → Wave B1 harness wiring 불필요".
That is TRUE for the **reachability check** (weak-connectivity via INSTANCE_LINK_PREDICATES incl ho:tagged/skos:broader)
but FALSE for **SHACL `ho:ComponentConnectivityShape`** (targetClass `ho:HarnessComponent`, requires each to be object of
`hasComponent`/sub-property from a Harness). **Channel ⊑ HarnessComponent and Guardrail ⊑ HarnessComponent → they MUST be
hasChannel/hasGuardrail-wired into a Harness; a concept tag is NOT enough.** DesignPattern and Concept are NOT
HarnessComponents (appliesPattern/tagged are not hasComponent sub-props, no orphan shape) → patterns+concepts PASS on tags alone.
Result: 14 SHACL orphan violations = exactly the 13 new guardrails + chan-task-board. Patterns/concepts clean.

## → RESOLVED: dedicated host harness id:h-harness-factory (orchestrator granted harnesses.ttl)
Fix landed by adding a DEDICATED neutral host harness `id:h-harness-factory` in harnesses.ttl (mirrors
h-workspace-synthesis/h-peer-mesh library-host precedent), NOT h-multiagent (adding hasGuardrail/hasChannel to
h-multiagent breaks its byte-identical CLAUDE.md). It is a META-harness: subject = the methodology of building/verifying/
evolving harnesses (from revfactory/harness). Wiring: hasGuardrail gr-lang + all 13 new; hasChannel chan-task-board;
HarnessShape minimums reused by IRI (targetsDomain dom-design, addressesTask task-designdecision, hasSystemPrompt
sp-methodical, hasWorkflow wf-multiagent, usesTool tool-editor+tool-shell, usesModel mc-opus); appliesPattern
pat-orchestrator-workers (default). requiresCapability ONLY internally-provided: cap-orchestration(←wf-multiagent),
cap-fileedit(←tool-editor), cap-codeexec(←tool-shell) — cap-skill deliberately NOT required yet (provider = Wave B2).
derivedFrom h-multiagent, maturity draft, tagged c-multiagent/c-composition/c-agent-methodology. validate PASS, 158
individuals, SHACL orphan 0. Left room for Wave B2 (lifecycle workflows + cap-skill require) and Wave C (4 AssemblySections
+ demo hasTestScenario/hasFailurePolicy). RULE: Channel/Guardrail (⊑HC) authored in a wave that can't touch harnesses.ttl =
structural blocker; a host harness must be co-granted or the wave can't self-PASS. Do NOT weaken shapes, do NOT declare a
Harness inside a per-type non-harness file (violates split-core convention).

## concept reuse-vs-new decisions (flagged, not arbitrary)
Reused existing leaves: integration-coherence→c-grounding, single-responsibility→c-least-privilege,
generalize-not-overfit→c-design, absolute-paths & opus-required→c-multiagent, bounded-iteration→c-complexity-governance.
`gr-discriminating-eval` has NO apt existing leaf → tentatively tagged the generic parent `c-agent-methodology`; flagged for
orchestrator to decide whether to mint a dedicated leaf (file's established pattern is 1-concept-per-principle, but brief said
avoid proliferation). Created only the 4 concepts the brief mandated/needed.
