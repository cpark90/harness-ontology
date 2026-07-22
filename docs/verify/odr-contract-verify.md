# VERDICT — ODR contract-VERIFY axis (maturity levels 3–4)

- **Scope**: independent verification of the contract-VERIFY increment — TBox
  `ho:Contract` + property-chain reachability, `tools/verify_contract.py`, and the
  level-3 (`lpranging`) / level-4 (`contract-demo`) demos.
- **Verdict**: **pass-with-notes**. This legitimately demonstrates ODR **maturity
  level 3 (부합 검증 / contract-checked)** and **level 4 (기술 독립 실증 / INV-4)**.
- **Agent**: vnv. **Interpreter**: `/usr/bin/python3` (has rdflib/pyshacl/owlrl).
- **Method**: ran the tools against materialized trees; all temp symlinks/scratch
  removed; edited no `ontology/`, `tools/`, or `docs/` under review (only this report).

---

## 1. Central neutrality + structure (PASS)

| check | command | result |
|---|---|---|
| central validate | `tools/validate.py` | **PASS**, `all 96 individuals reachable`, SHACL conforms, capabilities satisfied |
| both loader paths agree | catalog-closure vs legacy glob (`HARNESS_CATALOG=/nonexistent`) instance count | **96 == 96** |
| contract terms absent from central abox | `grep -rn "capabilityContract\|ho:Contract\|contract-\|contractKind\|contractCheck" ontology/abox/` | **0 hits** |
| `ho:Contract` instances in central | `subjects(RDF.type, HO.Contract)` on central union | **0** |
| retrieve smoke | `tools/retrieve.py "design graph" --format json` | valid pack (keys: request/terms/seeds/nodes/edges/candidates/gaps/budget); **0** build-only props leaked (`contractCheck\|contractKind\|capabilityContract\|implementationRef\|selectionPolicy`) |

Vocabulary is central+neutral; the contract *individuals* are recipe-side. Central
instance count is unchanged at 96 — INV-1 (spec purity) holds.

## 2. TBox soundness — property-chain, no mistype (PASS)

- TBox diff is contained: `git diff --stat ontology/` = **only `harness.ttl`** (+25/−1).
  New terms exactly as listed: `ho:Contract`, `ho:capabilityContract`,
  `ho:contractKind`, `ho:contractCheck`, plus one added `owl:propertyChainAxiom`
  line on `ho:hasComponent`. **`ontology/shapes/` has no diff** — no bespoke shape
  added, nothing `sh:closed` weakened.
- 3-link chain `( ho:hasComponent ho:providesCapability ho:capabilityContract )`.
  Verified against the reasoned (`reason=True`) `lpranging` union:

| node | rdf:types (short) | is `ho:Harness`? |
|---|---|---|
| `h-lpranging` | Harness | yes (correct) |
| `tool-docgraph` (provider) | Tool, HarnessComponent, Thing | **no** (not mistyped) |
| `tool-simulator` (provider) | Tool, HarnessComponent, Thing | **no** |
| `cap-designgraph` / `cap-simulation` (chain middle) | Capability | **no** |
| `contract-docgraph-emitted` / `-parses` / `-simulation-bound` | Contract, HarnessComponent | rolled up: `h-lpranging ho:hasComponent contract` = **True** |

The chain makes each Contract a reachable, orphan-free `HarnessComponent`
(`lpranging` union validates: `all 119 individuals reachable`) **without**
mistyping the provider component or the capability as a Harness. The hasComponent
prefix correctly puts the inferred subject on the Harness — the two-link mistype
trap is avoided, mirroring the `ho:Candidate` rollup.

## 3. Level 3 — 부합 검증 (`lpranging`, contract-checked) (PASS)

`materialize.py h-lpranging` → `verify_contract.py h-lpranging --tree <t>`:

```
✓ [structural] Design-graph tool is emitted        file-exists:tools/docgraph.py            -> exists
✓ [executable] Design-graph tool is a valid module python3 -c "import ast; ast.parse(...)"  -> exit 0
✓ [structural] Design-simulation capability bound  file-contains:MANIFEST.json::cap-simulation -> substring present
3/3 contracts passed — PASS   (exit 0)
```

**Induced FAIL** (judge judges the *artifact*, not the graph): on a COPY of the
tree, `rm tools/docgraph.py` →

```
✗ [structural] Design-graph tool is emitted   -> missing: tools/docgraph.py
✗ [executable] Design-graph tool is a valid module -> exit 1: FileNotFoundError ... 'tools/docgraph.py'
✓ [structural] Design-simulation capability bound -> substring present
1/3 contracts passed — FAIL   (exit 1)
```

The union still `validate.py`-PASSes while the broken tree FAILs verify —
verification is a **separate step** operating on the emitted artifact, exactly as
the methodology (원리 3 / §5 검증) requires.

Determinism: two independent materialize runs are `diff -r` **identical**;
`verify_contract` is **byte-identical** on a repeat of the same tree, and
**per-contract verdicts are identical** across the two builds (the JSON differs
only in the embedded absolute `tree` path field, which is metadata, not a verdict).

## 4. Level 4 / INV-4 — 기술 독립 실증 (`contract-demo`) (PASS — the core claim)

`cap-greet` carries a structural (`file-exists:tools/greeter.py`) and an
executable behavioural (`python3 tools/greeter.py | grep -q 'hello world'`)
contract. One tool `tool-greeter`, two candidates.

| build | policy | selected | emitted `tools/greeter.py` | verify |
|---|---|---|---|---|
| A | `latest-stable` (shipped) | `cand-greeter-stable` (v1.0.0) | v1 — bare `print("hello world")` | **2/2 PASS** (exit 0) |
| B | `pinned:next` (scratch recipe copy) | `cand-greeter-next` (v2.0.0) | v2 — `greet()` fn + `__main__` guard | **2/2 PASS** (exit 0) |

