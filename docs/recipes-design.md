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
   `https://harness-ontology.dev/recipes/<name>` that `owl:imports` the central
   `.../schema` **and** the central `.../data/core/<type>` units it references.
   (Because the central seed harnesses in the `harnesses` unit cross-reference
   every other core unit, a recipe that `derivedFrom` a core harness imports the
   whole core — the composed union is then the full central 64 + the recipe's
   local nodes.)
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
