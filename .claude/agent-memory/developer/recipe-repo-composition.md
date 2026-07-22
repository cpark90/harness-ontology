# Recipe repo: composing a Harness from the neutral core parts

중앙 `harness-ontology`(중립 부품 라이브러리, core 64개)와 별개로, "부품을 어떻게
조립하는가"는 **recipe repo**(`harness-recipes`, 구 `harness-data-lpranging`)에 산다.
recipe = assembly spec: 중앙 core를 `owl:imports`하고 core 부품을 IRI로 묶어 완전한
`ho:Harness`를 조립하며, 도메인 특화 노드만 그 파일 안에 LOCAL로 선언. 중앙은 중립 유지.

## 핵심 함정 (겪음)

- **transitive import**: recipe가 `derivedFrom core:h-multiagent`처럼 `core/harnesses` 유닛을
  import하면, 그 유닛의 seed harness(h-coding/research/support)가 **다른 모든 core 유닛의
  컴포넌트**(sp-*, tool-*, wf-* 등)를 참조한다. 일부 유닛만 import하면 그 참조 노드들이
  data 없이 range 추론으로만 타입돼 SHACL `promptText`/`prefLabel` minCount 위반이 뜬다.
  → recipe는 **core 11개 유닛 전부** import해야 union이 완결(= 중앙 64 + recipe locals).
  gate "union = central 64 + recipe"도 이걸 요구.
- capability 짝: `requiresCapability`는 harness의 컴포넌트가 `providesCapability`해야 충족.
  `_components`는 hasGuardrail/hasWorkflow도 포함하므로 gr-traceability→cap-traceability,
  wf-multiagent→cap-orchestration이 워크플로/가드레일 경유로 충족된다(tool만이 아님).

## 조립 레시피 (lpranging 예)

- 문서 IRI `.../recipes/<name>`, 개체 IRI `@prefix id: <.../id/<name>/>` + `core:` prefix로
  중앙 노드 참조(D3). derivedFrom로 template 계보 남김(예: core:h-multiagent).
- REUSE(core: IRI): gr-* 9종, wf-multiagent, pat-orchestrator-workers, mc-opus,
  tool-shell/editor, task-architecture/designdecision, 중립 concept, generic cap.
- LOCAL(id:): Domain, concept 서브트리(root는 `core:scheme` topConceptOf), 도메인 tool+cap,
  persona SystemPrompt. text 노드엔 tokenEstimate, prefLabel/definition 영어.

## 검증 (clone→compose→central validate)

recipe repo엔 tool 없음. 중앙을 `./central/`로 clone(gitignore /central/), 중앙 validate.py를
env override로 실행:
```
HARNESS_CATALOG=catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<name> \
/usr/bin/python3 central/tools/validate.py   # PASS
```
catalog는 중앙 IRI→`central/…`, recipe IRI→`recipes/<name>/<name>.ttl` 매핑(경로는 catalog
디렉토리 기준). 로컬 proof는 `central` 심링크로 이 repo 가리켜 실행 후 **삭제**(payload
symlink-free 유지). CI는 recipe root IRI matrix로 recipe별 union 검증. 문서:
`docs/recipes-design.md`(federation-design.md에서 링크).

## reuse-max 레시피 (techdoc 예 — 신규 tool/cap 0개)

- 도메인이 core tool로 다 커버되면 **신규 tool·capability 없이** 조립 가능. techdoc(h-research
  파생)은 LOCAL 4개만: dom-, c-(broader core:c-communication), task-, sp-persona. requiresCapability
  4개 전부 core 컴포넌트가 provider: cap-retrieval←tool-retriever, cap-websearch←tool-websearch,
  **cap-citation←gr-cite(가드레일이 provider)**, cap-fileedit←tool-editor. tool만이 provider가
  아님을 재확인.
- union 개체수 = 중앙 64 + recipe local N (techdoc N=5 harness 포함 → 69). lpranging은 병존 유지(75).
- 로컬 concept은 `skos:broader core:<concept>`로 중앙 SKOS 트리에 바로 매달아도 됨(topConceptOf
  core:scheme 대신) — reachable. persona/task는 maturity draft, base가 mc-opus면 accuracy-review
  rigor 근거로 mc-opus 유지가 자연스러움.
