# ODR contract-VERIFY: spec contracts + artifact judgment (maturity 3–4)

This document specifies the **VERIFY axis** of Ontology-Driven Regeneration
(`docs/feedback/inquiries/METHODOLOGY.md`) as realised in this repo, and how it
advances the project to ODR **maturity levels 3 (부합 검증) and 4 (기술 독립
실증)**. Read `docs/odr-bind-lock.md` (BIND + Lock, levels 1–2) and
`docs/materialize-design.md` (EMIT) first — VERIFY is the follow-up increment.

METHODOLOGY.md names four axes — SPEC (what, tech-neutral), BIND (which
implementation), EMIT (deterministic render), **VERIFY (spec-conformance)** — and
principle 3 (명세-검증 일원화): *a spec is not an assertion but a verifiable
contract*, and the same spec is both the input to generation and the criterion of
verification. Before this increment the repo had SPEC, BIND+Lock and a
deterministic EMIT, plus `validate.py` — but `validate.py` proves the **graph** is
well-formed, not that an **emitted artifact** satisfies a capability's contract.
This increment closes that: capabilities carry **verifiable contracts**, and
`tools/verify_contract.py` judges the materialized tree against them.

## Where the VERIFY axis lives (INV-1, INV-3, INV-5)

| ODR concern | Artifact in this repo |
|---|---|
| **Contract vocabulary** (neutral) | central TBox: `ho:Contract`, `ho:capabilityContract`, `ho:contractKind`, `ho:contractCheck`. |
| **The contracts** (spec-side) | **recipe-side** `ho:Contract` individuals on a `ho:Capability` via `ho:capabilityContract` (e.g. `recipes/lpranging/`, `recipes/contract-demo/`). |
| **The judge** (deterministic) | `tools/verify_contract.py` — READS the union for contracts, RUNS them against a materialized tree, emits a pass/fail verdict. |

As with BIND, the **vocabulary** is central (neutral) while the **individuals**
are recipe-side, so the central SPEC never names an implementation (**INV-1**).
A contract hangs off a **Capability**, not a chosen implementation candidate, so
the verification criterion comes only from the spec (**INV-3 verification
independence**) and re-binding to a different candidate cannot change the verdict
(**INV-4 replacement harmlessness**). Dependency stays one-way SPEC ← … ← VERIFY:
`verify_contract.py` only reads the graph and the tree (**INV-5**).

## The Contract model (TBox, central)

- `ho:Contract` (`rdfs:subClassOf ho:HarnessComponent`) — a verifiable spec
  contract. Carries `ho:contractKind` and `ho:contractCheck`, plus the usual
  `skos:prefLabel` + `skos:definition`.
- `ho:capabilityContract` (`ho:Capability` → `ho:Contract`) — attaches a
  contract to a capability.
- `ho:contractKind` (`ho:Contract` → string) — `"executable"` or `"structural"`.
  A contract chooses exactly one; a capability may carry several contracts mixing
  both kinds.
- `ho:contractCheck` (`ho:Contract` → string) — the check, interpreted per kind
  (grammar below).

### Reachability without a bespoke shape

A `ho:Contract` is a `ho:HarnessComponent`, so `ComponentConnectivityShape`
requires it to be wired into a harness. Rather than a new shape, a **property
chain** on `ho:hasComponent` rolls contracts up to the harness that binds the
capability's provider:

```
ho:hasComponent owl:propertyChainAxiom
    ( ho:hasComponent ho:providesCapability ho:capabilityContract )
```

so `harness hasComponent component ∧ component providesCapability cap ∧ cap
capabilityContract contract ⇒ harness hasComponent contract`. The chain is
**prefixed with `hasComponent`** (three links) so the inferred subject is always
the Harness. A tempting two-link chain `( providesCapability capabilityContract )`
would instead conclude `component hasComponent contract` and — via
`hasComponent`'s `rdfs:domain ho:Harness` (prp-dom) — **mistype the provider
component as a Harness**, tripping `HarnessShape`. This mirrors the `ho:Candidate`
rollup (`docs/odr-bind-lock.md`) exactly. `ho:capabilityContract` is a plain
object property (`rdfs:domain ho:Capability`, `rdfs:range ho:Contract`),
registered in `ontology_lib` (`INSTANCE_CLASSES += Contract`,
`INSTANCE_LINK_PREDICATES += capabilityContract`). Central individual count is
unchanged (**96** on both loader paths): the vocabulary adds no instances.

## The two verification mechanisms (per-contract choice)

`verify_contract.py <harness-id> --tree <materialized-out-dir> [--format text|json]`
collects the harness's capability contracts (the capabilities it *requires* plus
the ones its components *provide*), then dispatches on `ho:contractKind`:

