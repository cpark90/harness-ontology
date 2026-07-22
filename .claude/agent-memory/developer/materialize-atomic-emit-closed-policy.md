# materialize hardening — atomic emit (N1) + closed selection-policy set (N2)

vnv notes N1/N2 on `tools/materialize.py`. Pure TOOLING change (no ontology/TBox/
shapes/recipe edits); validate stays PASS 96. Design doc = `docs/odr-bind-lock.md`
(atomicity subsection + "policy set is CLOSED" para).

## N1 — atomic emit (staging + os.replace), NOT direct write
- Problem: the `--lock` content-hash check runs **mid-emit** (in
  `emit_implementations`, after copyfile). Writing straight into `--out` left a
  half-written tree on failure (`.claude/agents/`, `tools/<impl>` present, no
  CLAUDE.md) — contradicting "nothing half-written".
- Chosen mechanism (brief's preferred): `materialize()` now builds the WHOLE tree
  into a sibling temp staging dir and only places it on FULL success.
  - `staging = tempfile.mkdtemp(prefix="."+basename+".tmp-", dir=os.path.dirname(abspath(out)))`
    — **must be in out's PARENT** so `os.replace` is a same-filesystem atomic
    rename (a cross-device `/tmp` staging would fall back to a non-atomic copy).
  - body extracted verbatim into `_emit_tree(g,h,out_dir,lock)` (the old
    materialize body, unchanged); `materialize()` wraps it: try→`_emit_tree` into
    staging, `except BaseException: shutil.rmtree(staging); raise`, then
    `_place_atomically(staging, out)`.
  - `_place_atomically`: if out absent → single `os.replace(staging,out)`. If out
    pre-exists → rename out to `out.bak-<pid>`, `os.replace(staging,out)`, rm
    backup (restore backup on swap failure). Pre-existing out is thus CLEANLY
    REPLACED (stale files gone), not merged. Swap only ever runs after full
    success → a FAILED build never disturbs out.
- Determinism preserved: staging path never enters any emitted file (dests are
  relative), so fresh build stays byte-identical to pre-change; `--lock` reproduce
  still byte-identical. Proven: baseline(pre-change) diff A1 = empty; A1==A2;
  B(--lock A1)==A1; success-over-preexisting == baseline + stale removed.
- N1 proof method: tampered lock (copy A1 lock, zero out LAST tool's contentHash;
  NOT the vendored lock). OLD partial reproduced via a driver that calls the
  sub-emitters straight into out (pre-change order) → agents+tools present, no
  CLAUDE.md. NEW: out-absent → stays ABSENT; out-preexist(sentinel) → UNTOUCHED
  (before==after sha), no `.claude/`/`tools/`/CLAUDE.md leak, no tmp-/bak- leftovers.

## N2 — unknown selectionPolicy = hard error (closed set)
- `select_candidate`: the tail `return ordered[-1]` used to swallow ANY policy
  ("unrecognised policy falls back to newest-first"). Added, after the `pinned:`
  branch: `if policy not in ("latest-stable","conservative"): raise ValueError(
  f"unrecognised ho:selectionPolicy '{policy}' for {tool_iri}; accepted policies
  are: {ACCEPTED_POLICIES}")` where `ACCEPTED_POLICIES="latest-stable / conservative
  / pinned:<tag>"`. Message names tool + bad value + accepted set (parity with the
  existing empty-`pinned:` error). Raised in resolve_selections → before any write.
- N2 proof: only reachable when a tool HAS candidates (`elif cands:` path);
  lpranging is all direct-ref, so make a **scratch recipe copy**: copy
  `lpranging.ttl` to scratch, give tool-docgraph `implementationCandidate` +
  `selectionPolicy "newest-please"` + a `ho:Candidate` (prefLabel+ref+version+tag),
  and a **scratch catalog IN THE SAME dir** `staging/harness-recipes/` (so the
  `./central`/`./recipes` relative maps still resolve — catalog paths resolve
  relative to the catalog file's dir) that remaps the recipe IRI to an ABSOLUTE
  scratch-ttl path. materialize → "REFUSING ... unrecognised ho:selectionPolicy
  'newest-please' ..." exit 1, out ABSENT. Unit check: latest-stable/conservative/
  pinned:<tag> route; ''/'LATEST-STABLE'/'stable'/'newest-please' all raise.

## gate fixture (lpranging materialize)
- run from repo root; `ln -sfn <repo-root> staging/harness-recipes/central` (rm
  after), `HARNESS_CATALOG=staging/harness-recipes/catalog-v001.xml`,
  `HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging`.
- lpranging materializes 28 comps / 3 roles / 3 channels / 2 direct-ref tools /
  3 scaffold / 3 skills. staging/ is gitignored; scratch catalog/ttl go in
  scratchpad EXCEPT the same-dir scratch catalog which must be rm'd from the repo.
