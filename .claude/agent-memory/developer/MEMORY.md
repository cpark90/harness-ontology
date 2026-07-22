# developer 역할 메모리

온톨로지 노드 저작 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/developer.md`. 노드 종류별 함정·모델링 패턴·capability 배선을 파일로 추가하고
아래에 한 줄로 인덱스한다.

- 완결 brief로 받은 배정분만 구현: 온톨로지 노드(`ontology/abox/`) 또는 배정 소스(`tools/**` 등).
  TBox·shapes·brief 밖 경로는 안 만짐. 검증(vnv)·커밋(inspection)은 안 함. 온톨로지 노드 스타일은
  `ONTOLOGYSTYLE.md` [지킴], 소스는 기존 컨벤션·언어 표준.
- 도구는 `rdflib` 등이 있는 인터프리터로(예: `/usr/bin/python3`). 셸 기본 python3엔 없을 수 있음.

<!-- 학습 인덱스 (한 줄씩) -->
- [odr-contract-verify](odr-contract-verify.md) — ODR VERIFY축(성숙도 3–4): capability에
  검증가능 `ho:Contract`(⊑HarnessComponent)+`ho:capabilityContract`+`ho:contractKind`
  (executable|structural)+`ho:contractCheck`. 도달성=**3-link chain** `hasComponent o
  providesCapability o capabilityContract ⊑ hasComponent`(2-link면 provider가 Harness 오타입,
  candidate trap 판박이; hasComponent에 propertyChainAxiom 2개 공존 OK). `tools/verify_contract.py`
  =VERIFY dual(harness+--tree→contract 판정, executable=subprocess exit0, structural grammar
  file-exists/file-contains/section[hash-strip], IRI-sort 결정성, fail→exit1). L3=faithful
  lpranging에 **contract만 추가**(합성candidate 금지, parse-check가 안전한 executable). L4=INV-4=
  별도 `recipes/contract-demo` 2-candidate swap(출력동일·소스상이→verify 동일 PASS). 중앙 96불변·neutral.
- [materialize-atomic-emit-closed-policy](materialize-atomic-emit-closed-policy.md) — materialize
  하드닝(vnv N1/N2, 순수 tooling·validate 96 불변). N1 atomic emit: `--lock` 해시체크가 mid-emit라
  직접 write는 실패 시 half-written→**sibling temp staging(mkdtemp in out's PARENT, 같은 fs여야
  os.replace가 atomic rename)**에 통째로 빌드 후 성공 시에만 `_place_atomically`(out 없으면 단일
  replace, 있으면 bak-<pid>로 aside 후 swap·실패시 복원=clean replace). body는 `_emit_tree`로
  추출(무수정), staging 경로는 산출파일에 안 들어감=byte-identical 유지. N2 closed set: select_candidate
  꼬리 `return ordered[-1]`가 모든 policy 삼킴→`if policy not in ("latest-stable","conservative"):
  raise`(tool+bad value+accepted set, pinned 빈매치 에러와 parity), resolve_selections서 write 전 raise.
  증명: 변조 lock(마지막 tool contentHash 0, 벤더 lock 아님)로 OLD partial(driver)↔NEW absent/untouched
  대조; N2는 direct-ref뿐이라 scratch recipe copy+**같은 dir scratch catalog**(상대 ./central 유지)로.
- [instruction-skill-emitter](instruction-skill-emitter.md) — Claude-Code SKILL(`.claude/skills/`)을
  `ho:Instruction`(⊑HarnessComponent)+`ho:hasInstruction`(⊑hasComponent)로 반영. 핵심: 둘 다
  **이미 TBox·INSTANCE_CLASSES에 존재**(0 instance였을 뿐)→스키마 무수정, 중앙 96 불변. 감사부터
  grep 확인(발명 금지). prefix `ins-`. 도메인특정→recipe LOCAL: prefLabel+`skos:notation`(trigger명)
  +definition+`ho:artifactTemplate`(vendored 경로)+tokenEstimate. 본문 substantial→byte-identical
  vendor(`skills/<name>/SKILL.md`, cp -p+cmp). emitter(materialize 7b, roles쌍둥이): copyfile
  byte-identical(render 아님), `## Skills`섹션 if-가드, MANIFEST `skills`배열, `_iter_components`가
  이미 hasInstruction 포함=카운트 자동. 게이트=recipe compose 113→116, 2런 IDENTICAL, 회귀=skill-less
  h-multiagent 여전히 materialize+섹션생략. 소스 레이아웃 dir-per-skill 미러.
- [materialize-channel-emitter](materialize-channel-emitter.md) — ho:Channel의 EMIT counterpart:
  roles 쌍둥이 패턴으로 `channel_record()` helper(CLAUDE.md 섹션+MANIFEST `channels` 배열 공유),
  `## Coordination channels` 섹션(if channels 가드, 없으면 생략), involvesUser는 `.toPython()`후 bool,
  IRI-sort 결정성. 순수 EMIT(TBox/shapes/ABox 무수정, 중앙96불변). 회귀=채널없는 중앙harness(h-coding),
  h-techdoc은 recipe라 중앙에 없음. lpranging=staging central 심링크+env override.
- [methodology-as-nodes](methodology-as-nodes.md) — 산문 절차(예: CLAUDE 워크플로)를 노드로:
  한 methodology=Workflow(step들 definition)+DesignPattern(접근)+Guardrail(규율)+Concept term ×N
  (broader c-agent-methodology), 전부 h-multiagent에 배선. Harness는 hasWorkflow/appliesPattern
  ≥2 가능(콤마 append). Workflow와 Concept가 prefLabel 겹쳐도 (class,label) dup이라 OK. 91→96(+5).
  ODR 연계: composition=SPEC 저작, ODR EMIT=render, materialize=step7 뒤 진입점. docs/composition-methodology.md.
- [glossary-term-layer](glossary-term-layer.md) — 거버넌스 원칙을 독립 term으로: `skos:Concept`=
  term(prefLabel+definition), `ho:Term` 발명 금지(drift). 검증기 사실: reachability/SHACL 모두
  **topConceptOf는 연결 안 침**(ConceptScheme는 non-instance)→top concept는 자식 skos:broader
  (inverse)로 삼. dup검사는 (class,label) 단위 advisory라 Guardrail/Concept 라벨 겹쳐도 OK.
  패턴=원칙term 1:1 guardrail 재tag(promptText tail 앵커, tokenEstimate 겹침 주의), cross-cutting은
  새 top c-agent-methodology 밑·도메인특정은 기존 top 밑. 77→91, gate 그린.
- [recipe-inherits-shared-parts-by-iri](recipe-inherits-shared-parts-by-iri.md) — `ho:derivedFrom`은
  lineage(provenance)일 뿐 컴포넌트 상속이 아님: 템플릿(core:h-multiagent)이 가진 hasChannel/hasRole
  등을 recipe harness가 자동으로 갖지 않음→충실 반영하려면 recipe ttl의 harness에 명시 edge 추가.
  공유 중립 파트(channels)는 **로컬 개체 저작 금지**, `core:` IRI로 REUSE(root import로 union에
  이미 존재). 술어순=h-multiagent 관례(hasRole→hasChannel→appliesPattern). materialize엔 channel
  emitter 없음=MANIFEST 컴포넌트 목록엔 뜨되(hasChannel⊑hasComponent) 전용 파일 미생성=정상.
  게이트=중앙77불변+심링크 compose PASS 94불변(edge만 추가, 새 개체 0)+2런 diff 결정성.
- [robust-recipe-import-closure](robust-recipe-import-closure.md) — recipe가 중앙 core를 개별
  유닛 열거로 import하면 새 core 유닛(roles/channels)이 bare IRI로 union에 들어와 SHACL prefLabel
  FAIL(P0 회귀). robust fix=recipe ttl이 개별 나열 대신 **중앙 root 온톨로지
  `<https://harness-ontology.dev/ontology>`** 하나만 owl:imports→전체 스토어 transitive 자동전파,
  recipe catalog에 root+schema+전 core(roles/channels)+authored 매핑(중앙 root catalog와 동일 목록,
  없는 파일은 loader가 graceful skip). 게이트는 repo-root cwd(HARNESS_CATALOG 상대경로 함정),
  central 심링크 fixture 후 rm, staging/는 git-ignored라 central-untouched 자동충족.
- [coverage-gap-prevention](coverage-gap-prevention.md) — 반영 coverage 갭(channel/skills 누락)
  recurrence-prevention을 두 축에 동시 반영: 중립 guardrail `gr-structural-coverage`(reviewed·
  tagged c-traceability·h-multiagent hasGuardrail 배선, gr-traceability/gr-no-arbitrary-decision과
  "반영 완전성" 축으로 구분) + CLAUDE.md 워크플로 step7 coverage-audit gate(vnv, validate≠done) +
  docs/lessons/. root cause=assembly-driven라 source-driven 완전열거 부재→어휘 없는 요소 불가시.
  원칙: 어휘 없는 소스 요소=schema EXTEND 신호, silent skip 아님. TBox 무수정, 76→77.
- [channel-coordination-core-unit](channel-coordination-core-unit.md) — 멀티에이전트 소통/조정
  채널을 `ho:Channel`(⊑HarnessComponent) 개체로 반영. roles.ttl과 쌍둥이 패턴: 새 core unit
  channels.ttl(catalog+root 3점 배선→두 로더 parity) + `ho:hasChannel`⊑hasComponent(domain 생략
  =Harness 상속, 새 shape 불요)·`ho:channelParticipant`(→Role)·`ho:involvesUser`(bool)·
  `ho:channelMedium`(string). tokenEstimate는 promptText 없어 Role 선례대로 생략. 3채널=agent-user
  (involvesUser true·승인게이트)/orchestrator-inspection(status markers·verify+inquiry lane)/dispatch
  (subagent spawn). h-multiagent에 hasChannel 배선. detail-check: 반영 전무였음(단어만 gr promptText).
- [role-taxonomy-new-core-unit](role-taxonomy-new-core-unit.md) — 멀티에이전트 역할 분류를
  `ho:Role` 개체로 반영 + 진짜 신규 core unit 추가: `ho:userFacing`(DatatypeProperty domain Role
  range boolean, 기존 datatype 스타일 모방·boolean은 따옴표 없는 `true`/`false`), 새
  `ontology/abox/core/roles.ttl`(자기 owl:Ontology 헤더·schema만 import)을 **catalog(repo root)
  + root owl:imports 둘 다** 배선해야 imports경로 resolve(glob은 자동)→두 로더 parity 검증
  (HARNESS_CATALOG=/nonexistent로 glob 강제 vs 기본, individual set·len(g) 동일). Role은 lean
  분류만(persona/tool-scope optional·YAGNI), hasRole⊑hasComponent로 h-multiagent 배선→non-orphan.
  user-facing(orchestrator/inspection) vs worker(false); inspection≠inspection-worker 별개 role.
- [faithful-source-reflection](faithful-source-reflection.md) — 실 소스 하네스를 recipe로
  FAITHFUL 반영: 합성 데모 제거(provenance `find`/`cmp`), BIND 후보→소스 단일 impl일 때 직접
  `implementationRef`로 collapse(union 83→81), `{{prefLabel}}` 스캐폴드 stub→실 표준문서 byte-identical
  vendor(render_from_template은 `{{}}`3토큰+trailing`\n`1개만 건드림→동일), tool이 reference/에
  있을 수도(cmp는 실경로), role=실 `.claude/agents/*` 1:1, 후보 없으면 vendored lock 제거(ODR§4-③,
  결정성은 2런 diff), 게이트=중앙64불변+core grep0+심링크 compose후 rm.
- [odr-bind-lock-candidates](odr-bind-lock-candidates.md) — ODR BIND축+Lock: `ho:Candidate`
  (⊑HarnessComponent) 구현후보·`ho:selectionPolicy`·`ho:candidateVersion/Tag`. **핵심 함정**:
  implementationCandidate를 hasComponent 서브프로퍼티로 하면 Tool subject가 prp-dom로 Harness
  오타입→HarnessShape trip(rolePersona 역방향). 해결=property chain `hasComponent o
  implementationCandidate ⊑ hasComponent`(후보가 harness로 roll-up, tool 무오염, 새 shape 불요).
  implementationRef/selectionPolicy는 domain 제거(Tool·Candidate/Harness 양쪽). materialize:
  결정적 policy(pinned:<tag>/latest-stable/conservative, ver key split·tie IRI), harness.lock.json
  (spec identity+sha256 content hash, 무타임스탬프), --lock strict 재현(mismatch=hard FAIL),
  policyApplied는 lock서 원본유지(A==B byte-identical), 후보-backed tool은 안정 파일명(tool stem+ext).
  _bound_impl_tools는 RDF.type Tool로 제한(후보가 hasComponent-reachable+implementationRef라 오검출).
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
  sort_keys+무타임스탬프→byte-identical), `most_specific_types` OWL RL 반사 subClassOf 버그는
  **중앙 수정됨**(self-edge 가드 `if sup != t`, 소비자 로컬 strip 제거)→Tool/Role 자동 concrete·
  byte-identical. **노출→해결된 latent gap**: `HO.Channel`이 `INSTANCE_CLASSES`에 없어 채널이
  HarnessComponent였음(등록 안 된 subtype 공통)→`HO.Channel` 한 줄 추가(orchestrator 승인)로
  concrete `['Channel']`. materialize `components[].type` 3줄만 HarnessComponent→Channel
  =의도된 교정(byte-identical은 "그 3줄 제외" 재해석, 검증=ORIG diff 정확히 3줄·2런 결정성).
  reachability 96 불변(채널은 HC 멤버십으로 이미 카운트). 감사법=ho: owl:Class 열거해
  subClassOf-HC∧instances>0∧not-in-set 탐지. P2 `ho:artifactTemplate`(datatype prop,
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
