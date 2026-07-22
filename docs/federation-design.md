# Federation design: GitHub-connected ontologies + pure-data repos

This document records the architecture for **federating** the harness ontology
across multiple GitHub repositories, the way
[`lu-w/auto`](https://github.com/lu-w/auto) federates an automotive ontology:
one authoritative schema/tooling repo plus one or more **pure-data** ABox
repos, composed into a single union graph by `owl:imports` + a Protégé-style
catalog.

Source of intent: the user inquiry and the inspection analysis in
`docs/feedback/inquiries/benchmark.md` (see its §2 gap analysis and §3/§4
recommendations, with file:line evidence). The four confirmed decisions below
were approved by the user in that cycle.

## Confirmed decisions

- **D1 — federation loading = `owl:imports` + catalog.** The union graph is
  assembled by resolving `owl:imports` through a Protégé `catalog-v001.xml`
  (ontology IRI → local file), **not** by directory glob and **not** by git
  submodules. This is exactly the mechanism `auto` uses (benchmark.md §1) and is
  the standard OWL federation primitive.
- **D2 — split repos.** A central **schema + tooling** repo (TBox + SHACL shapes
  + `validate`/`retrieve`/webui + guideline + CI) vs. one or more **pure-data**
  ABox repos (only Turtle individuals). This matches the user's "storage repo =
  pure data, clone/edit/push" request (benchmark.md §3b). *This dispatch only
  **prepares** the split — it does not create new git repos* (see §Migration).
- **D3 — domain/contributor sub-namespace.** Individual IRIs are minted as
  `https://harness-ontology.dev/id/<domain>/<slug>` so independent repos cannot
  collide on a bare slug (benchmark.md §3c). `core` is reserved for the central
  ontology.
- **D4 — two-tier validation gate.** A contributor runs the central `validate.py`
  locally, **and** each data repo's CI pulls the central `validate.py` to gate
  PRs (benchmark.md §3b, §4). The anti-orphan / anti-drift / buildable
  guarantees only hold over the **union** graph, so validation must always run
  against the composed union, never a single data file in isolation.

## Why the union graph is the load-bearing invariant

`docs/DESIGN.md` derives all three guarantees — anti-orphan (reachability +
SHACL connectivity), anti-drift (controlled TBox vocabulary), buildable
(capability satisfaction) — from validating **one merged, reasoned graph**.
Federation must therefore preserve "there is a single union to validate."
`owl:imports` + catalog gives exactly that: the import closure *is* the union.
A cross-repo edge (repo A's individual `hasComponent` repo B's individual) is
only reachable/type-checkable once both are pulled into the union, which is why
D1 (composition) and D4 (validate-the-union) are two halves of one design.

## Architecture

### Repo layout (D2)

```
central repo  (schema + tooling; authoritative)
├── ontology/
│   ├── harness-ontology.ttl        # root owl:Ontology — owl:imports the rest
│   ├── tbox/harness.ttl            # the vocabulary (owl:Ontology .../schema)
│   ├── shapes/harness-shapes.ttl   # SHACL (validation-only, NOT imported)
│   └── abox/                       # central "core"-domain data (seed, examples)
├── tools/                          # validate.py, retrieve.py, ontology_lib.py, webui
├── catalog-v001.xml                # ontology IRI → local file (Protégé format)
├── ONTOLOGYSTYLE.md, docs/…        # authoring rules + this design
└── .github/workflows/validate.yml  # central CI gate

data repo(s)  (pure Turtle ABox; per contributor / per domain)
├── <domain>.ttl                    # owl:Ontology .../data/<domain>,
│                                   #   owl:imports the central TBox IRI
├── catalog-v001.xml                # maps the central TBox IRI → a local clone
└── .github/workflows/validate.yml  # pulls central validate.py to gate PRs (D4)
```

The central repo carries **all tools**; a data repo carries **only data** (plus
a thin CI stub and a catalog). Working on a data repo = clone it (and the
central repo, for the TBox + tools), edit TTL, run the central `validate.py`
against the union, push / open a PR.

### Composition: how the union is assembled (D1)

1. A **root ontology** `ontology/harness-ontology.ttl` declares
   `<https://harness-ontology.dev/ontology> a owl:Ontology` and `owl:imports`
   the TBox IRI plus each ABox ontology IRI.
2. `catalog-v001.xml` (at the repo root, Protégé "auto" format) maps every
   ontology IRI to a local file:

   | ontology IRI | local file |
   |---|---|
   | `…/ontology` | `ontology/harness-ontology.ttl` |
   | `…/schema` | `ontology/tbox/harness.ttl` |
   | `…/data/core/<type>` | `ontology/abox/core/<type>.ttl` (11 per-component-type units) |
   | `…/data/<domain>` | *external pure-data repo — none active today (see Status below)* |
   | `…/data/authored` | `ontology/abox/authored.ttl` (webui output, optional) |

3. `tools/ontology_lib.load_graph()` reads the catalog, then does a BFS from the
   root ontology IRI following `owl:imports` transitively, resolving each IRI to
   a local file through the catalog and parsing it once. The import closure is
   the union. SHACL shapes are **never** imported (they are validation-only, kept
   out of the data graph exactly as before).
4. If the catalog / root ontology is absent or resolves nothing, the loader
   **falls back to the legacy directory glob** (`ontology/**/*.ttl`, skipping
   `shapes/`), so a partial checkout still loads.

Each importable file declares its own `owl:Ontology` and imports what it depends
on: the central `core` data imports the schema; an external `<domain>` data unit
would import the schema **and** `core` if it references core individuals (see D3).
This makes the dependency explicit and is what a real external data repo does:
`owl:imports <https://harness-ontology.dev/schema>`.

An external data repo joins the federation by (a) adding its ontology IRI +
local path to a catalog and (b) being listed in the composing root's
`owl:imports`. No tool code changes — that is the point of catalog-based
federation over a hardcoded glob.

### IRI sub-namespace (D3)

- **Entity IRIs:** `https://harness-ontology.dev/id/<domain>/<slug>`.
  - `<slug>` keeps the existing prefix + kebab-full-word rule
    (`ONTOLOGYSTYLE.md §2`): `h-…`, `tool-…`, `gr-…`, `sp-…`, `c-…`, …
  - `<domain>` is a short kebab segment naming the repo/contributor scope.
    `core` is **reserved** for the central ontology. A contributor picks a
    domain segment that is unlikely to collide (project or org name).
- **Ontology (document) IRIs** are separate from entity IRIs:
  `https://harness-ontology.dev/data/<domain>`. (The document that *contains*
  the individuals, used by `owl:imports`/catalog, is not the same as the IRIs of
  the individuals themselves — standard OWL practice.)
- **In Turtle**, this is expressed purely through the prefix binding, so node
  bodies stay unchanged: a `core`-domain file binds
  `@prefix id: <…/id/core/> .` and writes `id:h-coding`; a file that also
  references core nodes binds a second prefix `@prefix core: <…/id/core/> .`
  and writes `core:tool-editor`. Because two prefixes can point at the same
  namespace, cross-domain references resolve to the same IRI in the union.

### Validation gate (D4)

Two tiers, both validating the **union**, never a lone file:

1. **Contributor-local:** clone the central repo (TBox + tools) alongside the
   data repo, point the catalog at the local clones, run
   `/usr/bin/python3 tools/validate.py` → must print `PASS`. This is the fast
   feedback loop and is required before opening a PR
   (`docs/CONTRIBUTING-ONTOLOGY.md`).
2. **CI on the data repo:** the data repo's `validate.yml` checks out its own
   TTL **and** the central repo, composes the union via the catalog, and runs
   the central `validate.py`. A non-zero exit fails the PR check. This keeps the
   fail-at-contribution property the inquiry warned would otherwise be lost when
   tools leave the data repo (benchmark.md §3b).

The central repo keeps its own `.github/workflows/validate.yml`; the data-repo
variant is provided as a template (`docs/ci/data-repo-validate.yml`).

## Migration plan

Done in this dispatch (code + docs only, no new repos, no git):

1. **Loader (D1).** Rewrote `tools/ontology_lib.load_graph()` to resolve
   `owl:imports` via the catalog, with a glob fallback. Public functions
   (`load_graph`, `instance_nodes`, `instance_edges`, `label_of`,
   `most_specific_types`) keep their signatures so `validate.py`, `retrieve.py`
   and `tools/webui/server.py` are unchanged callers.
2. **Catalog + root (D1).** Added `catalog-v001.xml` and
   `ontology/harness-ontology.ttl`; added `owl:Ontology` headers to the ABox
   files so they are importable units.
3. **IRI migration (D3).** Re-based the central individuals: `seed.ttl` →
   `core` domain (`…/id/core/<slug>`). An external data unit would bind its own
   `@prefix id: <…/id/<domain>/>` and rewrite references to central nodes through
   a `core:` prefix — text-surgical (prefix rebind + the specific cross-domain
   references), the TTL is not machine-reserialized.
4. **Guideline + CI template (D4).** `docs/CONTRIBUTING-ONTOLOGY.md` and
   `docs/ci/data-repo-validate.yml`.

Status of external data units:

- **No active external data repo.** The federation currently loads **schema +
  core** only. The earlier `lpranging` domain-specific modeling — a concrete
  worked pilot of the split — was **RETIRED** per the neutral-parts principle:
  the ontology is a library of generalised, domain-independent reusable parts,
  not the description of one specific harness. Its reusable governance parts
  (verify-then-proceed, design-for-loss, traceability, no-arbitrary-decision,
  least-privilege, report-over-prompt, controlled-vocabulary guardrails; the
  orchestrator-workers pattern + multi-agent workflow; a methodical persona) were
  neutralised and folded into the `core` data units (`ontology/abox/core/*.ttl`,
  split per component type),
  and the domain-coupled nodes (UWB/RTLS/low-power tasks, tools, persona and
  concepts) were dropped. Consequently `…/data/lpranging` appears in **no**
  catalog entry or root `owl:imports`, and `staging/` holds no payload. The
  federation infra (D1 owl:imports + catalog, D3 IRI scheme, D4 two-tier gate)
  remains fully available for a **future** external domain part-collection.
  *(The previously-published pilot data repo, if any, is retired by inspection at
  git time — out of scope here.)*

Follow-ups for any future external data repo still need **inspection + the
user's GitHub account** (out of scope for developer; noted for orchestrator):
- **Central-repo publication + a stable resolver.** For catalogs across machines
  to agree, the `https://harness-ontology.dev/…` IRIs should eventually resolve
  (GitHub Pages / release tarball, as `auto` does with GitHub releases). Today
  the catalog maps IRIs to local clones, which is sufficient for local + CI
  validation.
- **webui domain-aware authoring.** The webui currently authors into the `core`
  domain (its `id:` prefix binds to `…/id/core/`). Letting a human pick a target
  domain in the editor UI is a webui-scoped follow-up; the loader and data model
  already support it.

## Example external data-repo layout (D2 made concrete)

No external data repo is active today (see Status of external data units). The
layout below is the **generic template** a future pure-data `<domain>` repo would
follow — a concrete instance simply substitutes its own domain segment:

```
harness-data-<domain>/             # pure data, no tools
├── <domain>.ttl                   # owl:Ontology  …/data/<domain>
│                                  #   owl:imports   …/schema , …/data/core
├── catalog-v001.xml               # maps …/schema and …/data/core to local
│                                  #   clones of the central + core repos
└── .github/workflows/validate.yml # == docs/ci/data-repo-validate.yml
```

Its individuals are `…/id/<domain>/<slug>`; its references to shared central
components (`core:tool-editor`, `core:h-coding`, `core:gr-lang`, …) are
`…/id/core/<slug>`, resolved in the union. Running the central `validate.py`
over `schema ∪ core ∪ <domain>` is what proves a cross-domain harness is
connected, well-typed and buildable.

## Composing the full federated union (when an external data repo exists)

**Status:** there is no active external data repo; central loads **schema +
core** only (see Status of external data units). The recipe below is how the
full federated union would be recomposed **once** a `<domain>` data repo exists —
central's own loaded union stays `schema + core`, but the federated invariants
(anti-orphan / anti-drift / buildable) must be checked over the **full** union
that includes every external data repo, so a split must never silently drop a
domain from federated validation.

There are two equivalent ways to recompose `schema ∪ core ∪ <domain>`, both
using the **central** `validate.py` (shapes and tools always come from central):

1. **Run from the data repo (the D4 gate — preferred).** Clone central next to
   the data repo and point the central loader at the *data repo's* catalog, whose
   root ontology's `owl:imports` closure is the union. This is exactly what the
   data repo's CI does:

   ```bash
   git clone https://github.com/<owner>/harness-data-<domain> <domain>
   git clone https://github.com/hhmm2728/harness_ontology <domain>/central
   HARNESS_CATALOG="$PWD/<domain>/catalog-v001.xml" \
   HARNESS_ROOT_ONTOLOGY="https://harness-ontology.dev/data/<domain>" \
   /usr/bin/python3 <domain>/central/tools/validate.py     # PASS = full union OK
   ```

   The data repo's catalog maps `…/schema` → `central/ontology/tbox/harness.ttl`,
   each central `…/data/core/<type>` → `central/ontology/abox/core/<type>.ttl`
   (the core unit is split per component type), and `…/data/<domain>` → its local
   `<domain>.ttl`. Nothing in central changes.

2. **Run from central over all repos.** Clone the external data repo somewhere,
   then supply a catalog that lists `…/schema`, `…/data/core` **and**
   `…/data/<domain>` (pointing at the clone's `<domain>.ttl`), with a root
   ontology that imports all three. Point `HARNESS_CATALOG` /
   `HARNESS_ROOT_ONTOLOGY` at it. (Equivalently, temporarily add the
   `…/data/<domain>` entry back to central's catalog/root against the clone.)

Because a data repo carries its own catalog and imports (option 1), it is the
canonical "compose the full union" recipe and needs no edit to central.

## Recipe repos: composing harnesses from the neutral parts

The federated data-repo mechanism above has a concrete, first-class use: a
**recipe repo** that stores many harness **blueprints**, each `owl:imports`-ing
the central neutral parts and composing a complete `ho:Harness` from them (adding
only the domain bindings a specialization needs). This keeps central a neutral
parts library while "how the parts are assembled" lives in recipes. The first
such repo is `cpark90/harness-recipes` (renamed from the retired
`harness-data-lpranging`), whose worked example recipe reconstructs the retired
`lpranging` harness as a composition over the core parts. Its layout, the anatomy
of a recipe unit, and its clone-central → compose-union → central-`validate.py`
gate are specified in **`docs/recipes-design.md`**.