- The two candidate *sources* genuinely differ (`diff impl/greeter_v1.py
  impl/greeter_v2.py` → differ), and the two *emitted* files differ
  (`diff demoA/tools/greeter.py demoB/tools/greeter.py` → differ).
- Both emitted tools actually run and print `hello world` (behaviour identical).
- The verdict is **identical PASS** per-contract; the filename slot
  `tools/greeter.py` is stable across candidates (swap changes content, not callers).

Different implementation, identical verdict → verification depended on the SPEC
(the capability's contract), not on the chosen candidate. This is genuine **INV-4
(교체 무해성)** / **INV-3 (검증 독립성)** evidence and is the point where the
methodology's core claim ("기술은 바뀌어도 같은 소프트웨어") is *demonstrated*,
not merely asserted. (Re-bind was effected via the existing BIND-axis
`ho:selectionPolicy` `pinned:next`, on a scratch copy of the recipe; the shipped
recipe stays `latest-stable` and pristine.)

## 5. Determinism / hygiene / safety (PASS)

- **Structural grammar rejects escapes** (`verify_contract.eval_structural`):
  `../../../etc/passwd`, `/etc/passwd`, `../../CLAUDE.md`, `../README.md` all
  **refused** ("escapes the tree"); an in-tree `tools/../tools/docgraph.py`
  normalises inside and is allowed; malformed / unknown ops rejected with a
  detail, not a crash.
- **Refusals**: bogus harness id → **exit 2**; `--tree` not a directory → **exit 2**;
  no-contract harness (`h-research`) → **vacuous 0/0 PASS**, exit 0.
- **Staging symlink-free at rest**: `find staging -type l` = none after cleanup.
- **Executable subprocess model**: `subprocess.run(shell=True, cwd=tree,
  capture_output=True, timeout=120)`, non-zero on any failure. **Judged sound and
  bounded** for its trust model: the check strings come from *spec-side* recipe TTL
  (authored/reviewed), so it is the same trust surface as running a repo's test
  suite in CI. The 120 s timeout refuses hangs; output is captured, not streamed;
  cwd is pinned to the tree. See Note N2 for the boundary.

## 6. Docs / maturity (PASS)

- `docs/odr-contract-verify.md` documents the Contract model, both mechanisms, the
  structural grammar (incl. the hash-stripped `section` heading rule), the 3-link
  chain + two-link mistype rationale, and both worked demos.
- `docs/odr-bind-lock.md` §"ODR maturity reached" is honestly updated to
  **"levels 3–4 demonstrated"** with the contract-VERIFY increment cited.

---

## Notes (non-blocking)

- **N1 — structural contracts are shallow by construction.**
  `file-contains:MANIFEST.json::cap-simulation` (the `cap-simulation` level-3
  contract) asserts the build *names* the capability in its manifest; it does not
  exercise simulation behaviour. This is correct for a `structural` kind (it checks
  wiring/presence), but it is close to tautological since `materialize` always
  writes `capabilityBindings`. Behavioural depth belongs in `executable` contracts
  (as the docgraph parse-check and the greeter behavioural check do). Not a defect;
  a reminder that a capability wanting a strong guarantee should carry at least one
  `executable` contract, not only structural ones.
- **N2 — executable contracts run arbitrary shell from the graph.** Sound within
  the repo's trust model (recipes are authored spec, same as CI test commands), but
  worth stating explicitly: `verify_contract.py` must only run over **trusted**
  recipe graphs; a hostile `ho:contractCheck` would execute on the verifier. The
  `structural` kind is the sandboxed alternative (path-escape-refused, no shell).
  No code change requested — this is an operational boundary to document.
- **N3 — re-bind ergonomics.** There is no `verify_contract`/`materialize` CLI flag
  to override `ho:selectionPolicy`; the INV-4 swap is done by editing the recipe's
  policy (BIND axis). This is by design (selection is a graph fact), and the
  mechanism (`pinned:<tag>`) works; noted only so future INV-4 demos know to copy
  the recipe rather than expect a `--policy` switch.

## Reproduction (commands actually run)

```
# central
/usr/bin/python3 tools/validate.py
PYTHONPATH=tools /usr/bin/python3 -c "<count INSTANCE_CLASSES subjects>"          # 96
PYTHONPATH=tools HARNESS_CATALOG=/nonexistent-catalog.xml /usr/bin/python3 ...    # 96 (glob path)

# recipe unions (temp symlink central -> repo root inside staging/harness-recipes,
# removed after; env: HARNESS_CATALOG=catalog-v001.xml, PYTHONPATH=central/tools)
HARNESS_ROOT_ONTOLOGY=.../recipes/lpranging      validate.py                       # PASS, 119 reachable
HARNESS_ROOT_ONTOLOGY=.../recipes/contract-demo  validate.py                       # PASS, 107 reachable
materialize.py h-lpranging --out <t>  ;  verify_contract.py h-lpranging --tree <t> # 3/3 PASS
  (copy tree, rm tools/docgraph.py) verify_contract ...                            # 1/3 FAIL, exit 1
materialize.py h-contract-demo --out demoA ; verify_contract ...                   # A: v1, 2/2 PASS
  (scratch recipe copy, sed selectionPolicy -> pinned:next) materialize demoB ...  # B: v2, 2/2 PASS
```

Routing: no ontology defect found. Notes N1–N3 are documentation/operational, for
orchestrator's awareness — none requires developer re-authoring to reach levels 3–4.