### executable

`ho:contractCheck` is a shell command run with **CWD = the materialized tree
root**; the contract **passes iff the command exits 0**. Output is captured (not
streamed) and a bounded timeout (120 s) refuses a hung check. Use this for real
behavioural checks — running the emitted tool and asserting its behaviour.

Examples:
- `python3 -c "import ast; ast.parse(open('tools/docgraph.py').read())"` — the
  emitted tool is a syntactically valid module (a tech-neutral "artifact is
  runnable" check).
- `python3 tools/greeter.py | grep -q 'hello world'` — running the emitted tool
  prints the expected greeting (a behavioural check that any correct candidate
  satisfies).

### structural

`ho:contractCheck` is a declarative assertion evaluated against the tree, in this
grammar (paths are **tree-relative**; a path that escapes the tree via `..` or an
absolute prefix is refused):

| assertion | passes iff |
|---|---|
| `file-exists:<path>` | `<path>` exists under the tree |
| `file-contains:<path>::<substring>` | `<path>` is a file and contains the literal `<substring>` |
| `section:<path>::<heading>` | `<path>` has a Markdown heading line whose text equals `<heading>` |

`section` compares on the **hash-stripped heading text**, so
`section:CLAUDE.md::Coordination channels` and
`section:CLAUDE.md::## Coordination channels` both match the line
`## Coordination channels`.

### Reporting / determinism

Contracts are processed in **IRI-sorted** order, so the report is deterministic.
The text report lists each contract's kind, label, capability, the check string
and a pass/fail detail; `--format json` adds captured detail for CI. **Exit code
is non-zero iff any contract fails.** A harness with no contracts verifies as a
vacuous `0/0 — PASS` (verification is opt-in per capability).

## Worked evidence

### Level 3 — 부합 검증 (faithful `lpranging`)

`recipes/lpranging/` (the faithful reflection of a real source harness — single
faithful impls, **no synthetic candidates**) gets three contracts on its domain
capabilities:

- `cap-designgraph` → `contract-docgraph-emitted` (**structural**
  `file-exists:tools/docgraph.py`) and `contract-docgraph-parses`
  (**executable** AST parse-check of the emitted tool).
- `cap-simulation` → `contract-simulation-bound` (**structural**
  `file-contains:MANIFEST.json::cap-simulation`).

`materialize.py h-lpranging` then `verify_contract.py h-lpranging --tree <out>`
→ **3/3 PASS** (exit 0). Removing the emitted tool makes the executable contract
**FAIL** (exit 1) — the judge actually judges the artifact. Verdicts are
deterministic across runs; the materialize tree stays byte-identical (A == A2).
lpranging remains faithful — contracts were added, not candidates.

### Level 4 / INV-4 — 기술 독립 실증 (`contract-demo`)

`recipes/contract-demo/` is a **deliberate demonstrator** (not a faithful
reflection): one tool `tool-greeter` provides `cap-greet` and carries **two
implementation candidates** — `cand-greeter-stable` (`impl/greeter_v1.py`, tag
`stable`, v1.0.0, a direct `print`) and `cand-greeter-next` (`impl/greeter_v2.py`,
tag `next`, v2.0.0, a function-built print) — with `ho:selectionPolicy`. Both emit
the **same greeting** from **different source**. `cap-greet` carries a structural
(`file-exists:tools/greeter.py`) and an executable behavioural
(`python3 tools/greeter.py | grep -q 'hello world'`) contract.

- Build A, policy `latest-stable` → `cand-greeter-stable` → `tools/greeter.py` is
  v1 → `verify_contract` **PASS** (2/2).
- Re-bind, policy `pinned:next` → `cand-greeter-next` → `tools/greeter.py` is v2
  (the emitted file **differs**) → `verify_contract` **PASS** (2/2), with
  **per-contract verdicts identical** to build A.

Different implementation, identical verdict: verification depended on the SPEC
(the capability's contract), not on the chosen implementation — this is the
**INV-4** evidence and the point (METHODOLOGY.md §6.4) at which the methodology's
core claim ("기술은 바뀌어도 같은 소프트웨어") is *demonstrated*. The emitted
filename is a stable slot (`tools/greeter.py`) across candidates, so the swap
changes content, not callers (behavioural equivalence, principle 2).

## ODR maturity reached

This increment advances the project from level 2 to **levels 3–4 demonstrated**:
level 3 (부합 검증) by the auto-judged lpranging contracts, level 4 (기술 독립
실증 / INV-4) by the `contract-demo` candidate swap keeping the same contracts
passing. Level 5 (dual document + software targets) remains partially realised
(CLAUDE.md/agents/scaffold docs + `tools/*.py` code), tracked in
`docs/materialize-design.md`.
