# 어휘 증가 증분(원형 노드 추가)의 재검증 레시피 (inspection)

"중앙에 새 부품 N개를 추가했고 다른 하네스는 불변"이라는 증분을 독립 실측할 때. 2026-07-25
Phase 0.6(205→223, Role/Guardrail/FailurePolicy/Concept 원형 18) 라운드에서 정립.

## 1. 연합 closure 델타 = **ID/라벨 충돌 탐지기** (제일 싼 고신뢰 게이트)
8 recipe를 federate validate 하고 **개체 수 증가분이 8건 모두 정확히 +N인지** 본다.
어느 recipe가 이미 같은 slug를 쓰고 있었다면 그 하나만 `+N-k`가 되어 즉시 드러난다.
실측: 210/216/220/223/225·225·225/228 → 전부 **+18**, drift 경고 0.
```bash
cd staging/harness-recipes   # central은 작업트리 symlink
for r in $(ls recipes); do HARNESS_CATALOG=$PWD/catalog-v001.xml \
  HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/$r \
  /usr/bin/python3 central/tools/validate.py 2>&1 | grep -oP 'all \K\d+'; done
```
HEAD 대비를 재려면 scratchpad에 staging을 복사하고 `central` 심링크만 **worktree**로 바꾼다.
staging이 published와 같은지는 `git hash-object catalog-v001.xml` vs
`gh api repos/<o>/<r>/contents/catalog-v001.xml -q .sha` 로 1줄 확인.

## 2. 원형 추가의 **진짜** 위험은 exact-duplicate가 아니라 federation 근사동의어
중앙 `role-analyst`("Analyst agent")를 추가해도 recipe-local **"Analyst role"**(03-newsletter),
**"Strategist role"**(46-product-manager)와 문자열이 달라 `validate.py`는 조용하다. 연합에서
같은 클래스에 원형과 그 인스턴스가 **무연결로 공존**하는 상태 — 원형 도입의 가치는 로컬이
원형을 **specialize** 할 때 생기는데, 그 관계를 담을 **술어가 없다**:
- `ho:specializes`는 `rdfs:domain/range ho:Harness`(TBox `harness.ttl:608`) — Role엔 못 쓴다.
- `ho:derivedFrom`은 도메인 무제약이지만 의미가 *provenance*("생성/각색됨")라 시간순이 반대인
  기존 노드엔 거짓이 된다.
⇒ 원형 노드를 늘리는 라운드에서는 **"archetype→instance 엣지 GAP"을 반드시 같이 보고**하라.
프로즈("Distinguished from …")로만 존재하면 질의도 검증도 불가능하다.

## 3. `id:` 참조 텍스트 — materialize는 해소, **retrieve는 안 한다**
"emit 시 라벨로 해소되니 definition에 `id:x`를 자유롭게 써도 된다"는 **절반만 참**이다.
- `materialize.py`: 투영 그래프에서 해소 → 산출 트리 grep 결과 **0건**(B7 수정 이후).
- `retrieve.py`: 해소 코드 없음 → **팩에 `id:fp-dispatch-timeout` 그대로 실린다**.
팩의 소비자가 cold-start 에이전트이므로 dangling reference는 여기서도 결함이다.
측정 1줄: 텍스트 술어(`definition`/`promptText`/`failureCondition`/`recoveryStrategy`/
`roleMemoryPolicy`)에 `\bid:[a-z]+-[a-z0-9-]+` 정규식 → 205시점 **32참조/17노드**,
223시점 **41/24**. 증분마다 늘어나므로 **추이로** 보고한다.

## 4. host 배선 검증은 "정상 변경" 쪽도 실측한다
전량을 library carrier 하나(`h-workspace-synthesis`)에 물리는 설계는 **불변(6하네스)**만
확인하면 반쪽이다. carrier 산출물이 **정확히 기대만큼** 바뀌었는지도 세라:
CLAUDE.md `<`1줄(definition 치환) / `>`23줄, Error handling 표 **5행**(신규 FailurePolicy 수),
`.claude/agents/` **6+6=12** 파일. 수가 안 맞으면 배선 누락이거나 조건부 렌더러 미발동.

## 5. recipes CI는 중앙 push로 재실행되지 않는다
`cpark90/harness-recipes`의 `validate-recipes` 워크플로에 **`workflow_dispatch` 트리거가 없어**
`gh workflow run`이 HTTP 422로 거부된다(중앙만 바뀐 라운드에선 CI가 아예 안 돈다).
⇒ 중앙 증분의 연합 축은 **로컬 8/8 federate가 유일한 게이트**다. 트리거 추가를 권고 항목으로.

## 관련
[[materialize-regression-check]] (lock 제외 불변식), [[federation-lockstep]] (catalog 동반),
[[quality-axis-audit-recipes]] (Q1 tokenEstimate·Q2 Jaccard 한계).
