# ONTOLOGYSTYLE.md
이 온톨로지 스타일은 노드 저작(authoring)·composition 시, 매 세션 시작 시 읽는다.
코드 스타일 문서 `CODESTYLE.md`(구현 repo)의 온톨로지판이다 — 그쪽이 소스 코드의
단일 진실 공급원이라면, 이 문서는 `ontology/` TTL 저작의 단일 진실 공급원이다.

## 1. 공통 철학 (표현 형식 무관)

목표는 코드 스타일과 같다: **일관성과 가독성**. 다른 사람(그리고 다음 세션의 agent)이
그래프를 보고 빠르게 이해하고, 무엇을 재사용해야 할지 알 수 있어야 한다.

- **[지킴]** 일관성이 최우선. 한 파일·한 abox 안에서 스타일을 섞지 않는다. 기존
  `ontology/abox/*.ttl`의 지역 컨벤션이 있으면 그것을 따른다.
- **[지킴]** 노드는 자기설명적으로. 좋은 `skos:prefLabel`과 `skos:definition`이 주석보다
  낫다. definition은 "무엇을 하는 노드인가"가 아니라 **"왜 존재하고 언제 고르는가"**를 적는다.
- **[지킴]** 노드는 작고 **단일 책임**. 한 `SystemPrompt` = 한 페르소나, 한 `Guardrail`
  = 한 정책, 한 `Tool` = 한 capability. 여러 정책·페르소나를 한 노드에 섞으면 재사용·검색·
  예산 계산이 모두 나빠진다 (구현판의 "함수는 작고 한 가지에 집중"과 같은 규칙).
- **[지킴]** 중복 대신 재사용. 새 노드를 만들기 전에 `python3 tools/retrieve.py "<개념>"`으로
  같은 것이 이미 있는지 찾는다. 같은 뜻의 노드를 둘 만드는 것이 이 repo가 막으려는 drift다.
- **[권장]** 영리하거나 특이한 모델링을 경계한다. "TBox가 금지하지 않았다"가 "써도 된다"는
  아니다. 등록된 관용 패턴(seed abox)을 먼저 따른다.
- **[지킴]** 매직 IRI·매직 문자열 금지. `ho:maturity` 값은 `draft | reviewed | stable |
  deprecated` 넷만. 태그·capability·domain은 등록된 individual만 가리킨다.
- **[지킴]** 들여쓰기는 **스페이스만**, 4칸. 탭을 쓰지 않는다.
- **[지킴]** `skos:prefLabel`은 한 줄. 프레디킷이 여럿이면 `;`로 끊어 줄바꿈한다(§4).

---

## 1a. 강인성 — 연결성 (anti-orphan)

`ontology/`에서 **고립 노드(orphan)는 예외가 아니라 build failure**다. `validate.py`의
SHACL 연결성 shape + 전역 reachability BFS가 이를 강제한다. (설계 원칙은
`docs/DESIGN.md` "Orphaned nodes → structural validation" 참조.)

- **[지킴]** 새 노드는 **같은 커밋 안에서** 그래프에 연결한다. 나중에 잇겠다며 뜬 노드를
  남기지 않는다 — reachability BFS가 island로 잡는다.
- **[지킴]** 모든 `HarnessComponent`는 ≥1개 `Harness`에서 `hasComponent`(또는 하위
  프로퍼티: `hasSystemPrompt`/`usesTool`/…)로 참조돼야 한다.
- **[지킴]** 모든 `Task`는 `addressedBy`(또는 `addressesTask`) 되거나 task taxonomy 안에
  있어야 한다. 모든 `Capability`는 `required` 또는 `provided` 돼야 한다. 모든 `Concept`는
  무언가를 `tagged` 하거나 SKOS 계층(`skos:broader`/`topConceptOf`)에 걸려 있어야 한다.
- **[지킴]** **capability 짝 맞춤**: harness가 `requiresCapability` 하는 것은 반드시 그
  harness의 컴포넌트 하나가 `providesCapability` 해야 한다. "연결됐지만 build 불가"한 harness를
  만들지 않는다 (구현판의 "I/O 반환값 무시 금지"에 대응 — 미충족을 무음으로 넘기지 않는다).
- **[권장]** 새 harness는 `ho:derivedFrom`으로 출처(템플릿)를 남긴다 — provenance는
  손실 내성의 온톨로지판(어디서 왔는지 복원 가능).

---

## 1b. 강인성 — 어휘 통제 (anti-drift)

