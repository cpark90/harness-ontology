# 품질 축 감사 레시피 (Q1 통일성 / Q2 건전성 / Q3 세분화)

`validate.py` PASS가 **증명하지 않는** 축을 기계적으로 재는 방법. 온톨로지를 고치지 않고
판정만 낼 때 쓴다. 스크립트는 scratchpad에 쓰고 repo엔 남기지 않는다(파일 경계).

## 0. 로딩 함정 — `reason=True`를 써라
`lib.load_graph(reason=False)`로 세면 **173개**만 나오고 `validate.py`의 **205개**와 어긋난다.
차이 32개는 `lib.INSTANCE_CLASSES`에 **등록되지 않은 클래스**의 개체들이라 추론된
`ho:HarnessComponent` 타입으로만 잡히기 때문. 감사 수치는 반드시 `reason=True`로.

**부수 발견(재사용)**: `INSTANCE_CLASSES` 미등록 클래스는 OPEN-ISSUES가 적은
`TestScenario`/`FailurePolicy` 2개가 아니라 **7개 / 개체 32개**다 —
`Agent`(5)·`AreaOfInterest`(5)·`AreaOfObservation`(10)·`ObservationSpace`(5)·`Memory`(3)·
`TestScenario`(2)·`FailurePolicy`(2). 증상: `most_specific_types()`가 `HarnessComponent`만
돌려줘 MANIFEST·retrieve 팩·prefix 감사에서 구체 타입이 증발한다. 클래스별 감사를 할 땐
`INSTANCE_CLASSES` 필터를 쓰지 말고 **asserted `rdf:type` 중 `ho:` 것에서 상위클래스를 뺀
것**을 직접 계산해야 정확하다(그렇게 하면 접두사 위반 0으로 정확히 나온다).

## 1. Q1 통일성 — 재는 항목과 해석
- **`ho:tokenEstimate` 누락**: 텍스트 프레디킷(정의·promptText·roleMemoryPolicy·scenario*·
  unobserved·observedFileScope…)을 가진 노드 중 값이 없는 것. `retrieve.py:token_cost()`의
  **fallback은 15토큰**이라 누락은 곧 **예산 과소계상**(실측 98노드, `chars/4` 기준 ~5200토큰
  과소) → anti-rot 방어가 샌다. 단 ONTOLOGYSTYLE §1c의 [지킴] **명시 범위**는
  SystemPrompt/Instruction/Guardrail/Example/Tool/Workflow뿐이고 그 범위 위반은 **0**이다 —
  "규칙 위반"이 아니라 **규칙의 범위가 좁다**고 보고해야 정확하다.
- **`maturity` 누락 58**: 전부 SpecConcept 계열(Concept 35·Capability 8·Task 6·Domain 4·
  DesignPattern 4·Constraint 1). shapes가 Memory/TestScenario/FailurePolicy/Agent/
  ObservationSpace에만 `maturity minCount 1`을 걸어서 생긴 비대칭.
- **`skos:definition` 누락 56 중 34가 Guardrail** — Guardrail은 `promptText`가 정책 본문이라
  definition이 관례적으로 없다. `ho:guardrailItem`은 **존재하지 않는 프레디킷**이다(휴리스틱
  짤 때 헛다리 주의).

## 2. Q2 건전성 — 근사 중복 탐지
라벨/정의를 토큰집합 Jaccard로 같은 클래스 안에서 짝지어 본다.
- **라벨 J≥0.5는 대부분 노이즈**다 — `os-*`("X observation space"), `as-*`("Assembly: X section")
  같은 **작명 패밀리**가 대량으로 걸린다(81쌍 중 대부분). 패밀리는 drift가 아니라 통일성의 증거다.
  실제로 볼 값어치가 있는 건 J≥0.6이면서 패밀리가 아닌 쌍(예: `role-inspection` vs
  `role-inspection-worker`, `wf-harness-evolution` vs `wf-verify-harness`).
- **정의 J≥0.55**는 템플릿 저작(`oa-*-internal` 9쌍)을 잘 드러낸다 — 이건 진짜 판단거리:
  "패밀리 일관성"인지 "복붙 blob"인지.

## 3. 도구 투영에서만 드러나는 결함 (실측으로만 잡힌다)
그래프만 봐서는 안 보이고 **소비자(tool)를 돌려야** 보이는 부류. 감사 때 반드시 같이 돌린다.
- **예산 조기 절단**: `retrieve.py`의 `traverse()`는 예산 초과 노드를 만나면 `break`한다.
  `ho:tokenEstimate`가 `AreaOfObservation`에서는 "1회 추론이 관측하는 양"(최대 12000)이라는
  **다른 의미**로 쓰이므로, 그런 노드가 프론티어에 뜨면 예산이 799 남아도 팩이 3노드에서 끝난다.
  재현: `retrieve.py "what does the inspection agent observe"` → `nodes=3, 125/900`.
