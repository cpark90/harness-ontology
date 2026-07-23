# Recipe design: composing harnesses from the neutral parts library

This document defines the **recipe repo** — the counterpart to the central
neutral parts library. It builds directly on the federation mechanism in
`docs/federation-design.md` (D1 `owl:imports` + catalog, D3 IRI sub-namespaces,
D4 two-tier validation gate); read that first.

## Why a separate recipe repo

The central repo (`cpark90/harness-ontology`) is deliberately a **neutral parts
library**: generalised, domain-independent guardrails, patterns, workflows,
prompts, tools, capabilities and concepts, split per component type under
`ontology/abox/core/*.ttl`. It never describes one specific harness — that is the
neutral-parts principle recorded in `federation-design.md` (Status of external
data units).

But "how the parts are used and assembled" still has to live somewhere. That is
the **recipe repo** (`cpark90/harness-recipes`, renamed from the retired
`harness-data-lpranging`). It holds *many* harness **blueprints**: each recipe is
an **assembly spec** that `owl:imports` the central parts and composes a complete
`ho:Harness` from them, adding only the domain-specific bindings a specialization
needs. Central stays neutral; specialization lives in recipes.

This is exactly a federated pure-data repo in `federation-design.md` terms (D2),
specialised to one job — *composition*. Its domain segment is per-recipe
(`.../id/<name>/…`), never `core` (reserved for central, D3).

## Repo layout

```
harness-recipes/
├── README.md                       # what the repo is; how to validate a recipe
├── catalog-v001.xml                # central IRIs -> ./central/ clone; recipe IRIs -> files
├── LICENSE  (Apache-2.0)           # same licence as central
├── .gitignore                      # ignores /central/ (the cloned parts library)
├── recipes/
│   └── <name>/
│       ├── <name>.ttl              # the recipe unit (owl:Ontology .../recipes/<name>)
│       └── README.md               # one-paragraph blueprint description
└── .github/workflows/validate.yml  # CI: clone central, compose union, run central validate.py
```

Adding a blueprint = a new `recipes/<name>/` directory plus one `<uri>` line in
the catalog and one matrix entry in CI. The repo scales to many recipes with no
central change.

## What a single recipe unit contains

A recipe file (`recipes/<name>/<name>.ttl`) is one importable data unit:

1. **An `owl:Ontology` header** with document IRI
   `https://harness-ontology.dev/recipes/<name>` that `owl:imports` the **single
   central root ontology** `https://harness-ontology.dev/ontology`. The root
   transitively `owl:imports` the central `.../schema` **and** every neutral
   `.../data/core/<type>` unit, so importing it alone resolves the ENTIRE central
   store — the composed union is the full central store + the recipe's local
   nodes. This is deliberately not an enumeration of individual core units: any
   new core unit central adds (e.g. new roles or channels) propagates into every
   recipe's union automatically, so a new central unit can never silently break a
   recipe's closure. The recipe's `catalog-v001.xml` must therefore map the root
   IRI **and** the central files it transitively resolves to their `./central/…`
   clone paths, kept in sync with central's own catalog, so the loader can
   BFS-follow the root's import closure.
2. **A composed `ho:Harness`** (`.../id/<name>/h-<name>`) that binds central
   neutral parts **by IRI** through the assembly predicates:
   `hasSystemPrompt` / `hasGuardrail` / `usesTool` / `usesModel` / `hasWorkflow` /
   `appliesPattern` / `requiresCapability`, plus `targetsDomain` / `addressesTask`
   and `tagged`. Reused central nodes are written through a `core:` prefix
   (`@prefix core: <…/id/core/> .`), exactly as D3 prescribes for cross-domain
   references.
3. **The domain-specific parts, declared LOCALLY** in the same unit under the
   recipe's own `@prefix id: <…/id/<name>/> .`: its `Domain`, its `Concept`
   sub-tree (rooted on the central `core:scheme`), its domain `Tool`s + their
   `Capability`s, and a persona `SystemPrompt`. These are wired into the harness
   so it is connected (no orphans) and buildable (every `requiresCapability` is
   met by a component that `providesCapability` it). Text-bearing nodes carry
   `ho:tokenEstimate`; every node has `skos:prefLabel` and, where useful,
   `skos:definition`, in English (`ONTOLOGYSTYLE §1d`). The harness records
   `ho:derivedFrom` its template for provenance.

