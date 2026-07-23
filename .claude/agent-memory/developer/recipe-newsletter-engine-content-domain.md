# Authoring corpus recipe 03-newsletter-engine (content domain, tool-scope variance)

Second harness-100 inc3 pilot. Recipe-local blueprint, 0 new central nodes,
format template = 21-code-reviewer.ttl / lpranging.ttl. 20 local nodes:
harness1 + dom1(dom-content) + task1(task-newsletter) + concept4(c-content root
topConceptOf core:scheme + curation/copywriting/deliverability broader) +
role4 + persona5(sp-<name> + sp-role×4) + instruction4. Reused ~22 core: IRIs.
Self-check: validate PASS (146 individuals = central 126 + 20), materialize
2-run IDENTICAL, all 4 skills byte-identical to corpus, skill stub → `.ref` exit0.

## Reusable facts confirmed here (beyond code-reviewer note)
- **QA-gate mapping when TWO review-flavoured agents exist.** Team had
  quality-reviewer AND editor-in-chief. Map the CROSS-VALIDATION/CONVERGENCE gate
  to core:role-synthesizer (quality-reviewer: cross-validate all deliverables,
  request rework, compile final integrated report — matches role-synthesizer def
  verbatim). The other, if it PRODUCES a new deliverable (editor-in-chief writes
  04_editorial_final.md, publish-ready version), stays a LOCAL worker role. Rule
  of thumb: synthesizer = terminal gate that judges+compiles; producing stage =
  local worker. Keeps 4 local + 1 reused = 5-agent team intact.
- **Tool scope varies per role & drives harness cap set.** curator/analyst use
  WebSearch/WebFetch → bound core:tool-websearch (provides cap-websearch);
  copywriter/editor edit-only. Source runs NO shell → did NOT bind tool-shell /
  cap-codeexec (unlike code-reviewer which had them). requiresCapability set is
  derived from the ACTUAL bound tools, not copied from the brief's reuse-map
  (map lists editor/shell as defaults; faithful reflection overrides). tool-websearch
  is a legit central REUSE (exists in core tools.ttl), not new-node — flagged since
  brief §1b reuse-map omitted it.
- **gr-scale-modes maps to a skill's "Scope-Based Modes" table** (full/copy/edit/
  analysis/review deploying different agent subsets) — bind it when the orchestrator
  skill has scope-based execution modes.
- **Local ho:Task when no central task fits.** task-newsletter (end-to-end build)
  had no core match → local id:task-newsletter, bound via addressesTask. Flag as new.
- **4 skills, 3 extending.** email-copywriting→copywriter, audience-segmentation→
  analyst+curator, deliverability-optimization→editor-in-chief+analyst; targets in
  skos:definition (GAP-5 augmentsRole not in TBox). tokenEstimate = skill body wc -w.
- **STUB test scope:** only SKILL artifactTemplate (+scaffold/impl) uses graceful
  `.ref` fallback. PERSONA (rolePersona) artifactTemplate uses central strict
  resolve_template → RAISES FileNotFoundError if absent (by design, same as
  code-reviewer). So test the stub path by repointing a SKILL ref, not a persona ref.

## Flags carried to orchestrator
- Same ephemeral scratchpad path (528b6512.../scratchpad/harness-100/en/03-newsletter-engine)
  in every artifactTemplate/dct:source — persistent corpus path must be confirmed
  and substituted before finalize/push. In .ttl header + README top warning.
- tool-websearch/cap-websearch added beyond brief §1b reuse-map (source uses WebSearch/
  WebFetch) — reported as faithful override, not drift.
