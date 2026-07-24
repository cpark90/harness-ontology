# developer 역할 메모리

온톨로지 노드 저작 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/developer.md`. 노드 종류별 함정·모델링 패턴·capability 배선을 파일로 추가하고
아래에 **한 줄로** 인덱스한다(상세는 각 토픽 파일에 — 인덱스는 "언제 그 파일을 열지"만 알려준다).

- 완결 brief로 받은 배정분만 구현: 온톨로지 노드(`ontology/abox/`) 또는 배정 소스(`tools/**` 등).
  TBox·shapes·brief 밖 경로는 안 만짐. 검증(vnv)·커밋(inspection)은 안 함. 온톨로지 노드 스타일은
  `ONTOLOGYSTYLE.md` [지킴], 소스는 기존 컨벤션·언어 표준.
- 도구는 `rdflib` 등이 있는 인터프리터로(예: `/usr/bin/python3`). 셸 기본 python3엔 없을 수 있음.
- **반복 핵심**: (1) 중간노드(subject≠Harness) 도달성=hasComponent **propertyChain**(직접 sub면
  rdfs:domain Harness로 mistype); Harness→X 직결만 직접 subPropertyOf hasComponent. (2) 한 술어가
  2클래스 공용이면 rdfs:domain **생략**+definition 명시(prp-dom mistype 회피, owl:unionOf repo 0회).
  (3) ⊑HarnessComponent 개체는 SHACL ComponentConnectivityShape→반드시 harness 배선/rollup(concept
  tag만으론 부족). (4) 기존 하네스 bound 노드의 prefLabel/definition 수정=그 CLAUDE.md 변함(byte-id 깨짐);
  materialize emitter 안 읽는 술어 추가는 CLAUDE.md 불변→2run cmp로 증명(git無). (5) recipe closure는
  HARNESS_ROOT_ONTOLOGY=recipe **IRI**(디렉토리경로X)로 로드해야 recipe-local 포함.
  (6) 비-HC 신규 leaf·신규 클래스는 `lib.INSTANCE_CLASSES` 등록 필수(미등록=개체 증발).

<!-- 학습 인덱스 (한 줄씩) -->
- [tool-side-registries-and-path-globs](tool-side-registries-and-path-globs.md) — 도구쪽 화이트리스트 3종(`INSTANCE_CLASSES`·`INSTANCE_LINK_PREDICATES`·webui `ORDER`)과 경로 glob의 **조용한 실패** 감사법. 게이트=추론 유무 **개체수 파리티**(owlrl이 누락 leaf를 상위타입으로 가림), 파급은 MANIFEST `type`뿐, before/after는 monkeypatch로(git無), DA-4 이후 glob은 `**`+`recursive=True`.
- [retrieve-pack-quality-budget-lifecycle](retrieve-pack-quality-budget-lifecycle.md) — 팩 **품질** 결함 2건: `tokenEstimate` 의미 과부하→예산초과 노드가 팩을 조기절단(⇒`ho:observedTokenVolume` 분리+shape `sh:path` repoint, 불변식=초과노드 0), traverse `break`→`continue`, `ho:maturity` 미독→폐기가 후계 위(⇒`lifecycle_factor` 0.35를 seed·hop **양쪽**에, 배수는 스윕 실측으로).
- [corpus-attribute-inventory-method](corpus-attribute-inventory-method.md) — 외부 코퍼스 전수 **분석** 방법: 중간산출 json으로 컨텍스트 절약, 판정은 label 아닌 definition/promptText로, GAP 3분류(신규/altLabel흡수/도메인특수), coverage %는 우주 3개로 분리(구조중립 축은 매우 빨리 포화).
- [retrieve-projection-determinism](retrieve-projection-determinism.md) — read projection 재현성: 비결정성 발생원 지도(set 순회·owlrl insert 순서)와 총순서 키 `(-score, str(node))`, 동점이 seed 컷에 새면 membership까지 변함, 가드=`check_determinism.py`(시드를 **서로 다르게** 흔들어 md5 동일 요구).
- [execution-mode-first-class-axis](execution-mode-first-class-axis.md) — 실행 topology를 tag에서 **1급 속성**으로 승격(`ho:ExecutionMode`+`hasExecutionMode`). 확장성=값을 개체로 열거(닫힌 `sh:in` 금지), 비-HC 신규 leaf 체크리스트, 폐기는 삭제 대신 maturity+superseded, ★채널(전달매체) ≠ spawn topology(직교).
- [assembly-sections-run-behaviour-renderers](assembly-sections-run-behaviour-renderers.md) — GAP-4 run-behaviour 섹션+materialize 렌더러. ★byte-id 불변식은 **리팩터 보호용이지 이미 그래프에 있는 데이터를 드러내는 기능을 막는 근거가 아니다**(orchestrator 판정), 렌더러는 전부 조건부 early-return, 증명은 scratch overlay.
- [verification-unit-relocation](verification-unit-relocation.md) — `core/verification/` 신설=순수 relocation(라인슬라이스 byte-fidelity, 개체수 불변). federation 4점, ★dedicated `catalog-<recipe>.xml` 미갱신은 에러 없이 **부분 closure**로 FAIL.
- [revfactory-p1-lifecycle-verify-abox](revfactory-p1-lifecycle-verify-abox.md) — 메타 파트는 전용 host(`h-harness-factory`)에 배선(h-multiagent에 물리면 CLAUDE.md byte-id 깨짐). ★brief의 "land됨" 목록 불신—TBox 실물 grep 후 저작, 없으면 GAP 보고.
- [abox-da4-groupdir-reorg-recipe-sync](abox-da4-groupdir-reorg-recipe-sync.md) — REORG-2: recipe staging catalog를 그룹경로로 동기화. ★공유 catalog에 전 recipe uri가 있어야 per-recipe closure 검증 가능. stale docs 3곳(평면경로 서술).
- [abox-da4-groupdir-reorg](abox-da4-groupdir-reorg.md) — REORG-1 중앙 ABox→그룹 디렉토리 순수 이동+grab-bag split. 논리 IRI는 위치독립→catalog uri경로만 갱신, split은 byte 라인슬라이스, validate 개체수 불변.
- [da4-intermediate-superclass-taxonomy](da4-intermediate-superclass-taxonomy.md) — flat→중간계층 순수 TBox 재부모화: owlrl transitivity로 leaf 인스턴스 타입 유지→shape/count/materialize 무영향, 중간클래스는 INSTANCE_CLASSES 불요(직접 인스턴스 0). 단일상속.
- [da2-definition-disambiguation](da2-definition-disambiguation.md) — `skos:definition`만 편집=구조 무변경 zero-risk. 혼동쌍 de-conflate=자기지칭 제거+"Distinguished from ho:X" 절. ★brief가 인용한 prop이 실재하는지 grep 확인.
- [da1-observation-tripartite-split](da1-observation-tripartite-split.md) — `ObservationArea`→3클래스(ObservationSpace=CAN-observe / AreaOfInterest=intent / AreaOfObservation=realized) 원자 refactor. 도달성=3-link chain, 공용 술어는 domain 생략.
- [mas-wave3b-infospace-abox](mas-wave3b-infospace-abox.md) — 정보공간 투영사슬 ABox. orphan회피=WEAK-CONNECTIVITY(투영술어를 INSTANCE_LINK에 등록, 방향무관)→host harness 불요.
- [mas-wave3a-infospace-tbox](mas-wave3a-infospace-tbox.md) — 비-HC 클래스(EnvironmentSpace·GlobalState)+투영속성 4개는 **어느 것도 ⊑hasComponent 금지**(Harness→X여도 비-HC면 mistype).
- [mas-wave2-agent-observationarea-abox](mas-wave2-agent-observationarea-abox.md) — agent/observation ABox: 기존 capability SOFT 재사용, anti-orphan은 chain으로 해결해 harness엔 `hasAgent`만.
- [mas-wave1-agent-observationarea-tbox](mas-wave1-agent-observationarea-tbox.md) — `ho:Agent`·ObservationArea TBox. 중간노드 orphan방지=hasComponent propertyChain 추가, 크기는 tokenEstimate 재사용(→후에 observedTokenVolume으로 분리됨).
- [revfactory-wave-b1-coordination-governance](revfactory-wave-b1-coordination-governance.md) — coordination/governance 파트 대량 저작. ★Channel/Guardrail은 concept tag만으론 orphan→전용 중립 host harness에 배선 필수.
- [revfactory-tbox-wave-a](revfactory-tbox-wave-a.md) — 방법론 TBox(TestScenario/FailurePolicy⊑HC + 직접sub 2 + refinement edge 2). Harness+Instruction 공용 datatype은 domain 생략.
- [agent-memory-tier-model](agent-memory-tier-model.md) — firmware/cache/long-term 3-tier=`ho:Memory`⊑HC+`hasMemory` 직접sub, 구분은 4 discriminator(closed `sh:in`).
- [corpus-persist-local-path-canonical-source](corpus-persist-local-path-canonical-source.md) — 코퍼스 로컬경로 영속화: `artifactTemplate`=fetch용 LOCAL 절대경로 vs `dct:source`=canonical URL.
- [recipe-ml-experiment-newdomain-pilot](recipe-ml-experiment-newdomain-pilot.md) — 신규 도메인 recipe: 로컬 Concept tree는 `topConceptOf`로. ★persona `artifactTemplate` 부재=materialize HARD-FAIL(skill은 .ref stub).
- [recipe-fullstack-webapp-toolscope-variation](recipe-fullstack-webapp-toolscope-variation.md) — worker+gate 하이브리드 역할은 synthesizer 재사용 부적합→LOCAL role. RULE: 순수 gate만 synthesizer. Tool-scope 변이=역할별 roleTool slice.
- [recipe-authoring-code-reviewer-pilot](recipe-authoring-code-reviewer-pilot.md) — recipe 저작 기본형: worker persona=INLINE promptText+full body artifactTemplate, QA gate는 중앙 role 바인딩, staging catalog 상대 uri.
- [central-library-growth-host-harness](central-library-growth-host-harness.md) — 재발 중립파트 promote-once. anti-orphan을 위해 h-multiagent에 물리지 말고(byte-id) **전용 host harness** 신설, capability는 Role 경유 충족.
- [task-dag-and-coordination-topology](task-dag-and-coordination-topology.md) — `ho:Deliverable`+step DAG(도달성 3-link chain, DAG는 MANIFEST-only). topology=Pattern+Channel 쌍+중립 host.
- [assembly-order-graph-driven](assembly-order-graph-driven.md) — CLAUDE 섹션 순서를 그래프로(`ho:AssemblySection`+assemblyOrder+closed sectionKind). Harness→X 직결이라 직접 subPropertyOf.
- [systemprompt-section-decomposition](systemprompt-section-decomposition.md) — SystemPrompt→`ho:PromptSection` 분해(hasSection plain+sectionOrder, 도달성 2-link chain, section-less blob 병존).
- [workflow-step-decomposition](workflow-step-decomposition.md) — Workflow→`ho:WorkflowStep` 분해(hasStep plain+stepOrder+stepUsesTool/ByRole/GuardedBy, materialize 중첩 emit).
- [recipe-product-manager-pilot](recipe-product-manager-pilot.md) — least-privilege tool 세트(HarnessShape가 요구 안 하는 capability는 빼도 PASS). NEW 도메인+LOCAL Task.
- [recipe-newsletter-engine-content-domain](recipe-newsletter-engine-content-domain.md) — QA gate 2종(convergence=중앙 synthesizer REUSE / producing=LOCAL). **tool scope가 harness capability set을 결정**한다.
- [recipe-references-not-stored-artifacts](recipe-references-not-stored-artifacts.md) — recipe=parts+methodology+references+README, concrete build 문서 저장 금지(vendoring 안티패턴). materialize FETCH 대칭.
- [odr-contract-verify](odr-contract-verify.md) — capability에 `ho:Contract`+contractKind/Check(도달성 3-link chain), `verify_contract.py` dual.
- [materialize-atomic-emit-closed-policy](materialize-atomic-emit-closed-policy.md) — materialize 하드닝: atomic emit + closed policy set(미인식 값은 raise).
- [instruction-skill-emitter](instruction-skill-emitter.md) — Claude SKILL=`ho:Instruction`⊑HC(스키마 무수정), recipe LOCAL, emitter=`## Skills`+MANIFEST.
- [materialize-channel-emitter](materialize-channel-emitter.md) — `ho:Channel` EMIT: `channel_record()` helper + if-channels 가드, 중앙 산출 불변.
- [methodology-as-nodes](methodology-as-nodes.md) — 산문 절차→Workflow+DesignPattern+Guardrail+Concept×N(broader)로 분해, 전부 host harness에 배선.
- [glossary-term-layer](glossary-term-layer.md) — 거버넌스 원칙=독립 `skos:Concept`(`ho:Term` 발명 금지). `topConceptOf`는 연결로 안 쳐줌→top은 자식 broader로.
- [recipe-inherits-shared-parts-by-iri](recipe-inherits-shared-parts-by-iri.md) — `derivedFrom`=lineage일 뿐 컴포넌트 상속 아님→충실 반영은 명시 edge. 공유 중립파트는 로컬 저작 금지, core: IRI REUSE.
- [robust-recipe-import-closure](robust-recipe-import-closure.md) — recipe는 중앙 root 온톨로지 하나만 `owl:imports`→새 core 유닛 자동 전파. catalog=root+전 core.
- [coverage-gap-prevention](coverage-gap-prevention.md) — coverage 갭방지 가드레일+CLAUDE step7 audit gate. 어휘 없는 소스 요소=schema EXTEND 신호(silent skip 금지).
- [channel-coordination-core-unit](channel-coordination-core-unit.md) — 채널=`ho:Channel`⊑HC 개체+새 core unit(catalog+root 3점 배선).
- [role-taxonomy-new-core-unit](role-taxonomy-new-core-unit.md) — 역할=`ho:Role` 개체+새 core unit. 새 유닛은 catalog·root **둘 다** 등록해야 로더 parity.
- [role-characteristics-optional-userfacing](role-characteristics-optional-userfacing.md) — role 특성은 기존 파트 REUSE로 명시, optional bool은 present-only, roleTool의 새 tool은 harness `usesTool`에도.
- [faithful-source-reflection](faithful-source-reflection.md) — 실소스 FAITHFUL 반영: 합성 데모 제거, 후보 단일이면 implementationRef로 collapse, role은 실제 파일과 1:1.
- [odr-bind-lock-candidates](odr-bind-lock-candidates.md) — `ho:Candidate`+selectionPolicy+lock(sha256). `implementationCandidate`는 property chain rollup(직접 sub면 Tool mistype).
- [materialize-roles-impl-scaffold](materialize-roles-impl-scaffold.md) — materialize 증분2: Role emit(.claude/agents), implementationRef byte-copy(→.ref stub), scaffold mirror.
- [materialize-build-projection](materialize-build-projection.md) — `materialize.py`=retrieve의 DUAL(validate 게이트 후 build, 결정성, artifactTemplate 치환·부재시 graph fallback).
- [neutral-parts-decomposition](neutral-parts-decomposition.md) — 온톨로지=domain-INDEPENDENT PART 라이브러리: 거버넌스 문서→중립 파트로 분해하고 도메인 명사 제거.
- [model-external-harness](model-external-harness.md) — 외부 하네스 abox 모델링 대응표(role→Workflow+pattern, tool→Tool+cap, 규칙→Guardrail, requires↔provides 짝, `ho:tagged` 필수).
- [webui-svelte-frontend](webui-svelte-frontend.md) — tools/webui Svelte+Vite 구성(vite outDir=../static, 멀티스테이지 Dockerfile, /api/*).
- [split-core-per-type-units](split-core-per-type-units.md) — core seed.ttl→타입별 다중 문서로 byte-identical 이동+root union 배선(각 유닛은 schema만 import).
- [recipe-repo-composition](recipe-repo-composition.md) — recipe repo=assembly spec(core owl:imports+IRI 참조, 도메인만 LOCAL), 검증은 env override로 중앙 validate.py.
- [guardrail-item-datatype-property](guardrail-item-datatype-property.md) — 규칙 세부는 별도 노드가 아니라 datatype property 1개+ABox 다중 리터럴(`sh:closed` 없으면 shapes 무수정).
- [federation-owl-imports-catalog](federation-owl-imports-catalog.md) — GitHub 연합: glob→`owl:imports`+catalog 로더(glob fallback·env override), IRI 규약 `.../id/<domain>/<slug>`.
- [emitted-text-iri-token-projection](emitted-text-iri-token-projection.md) — definition의 `id:`/`ho:` 인용은 저자용으론 옳지만 산출 문서엔 dangling ⇒ 그래프 무변경 + **emit 진입부에서 리터럴만 해소한 그래프 복사본**을 렌더(모든 렌더러 자동 커버). artifactTemplate 본문은 의도적 미해소.
- [ontologystyle-naming-table-audit](ontologystyle-naming-table-audit.md) — §2 접두사표 실측 감사: 근거는 참조 아닌 **선언** grep(허구 행 3건 발견), 0-인스턴스 클래스는 recipe IRI 예시로 유지, 중간 superclass는 행 없음.