의미가 조용히 갈라지는 것(drift)을 손실만큼 정상 위험으로 다룬다. TBox와 SKOS 통제
어휘가 방어선이다. (원칙: `docs/DESIGN.md` "Context drift → controlled vocabulary".)

- **[지킴]** **TBox가 유일한 어휘**다. 새 `ho:` 클래스·프로퍼티를 발명하지 않는다. 기존
  클래스/프로퍼티/`ho:Concept`를 재사용한다. 근사 동의어 클래스나 untyped edge를 만드는
  것이 바로 이 repo가 막는 drift다 (구현판의 terminology 규칙과 동일한 취지).
- **[지킴]** `skos:prefLabel`은 **필수이고 클래스 안에서 유일**하다(`validate.py` 중복 검사).
  동의어는 새 노드가 아니라 `skos:altLabel`로 붙인다 — "RAG"와 "Document retrieval"은 한
  노드의 pref/alt이지 두 노드가 아니다.
- **[지킴]** edge는 **typed** 하게. SHACL `sh:class`가 range를 강제하므로 엉뚱한 타입을
  가리키는 edge를 만들지 않는다. 임의 `rdf:Property`로 관계를 급조하지 않는다.
- **[지킴]** 새 `ho:Concept`가 정말 필요하면 **같은 커밋에서** `skos:broader` 부모에 걸거나
  최소 하나를 `tagged` 하게 한다 — 안 그러면 orphan으로 잡힌다.
- **[권장]** label·definition의 언어는 **영어 용어 기반**. 프로젝트 도메인 용어를 자체
  생성하기 전에 업계 표준 용어(ReAct, plan-execute, RAG 등)를 먼저 쓴다.

---

## 1c. 강인성 — 예산 (anti-rot)

그래프는 커져도 agent가 읽는 context는 유계여야 한다. `retrieve.py`의 예산 상한이 방어선
이므로, 노드는 **예산 계산이 정확하도록** 저작한다. (원칙: `docs/DESIGN.md` "Context rot".)

- **[지킴]** **텍스트를 지닌 노드에는 `ho:tokenEstimate`를 반드시 붙인다**
  (`promptText`가 있는 SystemPrompt/Instruction/Guardrail/Example, 그리고 Tool/Workflow).
  빠지면 projection 예산이 부정확해져 context rot 방어가 샌다.
- **[지킴]** **온톨로지 전체를 context에 로드하지 않는다.** 요청 처리·composition은 항상
  `python3 tools/retrieve.py "<request>"`가 준 pack에서 시작한다 (CLAUDE.md 골든룰 1).
- **[권장]** `promptText`는 최소·자기완결로. 긴 프롬프트를 한 노드에 몰지 말고 재사용
  가능한 `Instruction`으로 쪼갠다 — 예산 admission이 노드 단위로 걸리기 때문.
- **[권장]** `ho:salience`(0..1)로 중요도 prior를 준다 — 자주 template이 되는 base harness는
  높게, 특수 변형은 낮게. 소비자(retrieval 랭킹) 없는 값을 과하게 붙이지 않는다(YAGNI).

---

## 1d. 주석·definition 표준

- **[지킴]** `skos:definition`/`rdfs:comment`는 **그래프가 스스로 못 보여주는 것만** 적는다:
  선택의 이유(언제 이 노드를 고르나·기각한 대안), 제약(latency/cost/privacy), 불변식.
- **[지킴]** 다음은 쓰지 않는다: label 재진술("Coding harness는 coding harness다"), 수정
  이력·리뷰 대화성 코멘트, 주석 처리된 죽은 트리플. (발견 시 삭제 대상.)
- **[지킴]** TTL 파일 상단 배너는 그 abox의 역할 요약 1–3줄 + 공개 계약(어떤 harness군을
  담는지)만. seed.ttl의 배너 스타일(`####`, `#====`)을 따른다.
- **[지킴]** 언어는 **한글 설명 + 용어는 영어**(CLAUDE 계열 언어 규칙). 단 `skos:prefLabel`·
  `definition` 같은 그래프 데이터 값은 **영어**로 쓴다(seed abox와 일관 — 검색 대상 텍스트).

---

## 2. 개체(individual) 네이밍

seed abox의 접두사 규약을 그대로 따른다. IRI는 `id:` 네임스페이스, 소문자 kebab-case,
`<kind>-<slug>` 꼴.

