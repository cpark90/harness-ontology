# Harness composition: assembling a harness from ontology parts

This document specifies the **composition methodology** — building a new harness
by *composing the ontology's reusable, typed parts* rather than authoring one
from scratch — as the ontology itself now formalizes it. It is the authoring
counterpart to the **ODR EMIT** render path (`docs/odr-bind-lock.md`,
`docs/materialize-design.md`): composition **assembles the SPEC**; ODR
BIND/EMIT/Lock **render and reproduce** it.

The process is documented operationally in `CLAUDE.md` §"Composing a new harness
(the intended workflow)". This doc records how those steps are captured as
first-class ontology nodes so the methodology is itself discoverable, reusable
and connected (not just prose).

## The nodes (central, neutral, `.../id/core/`)

| Node | Type | Role in the methodology |
|---|---|---|
| `wf-compose-harness` | `ho:Workflow` | the 7-step composition process (below), as a reusable workflow |
| `pat-ontology-composition` | `ho:DesignPattern` | the pattern: assemble from a bill-of-materials of typed parts, not from scratch |
| `gr-reuse-first` | `ho:Guardrail` | the anti-drift / anti-orphan discipline: reuse first, connect any new part in the same change |
| `c-composition` | `ho:Concept` | term "Harness composition", `skos:broader c-agent-methodology` |
| `c-reuse-first` | `ho:Concept` | term "Reuse-first authoring", `skos:broader c-agent-methodology` |

All five are wired into the neutral template `h-multiagent` (a harness holds
≥1 workflow and ≥1 pattern): `ho:hasWorkflow wf-compose-harness` (alongside the
existing `wf-multiagent`), `ho:appliesPattern pat-ontology-composition`
(alongside `pat-orchestrator-workers`), and `ho:hasGuardrail gr-reuse-first`.
The two new terms hang under the existing methodology top concept
`c-agent-methodology`, so nothing is orphaned. Reusing existing `ho:`
vocabulary only — no TBox class or property was added (`CLAUDE.md` §"Adding
vocabulary").

## The 7 steps (as `wf-compose-harness` formalizes them)

1. **Retrieve a budget-capped context pack** for the request
   (`tools/retrieve.py`) — never load the whole ontology (`CLAUDE.md` golden
   rule 1; the anti-context-rot term `c-bounded-context`).
2. **Take a template**: the top base-harness candidate from the pack, or a
   `ho:DesignPattern` when none fits.
3. **Bind every capability**: for each `requiresCapability` in scope, bind a
   component that `providesCapability` it. The pack's "Capability gaps" lists
   what is missing; fill each by **reusing** an existing component or authoring
   a new one (`gr-reuse-first`).
4. **Assemble the shape minimums**: 1 `SystemPrompt` + ≥1 `Workflow` + tools +
   guardrails + 1 `ModelConfig`, as enforced by `ho:HarnessShape`.
5. **Write back as new individuals**: `skos:prefLabel`, `ho:maturity "draft"`,
   `ho:derivedFrom` the template, `ho:tokenEstimate` on every node carrying
   text, and existing `ho:Concept` tags so the result is discoverable, not
   orphaned.
6. **Validate**: `tools/validate.py` must print `PASS` — connectivity (no
   orphan islands), typing (SHACL), and capability satisfaction.
7. **Coverage-audit gate** (`CLAUDE.md` step 7): green `validate.py` is not yet
   "done". Enumerate every structural element of the source and map each to a
   representation; an unrepresented harness-structural element (role, tool,
   guardrail, channel, standard) is a GAP to fill, and a missing vocabulary
   category triggers a TBox extension rather than a silent skip.

After the gate, the validated spec is **materialized** — the ODR **EMIT** axis
(`tools/materialize.py`) renders it into the artifact tree.

## Relationship to ODR

The two methodologies are complementary halves of one lifecycle:

- **Composition** (this doc) produces the **SPEC**: the neutral, typed,
  long-lived graph of parts assembled into a harness. It answers *what the
  harness is* in technology-neutral terms.
- **ODR** consumes that spec. Its axes (`docs/odr-bind-lock.md`) are **BIND**
  (which concrete implementation realizes each tool, recipe-side), **EMIT**
  (deterministic render of spec + bind → file tree), and **Lock** (snapshot for
  reproducibility). Composition's step-7 "materialize" is exactly the handoff
  into EMIT.

So `wf-compose-harness` ends where `docs/odr-bind-lock.md` begins: composition
authors and validates the spec; ODR binds an implementation, emits the
artifacts deterministically, and locks the selection so the build reproduces.
Dependency is one-way — composition never depends on a particular
implementation, preserving spec purity (ODR INV-1).
