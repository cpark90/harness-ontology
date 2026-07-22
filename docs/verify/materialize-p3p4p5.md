---
title: vnv verdict — materialize increment 2 (P3 implementationRef / P4 roles / P5 scaffold)
verdict: pass
date: 2026-07-22
scope: TBox ho:Role + 7 props; tools/ontology_lib.py; tools/materialize.py; lpranging recipe; docs/materialize-design.md
interpreter: /usr/bin/python3 (rdflib/pyshacl/owlrl present)
---

# Verdict: PASS

The P3/P4/P5 materialize increment is built to spec (verification) and does the
right thing (validation). All 6 requested checks reproduced with evidence below.
No ontology/tools/docs edited; no git run; the one temp `central` symlink was
removed and no at-rest symlink remains under `staging/`.

## 1. Structural / neutrality — PASS

`/usr/bin/python3 tools/validate.py` (central, unchanged):

```
loaded graph: 1564 triples (post-reasoning)
✓ SHACL conforms  ✓ all 64 individuals reachable  ✓ capabilities  → PASS
```

- Central abox count **64**, unchanged (role individuals live in the recipe, not central).
- `grep -rnE "hasRole|implementationRef|role-|ho:Role|rolePersona|scaffold" ontology/abox/core/` → **0** hits. Central stays neutral.
- `retrieve.py "multi-agent orchestration design"` smoke: exit 0, budget 894/900,
  base candidate "Multi-agent orchestration harness" — READ projection unaffected
  (build-only props implementationRef/scaffold are ignored by retrieve, as designed).

## 2. Anti-drift on TBox — PASS (design points sound)

New schema terms are exactly **1 class + 7 properties** and nothing else:
`ho:Role`; `ho:hasRole, ho:rolePersona, ho:roleTool, ho:roleGuardrail,
ho:roleMemoryPolicy, ho:implementationRef, ho:scaffold`. Each is exercised by the
lpranging recipe (roles / tool refs / harness scaffold), so none is a dangling
vocabulary orphan. All carry `rdfs:label` + `skos:definition`.

Two load-bearing design decisions, both verified sound:

- **`ho:hasRole rdfs:subPropertyOf ho:hasComponent`** (harness.ttl:158). This is
  what makes a `ho:Role` individual harness-reachable and SHACL-valid **without a
  new shape**. Evidence: `ontology/shapes/harness-shapes.ttl` is **byte-identical
  to the initial commit** (`git diff cb33d45 HEAD -- ontology/shapes/…` = empty) —
  no shape was added or weakened — yet the composed union (§3) validates with the 3
  roles reachable. `INSTANCE_LINK_PREDICATES` also gained hasRole/rolePersona/
  roleTool/roleGuardrail so the python reachability walk sees the same edges.
- **`ho:scaffold` has NO `rdfs:domain`** (harness.ttl:277-280). Confirmed there is
  no real `rdfs:domain` predicate — the only textual "rdfs:domain" is inside the
  `skos:definition` string (which itself documents *why*). Sound: if scaffold had
  domain `ho:HarnessComponent` (like `artifactTemplate` does), OWL RL would infer
  the `ho:Harness`/`ho:Domain` it attaches to as a component and trip the orphan
  shape. No domain → it can hang off a Harness/Domain and only emits standalone
  files, never a component section.

## 3. Role reachability — PASS

Composed the lpranging owl:imports union (temp `central` symlink → this repo,
`HARNESS_CATALOG=catalog-v001.xml HARNESS_ROOT_ONTOLOGY=…/recipes/lpranging`):

```
loaded graph: 1870 triples
✓ SHACL conforms  ✓ all 81 individuals reachable from a Harness  ✓ capabilities → PASS
```

Grown count **81** = central 64 + 17 local (1 domain, 4 concepts, 2 caps, 2 tools,
4 SystemPrompts [sp-lpranging + 3 role personas], 3 Roles, 1 Harness). The 3
`ho:Role` reach from `h-lpranging` via `hasRole`; the 3 role personas reach via
both `hasSystemPrompt` and `rolePersona`. No orphans.

## 4. Full-tree materialize (core deliverable) — PASS

`materialize.py h-lpranging --out <scratch>` over the validated union emitted:

```
CLAUDE.md
MANIFEST.json
.claude/agents/{developer,inspection,vnv}.md
tools/docgraph.py
tools/sim_grid_reservation.py
DESIGN_HARNESS_STANDARD.md
docs/README.md
```