| 종류 | 접두사 | 예 |
|---|---|---|
| Domain | `dom-` | `id:dom-coding` |
| Task | `task-` | `id:task-bugfix` |
| Capability | `cap-` | `id:cap-codeexec` |
| Concept | `c-` | `id:c-softeng` |
| DesignPattern | `pat-` | `id:pat-react` |
| Constraint | `con-` | `id:con-lowlatency` |
| ModelConfig | `mc-` | `id:mc-opus` |
| Tool | `tool-` | `id:tool-shell` |
| Workflow | `wf-` | `id:wf-react` |
| Guardrail | `gr-` | `id:gr-cite` |
| SystemPrompt | `sp-` | `id:sp-coding` |
| Instruction | `ins-` | `id:ins-verify-then-proceed` |
| Example | `ex-` | `id:ex-…` |
| Harness | `h-` | `id:h-coding` |

- **[지킴]** slug은 **의미가 드러나는 full word**. 자체 약어를 만들지 않는다(코드 식별자
  규칙과 동일). 관용 축약(`mc`=model config 등 접두사)만 표에 등록된 대로 쓴다.
- **[지킴]** ID는 재사용하지 않는다. 폐기 노드는 삭제 대신 `ho:maturity "deprecated"`.

---

## 3. 프레디킷 순서 (한 노드 블록)

가독성을 위해 프레디킷을 **일정한 순서**로 나열한다(seed abox 관례):

1. `a`(rdf:type)
2. `skos:prefLabel` → `skos:altLabel`
3. `skos:definition`
4. 타게팅·조립: `ho:targetsDomain` → `ho:addressesTask` → `ho:hasSystemPrompt` →
   `ho:usesTool` → `ho:hasWorkflow` → `ho:hasGuardrail` → `ho:usesModel` →
   `ho:hasInstruction` → `ho:hasExample`
5. `ho:appliesPattern` → `ho:requiresCapability` / `ho:providesCapability` →
   `ho:constrainedBy` → `ho:dependsOn` → `ho:specializes` / `ho:derivedFrom`
6. `ho:tagged`
7. 데이터: `ho:promptText` → `ho:tokenEstimate` → `ho:salience` → `ho:maturity`

- **[권장]** 같은 프레디킷의 여러 값은 콤마로 한 줄에(`ho:usesTool id:a, id:b`), 길면
  콤마 뒤 줄바꿈해 정렬.

---

## 4. Turtle 포맷

- **[지킴]** prefix 블록은 파일 상단에, seed 순서(`ho`, `id`, `owl`, `rdf`, `rdfs`, `xsd`,
  `skos`, `dct`)를 따른다. `id:`는 abox에만.
- **[지킴]** 스키마(클래스·프로퍼티)는 `tbox/`, 개체는 `abox/`. abox에서 새 클래스·프로퍼티를
  선언하지 않는다.
- **[권장]** 짧은 노드(레이블만)는 **한 줄**로:
  `id:dom-coding a ho:Domain ; skos:prefLabel "Software coding" ; ho:salience 0.9 .`
- **[권장]** 텍스트·프레디킷이 여럿인 노드는 **여러 줄**, 프레디킷마다 4칸 들여쓰기:
  ```turtle
  id:sp-coding a ho:SystemPrompt ;
      skos:prefLabel "Coding agent persona" ;
      ho:promptText "You are a meticulous software engineer. ..." ;
      ho:tokenEstimate 90 ; ho:maturity "stable" .
  ```
- **[지킴]** 마지막 트리플은 `.`로 닫는다. 섹션은 seed의 `#===== ... =====` 배너로 구분한다.
- **[권장]** 한 줄이 과도하게 길면(대략 100자↑) 끊는다. `promptText`처럼 본질적으로 긴
  리터럴은 예외 — 한 리터럴을 인위로 쪼개지 않는다.

---

## 셀프체크

작업 완료 전 반드시 실행한다. `validate.py`는 이 스타일의 강제 항목(1a·1b·1c)을 기계적으로
검사하는 게이트다 — 통과가 곧 "연결됨·타입 정합·drift 없음"의 증거다.

```bash
python3 tools/validate.py          # 반드시 PASS. FAIL이면 shape가 아니라 온톨로지를 고친다.
python3 tools/retrieve.py "<새 노드가 답할 request>"   # 새 노드가 실제로 검색되는지 확인
```

> 환경 주의: 이 저장소의 도구는 `rdflib`/`pyshacl`/`owlrl`가 있는 인터프리터로 실행해야
> 한다. 셸 기본 `python3`에 없으면 그 셋이 설치된 인터프리터로 실행한다(예: `/usr/bin/python3`).

규칙을 어길 땐 **[지킴]/[권장]** 항목에 한해 그 노드의 `rdfs:comment`나 커밋 메시지에 사유를
한 문장 남긴다 — 말없이 머지하지 않는다.
