# V&V verdict — ODR BIND + Lock increment + lpranging re-reflection

- **Scope**: the ODR BIND axis + ③ Lock increment — TBox terms (`ho:Candidate`,
  `ho:implementationCandidate`, `ho:candidateVersion`, `ho:candidateTag`,
  `ho:selectionPolicy`; `ho:hasComponent` property chain; `ho:implementationRef`
  domain removal), `tools/materialize.py` (policy resolution + lock), `tools/ontology_lib.py`
  registration, and the `staging/harness-recipes/recipes/lpranging/` recipe (2 candidates,
  vendored `harness.lock.json`).
- **Judged against**: `docs/feedback/inquiries/METHODOLOGY.md` (ODR invariants/maturity) and
  `docs/odr-bind-lock.md`.
- **Interpreter**: `/usr/bin/python3` (rdflib/pyshacl/owlrl present).
- **Verdict**: **pass-with-notes**. All 7 requested checks reproduce as claimed. Two notes,
  both on the failure path / robustness, neither undermines neutrality, validation, or the
  level-2 reproducibility claim.

---

## 1. Central neutrality & structure — PASS

```
/usr/bin/python3 tools/validate.py            -> PASS; "all 64 individuals reachable"; SHACL/reachability/capabilities all ✓
loader equivalence: catalog=64 individuals ; HARNESS_CATALOG=/nonexistent glob-fallback=64  (agree)
grep -rn 'Candidate|implementationCandidate|selectionPolicy|cand-|candidateVersion|candidateTag' ontology/abox/core/  -> 0 hits
retrieve.py "multi-agent orchestration harness" --format json -> top candidate "Multi-agent orchestration harness", pack intact
```
Central SPEC stays 64 on both loader paths; no BIND vocabulary or candidate individual leaked
into `ontology/abox/core/` (**INV-1 spec purity**). Retrieve smoke unaffected.

## 2. TBox design soundness — the ratified deviation — PASS

New terms (git diff, `-U0`): **exactly** `ho:Candidate`, `ho:implementationCandidate`,
`ho:candidateVersion`, `ho:candidateTag`, `ho:selectionPolicy` — no more, no fewer. Domains
(rdflib): `implementationCandidate→Tool`, `candidateVersion/candidateTag→Candidate`,
`selectionPolicy→[]` (none), `implementationRef→[]` (domain **removed**, was `ho:Tool`).
`ho:hasComponent` gains `owl:propertyChainAxiom ( ho:hasComponent ho:implementationCandidate )`.
Each new term is used in the recipe (Candidate×2, implementationCandidate on tool-docgraph,
version/tag on both candidates, selectionPolicy on tool-docgraph).

**Property-chain type check** (reasoned lpranging union, `load_graph(reason=True)`):
```
tool-docgraph rdf:types = ['HarnessComponent', 'Thing', 'Tool']   # NOT ho:Harness
tool-docgraph IS ho:Harness?  False
cand-docgraph-stable: harness hasComponent it? True | Candidate? True | Harness? False | Tool? False
cand-docgraph-next  : harness hasComponent it? True | Candidate? True | Harness? False | Tool? False
tool-simulator IS ho:Harness? False
```
The chain rolls both candidates up to `h-lpranging` as `hasComponent` objects (orphan-free,
SHACL-valid) **without** mistyping the Tool as a Harness — so `HarnessShape` is not tripped.
Shapes unchanged: `git status ontology/shapes/` = no tracked modifications; `grep sh:closed
ontology/shapes/` = none. No new/weakened shape.

