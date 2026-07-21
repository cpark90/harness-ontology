"""Style-preserving, surgical writes to the ABox TTL files.

We never rdflib-serialize the whole graph: that would destroy the hand-authored
section banners, comments, one-line-vs-multiline style and predicate order that
make the TTL human-diffable (ONTOLOGYSTYLE §3·§4). Instead we render a single
node block per ONTOLOGYSTYLE and splice it into the target file as text —
replacing the subject's existing block or appending a new one — then write
atomically (temp + os.replace) so a crash never exposes a half-written file.

Validation is done by the caller against the parsed graph; persistence here is
purely textual.
"""
from __future__ import annotations

import glob
import os
import re
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ABOX_DIR = os.path.join(ROOT, "ontology", "abox")

# Predicate emission order (subject `a` first, then labels, then structure,
# then datatype props) — mirrors ONTOLOGYSTYLE §3.
ORDER = [
    "skos:prefLabel", "skos:altLabel", "skos:definition",
    "ho:targetsDomain", "ho:addressesTask", "ho:hasSystemPrompt",
    "ho:usesTool", "ho:hasWorkflow", "ho:hasGuardrail", "ho:usesModel",
    "ho:hasInstruction", "ho:hasExample", "ho:appliesPattern",
    "ho:requiresCapability", "ho:providesCapability", "ho:constrainedBy",
    "ho:dependsOn", "ho:specializes", "ho:derivedFrom", "ho:tagged",
    "skos:broader", "skos:narrower", "skos:related", "skos:topConceptOf",
    "ho:promptText", "ho:tokenEstimate", "ho:salience", "ho:maturity",
]
STRING_PREDS = {"skos:prefLabel", "skos:altLabel", "skos:definition",
                "ho:promptText", "ho:maturity"}

_SUBJECT_RE = re.compile(r"^(id:[A-Za-z0-9_-]+)\b")

# The webui authors into the `core` domain (D3, docs/federation-design.md); the
# authored.ttl unit is importable as .../data/authored and is already listed in
# catalog-v001.xml + the root ontology, so it joins the union when first created.
_HEADER = (
    "@prefix ho:    <https://harness-ontology.dev/schema#> .\n"
    "@prefix id:    <https://harness-ontology.dev/id/core/> .\n"
    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"
    "@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n"
    "@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .\n"
    "@prefix skos:  <http://www.w3.org/2004/02/skos/core#> .\n\n"
    "<https://harness-ontology.dev/data/authored> a owl:Ontology ;\n"
    "    owl:imports <https://harness-ontology.dev/schema> .\n\n"
    "# Nodes authored via the web UI (tools/webui). Same TBox vocabulary as the\n"
    "# other abox files — kept separate only so authored nodes are easy to find.\n\n"
)


class Conflict(Exception):
    """Raised when a target file changed on disk since the caller read it."""


def _lit(value) -> str:
    s = (str(value).replace("\\", "\\\\").replace('"', '\\"')
         .replace("\n", "\\n").replace("\r", ""))
    return f'"{s}"'


def render_block(node: dict) -> str:
    """Render one node's TTL block from a structured dict. `id` and `type` are
    prefixed names (e.g. 'id:h-foo', 'ho:Harness'); other keys are prefixed
    predicates whose values are strings, numbers, or lists of 'id:' refs."""
    subject = node["id"]
    pairs = [("a", node["type"])]
    for pred in ORDER:
        if pred not in node:
            continue
        value = node[pred]
        if value is None or value == "" or value == []:
            continue
        if pred in STRING_PREDS:
            vals = value if isinstance(value, list) else [value]
            rendered = ", ".join(_lit(v) for v in vals if str(v) != "")
        elif pred == "ho:tokenEstimate":
            rendered = str(int(value))
        elif pred == "ho:salience":
            rendered = f"{float(value)}"
        else:  # object property -> id: refs
            vals = value if isinstance(value, list) else [value]
            vals = [v for v in vals if v]
            rendered = ", ".join(vals)
        if not rendered:
            continue
        pairs.append((pred, rendered))
    body = " ;\n    ".join(f"{p} {v}" for p, v in pairs)
    return f"{subject} {body} ."


def abox_files() -> list[str]:
    return sorted(glob.glob(os.path.join(ABOX_DIR, "*.ttl")))


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def _iter_blocks(text: str):
    """Yield (subject, start_line, end_line) for each `id:... .` block. A block
    starts at a line beginning with `id:<name>` and ends at the first following
    line whose stripped text ends with '.'."""
    lines = text.split("\n")
    i, n = 0, len(lines)
    while i < n:
        m = _SUBJECT_RE.match(lines[i])
        if m:
            j = i
            while j < n and not lines[j].rstrip().endswith("."):
                j += 1
            yield m.group(1), i, min(j, n - 1)
            i = j + 1
        else:
            i += 1


def find_subject_file(subject: str):
    for path in abox_files():
        for subj, _i, _j in _iter_blocks(_read(path)):
            if subj == subject:
                return path
    return None


def _replace_block(text: str, subject: str, new_block: str):
    lines = text.split("\n")
    for subj, i, j in _iter_blocks(text):
        if subj == subject:
            return "\n".join(lines[:i] + new_block.split("\n") + lines[j + 1:])
    return None


def _check_mtime(path: str, expected_mtimes) -> None:
    if not expected_mtimes:
        return
    want = expected_mtimes.get(os.path.basename(path))
    if want is not None and abs(os.path.getmtime(path) - float(want)) > 1e-6:
        raise Conflict(f"{os.path.basename(path)} changed on disk since read")


def plan_upsert(node: dict, target_basename: str = "authored.ttl",
                expected_mtimes: dict | None = None) -> dict:
    """Compute the write without performing it. Returns
    {file, old, new, created} — `old` is None when a new file is created."""
    subject = node["id"]
    block = render_block(node)
    existing = find_subject_file(subject)
    if existing:
        _check_mtime(existing, expected_mtimes)
        old = _read(existing)
        new = _replace_block(old, subject, block)
        return {"file": existing, "old": old, "new": new, "created": False}

    path = os.path.join(ABOX_DIR, target_basename)
    if os.path.exists(path):
        _check_mtime(path, expected_mtimes)
        old = _read(path)
        new = old.rstrip("\n") + "\n\n" + block + "\n"
        return {"file": path, "old": old, "new": new, "created": False}
    return {"file": path, "old": None, "new": _HEADER + block + "\n",
            "created": True}


def atomic_write(path: str, text: str) -> None:
    directory = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".ttl.tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def restore(path: str, old: str, created: bool) -> None:
    """Undo a write: delete a newly-created file, or restore prior content."""
    if created:
        if os.path.exists(path):
            os.remove(path)
    else:
        atomic_write(path, old)
