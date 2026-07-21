#!/usr/bin/env python3
"""Validate the harness ontology.

Layers of defense (see docs/DESIGN.md):
  1. OWL RL reasoning        -> logical consistency, type/inverse closure
  2. SHACL shapes            -> local structural invariants (orphans, drift)
  3. Global reachability     -> disconnected islands (orphan components)
  4. Capability satisfaction -> every harness can actually be built
  5. Duplicate detection     -> vocabulary drift / redundant nodes

Exit code is non-zero if any hard check fails, so this drops straight
into CI / a pre-commit gate.

Usage:
    python3 tools/validate.py            # human summary (prints PASS/FAIL)
    python3 tools/validate.py --json     # structured JSON (for the web UI / CI)
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import sys
from collections import defaultdict, deque

from rdflib import Graph, RDF
from rdflib.namespace import SKOS

import ontology_lib as lib
from ontology_lib import HO


def _print_header(title: str) -> None:
    print(f"\n=== {title} ===")


def check_shacl(data: Graph):
    """Returns (conforms, report_text). report_text is '' when it conforms."""
    from pyshacl import validate
    shapes = Graph()
    shapes.parse(os.path.join(lib.ONT_DIR, "shapes", "harness-shapes.ttl"),
                 format="turtle")
    conforms, _report_graph, report_text = validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="none",          # we already reasoned
        advanced=True,             # sh:or, inversePath
        meta_shacl=False,
    )
    _print_header("SHACL structural invariants")
    if conforms:
        print("✓ conforms — no orphaned/under-specified nodes")
    else:
        print("✗ SHACL violations:")
        print(report_text.strip())
    return conforms, ("" if conforms else report_text.strip())


def check_reachability(g: Graph):
    """Every individual must be weakly connected to some Harness.
    Returns (ok, orphans) where orphans is a list of {label, uri}."""
    _print_header("Global reachability (orphan islands)")
    nodes = lib.instance_nodes(g)
    adj: dict = defaultdict(set)
    for s, _p, o in lib.instance_edges(g):
        adj[s].add(o)
        adj[o].add(s)  # weak (undirected) connectivity

    roots = set(g.subjects(RDF.type, HO.Harness))
    seen: set = set()
    q = deque(roots)
    seen.update(roots)
    while q:
        n = q.popleft()
        for m in adj[n]:
            if m not in seen:
                seen.add(m)
                q.append(m)

    orphans = sorted(nodes - seen, key=lambda n: lib.label_of(g, n))
    if not orphans:
        print(f"✓ all {len(nodes)} individuals reachable from a Harness")
        return True, []
    print(f"✗ {len(orphans)} orphaned individual(s) (no path to any harness):")
    for n in orphans:
        print(f"    - {lib.label_of(g, n)}  <{n}>")
    return False, [{"label": lib.label_of(g, n), "uri": str(n)} for n in orphans]


def check_capability_satisfaction(g: Graph):
    """For each harness, every required capability must be provided by one
    of its own components. Returns (ok, gaps) where gaps is a list of
    {harness, missing:[...]}."""
    _print_header("Capability satisfaction")
    ok = True
    gaps = []
    for h in sorted(g.subjects(RDF.type, HO.Harness),
                    key=lambda n: lib.label_of(g, n)):
        required = set(g.objects(h, HO.requiresCapability))
        provided = set()
        for _p, comp in _components(g, h):
            provided.update(g.objects(comp, HO.providesCapability))
        gap = required - provided
        if gap:
            ok = False
            names = ", ".join(lib.label_of(g, c) for c in gap)
            print(f"✗ {lib.label_of(g, h)} is missing providers for: {names}")
            gaps.append({"harness": lib.label_of(g, h),
                         "missing": [lib.label_of(g, c) for c in gap]})
    if ok:
        print("✓ every harness's required capabilities are provided internally")
    return ok, gaps


def _components(g: Graph, harness):
    for p in (HO.hasComponent, HO.hasSystemPrompt, HO.usesTool, HO.hasGuardrail,
              HO.hasWorkflow, HO.usesModel, HO.hasExample, HO.hasInstruction):
        for o in g.objects(harness, p):
            yield p, o


def check_duplicates(g: Graph):
    """Same class + same (case-folded) prefLabel == likely drift/dup.
    Advisory (does not fail the build). Returns a list of dup groups."""
    _print_header("Duplicate / drift detection (warning only)")
    by_key = defaultdict(list)
    for n in lib.instance_nodes(g):
        label = lib.label_of(g, n).strip().lower()
        types = tuple(lib.most_specific_types(g, n))
        by_key[(types, label)].append(n)
    dups = {k: v for k, v in by_key.items() if len(v) > 1}
    if not dups:
        print("✓ no duplicate labels within a class")
    else:
        for (types, label), members in dups.items():
            tnames = "/".join(t.split("#")[-1] for t in types)
            print(f"⚠ {len(members)} '{label}' [{tnames}] share a label:")
            for m in members:
                print(f"    - <{m}>")
    return [{"label": label,
             "types": [t.split("#")[-1] for t in types],
             "members": [str(m) for m in members]}
            for (types, label), members in dups.items()]


def run_structured() -> dict:
    """Load from disk, run every check, and return a structured result dict.
    Human prints are captured (kept out of the returned data) so callers like
    the web UI / CI get clean JSON. Reloads the graph so the verdict is always
    against current on-disk TTL."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        g = lib.load_graph(reason=True)
        shacl_ok, shacl_report = check_shacl(g)
        reach_ok, orphans = check_reachability(g)
        cap_ok, gaps = check_capability_satisfaction(g)
        dups = check_duplicates(g)
    hard_ok = shacl_ok and reach_ok and cap_ok
    return {
        "pass": hard_ok,
        "triples": len(g),
        "shacl": {"ok": shacl_ok, "report": shacl_report},
        "reachability": {"ok": reach_ok, "orphans": orphans},
        "capabilities": {"ok": cap_ok, "gaps": gaps},
        "duplicates": dups,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate the harness ontology.")
    ap.add_argument("--json", action="store_true",
                    help="emit structured JSON instead of the human summary")
    args = ap.parse_args(argv)

    if args.json:
        try:
            result = run_structured()
        except Exception as exc:  # noqa: BLE001
            print(json.dumps({"pass": False, "error": str(exc)}))
            return 2
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["pass"] else 1

    print("Loading ontology and applying OWL RL reasoning...")
    try:
        g = lib.load_graph(reason=True)
    except Exception as exc:  # noqa: BLE001
        print(f"✗ failed to load/reason: {exc}")
        return 2
    print(f"  loaded graph: {len(g)} triples (post-reasoning)")

    results = {
        "SHACL": check_shacl(g)[0],
        "reachability": check_reachability(g)[0],
        "capabilities": check_capability_satisfaction(g)[0],
    }
    check_duplicates(g)  # advisory

    _print_header("Summary")
    hard_ok = all(results.values())
    for name, ok in results.items():
        print(f"  {'✓' if ok else '✗'} {name}")
    print(f"\n{'PASS' if hard_ok else 'FAIL'}")
    return 0 if hard_ok else 1


if __name__ == "__main__":
    sys.exit(main())