**Judgment (a)**: the deviation from the brief's original `implementationCandidate
rdfs:subPropertyOf ho:hasComponent` idea to a `propertyChainAxiom` is **sound and should be
ratified**. The sub-property route would (via `hasComponent rdfs:domain ho:Harness`, prp-dom)
infer the *Tool* subject to be a `ho:Harness` and trip `HarnessShape` — the exact mirror of the
recorded `rolePersona` domain-trip. The chain achieves reachability with no mistyping and no new
shape; verified empirically above. The parallel `implementationRef`/`selectionPolicy` domain
removals are also correct (a `Tool` domain would mistype a Candidate carrying `implementationRef`;
`selectionPolicy` legitimately applies to both Tool and Harness) — every user is explicitly
typed, central stays 64 on both loaders, so validation is unchanged.

## 3. BIND / policy correctness — PASS

Compose (temp `central` symlink → repo, removed after):
```
compose validate (union) -> PASS; "all 83 individuals reachable"   (81 + 2 candidates)
materialize h-lpranging (no lock) -> A
  Design-graph tool: cand-docgraph-stable [latest-stable] -> tools/docgraph.py
cmp A/tools/docgraph.py recipes/lpranging/impl/docgraph.py     -> IDENTICAL   (stable picked)
cmp A/tools/docgraph.py recipes/lpranging/impl/docgraph_v2.py  -> differ @ byte 36 (exit 1)
```
`latest-stable` deterministically selected the only `stable`-tagged candidate (v1.4.0); the
emitted file is byte-identical to the proven `impl/docgraph.py` and differs from the v2 rewrite.
Emitted filename is the stable tool-derived `tools/docgraph.py` (behavioural equivalence).

## 4. Lock reproducibility (INV-2, principle 5) — PASS

```
diff recipes/lpranging/harness.lock.json  A/harness.lock.json          -> identical (vendored == fresh)
materialize --lock recipes/lpranging/harness.lock.json --out B ; diff -r A B  -> empty (A == B, INV-2)
materialize (2nd fresh) --out A2 ; diff -r A A2                        -> empty (A == A2, principle 5 determinism)
```
Tamper (scratch copies; **vendored lock never modified** — confirmed pristine via git status):
```
lock w/ contentHash -> sha256:000...0 : exit 1, "REFUSING ... lock content-hash mismatch ... (INV-2)"
lock w/ individualCount=999           : exit 1, "REFUSING ... individualCount=999 but ... 83 ... (INV-2)"
```
Both refuse loudly (non-zero exit, no successful build).

**Note N1 (failure-path atomicity, not a functional defect).** The two tamper paths differ in
cleanliness. The `individualCount` tamper fails in `_verify_lock_spec` *before any write* → out
dir is empty. The `contentHash` tamper fails **after** `shutil.copyfile`, because the per-tool
hash gate in `emit_implementations` runs after the copy; the out dir is left with partial
artifacts — `.claude/agents/{developer,inspection,vnv}.md` and the copied `tools/docgraph.py`,
but **no** `CLAUDE.md`, `MANIFEST.json`, or `harness.lock.json`. This contradicts the wording
"nothing half-written" in `docs/odr-bind-lock.md` §"The lock". The *reproducibility contract*
still holds (a tampered lock can never silently emit a divergent complete build — exit 1, no
completing files), so this is a robustness/wording nit, not an INV-2 break. Recommend either
hashing all selected files against the lock before any emit, or emitting to a temp dir + atomic
move, or softening the doc claim. → route to developer/orchestrator if the atomicity guarantee
is desired.

## 5. INV-4 (replacement harmlessness) — PASS

Scratch recipe copy, policy switched `latest-stable`→`pinned:next` (shipped recipe untouched):
```
compose validate (pinned:next)        -> PASS
materialize -> SWAP ; Design-graph tool: cand-docgraph-next [pinned:next] -> tools/docgraph.py
cmp SWAP/tools/docgraph.py recipes/lpranging/impl/docgraph_v2.py -> IDENTICAL (v2 selected)
cmp SWAP/tools/docgraph.py recipes/lpranging/impl/docgraph.py    -> differ (exit 1)
emitted filename: tools/docgraph.py  (STABLE — same slot, different impl)
```
A different binding under the same spec: the emitted implementation observably changes to v2,
the filename does **not** change (callers unaffected), and **both** compose-validate and emit
still PASS — verification is unchanged by re-binding (**INV-4**).

**Note N2 (minor, soft-fallback).** `select_candidate` treats "latest-stable and any
**unrecognised** policy" identically (`ordered[-1]`) — a typo'd policy string silently behaves as
`latest-stable` rather than hard-erroring (unlike `pinned:<tag>`, which correctly hard-errors on
no match). Documented behavior, but it can mask a misconfigured policy. Non-blocking; optional
hardening (warn/error on unknown policy).

## 6. Full-tree re-reflection — PASS

`A/` tree carries every ODR axis:
```
CLAUDE.md              -> ## Persona / ## Operating rules (incl. "Korean/English only" language
                          bullets) / ## Process / ## Model / ## Roles
