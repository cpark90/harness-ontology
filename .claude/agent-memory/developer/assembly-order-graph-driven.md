# Assembly order as graph SPEC — AssemblySection (Stage c)

finer-harness-decomposition-assembly Stage (c), the high-risk one: move the
CLAUDE.md section ASSEMBLY ORDER out of hardcoded materialize code into the graph
so "how parts are assembled" is inspectable + per-harness redefinable; materialize
only READS it. Preserve byte-identical CLAUDE.md.

## TBox vocab (central, neutral)
- `ho:AssemblySection ⊑ HarnessComponent`.
- `ho:hasAssemblySection` Harness→AssemblySection. ★ **Direct `rdfs:subPropertyOf ho:hasComponent`**
  (like hasRole/hasChannel), NOT a propertyChain. TRAP I hit: I first added a 5th
  `propertyChainAxiom (hasComponent hasAssemblySection)` mirroring hasStep/hasSection —
  WRONG. Those chains work because the subject is an intermediate (Workflow/SystemPrompt)
  reached via hasComponent; `harness hasComponent workflow ∧ workflow hasStep step`. But
  AssemblySection hangs DIRECTLY off the Harness, so the chain would need `harness
  hasComponent harness` (not asserted → sections unreachable). Since hasAssemblySection's
  SUBJECT genuinely IS the Harness, a plain sub-property is correct and safe (no prp-dom
  mistype — unlike hasStep/hasSection whose subject isn't a Harness). Rule of thumb:
  Harness→X assembly edge = sub-property of hasComponent; Intermediate→X = propertyChain.
- `ho:assemblyOrder` (domain AssemblySection, xsd:integer; 1-based, unique per holder = total order).
- `ho:sectionKind` (domain AssemblySection, xsd:string) CLOSED enum matching emitter renderers:
  overview/persona/operating-rules/process/model/roles/channels/skills.

## ABox default (core/harnesses.ttl)
8 shared `id:as-*` AssemblySections (order 1..8 = current fixed order) attached to
`id:h-multiagent` via hasAssemblySection. This does double duty: (1) anti-orphan
(sections reachable via h-multiagent), (2) IS the central DEFAULT every harness inherits.
`lib.DEFAULT_ASSEMBLY_HOLDER = ID_CORE["h-multiagent"]` = single well-known location both
materialize+validate resolve. prefLabels unique in class ("Assembly: <kind> section").

## materialize (tools/materialize.py) — the refactor
- Extracted each hardcoded section into `_render_<kind>(g,h,out,ctx)` appending EXACT same
  lines; `SECTION_RENDERERS` dict kind→fn (also THE closed set of buildable kinds).
- `resolve_assembly_order(g,h)`: own hasAssemblySection → else DEFAULT_ASSEMBLY_HOLDER's →
  else ValueError. Checks per-section order present+int, kind present+known, orders unique
  (duplicate→raise). Returns kind list sorted by order.
- `build_claude_md` now just: `for kind in resolve_assembly_order: SECTION_RENDERERS[kind](...)`.
  ctx carries sources/roles/channels/instructions/role_personas. Conditional renderers
  (roles/channels/skills) self-suppress when empty → byte-identical to old `if roles:` guards.
- Error path is defense-in-depth: validate gate refuses first, but resolve_assembly_order
  ALSO raises → materialize exit 1, atomic emit leaves NO output dir.

## Gates
- SHACL `AssemblySectionShape` (shapes/): per-node assemblyOrder 1..1 int + sectionKind 1..1 sh:in enum.
- `validate.check_assembly_order` (validate.py, wired into run_structured hard_ok + main): SET-level
  totality (unique orders per holder) + default holder non-empty. Both added to summary.
- ontology_lib: HO.AssemblySection→INSTANCE_CLASSES; HO.hasAssemblySection→INSTANCE_LINK_PREDICATES.

## Byte-identical PROOF (the crux)
CLAUDE.md diff baseline-vs-post = IDENTICAL for all harnesses (order default == old fixed).
MANIFEST/lock DO change (expected): h-multiagent MANIFEST +8 AssemblySection components,
tokenEstimate +142; every lock's spec.individualCount 102→110 (union grew). NOT a CLAUDE.md
regression. Determinism: two runs diff -r IDENTICAL. individuals 102→110.

## Scratch-overlay testing pattern (error/redefine without polluting repo)
Env-override federation (memory recipe-repo-composition): scratch catalog maps core IRIs to
REAL repo files (absolute paths) + adds scratch root(s)+data unit(s); run with
HARNESS_CATALOG + HARNESS_ROOT_ONTOLOGY. redefine harness = own hasAssemblySection w/ new
orders (model before persona) → materialize emits reordered sections (proves redefinability).
broken harness = duplicate assemblyOrder 2 → validate FAIL + materialize exit 1 no output.
All in scratchpad; no symlinks/files left in repo.
