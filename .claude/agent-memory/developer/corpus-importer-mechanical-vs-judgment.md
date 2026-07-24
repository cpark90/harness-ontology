# Corpus importer (tools/import_corpus.py) — mechanical vs judgment split

`import_corpus.py <corpus-dir> [--out <recipe-dir>]` turns one harness-100 corpus
harness (`.claude/CLAUDE.md` + `agents/*.md` + `skills/*/skill.md`) into a **draft**
recipe TTL. Built + validated against the 5 hand-authored pilots as oracle
(03/16/21/31/46). Reusable facts:

## Naming derivation (deterministic, matches pilots)
- id: domain = **full corpus dirname** (`21-code-reviewer`); shortname = dirname minus
  `^\d+-` (`code-reviewer`).
- harness `id:h-<shortname>`; orchestrator persona `id:sp-<shortname>` (no artifactTemplate);
  worker persona `id:sp-role-<agentfile>`; role `id:role-<agentfile>`; instruction
  `id:ins-<skilldir>`. prefLabel = capitalize-first-char of the source name (pilots
  hand-EXPAND abbrevs e.g. `frontend-dev`→"Frontend-developer" = judgment ②, id unchanged).
- **orchestrator skill = the skill dir whose name == shortname** (exception 0 across corpus).
  Others are extending skills.

## The mechanical oracle that PASSES exactly
- **Instruction `ho:tokenEstimate` = `wc -w` of the whole skill.md file** (frontmatter
  included). Matched pilots to the token across all 5 (945/1019/784, 984/854/1050, …).
  Python `len(text.split())` == `wc -w` for these files.
- `ho:artifactTemplate` = absolute path into the corpus (`<abs>/.claude/agents/<x>.md`,
  `…/skills/<d>/skill.md`) — matches pilots byte-for-byte.
- **`ho:augmentsRole`**: parse the extending skill's `## Target Agent(s)` section,
  extract backtick tokens that name a known agent file → `id:role-<token>` (repeatable).
  Reproduced refactoring-catalog→{arch,perf}, vuln-patterns→security. NOTE the pilots
  PREDATE augmentsRole (they wrote "TARGET AGENT: x" in skos:definition), so the importer
  is MORE correct than the frozen pilot here — not a defect, a supersession.
- persona `ho:promptText` = **first paragraph after the body H1** ("You are a … specialist.")
  — a one-para seed, NOT the vendored body; satisfies SystemPromptShape (promptText is
  REQUIRED, minCount 1). tokenEstimate = wc of that seed. Pilots hand-rewrite promptText to
  a richer neutral summary (~60 words) = ②; importer's seed (~15 words) differs in wording only.

## What the importer REFUSES (MUST NOT → flag), = the "human work per recipe"
Emitting these is judgment; the importer leaves them unbound + a FLAG header comment:
1. **targetsDomain + addressesTask** — the ONLY two SHACL(HarnessShape) violations the
   draft carries (proven: closure SHACL on generated 21 → exactly those 2, nothing else).
   So an importer draft validates for graph-integrity of every node it emits; it is
   HarnessShape-incomplete by exactly the 2 semantic bindings. Clean ② measurement.
2. usesModel (source has model 0/489), hasGuardrail+roleGuardrail, usesTool+roleTool
   (tools 0/489 → least-privilege slice is inference), requiresCapability(+provider wiring),
   ho:tagged + local Concepts, appliesPattern/hasChannel beyond wf-multiagent, roleMemoryPolicy.
3. **QA-gate collapse decision** (promote-once): terminal QA/synthesizer agent MAY be dropped
   as a local role and REUSED as `core:role-synthesizer` to satisfy cap-synthesis — OR kept
   local. This VARIES per recipe: 21/03/31/46 collapse review-synthesizer/quality-reviewer/
   experiment-reviewer/pm-reviewer → core:role-synthesizer; **16 keeps qa-engineer LOCAL**
   (it's a test-ENGINEER worker, not a pure gate — see 16 pilot's own flagged comment).
   Importer keeps ALL agents local + flags candidates (regex synthesizer|reviewer|qa|quality,
   deliberately over-inclusive; human picks the true terminal gate from the DAG).

## Corpus-uniform CONSTANTS the importer DOES bind (justified by roadmap §0 uniformity)
`hasWorkflow core:wf-multiagent` (needed for HarnessShape, all corpus = orchestrator-workers),
`hasExecutionMode core:mode-agent-teams` (Agent Team 100/100), `derivedFrom core:h-multiagent`,
`dct:source`(canonical github URL)/`dct:license "Apache-2.0"`, `ho:maturity "draft"`.

## Out of THIS brief's SHOULD (not emitted; future importer extension)
TestScenario + FailurePolicy extraction (sources provide them, pilots got them via a later
backfill). Brief SHOULD didn't list them → respected the boundary, flagged as future work.

## Gotchas hit
- The capability hard-stop guard regex must **skip comment lines** first, else it matches the
  FLAG text "no ho:requiresCapability bound" and false-hard-stops. (`ln.lstrip().startswith('#')`.)
- Determinism: sort `os.listdir` for agents/skills; collapse promptText whitespace to one line
  (`" ".join(s.split())`); no timestamps. 2-run `diff -r` = identical, verified.
- Central `validate.py` PASS @223 unchanged (importer writes only tools/ + scratch; corpus read-only).