.claude/agents/        -> developer.md, inspection.md, vnv.md
tools/docgraph.py      -> real code via candidate (764 lines, resolved), sim_grid_reservation.py (277)
DESIGN_HARNESS_STANDARD.md, docs/README.md   -> scaffold fragments (2)
MANIFEST.json          -> components/capabilityBindings(6)/implementations(2 resolved)/roles(3)/
                          scaffold(2)/derivedFrom/templateSources/tokenEstimate
harness.lock.json      -> spec identity + per-tool selected/ref/version/tag/policyApplied/contentHash
```
Vendored lock hashes match the vendored `impl/` files (recomputed sha256):
`tool-docgraph → sha256:a0b5e722…` = `impl/docgraph.py`; `tool-simulator → sha256:c6639c37…`
= `impl/sim_grid_reservation.py`. `ho:tokenEstimate` present on the new text-bearing nodes
(11 occurrences in the recipe; candidates, tools, personas all carry it).

## 7. ODR invariants overall — PASS

- **INV-1** (spec purity): core grep = 0; the BIND *vocabulary* is central+neutral (names a
  Class, not a file), the BIND *individuals* (candidates, refs, versions, policy) live recipe-side.
- **INV-5** (one-way SPEC ← BIND ← EMIT): materialize wrote only to scratch `--out` dirs; git
  status shows the only modified tracked files are the intended increment edits
  (`harness.ttl`, `materialize.py`, `ontology_lib.py`) — no writes into `ontology/` or the
  shipped recipe.
- **INV-2 / principle 5**: shown in §4 (A==B from lock; A==A2 determinism; tamper refused).

**Judgment (b)**: the increment **legitimately reaches ODR maturity level 2 (재현 가능 /
reproducible via lock)**. Level 1 (determinism) is proven by A == A2; level 2 by A == B from the
lock alone, plus loud refusal on a tampered lock. Levels 3–4 are correctly declared **open** in
`docs/odr-bind-lock.md` — `validate.py` proves the *graph* is well-formed, not that an emitted
artifact satisfies a capability's *contract*; contract-VERIFY (INV-3) and an artifact-level INV-4
proof are the next axis. The doc's scoping is honest and matches the evidence.

---

## Reproduction (all commands, `/usr/bin/python3`)

```
# central
/usr/bin/python3 tools/validate.py
HARNESS_CATALOG=/nonexistent /usr/bin/python3 -c "import importlib,tools.ontology_lib as l; importlib.reload(l); g=l.load_graph(); print(len(l.instance_nodes(g)))"

# compose (temp symlink, removed after)
ln -sfn "$(pwd)" staging/harness-recipes/central ; cd staging/harness-recipes
HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging /usr/bin/python3 central/tools/validate.py
# type check: PYTHONPATH=central/tools /usr/bin/python3 -c "... load_graph(reason=True); query rdf:type of tool-docgraph ..."
# no-lock build A, cmp vs impl/docgraph.py & impl/docgraph_v2.py
/usr/bin/python3 central/tools/materialize.py h-lpranging --out <A>
# reproduce B from vendored lock; diff -r A B
/usr/bin/python3 central/tools/materialize.py h-lpranging --lock recipes/lpranging/harness.lock.json --out <B>
# tamper scratch locks (contentHash / individualCount) -> exit 1
# INV-4: cp recipe to scratch, swap selectionPolicy latest-stable->pinned:next, materialize, cmp vs docgraph_v2.py
rm -f staging/harness-recipes/central   # cleanup
```

All temp symlinks and scratch copies created for this verdict were removed; the vendored recipe
and lock are pristine (git status clean for `staging/harness-recipes/recipes/lpranging/`).
