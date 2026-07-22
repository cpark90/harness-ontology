# ODR BIND + Lock: implementation candidates, selection policy, reproducible locks

This document specifies the **BIND axis** and the **③ Lock** step of the
Ontology-Driven Regeneration methodology (`docs/feedback/inquiries/METHODOLOGY.md`)
as realised in this repo. It extends the build projection
(`docs/materialize-design.md` — read that first) with the machinery that lets one
neutral spec be realised by *different implementations over time* while staying
**reproducible**. It is the follow-up increment after EMIT (P1/P2) and roles /
implementation refs (P3/P4/P5).

METHODOLOGY.md names four axes — SPEC (what, tech-neutral), BIND (which
implementation), EMIT (deterministic render), VERIFY (spec-conformance) — and a
six-step cycle whose third step, **③ Lock**, snapshots "what was actually
selected this generation" so a build reproduces. The **SPEC** that these axes
render is *assembled* by the composition methodology
(`docs/composition-methodology.md`, workflow `wf-compose-harness`): composition
authors and validates the neutral spec, ODR BIND/EMIT/Lock render and reproduce
it. Before this increment the repo
had a strong SPEC and a deterministic EMIT but **no BIND layer and no lock**
(inspection's audit, METHODOLOGY.md §"가장 약한 지점" #1). This closes that gap.

## Where each axis lives (INV-1, INV-5)

| ODR axis | Artifact in this repo |
|---|---|
| **SPEC** (neutral, long-lived) | central `ontology/abox/core/` (the 64 neutral parts) + the neutral TBox *vocabulary*. Names a `ho:Tool` and the `ho:Capability` it provides — never a file, library, or version. |
| **BIND** (dated, replaceable) | **recipe-side** `ho:Candidate` individuals + `ho:selectionPolicy`, e.g. `staging/harness-recipes/recipes/lpranging/`. Which file/version realises a tool lives here. |
| **EMIT** (deterministic) | `tools/materialize.py` — READS spec+bind(+lock), writes the file tree. |
| **VERIFY** | `tools/validate.py` (SHACL/reachability/capability), run as materialize's pre-emit gate. |

The **vocabulary** for BIND is central (TBox terms below), because vocabulary is
neutral; the **individuals** (candidates, versions, policies) are recipe-side, so
the central SPEC never learns an implementation's name — **INV-1 spec purity**.
Dependency is one-way SPEC ← BIND ← EMIT (**INV-5**): materialize only reads.

## TBox vocabulary added (central, neutral)

- `ho:Candidate` (`rdfs:subClassOf ho:HarnessComponent`) — one implementation
  option for a Tool: a concrete `ho:implementationRef` (file/URL) plus
  `ho:candidateVersion` and `ho:candidateTag`.
- `ho:implementationCandidate` (Tool → Candidate) — associates a tool with an
  option.
- `ho:candidateVersion` / `ho:candidateTag` (Candidate → string).
- `ho:selectionPolicy` (Tool **or** Harness → string) — how EMIT picks when no
  lock is given (tool-level overrides harness-level default).
- `ho:implementationRef` — now carried by a **Candidate** (which file this option
  resolves to) or, degenerately, directly by a **Tool** (a single implicit
  candidate). Precedence: **explicit candidates > direct ref > stub**.

### Reachability without a bespoke shape (design note)

A `ho:Candidate` is a `ho:HarnessComponent`, so `ComponentConnectivityShape`
requires it to be wired into a harness (no orphans). The obvious move — making
`ho:implementationCandidate rdfs:subPropertyOf ho:hasComponent` — is **wrong
here**: `ho:hasComponent` has `rdfs:domain ho:Harness`, so under OWL RL the
*Tool* subject of the edge would be inferred a **Harness** (prp-dom) and trip
`HarnessShape` (a tool has no domain/task/workflow). This is the mirror of the
`rolePersona` domain-trip already recorded in the developer memory.

Instead a **property chain** rolls candidates up to the harness that binds the
tool:

```
ho:hasComponent owl:propertyChainAxiom ( ho:hasComponent ho:implementationCandidate )
```

so `harness hasComponent tool ∧ tool implementationCandidate cand ⇒ harness
hasComponent cand`. The candidate becomes an orphan-free component of the
**harness** (which is correctly a Harness), the tool is **not** mistyped, and no
new SHACL shape is needed. `ho:implementationCandidate` itself is a plain object
property (`rdfs:domain ho:Tool`, `rdfs:range ho:Candidate`), registered in
`ontology_lib` (`INSTANCE_CLASSES += Candidate`,
`INSTANCE_LINK_PREDICATES += implementationCandidate`) so retrieve/validate see it.

`ho:implementationRef` and `ho:selectionPolicy` carry **no `rdfs:domain`**: a
`Tool`-only domain would (prp-dom) mistype a Candidate carrying `implementationRef`
as a Tool, and a `selectionPolicy` usable on both Tool and Harness cannot have a
single conjunctive domain. Dropping the domain only removes inference; every user
is explicitly typed, so validation is unchanged (central stays **64** on both
loader paths).

## Selection policy — the deterministic ordering rule (④, principle 5)

When no lock is supplied, EMIT resolves each tool's candidates with a **total,
deterministic** order so `(spec + policy)` always yields the same choice:

1. **`pinned:<tag>`** — keep only candidates whose `candidateTag == <tag>`; if
   none, **hard error** (a pin that matches nothing is a misconfiguration).
2. **`latest-stable`** (the default) — prefer candidates tagged `stable`; among
   the chosen pool, pick the **highest** `candidateVersion`.
3. **`conservative`** — prefer `stable`; among the pool, pick the **lowest**
   `candidateVersion`.

Ties break by `candidateVersion` then candidate **IRI** (ascending), both total,
so the outcome never depends on set/dict iteration order. Version comparison
splits on `.`/`-`/`+`/`_`; numeric segments compare numerically and outrank
non-numeric labels (`1.10.0 > 1.9.0`). A tool-level `ho:selectionPolicy` overrides
a harness-level default; absent both, `latest-stable`.

**The policy set is CLOSED.** `latest-stable`, `conservative`, and `pinned:<tag>`
are the *only* accepted values; any other `ho:selectionPolicy` string is a **hard
error** naming the tool, the bad value, and the accepted set — exactly like a
`pinned:<tag>` that matches nothing. A misconfigured policy (a typo, an
unimplemented strategy) must never silently fall back to a default and quietly
pick something: silent fallback would let a spec think it pinned a strategy it
did not. The error is raised during selection resolution, before any file is
written, so a bogus policy refuses the build rather than emitting.

## The lock — ③ snapshot & reproducibility contract (INV-2)

Every build writes **`harness.lock.json`** into the output tree. It is the
immutable record of what was selected, fully deterministic (no timestamps, keys
sorted) so it is itself byte-identical across runs:

```json
{
  "lockVersion": 1,
  "spec": { "harness": "<IRI>", "prefLabel": "…", "individualCount": 83 },
  "tools": {
    "<tool IRI>": {
      "selected": "<candidate IRI | null for a direct ref>",
      "ref": "<file/URL>", "version": "…", "tag": "…",
      "policyApplied": "latest-stable | pinned:<tag> | conservative | direct-ref",
      "contentHash": "sha256:<hex of the copied file | null if stub>"
    }
  }
}
```

- **Emit a lock** (fresh, no `--lock`): resolve by policy, copy each selected
  file, hash it, record the snapshot.
- **Consume a lock** (`--lock <file>`): resolve **strictly** from it. Before
  emitting, the lock's **spec identity** (`harness` IRI + union `individualCount`)
  must match the current graph; each pinned candidate must still exist with the
  same `ref`; and after copying, each file's freshly-computed `contentHash` must
  equal the locked hash. **Any mismatch fails loudly** (non-zero exit, nothing
  half-written) — the lock either reproduces exactly or refuses. A lock never
  relaxes validation: the pre-emit `validate` gate still runs regardless.

### Atomic emit — the "nothing half-written" contract holds

"Nothing half-written" is now a **structural guarantee**, not a hope. The lock's
content-hash check runs mid-emit (after a file is copied), so a naive build that
wrote straight into `--out` would leave a partial tree (`.claude/agents/`,
`tools/<impl>`) on a hash mismatch. Instead `materialize()` builds the **whole
tree into a sibling temp staging dir** (`tempfile.mkdtemp` in `--out`'s parent,
so it is on the same filesystem) and runs every gate — selection-policy
resolution *and* the `--lock` content-hash check — while writing into staging.
Only on **full success** is staging placed at `--out` by an **atomic rename**
(`os.replace`): when `--out` does not exist this is a single atomic move; when it
pre-exists the old tree is renamed aside and removed only after the new tree is
in place (restored if the swap itself fails). On **any** failure the staging dir
is removed and `--out` is left **untouched** (or absent if it never existed) —
never a half-merged tree. Determinism and happy-path output are unchanged: the
staging path never enters any emitted file, so a fresh build is byte-identical to
before, and a pre-existing `--out` is cleanly replaced rather than partially
overwritten.

`policyApplied` is carried forward unchanged when reproducing (not relabelled to
"lock"), so a reproduced tree — lock file included — is **byte-identical** to the
original; the "reproduced from lock" fact lives in the build report, not in
mutated snapshot fields.

### Stable emitted filenames (behavioural equivalence, principle 2)

A candidate-backed tool emits a **stable** filename derived from the tool
(`tool-docgraph` → `tools/docgraph.py`, extension from the selected file), so
swapping the implementation candidate does **not** rename the file or break
callers — the same tool "slot" is realised by a different implementation, which is
exactly ODR's behavioural-equivalence notion of "same software". A degenerate
direct-ref tool keeps its ref's basename (preserving increment-1/2 behaviour).

## Worked evidence — lpranging (INV-2, INV-4, principle 5)

`recipes/lpranging/` binds `tool-docgraph` to two candidates —
`cand-docgraph-stable` (`impl/docgraph.py`, tag `stable`, v1.4.0) and
`cand-docgraph-next` (`impl/docgraph_v2.py`, tag `next`, v2.0.0) — with
`ho:selectionPolicy "latest-stable"`; `tool-simulator` stays a single direct ref
(the degenerate path). Composing over the central union validates (83 individuals
= 81 + 2 candidates).

- **Fresh build A** (`--out A`): `latest-stable` → `cand-docgraph-stable` (the
  only `stable` tag) → `tools/docgraph.py` = the proven impl; `A/harness.lock.json`
  written.
- **Reproduce B** (`--out B --lock A/harness.lock.json`): `diff -r A B` is
  **empty** — byte-identical reproduction (**INV-2**).
- **Determinism**: a second fresh build equals A byte-for-byte (**principle 5**).
- **INV-4 (replacement harmlessness)**: switching the policy to `pinned:next`
  makes `tools/docgraph.py` hold the **v2** implementation (selection observably
  changed), yet the compose `validate` **and** the emit still PASS — a different
  binding under the same spec keeps verification passing.
- **Contract**: tampering with a lock's `contentHash` or `individualCount` makes
  a `--lock` build **refuse** (exit 1).

## ODR maturity reached

Per METHODOLOGY.md §6 this increment brought the project to **level 2
(재현 가능 / reproducible via lock)**: level 1 (재생성 가능 / deterministic
regeneration, principle 5) is shown by A == A2, and level 2 by A == B from the
lock alone. The follow-up **contract-VERIFY increment
([`docs/odr-contract-verify.md`](odr-contract-verify.md))** then advanced the
project to **levels 3–4 demonstrated**: `validate.py` proves the *graph* is
well-formed, but capabilities now also carry verifiable **`ho:Contract`s** that
`tools/verify_contract.py` runs against the emitted tree — level 3 (부합 검증) by
the auto-judged lpranging contracts, and level 4 (기술 독립 실증 / INV-4) by the
`contract-demo` recipe, where re-binding a tool to a different implementation
candidate keeps the same spec contract passing (verification depends on the SPEC,
not the chosen implementation). Level 5 (dual document + software targets) is
partially realised (CLAUDE.md/agents/scaffold docs + `tools/*.py` code) and
tracked in `docs/materialize-design.md`.
