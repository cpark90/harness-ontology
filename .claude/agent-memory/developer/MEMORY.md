# developer 역할 메모리

온톨로지 노드 저작 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/developer.md`. 노드 종류별 함정·모델링 패턴·capability 배선을 파일로 추가하고
아래에 한 줄로 인덱스한다.

- 완결 brief로 받은 배정분만 구현: 온톨로지 노드(`ontology/abox/`) 또는 배정 소스(`tools/**` 등).
  TBox·shapes·brief 밖 경로는 안 만짐. 검증(vnv)·커밋(inspection)은 안 함. 온톨로지 노드 스타일은
  `ONTOLOGYSTYLE.md` [지킴], 소스는 기존 컨벤션·언어 표준.
- 도구는 `rdflib` 등이 있는 인터프리터로(예: `/usr/bin/python3`). 셸 기본 python3엔 없을 수 있음.

<!-- 학습 인덱스 (한 줄씩) -->
- [materialize-roles-impl-scaffold](materialize-roles-impl-scaffold.md) — materialize 증분2:
  P4 `ho:Role`(subClassOf HarnessComponent + `ho:hasRole` subPropertyOf hasComponent→reachable·
  shape 자동, rolePersona/roleTool/roleGuardrail/roleMemoryPolicy; persona는 hasSystemPrompt로도
  바인딩해야 연결·top Persona서 제외→`.claude/agents/<slug>.md`), P3 `ho:implementationRef`
  (실파일 tools/<basename> byte-copy·resolve repo→catalog→abs·못찾으면 .ref stub·절대경로 이식성caveat),
  P5 `ho:scaffold`(domain 없음 필수-artifactTemplate은 HarnessComponent domain이라 Harness 붙이면
  orphan trip; scaffold/ marker 이후로 dest mirror). registry에 HO.Role 등록·중앙 64 불변·81 union.
- [materialize-build-projection](materialize-build-projection.md) — `tools/materialize.py`
  = retrieve의 DUAL(BUILD 투영: validated harness IRI→`CLAUDE.md`+`MANIFEST.json` 파일트리).
  validate.run_structured() 게이트 후 build("only validated materializes"), 결정성(IRI sort+
  sort_keys+무타임스탬프→byte-identical), `most_specific_types` OWL RL 반사 subClassOf 함정은
  소비자에서 HarnessComponent 드롭으로 우회(lib 불변). P2 `ho:artifactTemplate`(datatype prop,
  domain HarnessComponent, 파일참조·absent⇒graph fallback·{{prefLabel}}/{{promptText}} 치환,
  path resolution=repo root→catalog dir). 데모 catalog=절대경로 scratch(central clone 불요).
- [neutral-parts-decomposition](neutral-parts-decomposition.md) — 온톨로지 = domain-INDEPENDENT
  재사용 PART 라이브러리(특정 harness 서술 아님): governance doc→중립 Guardrail/Pattern/Workflow/
  SystemPrompt로 분해, gr-lang 재사용·도메인 명사 제거·domain tool dependsOn strip. anti-orphan
  때문에 파트를 중립 harness(h-multiagent) 하나에 배선 필수. seed.ttl(core)에 append(plumbing 불요).
  도메인 split 은퇴: catalog/root infra 유지·엔트리만 drop·NOTE는 retired로·staging 삭제·grep은 노드만(주석 허용).
- [model-external-harness](model-external-harness.md) — 외부 멀티에이전트/설계 하네스를 abox로
  모델링: role split→Workflow+pat-orchestrator-workers, tool→Tool+cap, CLAUDE 규칙→Guardrail,
  gr-lang 재사용, 캡 requires↔provides 짝, 개념 reachability(ho:tagged 필수·topConceptOf 부족).
- [webui-svelte-frontend](webui-svelte-frontend.md) — tools/webui 프론트 Svelte+Vite 재작성:
  vite outDir=../static·emptyOutDir, compose ./tools 마운트 제거(shadowing), Dockerfile 멀티스테이지,
  Svelte5 mount/a11y, /api/* 응답 형태·retrieve id는 full URI.
- [split-core-per-type-units](split-core-per-type-units.md) — 중앙 core seed.ttl→컴포넌트
  타입별 다중 문서(`ontology/abox/core/<type>.ttl`, 11 units/64 개체) 재파일: 라인 슬라이스
  스크립트로 byte-identical 이동(triple diff 0 검증), wiring=root union(각 유닛 schema만 import·
  root가 11개 나열), Constraint 별도 파일 함정, 두 로더 경로 동치 증명, retrieve 동점 tie-order만
  재배열(candidates/gaps 불변), ONTOLOGYSTYLE §4 다중 core 규칙 추가. seed.ttl live ref만 갱신.
- [recipe-repo-composition](recipe-repo-composition.md) — 중립 core에서 Harness 조립하는
  recipe repo(harness-recipes): recipe=assembly spec(core owl:imports+IRI 참조로 Harness 조립,
  도메인 노드만 LOCAL). 함정=transitive import(core/harnesses가 다른 유닛 전부 참조→core 11유닛
  전부 import해야 union 완결, gate=중앙64+recipe locals). cap짝은 gr/wf 컴포넌트도 provider.
  검증=clone central→env override(HARNESS_CATALOG/ROOT_ONTOLOGY)로 중앙 validate.py, 로컬 proof
  심링크는 실행후 삭제(payload symlink-free). CI=recipe root IRI matrix. docs/recipes-design.md.
- [guardrail-item-datatype-property](guardrail-item-datatype-property.md) — 규칙 세부를 별도
  노드 아닌 **컴포넌트 item/field**로: 사용자 인가 vocab ext로 TBox datatype property 1개 추가
  (`ho:languageCondition` domain Guardrail range string, promptText 스타일 모방)+ABox 값 콤마
  다중 리터럴(artifact당 1, 영어). shapes는 `sh:closed` 없으면 무수정. 중앙 노드 enrich=IRI
  재사용 recipe에 자동 반영(심링크 검증후 삭제·개체수 불변).
- [federation-owl-imports-catalog](federation-owl-imports-catalog.md) — GitHub 연합(D1–D4):
  glob→owl:imports+catalog 로더(glob fallback 유지·shapes skip·env override로 data repo CI),
  IRI `.../id/<domain>/<slug>` 마이그(prefix 바인딩만·cross-domain은 core: prefix·union에서 병합),
  webui flat id/ 베이스 core화, Write 툴 stray `</content>` 제거 gotcha.
