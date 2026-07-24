# DA-4 — flat class taxonomy → intermediate superclass layer (pure TBox reparenting)

Insert a MAS-tuple-aligned middle layer between leaves and their tops WITHOUT touching
ABox/tools/shapes. File-exclusive = `tbox/harness.ttl` ONLY. Design: `disambiguation-audit.md` §G.

## What was flat → what got a middle layer
- 22 `⊑ho:HarnessComponent` leaves regrouped under **9 new intermediates** (each `⊑HarnessComponent`):
  Behavioral(SystemPrompt/PromptSection/Guardrail/Instruction/Example) · Observational(ObservationSpace/
  AreaOfInterest/AreaOfObservation) · Operational(Tool/Candidate) · State(Memory) · Organization(Agent/
  Role/Channel) · Process(Workflow/WorkflowStep/Deliverable) · Verification(Contract/TestScenario/
  FailurePolicy) · Assembly(AssemblySection) · Substrate(ModelConfig).
- 7 non-component leaves (had NO subClassOf) got a **new** parent under **2 new top-level** classes:
  `ho:SpecConcept`(Capability/Task/Domain/DesignPattern/Constraint) · `ho:InformationSpace`
  (EnvironmentSpace/GlobalState). Both top-level owl:Class, NOT ⊑HarnessComponent.
- `ho:Concept`(⊑skos:Concept, vocab layer) untouched. Domain stays SpecConcept (single parent);
  it still participates in the 4-space chain via properties (scopedFrom/describesDomain), not subclassing.

## Why it's zero-risk (the load-bearing insight)
- **owlrl transitivity**: a leaf 2 hops from HarnessComponent (leaf⊑Intermediate⊑HarnessComponent)
  still infers `a HarnessComponent` for every instance → ComponentConnectivityShape / reachability /
  Capability shape targetClass all still hit leaf instances. Same precedent as the old Memory⊑HC.
- **Intermediates get NO INSTANCE_CLASSES entry** (tools untouched): they have zero direct instances;
  leaves remain the direct rdf:type, counted via HarnessComponent subsumption as before. 185 invariant.
- **materialize byte-identity is automatic**: no emitter reads rdfs:subClassOf / class hierarchy; only
  per-NODE prose. h-multiagent CLAUDE.md byte-identical (2-run cmp, full tree diff clean).
- class-level skos:definition is NOT rendered into any CLAUDE.md (DA-2 precedent) → new intermediate
  defs are inert for the build.

## Edit mechanics
- Each leaf edited via the unique 2-line anchor `ho:X a owl:Class ;\n    rdfs:subClassOf ho:HarnessComponent ;`
  (class name makes it unique; plain replace_all would clobber all 22). Non-component leaves lacked
  subClassOf → INSERTED a new `rdfs:subClassOf` line between `a owl:Class ;` and `rdfs:label`.
- Predicate order kept: `a owl:Class ; rdfs:subClassOf ; rdfs:label ; skos:definition .`
- Sanity grep: `grep -B1 "subClassOf ho:HarnessComponent" | grep "a owl:Class"` must list EXACTLY the
  9 intermediates (no leaf leaks left pointing directly at HarnessComponent).

## Verification (all green)
central validate PASS 185 individuals invariant; materialize h-multiagent byte-identical;
recipe 21-code-reviewer closure PASS (HARNESS_CATALOG=catalog-v001.xml +
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/21-code-reviewer). No flag needed —
single-inheritance throughout, no shape/property touched.