- **deprecated 무자각**: `retrieve.py`에 `ho:maturity`를 읽는 코드가 0줄이라 폐기 노드가
  후계보다 상위 랭크로 실린다(`pat-sub-agents` rel 8.1 > `mode-sub-agents` 6.3).
- **내부 IRI 유출**: `materialize.py`가 `skos:definition`/`promptText`를 **그대로** 렌더하므로
  disambiguation 문구의 `id:`/`ho:` 참조가 산출 CLAUDE.md에 dangling reference로 남는다
  (21노드·50회, `h-peer-mesh` 10 / `h-harness-factory` 9). scratch `--out`으로 7 하네스를
  빌드해 `grep -oP "\bid:[a-z]+-[a-z0-9-]+"` 하면 즉시 잡힌다.

## 3b. 그 3결함의 수정 검증법 (2026-07-25 land, `8aecd6f`·`f71a033`)
수정 증분을 재검증할 때 **결함별 불변식 1줄**로 재라. 브리프 수치를 그대로 믿지 말 것.
- 예산 절단: `tokenEstimate > DEFAULT_BUDGET(900)`인 노드 **0개**(수정 전 10) +
  `"what does the inspection agent observe"` **37 nodes/892**(전 3/125). 술어 이관은 개체를 늘리지
  않으므로 **205 불변**이 같이 걸리는 게이트.
- deprecated 랭킹: 후계 > 폐기 **이면서 폐기가 팩에 남아 있을 것**(숨김은 결함이지 수정이 아니다).
  json의 `maturity` 필드 존재도 같이 본다. ★json 노드 키는 `type`이 아니라 **`types`(리스트)** —
  `type`으로 읽으면 `None`이 나와 §B.3(INSTANCE_CLASSES) 결함으로 오진한다.
- IRI 유출: grep은 `CLAUDE.md`가 아니라 **산출 트리 전체**에 걸어라(MANIFEST.json에도 definition이
  복제된다). 남는 1건은 대개 `ho:artifactTemplate` **본문 파일**(설계상 미해소)이므로 old/new
  동일한지로 회귀 여부를 가른다.

## 3c. 산출물 회귀의 "성격" 판정 — line-for-line 여부
라벨 치환 같은 수정은 **줄 수가 변하면 안 된다**. `diff | grep -c '^<'` == `grep -c '^>'` 이고
`wc -l` old==new 면 순수 치환, 아니면 문장이 생기거나 사라진 것 = 조사 대상.
추가로 **변경된 old 줄이 전부 토큰을 갖고 있었는지** 역확인하면 "치환 외의 변경 0"이 증명된다.
MANIFEST의 `tokenEstimate` 합 변화(49888→2383)는 **관측량 오염 제거**이지 회귀가 아니지만,
바뀐 하네스가 관측 컴포넌트를 물고 있는 하나(`h-multiagent`)뿐인지 확인해야 그렇게 말할 수 있다.

## 3d. 파급효과는 연합까지 — 8 recipe federate + **산출물**까지 본다
중앙 tools/TBox 수정도 recipe 산출물을 바꾼다(중앙 컴포넌트 definition이 recipe 문서에 렌더되므로).
`staging/harness-recipes/central` 심링크로 8건 federate PASS를 먼저 걸고(→ `federation-lockstep`),
그 다음 recipe 하네스를 **materialize**해 old/new diff까지 본다. recipe의 하네스 slug는
`grep -rhoP "^id:\Kh-[a-z0-9-]+" recipes/<R>/*.ttl`로 뽑는다. 교차 도메인 인용
(techdoc의 `core:h-research`)이 라벨로 해소되는지가 resolver의 진짜 시험대.

## 4. 회귀 가드의 실효성 검증 (negative control)
가드 스크립트가 **정말 실패를 잡는지**는 옛 버전에 돌려봐야 안다. repo를 건드리지 않는 방법:
scratchpad에 `tools/` 트리를 만들어 `git show HEAD:tools/<tool>.py`를 넣고, 같은 디렉토리에
현재 가드와 `ontology_lib.py` **심링크**, 상위에 `ontology`·`catalog-v001.xml` 심링크를 건다
(가드가 `Path(__file__).parent`로 대상을 찾고 `cwd=TOOLS.parent`로 실행하기 때문).
`ontology_lib.py` 심링크를 빼먹으면 `ModuleNotFoundError`로 FAIL이 나서 **가짜 negative
control**이 된다 — 실패 사유가 결함이 맞는지 출력을 반드시 읽을 것.
