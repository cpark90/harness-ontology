#!/usr/bin/env python3
"""Determinism gate for the READ projection (`tools/retrieve.py`).

`materialize.py` (the write projection) is held to byte-identity: the same
graph must build the same CLAUDE.md every time. This is the same gate for the
other direction — **the same request must project the same context pack in
every process**. Without it a "work from the pack" agent is not reproducible
and a projection diff cannot be used as evidence (an unrelated edit shows up
as a meaningful diff, or a real regression hides inside the noise).

The failure mode this catches is order leaking out of hash-randomised
iteration (`set` of `URIRef`, OWL-RL materialisation order) into a ranking
tie-break, where the token budget then cuts the tie group at an arbitrary
point. So each probe request is run in several FRESH interpreters with
DIFFERENT `PYTHONHASHSEED` values, plus one run with the ambient (randomised)
seed, and every run must produce identical bytes.

  DO NOT "fix" a failure here by pinning PYTHONHASHSEED — pinning one seed
  hides exactly the bug this gate exists to catch. Fix the ordering instead:
  sort on a total key (score descending, IRI ascending).

Usage:
    python3 tools/check_determinism.py
    python3 tools/check_determinism.py --request "my query" --runs 5
"""
from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
RETRIEVE = TOOLS / "retrieve.py"

# Probe requests. Each hits a large tie group at the budget/seed cut, which is
# where non-determinism used to change pack membership — not just its order.
DEFAULT_REQUESTS = [
    "workflow steps and deliverables",
    "code review harness with tests",
    "multi-agent harness that spawns short-lived sub-agents",
    "cited research summary",
]

# One run per entry. `None` = inherit the ambient, randomised seed; the fixed
# values force provably different string-hash orders in the other runs.
SEED_PLAN = [None, "0", "1", "2"]


def _run(request: str, fmt: str, seed: str | None) -> str:
    env = dict(os.environ)
    if seed is None:
        env.pop("PYTHONHASHSEED", None)   # ambient randomisation, on purpose
    else:
        env["PYTHONHASHSEED"] = seed
    proc = subprocess.run(
        [sys.executable, str(RETRIEVE), request, "--format", fmt],
        capture_output=True, env=env, cwd=str(TOOLS.parent),
    )
    if proc.returncode != 0:
        raise SystemExit(f"retrieve.py failed for {request!r}:\n"
                         f"{proc.stderr.decode(errors='replace')}")
    return proc.stdout.decode()


def check(request: str, fmt: str, runs: int) -> tuple[bool, dict[str, list[str]]]:
    """Run `request` `runs` times in fresh processes; group outputs by digest."""
    by_digest: dict[str, list[str]] = {}
    for i in range(runs):
        seed = SEED_PLAN[i % len(SEED_PLAN)]
        out = _run(request, fmt, seed)
        digest = hashlib.md5(out.encode()).hexdigest()
        by_digest.setdefault(digest, []).append(
            f"run{i}(PYTHONHASHSEED={seed or 'random'})")
    return len(by_digest) == 1, by_digest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--request", action="append", dest="requests",
                    help="probe request (repeatable; defaults to the built-in set)")
    ap.add_argument("--runs", type=int, default=len(SEED_PLAN),
                    help=f"runs per request (default {len(SEED_PLAN)})")
    ap.add_argument("--format", choices=["md", "json", "both"], default="both",
                    help="pack format(s) to compare (default both)")
    args = ap.parse_args()

    requests = args.requests or DEFAULT_REQUESTS
    formats = ["md", "json"] if args.format == "both" else [args.format]
    runs = max(2, args.runs)          # one run can never prove reproducibility
    failures = 0
    for request in requests:
        for fmt in formats:
            ok, groups = check(request, fmt, runs)
            tag = f"[{fmt}] {request!r}"
            if ok:
                print(f"  ok   {tag} — {runs} runs, 1 distinct pack")
            else:
                failures += 1
                print(f"  FAIL {tag} — {len(groups)} distinct packs:")
                for digest, who in groups.items():
                    print(f"         {digest[:12]}  {', '.join(who)}")

    print()
    if failures:
        print(f"FAIL — {failures} request/format pair(s) are not reproducible.\n"
              "The pack must not depend on the process. Sort every ranking on a\n"
              "total key (score descending, IRI ascending); do not pin "
              "PYTHONHASHSEED.")
        return 1
    print("PASS — every request projects a byte-identical pack across processes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
