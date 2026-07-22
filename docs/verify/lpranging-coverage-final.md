# lpranging recipe — coverage / completeness audit (FINAL, vnv)

**Supersedes** the BLOCKER verdict in `docs/verify/lpranging-coverage.md`. Same
question — does the recipe `staging/harness-recipes/recipes/lpranging/` reflect the
harness structure *without missing parts*? — re-audited after two fixes: (1) the P0
recipe-closure regression was resolved, (2) coordination **channels** are now modeled
and wired into `h-lpranging`.

**Interpreter**: `/usr/bin/python3` (rdflib/pyshacl/owlrl). Recipe commands run from
`staging/harness-recipes/` with a temp `central` symlink → repo root, removed at end.
Every claim below is from the actual composed union graph and the tools.

**VERDICT: `pass` — lpranging is now reflected completely.** No missing
harness-structural part remains; channels are represented and roll up; the P0 is gone
(the union VALIDATES and materializes). Residual absences are the acceptable GAP-A
(out-of-model domain content) and the low-severity GAP-B2 (3 skills). No NEW gap found.

---

## 1. P0 RESOLVED — recipe union validates and materializes

Prior state: union FAILed SHACL (7 role `prefLabel` violations) and
`materialize.py` REFUSED. Now:

```
cd staging/harness-recipes && ln -sfn /home/cpark/git/harness_ontology central
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
/usr/bin/python3 central/tools/validate.py
```
→ **PASS**. Evidence (tool output): `loaded graph: 2270 triples`;
`✓ conforms — no orphaned/under-specified nodes`;
**`✓ all 94 individuals reachable from a Harness`** (the expected ~94);
`✓ every harness's required capabilities are provided internally`;
`✓ no duplicate labels within a class`. Exit 0.

**Fix applied = Option A (confirmed in the files, cleaner than the prior 2-line
enumeration recommendation):**
- `recipes/lpranging/lpranging.ttl:51-53` — the recipe is now
  `owl:imports <https://harness-ontology.dev/ontology>` **only** (the single central
  ROOT). No per-unit enumeration remains.
- The central root `ontology/harness-ontology.ttl` `owl:imports` the schema **and every
  core unit**, including `.../data/core/roles` (line 31) and `.../data/core/channels`
  (line 32) — so all core units transitively enter the recipe union; a newly added
  central unit can never again silently break a recipe's closure.
- `staging/harness-recipes/catalog-v001.xml` maps the ROOT (`id="root"`, line 37) plus
  `core-roles` (line 50) and `core-channels` (line 51) to `central/…`. The catalog
  comment (lines 11-18) documents the "import the root, propagate every core unit"
  contract. This is the structural cause of the P0 being gone, not a patch over symptoms.

## 2. Channels now represented and wired

Union query (env as above, `ontology_lib.load_graph(reason=True)`):

- `h-lpranging` (`https://harness-ontology.dev/id/lpranging/h-lpranging`) carries **all 3**
  `ho:hasChannel` edges → `core:chan-agent-user`, `core:chan-orchestrator-inspection`,
  `core:chan-dispatch`.
- Each resolves to a typed `ho:Channel` with participants (roles) + `involvesUser` +
  `channelMedium`:
  - `chan-agent-user` — participants {role-orchestrator, role-inspection}; involvesUser
    **true**; medium "durable file channel (inbox/report)".
  - `chan-orchestrator-inspection` — {role-orchestrator, role-inspection}; involvesUser
    false; medium "persistent file channel + status markers (wip->rename, frontmatter
    status)".
  - `chan-dispatch` — {role-orchestrator, role-developer, role-research,
    role-inspection-worker, role-vnv, role-design}; involvesUser false; medium
    "dispatch (subagent spawn)".
- **Reused by `core:` IRI, no drift**: `non-core Channel individuals: []` — the recipe
  defines **no local** channel individual (`grep` for `a ho:Channel` in `lpranging.ttl`
  = none); it only references the central ones. The 3 channels are also on central
  `core:h-multiagent` (`harnesses.ttl:100`), from which `h-lpranging` derives.
- `ho:hasChannel rdfs:subPropertyOf ho:hasComponent` = **True** in the reasoned union, so
  channels are first-class connected components (orphan-free, reachability-counted).

## 3. Materialize — succeeds, deterministic, channels roll up

```
… central/tools/materialize.py h-lpranging --out <scratch>
```
→ `✓ materialized Low-power ranging system-design agent`; **25 components** (was 22
before channels; +3), ~1086 tokens, 6 capability bindings, 3 roles, 2/2 impls copied,
3 scaffold fragments, fresh `harness.lock.json`. Two runs `diff -r` **IDENTICAL**
(deterministic). Emitted tree unchanged in shape from the prior faithful-reflection
audit: `CLAUDE.md`, `MANIFEST.json`, `.claude/agents/{developer,vnv,inspection}.md`,
`tools/{docgraph.py,sim_grid_reservation.py}`, `{DESIGN_HARNESS_STANDARD,CODESTYLE}.md`,
`docs/ONTOLOGY.md`, `harness.lock.json`.