- **Copied code byte-identical to source** (`cmp` + `sha256sum`):
  - `tools/docgraph.py` — IDENTICAL, 32560 B, sha256 `a0b5e722…a6ed` matches
    `~/git/agrtls/device_harvest_lp/lpranging/tools/docgraph.py`.
  - `tools/sim_grid_reservation.py` — IDENTICAL, 11309 B, matches
    `…/lpranging/reference/sim_grid_reservation.py`.
- **CLAUDE.md** carries a `## Roles` summary listing all 3 sub-agents with their
  `.claude/agents/<slug>.md` reference.
- **Per-role agent files** each carry persona (rolePersona) + least-privilege
  scoped tools/guardrails + memory policy, and the scopes are **strict subsets**
  of the harness bindings (verified against the recipe ttl):
  - developer: tools editor+shell; guardrails lang, least-privilege, no-arbitrary-decision, verify-proceed.
  - inspection: tools shell+docgraph; guardrails controlled-vocabulary, lang, report-over-prompt, traceability.
  - vnv: tools shell+simulator; guardrails lang, report-over-prompt, verify-proceed.
  - vnv.md excerpt (persona + scope):
    ```
    # Verification-and-validation role
    You are a verification-and-validation sub-agent. ... separating verification
    (built to spec) from validation (built the right thing). ...
    ## Tools
    - **Shell tool**
    - **Design simulator tool** — Discrete-event simulation ...
    ## Guardrails
    - **Korean/English only** …  - **Report over prompt** …  - **Verify then proceed** …
    ## Memory policy
    Read and write only .claude/agent-memory/vnv/: …
    ```
    (Note: vnv's scope correctly excludes editor and docgraph — least privilege honoured.)
- **MANIFEST.json** extends with `roles` (agentFile + tools + guardrails per role),
  `implementations` (both `status: resolved`, dest `tools/docgraph.py` /
  `tools/sim_grid_reservation.py`), and `scaffold`
  (`DESIGN_HARNESS_STANDARD.md`→root, `README.md`→`docs/README.md`).

## 5. Gate + determinism + regression — PASS

- **Determinism**: two runs, `diff -r lp1 lp2` = IDENTICAL.
- **Gate refusals** (both before any write; **out dir never created**):
  - bogus id `h-nonexistent` → exit **2**, lists known harnesses, no out dir.
  - non-validating union (scratch catalog importing only schema+core/harnesses so
    harness components are unresolved) → exit **1**, "REFUSING to materialize", no out dir.
- **Regression**:
  - central `h-multiagent` (no roles) → tree is **only CLAUDE.md + MANIFEST.json**
    (increment-1 tree behaviour intact). MANIFEST gains `roles/implementations/
    scaffold` keys but as empty lists — additive, benign.
  - `h-techdoc` recipe → still materializes (CLAUDE.md + MANIFEST, 1 template source).

## 6. Design doc — PASS

`docs/materialize-design.md` documents the Role model (§"First-class roles (P4)"),
the implementationRef fetch + 3-step path resolution + `.ref` stub fallback
(§"Tool implementation refs (P3)"), the scaffold marker-strip mapping and the
no-domain rationale (§"Standard / docs scaffold (P5)"), and marks P3/P4/P5
implemented. The **portability caveat is explicitly documented** (absolute refs
resolve only on a machine with that checkout; recommends shipping code in the
recipe repo with a repo-relative ref; the `stub` fallback is the "did-not-travel"
signal).

## Judgment on the implementationRef portability caveat — acceptable (does not block)

The lpranging refs are absolute paths under `~/git/agrtls/…` that resolve only on
this machine. This is **acceptable for a worked demo** and should **not block**:

1. It is a documented, deliberate trade-off (design doc §Portability caveat), not
   an oversight.
2. It fails **safe**: an unresolvable ref yields a `tools/<basename>.ref` stub, not
   a crash — materialize still produces a valid tree, and the stub is a visible
   "ref did not travel" marker.
3. It does not touch neutrality or validation: implementationRef is build-only and
   central-abox-free; the range already permits repo-relative or URL refs, so the
   portable fix needs no schema change — only recipe authoring.

Recommendation (non-blocking, for a shippable recipe): move the two tool sources
into the recipe repo and switch to repo-relative refs so the copy is machine-
independent. Route as a recipe-authoring follow-up (developer dispatch), not a
defect in this increment.

## Notes / follow-ups (do not block PASS)

- Manifest schema for role-less harnesses now always includes empty
  `roles/implementations/scaffold` keys. Additive and deterministic; flagged only
  so downstream consumers expect the keys.
- Provenance aside (inspection's domain, not a vnv defect): the P3/P4/P5 terms and
  the increment-1 materialize landed in the same commit `e726cd1`; working tree is
  clean for `ontology/`+`tools/`, only `docs/materialize-design.md` (+ developer
  memory) are uncommitted.