The central library never learns a domain term: all domain nodes live in the
recipe, and central `ontology/abox/core/**` stays grep-clean of any domain noun.

## What a recipe stores — spec + explanation + references, NOT concrete artifacts

A recipe holds the **composition spec** (part IRIs assembled into a harness), an
**explanation** of that composition (which parts + methodology were used, how, and
what result), and **references** to the concrete build artifacts — it must **not
store the concrete build documents themselves** (real tool code, standard/doc
files, skill bodies). Storing copies of those artifacts is *vendoring*, and it
re-introduces exactly what the neutral-parts / anti-drift discipline removes: the
recipe would drift from the real source, duplicate its content, and blur the
spec/implementation boundary.

This is the ODR line made concrete at the recipe level: **implementation is
referenced (and regenerated at build), never stored in the spec** (ODR INV-1,
`docs/composition-methodology.md`). A recipe therefore carries:

1. the **spec** — the composed `ho:Harness` and its part IRIs (§ above);
2. the **explanation** — the recipe `README.md` (and `skos:definition` /
   comments) describing *which* neutral parts + local bindings were used, *which*
   methodology assembled them, *how*, and *what* harness results; and
3. **references** to concrete artifacts — `ho:implementationRef` (tool code),
   `ho:scaffold` (standard/doc fragments) and skill `ho:artifactTemplate`
   (skill bodies), each a path/URL to the real source, **not a stored copy**.

At build, `materialize.py` **fetches** every reference into the tree
(`docs/materialize-design.md`); a reference that does not resolve becomes a
fail-safe `.ref` **stub**, never a build failure. The worked example
(`recipes/lpranging/`) applies this literally: its tool/scaffold/skill references
point at the real source harness on disk and are fetched at build, so the recipe
stores no `.py` and no `SKILL.md` body — only TTL + README + reference strings.

**Reference reach is a modeling choice.** A repo-relative reference (code shipped
beside the `.ttl`) is portable but is itself a stored copy — acceptable only for
genuinely recipe-owned assets. A reference to an **external** source (absolute
path or fetchable URL) keeps the recipe a pure spec-plus-references but resolves
only where that source is reachable (else a stub). The lpranging example
deliberately takes the external-reference form (non-portable, but stores nothing);
its README states that tradeoff explicitly.

## How a recipe validates (clone central → compose union → central validate.py)

Validation always runs over the **union** (central parts + the recipe), never a
lone file, using the **central** `validate.py` and SHACL shapes — the D4
invariant that anti-orphan / anti-drift / buildable only hold over the merged,
reasoned graph.

```bash
# in the recipe repo:
git clone https://github.com/cpark90/harness-ontology central   # the parts library
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<name> \
/usr/bin/python3 central/tools/validate.py                       # must print PASS
```

`HARNESS_ROOT_ONTOLOGY` selects which recipe's `owl:imports` closure to compose.
The central loader (`tools/ontology_lib.load_graph`) BFS-resolves that closure
through the recipe's `catalog-v001.xml`, whose `central/…` entries point at the
clone and whose `recipes/…` entries point at the local recipe files. `PASS`
means the composed harness is connected, well-typed and buildable. This is the
same env-override gate a pure-data repo uses in `federation-design.md`
(D4 / "Composing the full federated union", option 1). CI
(`.github/workflows/validate.yml`) runs it per recipe (a matrix over recipe root
IRIs) so a recipe that breaks the union fails at contribution time.

The recipe repo carries **no tools** — it pulls central's `validate.py` and
shapes, exactly like any federated data repo. `/central/` is gitignored (cloned
in, never vendored).

## Repo rename

The recipe repo is the **renamed** `harness-data-lpranging → harness-recipes`.
The old name framed it as one domain's data; the new name reflects its actual
role — a collection of many harness blueprints. The `lpranging` modeling returns
here not as central domain data (it was retired from central per the
neutral-parts principle, see `federation-design.md`) but as the **worked example
recipe** (`recipes/lpranging/`), demonstrating the pattern end to end: the
neutral orchestrator-workers template specialised into a low-power UWB ranging
(RTLS) system-design harness. The rename itself (archived repo → new name) is an
inspection + GitHub-account step, out of scope for authoring.
