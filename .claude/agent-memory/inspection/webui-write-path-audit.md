# web UI 쓰기 경로 감사 — 손실 재현을 read-only로 하는 법

`tools/webui`는 **저장하면 지운다**. 감사할 때 절대 실제 저장(PUT/atomic_write)을 하지 말고,
아래 read-only 조합으로 같은 수치를 낸다. 스크립트는 scratchpad에만 둔다(파일 경계).

## 1. 안전한 재현 3층
1. **`ttl_writer.plan_upsert(node)`** 는 텍스트를 *계산만* 한다(`atomic_write`를 부르는 건
   `server.api_put_node`). 반환 `{"old","new"}`를 `_iter_blocks`로 잘라 블록 diff를 낸다.
   호출 후 `git status --porcelain`으로 무변화 확인을 **매번** 남길 것.
2. **집계**는 그래프에서 직접: `load_graph(reason=False)`의 개체별 술어를 `ttl_writer.ORDER`
   집합과 대조. 프런트 의미론까지 충실히 흉내내려면 `server.DATA_PREDS`(리터럴 7종) +
   TBox `owl:ObjectProperty` 전부(=`Editor.svelte`가 되돌려 보내는 범위)를 통과 조건에 넣는다.
3. **게이트 실효성**은 in-memory 그래프 복사 → 해당 개체의 손실 트리플 제거 →
   `apply_reasoning` → `pyshacl.validate(shapes=ontology/shapes/harness-shapes.ttl,
   advanced=True, inference="none")`. **개체 하나씩** 돌려야 의미가 있다(여러 개를 한꺼번에
   지우면 h-multiagent 같은 허브가 전부 orphan을 만들어 전건이 FAIL로 뭉개진다).

## 2. 실측 기준선 (2026-07-25, 205 개체)
- `ORDER` 28종 / TBox `ho:` 술어 97종(obj 57 + data 40) / `server.DATA_PREDS` 7종.
- 손실: **82/205 개체 · 375 트리플 · 56 술어**. GET 응답에조차 없는 리터럴 **135 트리플/23종**.
- 게이트 분류: **조용한 손실 27 개체/131 트리플**, **validate FAIL→restore 55 개체/244 트리플**.
  ⇒ "validate가 막아준다"는 **거짓**이고, 동시에 55개는 **편집 자체가 불가능**하다.
- 대표 `id:chan-dispatch`: 9줄→**6줄**, 소실은 `channelParticipant`(6)·`involvesUser`·
  `channelMedium` **3술어 8트리플**. ★브리프의 "9줄→2줄, definition/tagged/maturity 소실"은
  **재현 안 됨** — 그 셋은 `ORDER`에 있어 보존된다. 전달받은 수치는 항상 다시 재라.
- `INSTANCE_LINK_PREDICATES` 누락 9종·78 edge. 이 중 `hasAgent/hasChannel/hasMemory`(14)만
  `subPropertyOf hasComponent`라 추론으로 구제되고 **나머지 6종·64 edge는 추론 무관하게 소실**.
  소비자는 `instance_edges()`를 쓰는 3곳뿐: `server.py:150`(그래프뷰, asserted라 78 전부 누락)·
  `retrieve.py:160,249`·`validate.py:67`.

## 3. 레지스트리 표류(registry drift)가 이 repo의 반복 결함 패턴
`INSTANCE_CLASSES`(§B3) · `abox_files()` glob(§B8) · `ORDER`/`DATA_PREDS`(§B13) ·
`INSTANCE_LINK_PREDICATES`(§B14) — 전부 **TBox/디스크가 진실인데 파이썬 리터럴이 사본**이라
생긴 같은 결함이다. 증상은 항상 **에러 없는 조용한 축소**. 감사 처방도 하나로 통일된다:
**"사본 == 원본"을 재는 불변식 1줄**을 만들어 그것만 보면 된다
(예: `instance_nodes(reason=True) == instance_nodes(reason=False)`,
`asserted 개체→개체 술어 중 목록 밖 = 0`, `plan_upsert가 삭제하는 트리플 = 0`).
새 결함을 상신할 땐 이 계열임을 명시하고 "목록 확장"과 "TBox에서 생성"을 같은 결정으로 묶어라.

## 4. C1(INSTANCE_CLASSES) 류 수정의 파급 측정 레시피
개체 계수 경로를 바꾸는 수정은 **산출물과 연합까지** 재야 한다.
- `git worktree add <scratch>/wt-head HEAD` 로 old 도구를 얻고 7 하네스를 old/new 양쪽에
  materialize → `diff -rq`. 차이가 MANIFEST뿐인지, 그리고 **JSON leaf를 평탄화해 바뀐 키의
  마지막 세그먼트를 세면** "바뀐 건 `type` 32개뿐"을 정확히 증명할 수 있다.
- 연합: 8 recipe를 `staging/harness-recipes`에서 `HARNESS_CATALOG`/`HARNESS_ROOT_ONTOLOGY`로
  돌리되, **recipe별 전용 catalog가 있으면 그것을 쓴다**(`catalog-<recipe>.xml`, 없으면
  `catalog-v001.xml`). 개체 수를 old 클래스집합/new 클래스집합 양쪽으로 세면
  `new_reason == old_reason`(회귀 없음)과 `noreason`이 32 올라 parity를 얻은 것이 한 번에 보인다.
