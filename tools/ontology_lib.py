"""Shared helpers for loading and reasoning over the harness ontology.

Both validate.py and retrieve.py build on this so the graph is loaded and
reasoned identically everywhere (one source of truth).
"""
from __future__ import annotations

import glob
import os
from typing import Iterable

import rdflib
from rdflib import Graph, Namespace, URIRef, RDF, RDFS
from rdflib.namespace import SKOS

HO = Namespace("https://harness-ontology.dev/schema#")
ID = Namespace("https://harness-ontology.dev/id/")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONT_DIR = os.path.join(ROOT, "ontology")

# Predicates that connect one *instance* to another (used for the graph
# view). Datatype/annotation predicates are intentionally excluded.
INSTANCE_LINK_PREDICATES = {
    HO.hasComponent, HO.componentOf, HO.hasSystemPrompt, HO.usesTool,
    HO.hasGuardrail, HO.hasWorkflow, HO.usesModel, HO.hasExample,
    HO.hasInstruction, HO.targetsDomain, HO.addressesTask, HO.addressedBy,
    HO.requiresCapability, HO.providesCapability, HO.appliesPattern,
    HO.constrainedBy, HO.dependsOn, HO.specializes, HO.derivedFrom,
    HO.tagged, SKOS.broader, SKOS.narrower, SKOS.related,
}

# The classes we treat as first-class ontology individuals.
INSTANCE_CLASSES = {
    HO.Harness, HO.HarnessComponent, HO.SystemPrompt, HO.Instruction,
    HO.Tool, HO.Guardrail, HO.Workflow, HO.ModelConfig, HO.Example,
    HO.Capability, HO.Domain, HO.Task, HO.DesignPattern, HO.Constraint,
    HO.Concept,
}


def load_graph(reason: bool = True) -> Graph:
    """Load every .ttl under ontology/ and (optionally) materialise the
    OWL RL closure so subclass typing, inverses and sub-properties are
    explicit — SHACL and traversal both rely on that."""
    g = Graph()
    g.bind("ho", HO)
    g.bind("id", ID)
    g.bind("skos", SKOS)
    for path in sorted(glob.glob(os.path.join(ONT_DIR, "**", "*.ttl"), recursive=True)):
        # Shapes are validation-only; don't fold them into the data graph.
        if os.sep + "shapes" + os.sep in path:
            continue
        g.parse(path, format="turtle")
    if reason:
        apply_reasoning(g)
    return g


def apply_reasoning(g: Graph) -> Graph:
    """Materialise OWL RL closure in place."""
    import owlrl
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    return g


def instance_nodes(g: Graph) -> set[URIRef]:
    """All URIRef individuals typed (directly or via inference) as one of
    our ontology classes."""
    nodes: set[URIRef] = set()
    for cls in INSTANCE_CLASSES:
        for s in g.subjects(RDF.type, cls):
            if isinstance(s, URIRef):
                nodes.add(s)
    return nodes


def instance_edges(g: Graph) -> list[tuple[URIRef, URIRef, URIRef]]:
    """(subject, predicate, object) triples that link two individuals."""
    edges = []
    nodes = instance_nodes(g)
    for s, p, o in g:
        if p in INSTANCE_LINK_PREDICATES and s in nodes and o in nodes:
            edges.append((s, p, o))
    return edges


def label_of(g: Graph, node: URIRef) -> str:
    for pred in (SKOS.prefLabel, RDFS.label):
        val = g.value(node, pred)
        if val is not None:
            return str(val)
    return node.split("#")[-1].split("/")[-1]


def most_specific_types(g: Graph, node: URIRef) -> list[URIRef]:
    """Asserted/inferred types of node that are in INSTANCE_CLASSES,
    dropping superclasses when a subclass is present."""
    types = {t for t in g.objects(node, RDF.type)
             if isinstance(t, URIRef) and t in INSTANCE_CLASSES}
    specific = set(types)
    for t in types:
        for sup in g.objects(t, RDFS.subClassOf):
            specific.discard(sup)
    return sorted(specific) if specific else sorted(types)
