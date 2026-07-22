# Materialize design: the build projection (recipe → harness file tree)

This document defines `tools/materialize.py`, the **build projection** of the
harness ontology. It is the counterpart to the approved feedback
`docs/feedback/recipe-to-buildable-harness.md`: a recipe is a bill-of-materials
graph, and until now there was no tool to render a validated recipe union into
an actual runnable harness file tree. `retrieve.py` reads; `validate.py` checks;
`materialize.py` **builds**.

This is the **first increment** — the spine (P1) plus template-file references
(P2), scoped to emitting `CLAUDE.md` + `MANIFEST.json`. The remaining
recommendations from the feedback (P3/P4/P5) are explicit follow-ups, listed at
the end as NOT-yet-done.

## retrieve ↔ materialize symmetry

The ontology is never handed to an agent whole; both tools are **projections**
of the union, in opposite directions:

| | `retrieve.py` (read) | `materialize.py` (build) |
|---|---|---|
| input | a natural-language request | a validated harness IRI/id |
| selection | lexical seeds + bounded BFS, token-budget capped | the harness's own components (deterministic) |
| output | a compact **context pack** to READ | a **file tree** to BUILD (`CLAUDE.md`, `MANIFEST.json`) |
| defends | context rot (bounded read) | drift/orphans (only a *validated* union builds) |
| loader | `ontology_lib.load_graph` (catalog/glob, env overrides) | same |

Both honour `HARNESS_CATALOG` / `HARNESS_ROOT_ONTOLOGY`, so a **recipe** union
(central neutral parts + a recipe's domain bindings) materializes exactly the
way the central store does. `ho:artifactTemplate` is a build-only concern:
`retrieve.py` ignores it, keeping the read projection unchanged.

## Validation gate — "only a validated harness materializes"

Before emitting a single file, `materialize.py` calls `validate.run_structured()`
(the same structured check `validate.py --json` uses) over the composed union.
If the union does not `PASS` (SHACL, reachability, capability satisfaction) the
tool **refuses**: it prints a clear message to stderr and exits non-zero, writing
nothing. This makes the build honest — a file tree is only ever produced from a
connected, well-typed, capability-complete graph. (Verified: pointing the loader
at an incomplete catalog that omits the central parts makes the union fail
validation and materialize refuses with exit 1, no output directory created.)

## CLI

```
materialize.py <harness-IRI-or-id> --out <dir> [--format text|json]
```

- `<harness-IRI-or-id>` — a full entity IRI, or a short id such as `h-techdoc`
  (resolved by matching the IRI's last path segment; ambiguity or absence is a
  hard error listing the known harnesses).
- `--out <dir>` — output directory for the emitted file tree (created if absent).
- `--format text|json` — the **stdout build report** only (a human summary vs the
  manifest as JSON). The files on disk are always emitted regardless of `--format`,
  mirroring `retrieve.py`'s `--format md|json` convention.

Run with an interpreter that has `rdflib`/`pyshacl`/`owlrl` (e.g.
`/usr/bin/python3`), like its peers.

## Emitted file tree

### `CLAUDE.md` — the operating doc

Assembled from the target harness's components in a **fixed section order**;
within a section, multiple components are sorted by IRI so the same input yields
byte-identical output (no timestamps, stable ordering):

| section | source predicate | rendered as |
|---|---|---|
| overview (`# title` + intro) | harness `skos:prefLabel` / `skos:definition` | heading + prose |
| `## Persona` | `ho:hasSystemPrompt` → `ho:promptText` | prose (via template if present) |
| `## Operating rules` | `ho:hasGuardrail` | one bullet per guardrail: prefLabel + promptText, with each `ho:languageCondition` as a sorted sub-bullet |
| `## Process` | `ho:hasWorkflow` (+ `ho:appliesPattern`) | bullets: workflow/pattern prefLabel + `skos:definition` |
| `## Model` | `ho:usesModel` → `ho:promptText` | bullet: prefLabel + config string |

### `MANIFEST.json` — the provenance / build record

A deterministic (`sort_keys`) JSON object with:

- `harness`, `prefLabel`, `derivedFrom` — identity + provenance.
- `components` — every bound component as `{iri, type, label}`, sorted by IRI.
- `capabilityBindings` — for each `ho:requiresCapability`, the component(s) that
  `ho:providesCapability` it (the composition proof, mirrored from
  `validate.check_capability_satisfaction`).
- `templateSources` — the template fragment paths actually rendered.
- `tokenEstimate` — the summed `ho:tokenEstimate` of the bound components (keeps
  the build budget-accurate, consistent with the anti-rot discipline).

## `ho:artifactTemplate` mechanism (P2)

The confirmed body-storage decision is **template-file references**, not inline
long-text blocks: a component may carry

```turtle
ho:artifactTemplate "tools/materialize_templates/persona.md.tmpl"
```

(a new `owl:DatatypeProperty`, `rdfs:domain ho:HarnessComponent`,
`rdfs:range xsd:string`, added to the TBox). When present, `materialize.py` reads
that fragment and renders it as the component's section, substituting the node's
graph data. When **absent**, it falls back to rendering the section from graph
data (the promptText/definition already in the node) — so the property is a
progressive enhancement, never a requirement.

**Substitution** is simple placeholder replacement from the node's graph data:
`{{prefLabel}}`, `{{promptText}}`, `{{definition}}`. This is intentionally
minimal (no template engine, no logic) — anti-drift and determinism over cleverness.

**Path resolution.** A `ho:artifactTemplate` value is a repo-relative path,
resolved against these roots in priority order, first existing file wins:

1. the **ontology repo root** (`ontology_lib.ROOT`) — where `tools/` and
   `ontology/` live;
2. the **catalog's directory** (`dirname(HARNESS_CATALOG)`) — the **recipe repo
   root** when a recipe union is materialized via `HARNESS_CATALOG`, so a recipe
   can ship its own template fragments next to its `.ttl`.

A path that is set but resolves to no file is a hard error (misconfiguration),
distinct from the property being absent (graph-data fallback).

Central stays neutral: the demo wires `ho:artifactTemplate` onto the **recipe**
node `id:sp-techdoc` (in `staging/harness-recipes/recipes/techdoc/techdoc.ttl`),
pointing at the reusable, domain-neutral fragment
`tools/materialize_templates/persona.md.tmpl` (a materialize tool asset, not an
ontology part).

## Follow-ups (NOT done in this increment)

These are the remaining feedback recommendations, deliberately out of scope here
and to be planned as separate dispatches:

- **P3 — tool implementation refs.** A `ho:implementationRef` (path/repo/template)
  linking a `ho:Tool` node to its real code (e.g. `id:tool-docgraph` ↔
  `tools/docgraph.py`), so the build can emit or fetch tool code. Today the
  manifest records tools by IRI/label only; no code is emitted.
- **P4 — first-class multi-agent roles.** A role artifact (persona + tool/guardrail
  scope + memory policy) modeled as a first-class node, materialized to
  `.claude/agents/<role>.md`. Today only the persona/workflow/pattern are rendered
  into a single `CLAUDE.md`.
- **P5 — standard / docs scaffold.** Attachable blueprint fragments (standard
  documents, a `docs/` tree) rendered into the harness file tree. Today only
  `CLAUDE.md` + `MANIFEST.json` are emitted.
