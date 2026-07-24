# Run-behaviour AssemblySections (9..12) + their materialize renderers

GAP-4 of the revfactory P1 follow-up: the `ho:sectionKind` enum already carried
`execution-mode` / `data-flow` / `error-handling` / `test-scenarios` but no
`ho:AssemblySection` individual and no `SECTION_RENDERERS` entry existed, so
TestScenario/FailurePolicy data never reached a materialized document.

## The trap that decides the whole task: WHICH new section may join the default set
The default order lives on `id:h-multiagent` (`lib.DEFAULT_ASSEMBLY_HOLDER`), and
EVERY harness without its own set inherits it. So a new section kind may be added
to that set **only if it emits NOTHING for h-multiagent** (its CLAUDE.md is the
byte-identity invariant). Check the base template's own parts BEFORE authoring:

| kind | reads | h-multiagent has it? |
|---|---|---|
| execution-mode | `appliesPattern` tagged `id:c-execution-mode` | no (no harness applies pat-agent-teams/sub-agents/hybrid) |
| error-handling | `hasFailurePolicy` | no |
| test-scenarios | `hasTestScenario` | no |
| **data-flow** | steps' `stepProduces`/`stepConsumes` | **YES** — it binds `wf-multiagent`, which carries `dlv-dispatch-brief`/`dlv-verified-result` |

⇒ first pass landed 3 (orders 9/11/12) and STOPPED on `as-data-flow`: an unbound
AssemblySection is not an option (⊑HarnessComponent ⇒ `ComponentConnectivityShape`
orphan FAIL), so the only in-boundary move was binding it to h-multiagent = a
document change the brief forbade. Reported as a GAP with the exact measured diff
instead of picking a side; order 10 held vacant meanwhile (holes are legal —
`check_assembly_order` demands uniqueness, not contiguity, so a reserved slot is a
cheap, renumber-free deferral).

**Orchestrator ruled (a): accept the change, land `as-data-flow` at order 10.**
The reasoning is the reusable part — a byte-identity invariant guards against
*refactors silently changing output*; it must NOT block a feature whose whole
point is to surface data the graph already held but the emitter never rendered.
When the two collide, escalate with the diff, don't suppress the feature. Result:
h-multiagent's CLAUDE.md gains ONLY an appended `## Data flow` (11 added lines,
`grep -c '^<'` on the diff = 0 ⇒ nothing else moved); every recipe pilot binding
`wf-multiagent` gains the same section (techdoc, whose steps name no deliverable,
does not) — the conditional guard keeps it truthful everywhere.

## MANIFEST can NOT stay byte-identical (the brief's gate was over-specified)
Binding anything new to h-multiagent adds it to `all_components` ⇒ MANIFEST gains
the component rows and `tokenEstimate` grows (final: +4 rows, 49794→49888), and
the lock's `individualCount` moves (198→202). Only **CLAUDE.md** byte-identity is
achievable/meaningful. Same finding as the original 8-section landing.

## Stale prose a sectionKind extension always leaves behind (grep these)
The `sh:in` enum in shapes was already 12-valued while the PROSE lagged at 8:
`ho:sectionKind` + `ho:AssemblySection` `skos:definition` (TBox — text-only fix,
needs orchestrator approval since TBox is out of a developer's boundary) and the
host harness's ABox banner ("Still missing (later wave): …"). Enum ≠ narrative;
fix both in the same wave.

## Renderer conventions (tools/materialize.py)
- Every new renderer is CONDITIONAL: read its parts first, `return` when empty —
  that is what keeps inheritance harmless for all pre-existing harnesses/recipes.
- `execution-mode`: **there is no `ho:ExecutionMode` class** (D2 lightening). Read
  `appliesPattern` filtered by `ho:tagged` = new `lib.EXECUTION_MODE_CONCEPT`
  (`id:c-execution-mode`), a well-known constant next to `DEFAULT_ASSEMBLY_HOLDER`.
  Left `_render_process` untouched (it still lists all patterns) — touching it
  risks byte-identity for zero present benefit.
- `data-flow`: join producers→consumers per Deliverable over `hasWorkflow o hasStep`
  (dedupe with a set, IRI-sort) — the DAG is not recoverable from `stepOrder`.
- `error-handling`: markdown table; `_cell()` escapes `|` and flattens newlines so
  a literal can never break row structure. Multi-valued fields sorted+joined.
- All literal lists sorted (`sorted(str(x) ...)`) for determinism.

## Proving renderers no central harness exercises
Scratch-overlay (see assembly-order-graph-driven): rewrite the repo catalog's
relative uris to ABSOLUTE into a scratchpad copy, append a scratch root
(`owl:imports` central root + scratch data unit) and a scratch harness that
declares its OWN `hasAssemblySection` (a SUBSET is fine — totality is per-harness)
plus the parts under test. Gotcha: the scratch harness must satisfy HarnessShape
including `ho:targetsDomain` (≥1 Domain) and `addressesTask`. Run with
`HARNESS_CATALOG` + `HARNESS_ROOT_ONTOLOGY`; nothing lands in the repo.
Recipe check needs `HARNESS_ROOT_ONTOLOGY=<recipe IRI>` (else the harness is
"not found").
