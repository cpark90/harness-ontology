# materialize increment 2 — roles (P4) / impl-ref (P3) / scaffold (P5)

`tools/materialize.py` 두 번째 증분. recipe→full multi-agent 하네스 트리(clone 없이).

## P4 first-class Role
- `ho:Role rdfs:subClassOf ho:HarnessComponent` → role 개체가 harness-reachable·counted,
  기존 orphan shape(inverse hasComponent)로 커버(shape 추가 불요).
- `ho:hasRole rdfs:subPropertyOf ho:hasComponent` (range Role) — **이게 핵심**: OWL RL이
  hasRole→hasComponent materialize해서 reachability/SHACL 자동 충족.
- scope: `ho:rolePersona`(→SystemPrompt) / `ho:roleTool`(→Tool) / `ho:roleGuardrail`(→Guardrail)
  + datatype `ho:roleMemoryPolicy`(→string). rolePersona/roleTool/roleGuardrail은
  INSTANCE_LINK_PREDICATES에도 추가(retrieve/BFS 그래프뷰).
- **함정(persona 연결성)**: rolePersona는 hasComponent 서브프로퍼티로 못 만듦(domain=Role→
  harness를 Role로 mistype). 그래서 role persona SystemPrompt는 harness에 `hasSystemPrompt`로
  **따로 바인딩**해야 ComponentConnectivityShape+SystemPromptShape 통과. 중복 방지로 materialize는
  top-level `## Persona`에서 role persona 제외(role 파일에만 렌더).
- roleTool/roleGuardrail은 harness가 이미 usesTool/hasGuardrail로 바인딩한 파트의 **subset**만
  가리킴(least-privilege) → orphan 안 생김.
- emit: `.claude/agents/<slug>.md`, slug=IRI 끝 세그먼트 `role-` prefix strip(role-developer→
  developer.md). frontmatter(name/description)+persona+`## Tools`+`## Guardrails`+`## Memory policy`.
  `CLAUDE.md`에 `## Roles` 요약.

## P3 implementationRef (실코드 COPY)
- `ho:implementationRef`(domain Tool, range string) = path/URL. materialize가 **실파일을
  tools/<basename>로 byte-copy**(shutil.copyfile). resolve 순서=repo root→catalog dir→절대경로.
- 못 찾으면(URL/부재) `tools/<basename>.ref` **stub** 작성(status stub) — tool 무음 드롭 금지·
  오프라인 graceful. MANIFEST implementations:[{tool,label,ref,status,dest}].
- **portability caveat**: 절대 ref는 그 checkout 있는 머신만 resolve. 이식성 원하면 recipe repo
  안에 코드 넣고 repo-relative ref(catalog dir 기준). 데모는 절대경로(~/git/agrtls/...) 사용.

## P5 scaffold (standard docs / docs-tree)
- **artifactTemplate 재사용 불가**: domain이 ho:HarnessComponent라 Harness/Domain에 붙이면
  OWL RL이 그 노드를 HarnessComponent로 추론→orphan shape trip. 그래서 새 `ho:scaffold`(domain
  없음·range string) 추가, standalone 파일 emit(section 아님).
- 값=repo-relative fragment path. harness/targetsDomain domain에 부착. {{prefLabel}}/{{definition}}
  치환은 **harness 노드**로. dest=source에서 `scaffold/` marker 이후(recipes/x/scaffold/docs/y.md
  →docs/y.md, .../scaffold/STANDARD.md→STANDARD.md). MANIFEST scaffold:[{source,dest}].

## 검증/데모
- Stage A gate: 중앙 abox 불변 64(TBox+ontology_lib registry만 변경), 두 로더(catalog imports/
  glob fallback) 동치, PASS. INSTANCE_CLASSES에 HO.Role 등록 필수.
- 데모 union: staging/harness-recipes catalog + central 심링크(→repo root, 실행후 rm).
  81 개체(75 prior + 3 role + 3 role persona). materialize h-lpranging→CLAUDE.md+
  .claude/agents/{developer,vnv,inspection}.md+tools/{docgraph.py 32560B real, sim_grid_reservation.py}
  +DESIGN_HARNESS_STANDARD.md+docs/README.md+MANIFEST.json. 결정성=2런 diff -r identical.
- gate는 materialize 내부 validate.run_structured()(env catalog로 recipe union) — 심링크 있어야 통과.
