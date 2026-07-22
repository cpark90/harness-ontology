#!/usr/bin/env python3
"""Build projection of the harness ontology — the DUAL of retrieve.py.

retrieve.py is the READ projection: given a request it emits a bounded
context pack for an agent to read. materialize.py is the BUILD projection:
given a VALIDATED harness it renders an actual runnable harness file tree
(CLAUDE.md + a build manifest) from the composed union.

  retrieve : ontology -> request-scoped context pack (what to READ)
  materialize : validated harness -> file tree (what to BUILD)

Only a validated harness materializes. Before emitting anything we run the
same structured validation validate.py runs; if the union does not PASS we
refuse (non-zero exit). This keeps the build honest: a file tree is only ever
produced from a connected, well-typed, capability-complete graph.

Increment 1 was the SPINE (P1) + template-file references (P2), emitting
CLAUDE.md + MANIFEST.json. Increment 2 (this file) adds first-class roles (P4:
.claude/agents/<role>.md per ho:hasRole), tool implementation refs (P3:
ho:implementationRef fetched/copied into tools/<basename>) and standard/docs
scaffold (P5: ho:scaffold / ho:artifactTemplate fragments rendered into the
tree). See docs/materialize-design.md.

Usage:
    /usr/bin/python3 tools/materialize.py h-techdoc --out build/techdoc
    /usr/bin/python3 tools/materialize.py https://harness-ontology.dev/id/techdoc/h-techdoc \
        --out build/techdoc --format json

Composition honours HARNESS_CATALOG / HARNESS_ROOT_ONTOLOGY exactly like
validate.py and retrieve.py, so a recipe union materializes the same way the
central store does.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys

from rdflib import Graph, RDF, URIRef
from rdflib.namespace import SKOS

import ontology_lib as lib
from ontology_lib import HO
import validate

# --- deterministic component ordering ---------------------------------
# Sections are emitted in this fixed order; within a section, multiple
# components are sorted by IRI so the same input yields byte-identical output.


def _sorted(nodes):
    return sorted(nodes, key=str)


def role_slug(role: URIRef) -> str:
    """Filename stem for a role's agent file: the IRI's last segment with a
    leading 'role-' stripped (id:role-developer -> 'developer'), mirroring the
    conventional .claude/agents/<name>.md naming."""
    tail = str(role).rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail[len("role-"):] if tail.startswith("role-") else tail


# --- 1. target resolution ---------------------------------------------
def resolve_harness(g: Graph, ref: str) -> URIRef:
    """Resolve a full IRI or a short id (e.g. 'h-techdoc') to a Harness node.
    Raises ValueError if it is absent or not a Harness."""
    harnesses = set(g.subjects(RDF.type, HO.Harness))
    node = URIRef(ref)
    if node in harnesses:
        return node
    # short id: match a harness IRI ending in /<ref> or #<ref>
    matches = [h for h in harnesses
               if str(h).rsplit("/", 1)[-1] == ref or str(h).rsplit("#", 1)[-1] == ref]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        known = ", ".join(sorted(str(h).rsplit("/", 1)[-1] for h in harnesses))
        raise ValueError(f"no harness matches '{ref}'. Known harnesses: {known}")
    raise ValueError(f"'{ref}' is ambiguous across {len(matches)} harnesses; use the full IRI")


# --- 2. template mechanism (P2) ---------------------------------------
def _template_bases() -> list[str]:
    """Roots against which a repo-relative ho:artifactTemplate path resolves,
    in priority order:
      1. the ontology repo root (tools/, ontology/ live here)
      2. the catalog's directory — the RECIPE repo root when a recipe union is
         materialized via HARNESS_CATALOG (so a recipe can ship its own
         template fragments next to its .ttl)
    First existing file wins."""
    bases = [lib.ROOT]
    catalog_dir = os.path.dirname(os.path.abspath(lib.CATALOG))
    if catalog_dir not in bases:
        bases.append(catalog_dir)
    return bases


def resolve_template(rel_path: str) -> str:
    for base in _template_bases():
        cand = os.path.normpath(os.path.join(base, rel_path))
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError(
        f"ho:artifactTemplate '{rel_path}' not found under any of: {_template_bases()}")


def render_from_template(g: Graph, node: URIRef, tmpl_path: str) -> str:
    """Read the template fragment and substitute the node's graph data.
    Supported placeholders: {{prefLabel}}, {{promptText}}, {{definition}}."""
    with open(resolve_template(tmpl_path), encoding="utf-8") as fh:
        text = fh.read()
    subs = {
        "{{prefLabel}}": lib.label_of(g, node),
        "{{promptText}}": str(g.value(node, HO.promptText) or ""),
        "{{definition}}": str(g.value(node, SKOS.definition) or ""),
    }
    for key, val in subs.items():
        text = text.replace(key, val)
    return text.rstrip("\n")


def render_component(g: Graph, node: URIRef, fallback: str) -> tuple[str, str | None]:
    """Return (section_body, template_source_or_None). If the node carries
    ho:artifactTemplate, render through it; otherwise use the graph-data
    fallback text supplied by the caller."""
    tmpl = g.value(node, HO.artifactTemplate)
    if tmpl is not None:
        return render_from_template(g, node, str(tmpl)), str(tmpl)
    return fallback, None


# --- 3. CLAUDE.md assembly --------------------------------------------
def _component_type(g: Graph, node: URIRef) -> str:
    """Most specific ontology type of a component. lib.most_specific_types can
    keep the generic ho:HarnessComponent alongside the real subtype (reflexive
    rdfs:subClassOf under OWL RL defeats its superclass-drop); prefer any
    concrete subtype so the manifest records Tool/Workflow/… not the abstract."""
    types = lib.most_specific_types(g, node)
    specific = [t for t in types if t != HO.HarnessComponent]
    chosen = specific or types
    return chosen[0].split("#")[-1] if chosen else "HarnessComponent"


def build_claude_md(g: Graph, h: URIRef, sources: list[str],
                    roles: list[URIRef]) -> str:
    """Assemble CLAUDE.md deterministically from the harness's components.
    `sources` is appended to with every template path actually used. `roles`
    (the harness's ho:hasRole objects, sorted) are summarised in a Roles section
    and their personas are omitted from the top-level Persona section — each
    role persona is rendered into its own .claude/agents/<role>.md instead."""
    out: list[str] = []
    role_personas = {p for r in roles for p in g.objects(r, HO.rolePersona)}

    # -- overview (harness prefLabel + definition) --
    out.append(f"# {lib.label_of(g, h)}")
    out.append("")
    definition = g.value(h, SKOS.definition)
    if definition:
        out.append(str(definition))
        out.append("")

    # -- persona (hasSystemPrompt, excluding per-role personas) --
    out.append("## Persona")
    out.append("")
    for sp in _sorted(g.objects(h, HO.hasSystemPrompt)):
        if sp in role_personas:
            continue
        fallback = str(g.value(sp, HO.promptText) or lib.label_of(g, sp))
        body, src = render_component(g, sp, fallback)
        if src:
            sources.append(src)
        out.append(body)
        out.append("")

    # -- operating rules (hasGuardrail) --
    out.append("## Operating rules")
    out.append("")
    for gr in _sorted(g.objects(h, HO.hasGuardrail)):
        fallback = str(g.value(gr, HO.promptText) or "")
        body, src = render_component(g, gr, fallback)
        if src:
            sources.append(src)
        out.append(f"- **{lib.label_of(g, gr)}** — {body}")
        for cond in sorted(str(c) for c in g.objects(gr, HO.languageCondition)):
            out.append(f"    - {cond}")
    out.append("")

    # -- process (hasWorkflow + appliesPattern) --
    out.append("## Process")
    out.append("")
    for wf in _sorted(g.objects(h, HO.hasWorkflow)):
        desc = g.value(wf, SKOS.definition)
        tail = f" — {desc}" if desc else ""
        out.append(f"- **Workflow: {lib.label_of(g, wf)}**{tail}")
    for pat in _sorted(g.objects(h, HO.appliesPattern)):
        desc = g.value(pat, SKOS.definition)
        tail = f" — {desc}" if desc else ""
        out.append(f"- **Pattern: {lib.label_of(g, pat)}**{tail}")
    out.append("")

    # -- model / config (usesModel) --
    out.append("## Model")
    out.append("")
    for mc in _sorted(g.objects(h, HO.usesModel)):
        cfg = g.value(mc, HO.promptText)
        tail = f" (`{cfg}`)" if cfg else ""
        out.append(f"- {lib.label_of(g, mc)}{tail}")
    out.append("")

    # -- roles (hasRole) — a multi-agent harness dispatches sub-agents --
    if roles:
        out.append("## Roles")
        out.append("")
        out.append("This harness dispatches the following sub-agents; each has "
                   "its own agent file under `.claude/agents/`.")
        out.append("")
        for r in roles:
            desc = g.value(r, SKOS.definition)
            tail = f" — {desc}" if desc else ""
            out.append(f"- **{lib.label_of(g, r)}** (`.claude/agents/"
                       f"{role_slug(r)}.md`){tail}")
        out.append("")

    return "\n".join(out)


# --- 4. build manifest ------------------------------------------------
def all_components(g: Graph, h: URIRef):
    """Every bound component of the harness, sorted by IRI, as
    (iri, type, prefLabel)."""
    seen = set()
    for _p, comp in _iter_components(g, h):
        seen.add(comp)
    return [(str(c), _component_type(g, c), lib.label_of(g, c)) for c in _sorted(seen)]


def _iter_components(g: Graph, h: URIRef):
    for p in (HO.hasSystemPrompt, HO.usesTool, HO.hasGuardrail, HO.hasWorkflow,
              HO.usesModel, HO.hasExample, HO.hasInstruction, HO.hasComponent):
        for o in g.objects(h, p):
            yield p, o


def capability_bindings(g: Graph, h: URIRef):
    """For each requiresCapability, the component(s) that provide it — the
    composition proof, mirrored from validate.check_capability_satisfaction."""
    providers = {}
    for _p, comp in _iter_components(g, h):
        for cap in g.objects(comp, HO.providesCapability):
            providers.setdefault(cap, set()).add(comp)
    bindings = []
    for cap in _sorted(g.objects(h, HO.requiresCapability)):
        bound = _sorted(providers.get(cap, set()))
        bindings.append({
            "capability": str(cap),
            "capabilityLabel": lib.label_of(g, cap),
            "providedBy": [{"iri": str(b), "label": lib.label_of(g, b)} for b in bound],
        })
    return bindings


def build_manifest(g: Graph, h: URIRef, sources: list[str]) -> dict:
    comps = all_components(g, h)
    total_tokens = 0
    for iri, _t, _l in comps:
        est = g.value(URIRef(iri), HO.tokenEstimate)
        if est is not None:
            total_tokens += int(est)
    return {
        "harness": str(h),
        "prefLabel": lib.label_of(g, h),
        "derivedFrom": _sorted(str(d) for d in g.objects(h, HO.derivedFrom)),
        "components": [{"iri": iri, "type": typ, "label": label}
                       for iri, typ, label in comps],
        "capabilityBindings": capability_bindings(g, h),
        "templateSources": sorted(set(sources)),
        "tokenEstimate": total_tokens,
    }


# --- 5. role emitter (P4) ---------------------------------------------
def build_role_md(g: Graph, role: URIRef, sources: list[str]) -> str:
    """Render one role's .claude/agents/<slug>.md: persona (rolePersona), its
    least-privilege tool/guardrail scope, and its memory policy. Deterministic
    (scope lists sorted by IRI)."""
    out: list[str] = []
    slug = role_slug(role)
    definition = g.value(role, SKOS.definition)

    # -- frontmatter (agent-file convention) --
    out.append("---")
    out.append(f"name: {slug}")
    if definition:
        out.append(f"description: {definition}")
    out.append("---")
    out.append("")
    out.append(f"# {lib.label_of(g, role)}")
    out.append("")

    # -- persona (rolePersona -> SystemPrompt) --
    persona = g.value(role, HO.rolePersona)
    if persona is not None:
        fallback = str(g.value(persona, HO.promptText) or lib.label_of(g, persona))
        body, src = render_component(g, persona, fallback)
        if src:
            sources.append(src)
        out.append(body)
        out.append("")

    # -- tool scope (roleTool) --
    tools = _sorted(g.objects(role, HO.roleTool))
    if tools:
        out.append("## Tools")
        out.append("")
        for t in tools:
            desc = g.value(t, SKOS.definition)
            tail = f" — {desc}" if desc else ""
            out.append(f"- **{lib.label_of(g, t)}**{tail}")
        out.append("")

    # -- guardrail scope (roleGuardrail) --
    guards = _sorted(g.objects(role, HO.roleGuardrail))
    if guards:
        out.append("## Guardrails")
        out.append("")
        for gr in guards:
            body = str(g.value(gr, HO.promptText) or "")
            sep = f" — {body}" if body else ""
            out.append(f"- **{lib.label_of(g, gr)}**{sep}")
        out.append("")

    # -- memory policy (roleMemoryPolicy) --
    policy = g.value(role, HO.roleMemoryPolicy)
    if policy is not None:
        out.append("## Memory policy")
        out.append("")
        out.append(str(policy))
        out.append("")

    return "\n".join(out)


def emit_roles(g: Graph, roles: list[URIRef], out_dir: str,
               sources: list[str]) -> list[dict]:
    """Write .claude/agents/<slug>.md for each role; return manifest records."""
    if not roles:
        return []
    agents_dir = os.path.join(out_dir, ".claude", "agents")
    os.makedirs(agents_dir, exist_ok=True)
    records = []
    for r in roles:
        slug = role_slug(r)
        body = build_role_md(g, r, sources)
        with open(os.path.join(agents_dir, f"{slug}.md"), "w",
                  encoding="utf-8") as fh:
            fh.write(body if body.endswith("\n") else body + "\n")
        records.append({
            "role": str(r),
            "label": lib.label_of(g, r),
            "agentFile": f".claude/agents/{slug}.md",
            "tools": _sorted(str(t) for t in g.objects(r, HO.roleTool)),
            "guardrails": _sorted(str(x) for x in g.objects(r, HO.roleGuardrail)),
        })
    return records


# --- 6. BIND axis: candidate selection, implementation emit, lock -----
# The ODR BIND axis. A Tool's implementation is resolved deterministically:
#   1. a supplied lock that pins the tool  -> use the locked candidate (INV-2),
#   2. else the tool's ho:implementationCandidate list -> apply the selection
#      policy (tool-level ho:selectionPolicy overrides harness-level; default
#      "latest-stable"),
#   3. else a direct ho:implementationRef on the tool (degenerate 1-candidate),
#   4. else a stub.
# Selection is TOTAL and DETERMINISTIC so (spec + policy) reproduces the same
# choice and (spec + lock) reproduces byte-identical output.
LOCK_FILENAME = "harness.lock.json"
DEFAULT_POLICY = "latest-stable"


def _resolve_implementation(ref: str) -> str | None:
    """Resolve an implementation ref to a readable local file path, or None if
    it names a URL / unresolvable path. Tries, in order: repo root, recipe dir
    (dirname of the catalog), then the ref as an absolute path."""
    if ref.startswith(("http://", "https://")):
        return None
    for base in _template_bases():  # repo root, then recipe/catalog dir
        cand = os.path.normpath(os.path.join(base, ref))
        if os.path.isfile(cand):
            return cand
    if os.path.isabs(ref) and os.path.isfile(ref):
        return ref
    return None


def _version_key(version: str) -> list:
    """A total, deterministic ordering key for a candidateVersion string.
    Numeric segments compare numerically and sort ABOVE non-numeric ones, so
    '1.10.0' > '1.9.0' and a numbered version outranks a bare label. Missing
    version sorts lowest."""
    if not version:
        return [(-1, 0, "")]
    key = []
    for seg in re.split(r"[.\-+_]", version):
        if seg.isdigit():
            key.append((1, int(seg), ""))
        else:
            key.append((0, 0, seg))
    return key


def _candidates(g: Graph, tool: URIRef) -> list[dict]:
    """All ho:implementationCandidate options of a tool as dicts
    {iri, ref, version, tag}, sorted by IRI for a stable base order."""
    out = []
    for c in _sorted(g.objects(tool, HO.implementationCandidate)):
        out.append({
            "iri": str(c),
            "ref": str(g.value(c, HO.implementationRef) or ""),
            "version": str(g.value(c, HO.candidateVersion) or ""),
            "tag": str(g.value(c, HO.candidateTag) or ""),
        })
    return out


def _policy_for(g: Graph, h: URIRef, tool: URIRef) -> str:
    """Effective selection policy for a tool: a tool-level ho:selectionPolicy
    overrides a harness-level default; absent both -> DEFAULT_POLICY."""
    tool_pol = g.value(tool, HO.selectionPolicy)
    if tool_pol is not None:
        return str(tool_pol)
    h_pol = g.value(h, HO.selectionPolicy)
    if h_pol is not None:
        return str(h_pol)
    return DEFAULT_POLICY


def select_candidate(policy: str, candidates: list[dict], tool_iri: str) -> dict:
    """Pick exactly one candidate under `policy`, totally and deterministically.
      * "pinned:<tag>": only candidates with that tag; else hard error.
      * "latest-stable" (default): prefer tag=="stable"; highest version wins.
      * "conservative": prefer tag=="stable"; LOWEST version wins.
    Ties break by candidate IRI (ascending). `candidates` is non-empty."""
    if policy.startswith("pinned:"):
        want = policy[len("pinned:"):]
        pool = [c for c in candidates if c["tag"] == want]
        if not pool:
            raise ValueError(
                f"selection policy '{policy}' for {tool_iri} matches no "
                f"candidate (tags present: "
                f"{sorted({c['tag'] for c in candidates})})")
        return sorted(pool, key=lambda c: (_version_key(c["version"]), c["iri"]))[-1]
    stable = [c for c in candidates if c["tag"] == "stable"]
    pool = stable or candidates
    ordered = sorted(pool, key=lambda c: (_version_key(c["version"]), c["iri"]))
    if policy == "conservative":
        return ordered[0]
    # latest-stable and any unrecognised policy fall back to newest-first
    return ordered[-1]


def _bound_impl_tools(g: Graph, h: URIRef) -> list[URIRef]:
    """Bound ho:Tool components that carry an implementation binding (candidates
    or a direct ref), sorted by IRI. Restricted to Tools: a Candidate is a
    HarnessComponent that the propertyChainAxiom also makes hasComponent-reachable
    and it carries an implementationRef, but it is resolved THROUGH its tool, not
    emitted on its own."""
    tools = {comp for _p, comp in _iter_components(g, h)
             if (comp, RDF.type, HO.Tool) in g
             and (g.value(comp, HO.implementationRef) is not None
                  or (comp, HO.implementationCandidate, None) in g)}
    return _sorted(tools)


def resolve_selections(g: Graph, h: URIRef, lock: dict | None) -> dict:
    """Resolve every implementation-bearing tool to a single selection, honouring
    a supplied lock (strict reproduction) or the selection policy. Returns an
    ordered dict {tool_iri: selection}; selection carries selected candidate IRI
    (or None for a direct ref), ref, version, tag, and the policy string applied
    ('lock' / 'direct-ref' / the policy / 'stub'). Content hashes are filled in
    later by the emitter."""
    if lock is not None:
        _verify_lock_spec(g, h, lock)
    selections: dict[str, dict] = {}
    for tool in _bound_impl_tools(g, h):
        tool_iri = str(tool)
        locked = (lock or {}).get("tools", {}).get(tool_iri)
        cands = _candidates(g, tool)
        if locked is not None:
            sel = _selection_from_lock(g, tool, locked, cands)
        elif cands:
            policy = _policy_for(g, h, tool)
            chosen = select_candidate(policy, cands, tool_iri)
            sel = {"selected": chosen["iri"], "ref": chosen["ref"],
                   "version": chosen["version"], "tag": chosen["tag"],
                   "policyApplied": policy}
        else:
            ref = str(g.value(tool, HO.implementationRef) or "")
            sel = {"selected": None, "ref": ref, "version": "", "tag": "",
                   "policyApplied": "direct-ref"}
        selections[tool_iri] = sel
    return selections


def _selection_from_lock(g: Graph, tool: URIRef, locked: dict,
                         cands: list[dict]) -> dict:
    """Reproduce a tool's selection strictly from a lock entry. The locked
    candidate (if any) must still exist in the graph with the same ref, so the
    lock names a real, current option (INV-2). The lock's ORIGINAL policyApplied
    is carried forward unchanged so a reproduced tree (and its regenerated lock)
    is byte-identical to the original — the 'reproduced from lock' fact lives in
    the build report, not in mutated snapshot fields."""
    policy = locked.get("policyApplied", "lock")
    sel_iri = locked.get("selected")
    if sel_iri is not None:
        match = next((c for c in cands if c["iri"] == sel_iri), None)
        if match is None:
            raise ValueError(
                f"lock pins candidate {sel_iri} for {tool} but the graph no "
                f"longer offers it (candidates: {[c['iri'] for c in cands]})")
        if match["ref"] != locked.get("ref"):
            raise ValueError(
                f"lock ref mismatch for {sel_iri}: lock={locked.get('ref')!r} "
                f"graph={match['ref']!r}")
        return {"selected": match["iri"], "ref": match["ref"],
                "version": match["version"], "tag": match["tag"],
                "policyApplied": policy}
    # direct-ref tool locked
    ref = str(g.value(tool, HO.implementationRef) or "")
    if ref != locked.get("ref"):
        raise ValueError(
            f"lock ref mismatch for direct-ref tool {tool}: "
            f"lock={locked.get('ref')!r} graph={ref!r}")
    return {"selected": None, "ref": ref, "version": "", "tag": "",
            "policyApplied": policy}


def _tool_stem(tool_iri: str) -> str:
    """Filename stem for a tool's emitted implementation: the IRI's last segment
    with a leading 'tool-' stripped (tool-docgraph -> 'docgraph')."""
    tail = tool_iri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail[len("tool-"):] if tail.startswith("tool-") else tail


def _dest_basename(tool_iri: str, ref: str, from_candidate: bool) -> str:
    """The emitted filename for a tool's implementation. A candidate-backed tool
    gets a STABLE name derived from the tool (stem + the selected file's
    extension) so swapping the implementation candidate does not rename the file
    or break callers (behavioural equivalence). A degenerate direct-ref tool
    keeps its ref's basename (preserving increment-1/2 behaviour)."""
    ref_base = os.path.basename(ref.rstrip("/")) or "implementation"
    if from_candidate:
        return _tool_stem(tool_iri) + os.path.splitext(ref_base)[1]
    return ref_base


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def emit_implementations(g: Graph, h: URIRef, out_dir: str,
                         selections: dict, lock: dict | None) -> list[dict]:
    """Copy each tool's selected implementation into tools/<basename> (or write
    a tools/<basename>.ref stub if unresolvable), recording a content hash on the
    selection. If a lock was supplied, the freshly-computed hash must equal the
    locked hash or the build fails loudly (reproducibility, INV-2). Returns
    manifest records sorted by tool IRI."""
    if not selections:
        return []
    os.makedirs(os.path.join(out_dir, "tools"), exist_ok=True)
    records = []
    for tool_iri in sorted(selections):
        sel = selections[tool_iri]
        ref = sel["ref"]
        basename = _dest_basename(tool_iri, ref, sel["selected"] is not None)
        resolved = _resolve_implementation(ref) if ref else None
        if resolved:
            dest_rel = f"tools/{basename}"
            shutil.copyfile(resolved, os.path.join(out_dir, dest_rel))
            content_hash = _sha256(resolved)
            status = "resolved"
        else:
            dest_rel = f"tools/{basename}.ref"
            with open(os.path.join(out_dir, dest_rel), "w",
                      encoding="utf-8") as fh:
                fh.write(f"# implementation stub for {tool_iri}\n"
                         f"# implementation ref could not be resolved to a "
                         f"local file (URL or missing path).\n"
                         f"# ref: {ref}\n")
            content_hash = None
            status = "stub"
        sel["contentHash"] = content_hash
        if lock is not None:
            locked = lock.get("tools", {}).get(tool_iri, {})
            if locked.get("contentHash") != content_hash:
                raise ValueError(
                    f"lock content-hash mismatch for {tool_iri}: "
                    f"lock={locked.get('contentHash')} built={content_hash}. "
                    f"The pinned implementation file changed — the lock no "
                    f"longer reproduces (INV-2).")
        records.append({"tool": tool_iri, "label": lib.label_of(g, URIRef(tool_iri)),
                        "selected": sel["selected"], "ref": ref,
                        "version": sel["version"], "tag": sel["tag"],
                        "policyApplied": sel["policyApplied"],
                        "status": status, "dest": dest_rel,
                        "contentHash": content_hash})
    return records


def _verify_lock_spec(g: Graph, h: URIRef, lock: dict) -> None:
    """The lock's spec identity must match the current graph, else it does not
    describe this build (INV-2)."""
    spec = lock.get("spec", {})
    if spec.get("harness") != str(h):
        raise ValueError(
            f"lock is for harness {spec.get('harness')} but building {h}")
    count = len(lib.instance_nodes(g))
    if spec.get("individualCount") != count:
        raise ValueError(
            f"lock spec individualCount={spec.get('individualCount')} but the "
            f"current union has {count} individuals — the spec changed, the "
            f"lock no longer reproduces it (INV-2).")


def build_lock(g: Graph, h: URIRef, selections: dict) -> dict:
    """The ODR ③ snapshot: what was actually selected this generation. Fully
    deterministic (no timestamps) so (spec + lock) => byte-identical output."""
    return {
        "lockVersion": 1,
        "spec": {
            "harness": str(h),
            "prefLabel": lib.label_of(g, h),
            "individualCount": len(lib.instance_nodes(g)),
        },
        "tools": {
            tool_iri: {
                "selected": sel["selected"],
                "ref": sel["ref"],
                "version": sel["version"],
                "tag": sel["tag"],
                "policyApplied": sel["policyApplied"],
                "contentHash": sel.get("contentHash"),
            }
            for tool_iri, sel in selections.items()
        },
    }


# --- 7. scaffold emitter (P5) -----------------------------------------
def _scaffold_dest(rel_path: str) -> str:
    """Output path for a scaffold fragment: everything after the (first)
    'scaffold/' marker segment in its source path, so the fragment tree mirrors
    cleanly regardless of where the recipe keeps it
    (recipes/lpranging/scaffold/docs/x.md -> docs/x.md,
    recipes/lpranging/scaffold/STANDARD.md -> STANDARD.md). If there is no
    marker, fall back to the basename."""
    norm = rel_path.replace("\\", "/").lstrip("/")
    marker = "scaffold/"
    idx = norm.find(marker)
    if idx != -1:
        return norm[idx + len(marker):]
    return os.path.basename(norm)


def emit_scaffold(g: Graph, h: URIRef, out_dir: str,
                  sources: list[str]) -> list[dict]:
    """Render ho:scaffold fragments attached to the harness (and its domains)
    into the output tree. Placeholders are substituted from the harness node.
    Return manifest records (sorted by source path)."""
    refs = set(g.objects(h, HO.scaffold))
    for dom in g.objects(h, HO.targetsDomain):
        refs.update(g.objects(dom, HO.scaffold))
    if not refs:
        return []
    records = []
    for ref in _sorted(refs):
        rel = str(ref)
        body = render_from_template(g, h, rel)
        sources.append(rel)
        dest_rel = _scaffold_dest(rel)
        dest = os.path.join(out_dir, dest_rel)
        os.makedirs(os.path.dirname(dest) or out_dir, exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(body if body.endswith("\n") else body + "\n")
        records.append({"source": rel, "dest": dest_rel})
    return records


# --- 8. emit ----------------------------------------------------------
def materialize(g: Graph, h: URIRef, out_dir: str,
                lock: dict | None = None) -> dict:
    """Render the harness file tree into out_dir. Returns the manifest dict.
    When `lock` is given, implementations are reproduced strictly from it
    (byte-identically, or the build fails); otherwise the selection policy is
    applied and a fresh harness.lock.json snapshot is written."""
    os.makedirs(out_dir, exist_ok=True)
    sources: list[str] = []
    roles = _sorted(g.objects(h, HO.hasRole))

    selections = resolve_selections(g, h, lock)
    claude_md = build_claude_md(g, h, sources, roles)
    role_records = emit_roles(g, roles, out_dir, sources)
    impl_records = emit_implementations(g, h, out_dir, selections, lock)
    scaffold_records = emit_scaffold(g, h, out_dir, sources)
    manifest = build_manifest(g, h, sources)
    manifest["roles"] = role_records
    manifest["implementations"] = impl_records
    manifest["scaffold"] = scaffold_records

    # The ODR ③ lock: written on every build. On a fresh build it snapshots the
    # policy-driven selection; when reproducing from a lock it is regenerated
    # identically (all fields deterministic) so `diff -r` of the two trees is
    # empty — the lock file itself included.
    lock_obj = build_lock(g, h, selections)

    with open(os.path.join(out_dir, "CLAUDE.md"), "w", encoding="utf-8") as fh:
        fh.write(claude_md if claude_md.endswith("\n") else claude_md + "\n")
    with open(os.path.join(out_dir, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(out_dir, LOCK_FILENAME), "w", encoding="utf-8") as fh:
        json.dump(lock_obj, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    return manifest


# --- CLI --------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("harness", help="harness IRI or short id (e.g. h-techdoc)")
    ap.add_argument("--out", required=True, help="output directory for the harness file tree")
    ap.add_argument("--lock", default=None,
                    help="reproduce a build from a harness.lock.json snapshot "
                         "(strict: spec identity + content hashes must match)")
    ap.add_argument("--format", choices=["text", "json"], default="text",
                    help="stdout build report (files are always emitted)")
    args = ap.parse_args(argv)

    # -- gate: only a validated harness materializes --
    try:
        result = validate.run_structured()
    except Exception as exc:  # noqa: BLE001
        print(f"✗ could not validate the union: {exc}", file=sys.stderr)
        return 2
    if not result["pass"]:
        print("✗ REFUSING to materialize: the composed union does not validate "
              "(only a validated harness materializes). Run tools/validate.py.",
              file=sys.stderr)
        return 1

    g = lib.load_graph(reason=True)
    try:
        h = resolve_harness(g, args.harness)
    except ValueError as exc:
        print(f"✗ {exc}", file=sys.stderr)
        return 2

    lock = None
    if args.lock:
        try:
            with open(args.lock, encoding="utf-8") as fh:
                lock = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"✗ could not read lock {args.lock}: {exc}", file=sys.stderr)
            return 2

    try:
        manifest = materialize(g, h, args.out, lock)
    except ValueError as exc:
        print(f"✗ REFUSING to materialize: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"✓ materialized {manifest['prefLabel']} -> {args.out}")
        print(f"  CLAUDE.md      ({len(manifest['components'])} components, "
              f"~{manifest['tokenEstimate']} tokens)")
        print(f"  MANIFEST.json  ({len(manifest['capabilityBindings'])} capability bindings, "
              f"{len(manifest['templateSources'])} template source(s))")
        if manifest["roles"]:
            print(f"  .claude/agents/ ({len(manifest['roles'])} role(s))")
        if manifest["implementations"]:
            n_res = sum(1 for r in manifest["implementations"] if r["status"] == "resolved")
            print(f"  tools/          ({n_res}/{len(manifest['implementations'])} "
                  f"implementation(s) copied)")
            for r in manifest["implementations"]:
                sel = r["selected"].rsplit("/", 1)[-1] if r["selected"] else "(direct ref)"
                print(f"      {r['label']}: {sel} "
                      f"[{r['policyApplied']}] -> {r['dest']}")
        if manifest["scaffold"]:
            print(f"  scaffold        ({len(manifest['scaffold'])} fragment(s))")
        mode = "reproduced from lock" if args.lock else "fresh lock written"
        print(f"  {LOCK_FILENAME}  ({mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
