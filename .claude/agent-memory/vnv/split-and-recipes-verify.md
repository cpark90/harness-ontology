# central per-type split + recipe-repo 검증 재현 절차 + 함정

seed.ttl → `ontology/abox/core/*.ttl` 타입별 분할, 그리고 `staging/harness-recipes/`
recipe-repo(중립 core를 owl:imports해 도메인 Harness 조립) 판정 시 표준 절차. 전부 `/usr/bin/python3`.

## Phase 1 (split) 재현
- **triple-equivalence proof**: pre = `git show HEAD:ontology/abox/seed.ttl`(working tree에서
  삭제됐어도 HEAD엔 있음), post = `core/*.ttl` union. `owl:Ontology` 헤더 subject(=`rdf:type
  owl:Ontology`인 subject)의 triple을 **제외**하고 양방향 diff. instance-triple symdiff 0,
  individual 64==64여야. 헤더 triple만 차이(pre 1 unit×2 vs post 11 unit×2 = 366 vs 386,
  instance는 둘 다 364). "무손실"의 유일한 증명.
- **로더 등가성**: `HARNESS_CATALOG=/nonexistent`로 glob fallback 강제 + `ontology_lib` reload
  → catalog+imports와 raw triple/individual symdiff 0 (여기선 1429 triples/64). (federation-verify.md와 동일 기법.)
- 11개 unit 각각 `owl:imports schema` **단일** import인지, root가 11 core+schema+authored 전부
  import하는지, catalog가 11 `.../data/core/<type>` 매핑하는지 확인.

## Phase 2 (recipe) 재현
- recipe-repo는 `./central` 심링크(또는 clone)로 central을 참조. **임시 심링크 만들고 검증 후 반드시 rm**
  (`ln -s $(pwd) staging/harness-recipes/central`). staging at-rest 심링크=0 확인이 hygiene 항목.
- compose validate: `cd staging/harness-recipes && HARNESS_CATALOG=catalog-v001.xml
  HARNESS_ROOT_ONTOLOGY=<recipe IRI> /usr/bin/python3 central/tools/validate.py` → union 75
  (64 central + 11 local), PASS. import closure가 정확히 central+recipe인지 개체수로 확인.
- **redefinition 0**: recipe 파일 단독 parse → `core:` IRI가 subject로 등장=0. grep이 다중행
  object-list 연속행(직전행 콤마)을 subject로 오탐하니 rdflib subject 집합으로 확증.
- requires→provides는 harness에 실제 바인딩된 컴포넌트 providesCapability로만 매칭. 도메인 cap은
  로컬 tool이, 재사용 core cap은 core 컴포넌트가 제공.
- 발견성: composed union retrieve는 도메인 harness #1, central-only retrieve는 중립only(도메인
  노드 0). central grep 시 쿼리-에코 헤더행(`# Context pack for`, `_matched terms`) 제외해야 오탐 없음.

## 판정 함정
- **"recipe가 core 11 전부 import"는 결함 아님**: `derivedFrom core:h-multiagent`가 단일문서
  `core/harnesses`(모든 seed harness 보유)를 끌어오고, 그 seed들이 나머지 모든 unit을 참조하므로
  union 닫힘(EdgeTypingShape) 위해 전부 import 필수. "바인딩한 것만"은 계보 유지+harnesses 단일
  문서 구조상 불가능. anti-rot은 union 크기가 아니라 retrieve projection(budget-cap) 계층이라
  런타임 비용 0. union 최소화가 목표면 central harnesses 입도 재분할 = central-side 변경 →
  inspection/orchestrator 라우팅. pass-with-notes로.
- maturity "reviewed" vs CLAUDE.md "draft-first" 산문: [지킴] 강제 아닌 curation 속성 → note only.

판정 리포트: `docs/verify/split-and-recipes.md` (pass-with-notes: 6항목 전부 통과;
notes=all-11 import 판정(acceptable) + maturity reviewed + authored.ttl 의도적 부재).

## techdoc 데모 (2번째 recipe) 추가 함정
- **base-candidate를 markdown grep으로 확인하지 말 것**: harness prefLabel이 slug와 다르면
  (예: `h-techdoc` → "Technical documentation agent", literal "techdoc" 없음) markdown 후보줄이
  grep에 안 걸려 "후보 누락"으로 **오판**한다. `retrieve.py --format json`의 `candidates[]`로
  #1 확인이 정답 (techdoc: rel 8.1로 central siblings 3.691 위 #1).
- **composed-union retrieve의 gap 리스트는 target harness만의 gap이 아님**: in-scope로 끌려온
  sibling harness들의 requiresCapability도 합산된다(예 techdoc pack gap=[Code execution,
  Multi-agent orchestration]은 coding/multiagent 것; techdoc 4개 cap은 전부 met). target의
  gap 여부는 그래프에서 harness의 requires→(bound component의)provides로 직접 확인.
- HarnessShape+requires→provides 그래프 직접읽기: `ontology_lib.load_graph()` 후 harness의
  hasSystemPrompt/hasWorkflow/usesTool/hasGuardrail/usesModel objects + requiresCapability를
  bound component들의 providesCapability로 매칭. techdoc: cap-citation은 tool 아닌 **guardrail
  gr-cite**가 provide(HarnessComponent provider면 됨).
- 판정: `docs/verify/techdoc-assembly.md` pass-with-notes. note=task-techdoc가 general한
  cited-authoring+accuracy-review라 core 승격 여지(borderline, 로컬도 defensible) + all-unit
  import(N2, acceptable) + gap-list 오독 주의(N3). sp/dom/c는 도메인특화 = 로컬 적정.