**Channel roll-up (honest state):** the 3 channels appear in `MANIFEST.json`
`components[]` as `{iri: core:chan-*, label: "…channel", type: HarnessComponent}` — they
enter the component inventory via `hasChannel ⊑ hasComponent`. There is **no dedicated
channel file-emitter**: no `.claude/…` channel file is written (the only file containing
channel data is `MANIFEST.json` itself). So channels are represented and inventoried and
build-visible, but not yet projected as their own artifact — the same honest posture the
task calls out. This is a projection-completeness note, not a modeling gap (the model
carries the full channel semantics; only a materialize emitter is absent).

## 4. Refreshed coverage verdict

**Now represented (complete for harness structure):** persona (`sp-lpranging`); all
operating rules including the `core:gr-lang` Korean/English language conditions (+ its
code/prose/terms sub-bullets); the multi-agent workflow + orchestrator-workers pattern;
model config (`mc-opus`); the 3 worker roles (+personas, tool/guardrail scopes,
`roleMemoryPolicy`); both operating tools with **byte-identical** vendored code
(`docgraph.py` 32560 B, `sim_grid_reservation.py` 11309 B); all 3 standard/vocabulary
docs as byte-identical scaffold; **AND the 3 coordination channels** (this audit's new
item). No drift: no duplicate labels, no untyped edges, no local near-synonym channels;
`validate.py` clean.

**Residual gaps (unchanged, both acceptable/low):**
- **GAP-A (acceptable, out-of-model)** — domain design-graph content: `docs/` (261+
  files: terminology/issues/requirements/lessons/software/hardware/research/feedback),
  `ARCHITECTURE/CONCEPT/SYSTEM_DESIGN.md`, `reference/` subtrees (~126 files),
  `exports/*.manifest`, `.claude/agent-memory/**` *content*, `.claude/settings.local.json`.
  Rationale stands: this is the *output* the harness produces (via `tool-docgraph` under
  the `docs/ONTOLOGY.md` vocabulary it ships) and per-machine runtime state — a harness
  BoM ships the *means* to regenerate the design graph, not the graph itself. Correct
  scope, stated so the recipe is not over-claimed as a full project snapshot.
- **GAP-B2 (low)** — the 3 `.claude/skills` / slash-commands (`check-docs`,
  `new-design-doc`, `resolve-issue`) are still unmodeled. The underlying capability
  (design-graph management) is already fully captured by `tool-docgraph` + the
  `docs/ONTOLOGY.md` scaffold; skills are thin procedural wrappers. `ho:Instruction`/
  `ho:Workflow` fit if parity is wanted, but `materialize.py` also has no skill-emit path,
  so B2 is a model+projection enhancement, not a one-liner. Low severity.

**NEW gap check: none.** The previously latent structural omission (channels) is now
closed; GAP-B1 (P0 closure) is resolved. Nothing else harness-structural in the source
is unrepresented.

## 5. Recurrence-prevention landed (sanity-checked, present)

- **`core:gr-structural-coverage` guardrail** — `ontology/abox/core/guardrails.ttl:41`
  (prefLabel "Structural coverage completeness", promptText: enumerate every source
  structural element, EXTEND schema rather than skip, verify coverage before declaring
  done; `tagged c-traceability`, tokenEstimate 58, maturity reviewed). Wired into
  `core:h-multiagent` at `harnesses.ttl:96`, so it flows into every derived harness's
  union.
- **CLAUDE.md step-7 "Coverage-audit gate"** — `CLAUDE.md:56-62`: green `validate.py`
  is not "done"; a source→representation coverage audit (vnv dispatch) must map every
  structural element or give an explicit acceptable reason, and a missing vocabulary
  category triggers TBox extension (channels named explicitly).
- **Lesson** — `docs/lessons/coverage-gap-channels.md` (2506 B) documents the missed
  channels/skills coverage gap.

---

## Reproduction summary (commands actually run)

```
cd staging/harness-recipes && ln -sfn /home/cpark/git/harness_ontology central
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
  /usr/bin/python3 central/tools/validate.py            # → PASS, 94 individuals
# union query via ontology_lib.load_graph(reason=True): 3 hasChannel edges, typed
#   ho:Channel w/ participants+involvesUser+medium; hasChannel ⊑ hasComponent = True;
#   non-core Channel individuals = []
… central/tools/materialize.py h-lpranging --out <scratch>   # → 25 components, det.
rm -f central                                            # temp symlink removed
```

No `ontology/`, `tools/`, or central `docs/` files were edited; no git was run; the
temp `central` symlink was removed. This report is the only artifact written.
