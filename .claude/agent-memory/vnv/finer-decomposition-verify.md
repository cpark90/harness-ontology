# finer harness decomposition + graph-driven assembly (scope c) 검증 재현 절차 + 함정

3-stage feature: (a) `ho:WorkflowStep`+`hasStep`, (b) `ho:PromptSection`+`hasSection`,
(c) `ho:AssemblySection`+`hasAssemblySection` (graph-driven materialize section order) + role-model
refinement. 전부 `/usr/bin/python3`. 판정: `docs/verify/finer-decomposition.md` (pass-with-notes).

## 핵심 anti-mistype 판정 (모델링 선택이 case별로 맞는지)
- **direct sub-property vs propertyChain 구분이 정답의 축**: subject가 Harness이면 direct
  subPropertyOf hasComponent (예 `hasAssemblySection`, hasRole/hasChannel와 동일) — 맞음.
  subject가 intermediate(Workflow/SystemPrompt)이면 direct는 domain=Harness로 그 중간노드를
  Harness로 mistype→HarnessShape trip. 그래서 (a)/(b)는 chain `( hasComponent hasStep )` /
  `( hasComponent hasSection )` 사용. 검증: reasoned graph에서 `(wf-multiagent,rdf:type,Harness)`
  =False, `(sp-methodical,…Harness)`=False, `(as-*,…Harness)`=False, `(h-multiagent,…Harness)`=True.
  그리고 `(hasStep,rdfs:subPropertyOf,hasComponent)`=False / `(hasAssemblySection,…)`=True 확인.
  (b)의 chain 첫 링크는 `hasSystemPrompt ⊑ hasComponent` 덕분에 성립.

## byte-identical의 정확한 의미 (N2 — 오판 주의)
- 보존 불변량 = **문서 top-level 섹션 ORDER + full-tree determinism**. 섹션 BODY 아님.
  (a)/(b)는 의도적으로 body를 바꾼다: Persona blob→3 ordered fragment, Process 1줄→3 ordered step.
  → 과거 산출물과 naive byte-diff하면 두 body가 DIFFER하는 게 정상(회귀 아님). "byte-identical
  preserving"은 heading 순서가 historical fixed order와 같음 + 2회 run `diff -r` IDENTICAL로 증명.
- historical fixed order = overview/Persona/Operating rules/Process/Model/Roles/Channels/Skills.
  h-multiagent가 default holder(`lib.DEFAULT_ASSEMBLY_HOLDER=core:h-multiagent`)라 as-1..8이 그 순서.

## error/redefine 재현 (임시 recipe, 실파일 미편집)
- scratch recipe: `ln -sfn $(pwd) <scratch>/recipe/central` + scratch catalog(central IRI→
  central/ontology/*, 추가로 central root `.../ontology`→central/ontology/harness-ontology.ttl
  매핑 필수—scratch harness가 이걸 import해 전 core 로드) + scratch.ttl(scratch harness는 core
  부품 재사용으로 HarnessShape 최소 충족). `HARNESS_CATALOG=<catalog> HARNESS_ROOT_ONTOLOGY=
  https://harness-ontology.dev/scratch central/tools/{validate,materialize}.py`. **끝나면 rm central**.
- **3 error mode의 게이트 분업 확인**: dup order→validate.check_assembly_order(SET-level)만 FAIL
  (SHACL는 통과=정상, 중복은 per-node 아님). missing order→SHACL MinCount+check 둘다. unknown
  sectionKind→SHACL `sh:in` InConstraint. materialize atomicity: dup harness materialize→gate가
  load/write 전에 validate 실행→REFUSE exit1 + **out dir 미생성**(atomic) 확인.
- redefine: scratch harness가 자기 `hasAssemblySection`(예 model=1/overview=2/persona=3, 나머지
  drop) 선언→union PASS→materialize heading이 그 순서로 바뀜, 그리고 h-multiagent default는 불변.

## role-model
- `userFacing` **present-only**: orchestrator/inspection만 true, worker 5개는 absent(None). 산출물
  검증: emitted `.claude/agents/*.md`에서 "User-facing role" 줄이 orchestrator.md/inspection.md에만.
- least-privilege: 각 role의 roleTool/roleGuardrail ⊆ harness usesTool/hasGuardrail (violation NONE).
- orchestrator/design는 roleTool 없음(Tools 섹션 부재)=defensible least-privilege, 결함 아님(N4).
- channel redefinability는 **TBox**(ho:Channel class / ho:hasChannel def)에 기술, 개별 channel
  individual skos:definition 아님 — 정위치(schema-wide 의미), N3 note only.

## 함정
- **loader catalog-vs-glob triple symdiff≠0 오탐 금지**: 여기선 44인데 전부 propertyChainAxiom
  RDF-list의 BNode 재라벨(rdf:first/rest/BNode). URI-individual symdiff=0이 진짜 등가 증명. (chain
  4개 생기며 BNode list가 늘어 이전보다 symdiff 큼.)
- materialize.py:51-53 주석 "emitted in this fixed order" stale(이제 resolve_assembly_order graph-
  driven) — N5 cosmetic.
