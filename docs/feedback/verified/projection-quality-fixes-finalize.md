---
source: [docs/feedback/retrieve-pack-quality-defects.md, docs/feedback/emitted-harness-iri-leak.md]
verdict: apply
status: reported
targets: [tools/retrieve.py, tools/materialize.py, ho:tokenEstimate, ho:observedTokenVolume, core:oa-*, core:pat-sub-agents]
source_brief: (orchestrator dispatch, E-1)
---
# 검증 보고 — 투영(projection) 품질 결함 2건 수정 land

inspection이 상신한 두 결함(`retrieve-pack-quality-defects.md` 결함 A·B,
`emitted-harness-iri-leak.md`)의 수정 증분을 **브리프를 믿지 않고 전 항목 독립 재실측**한 뒤
land했다. 두 증분은 서로 다른 소비자(read projection / build projection)를 고치므로 커밋을
분리했다.

## 파급효과 (impact)

### 증분 A — `ho:observedTokenVolume` 신설 + `retrieve.py` 예산·lifecycle
- **그래프**: TBox에 datatype property 1개 추가(`ho:observedTokenVolume`, domain
  `ho:AreaOfObservation`), `ho:tokenEstimate`·`ho:cognitiveCapacity`·`AreaOf{Interest,Observation}`
  definition 문구 갱신, `AreaOfObservationShape`의 `sh:path` repoint, abox AoO **10개체**의 값 이관
  + 텍스트 비용 재산정. **개체 수 불변(205)** — 술어 이관이지 노드 추가가 아니다(실측 확인).
- **소비자 파급**: `observedTokenVolume` 10노드 합 **48000**, `tokenEstimate` 최대 **205**,
  **예산(900) 초과 노드 10 → 0**. `materialize` MANIFEST의 컴포넌트 비용 합에서 관측량 48000이
  빠져 `h-multiagent` **49888 → 2383**(오염 제거이지 회귀 아님 — 다른 6하네스 MANIFEST의
  tokenEstimate는 불변).
- **랭킹 파급**: `lifecycle_factor()`가 seed·hop 양쪽에 곱해지므로 `deprecated` 3노드
  (`pat-sub-agents`·`pat-agent-teams`·`pat-hybrid`)만 강등된다. maturity 미선언 노드는 1.0이라
  나머지 그래프의 랭킹은 불변.

### 증분 B — `materialize.py` 투영 그래프
- **그래프 무변경**(디스크·메모리 저장본 모두). 렌더 직전 **문자열 리터럴만 해소한 복사본**을
  만드는 한 지점 수정이라, 현재 렌더러 전부(CLAUDE.md 섹션·role 파일·channel 기록·skill 본문·
  MANIFEST)와 **미래 렌더러까지** 자동으로 커버된다(per-callsite 화이트리스트 불요).
- **산출물 파급**: 중앙 7하네스 중 4개(`h-multiagent`·`h-peer-mesh`·`h-workspace-synthesis`·
  `h-harness-factory`)의 CLAUDE.md/MANIFEST만 변한다. **연합에도 전파** — recipe 산출물의
  중앙 컴포넌트 definition(`chan-peer`·`chan-workspace`·`pat-peer-mesh`)과 techdoc 자신의
  `core:h-research` 인용까지 라벨로 해소된다.

## 정합성 (inspection 독립 재검증, 2026-07-25)

| 항목 | 결과 |
|---|---|
| `tools/validate.py` | **PASS** — SHACL·reachability·capabilities·assemblyOrder, **205 individuals**, 중복 라벨 0 |
| `tools/check_determinism.py` | **PASS** — 4 probe × md/json = 8/8, 각 4 runs 1 distinct pack |
| `retrieve.py "what does the inspection agent observe"` | **37 nodes / 892 of 900** (수정 전 3 / 125) |
| 예산 초과 노드(`tokenEstimate > 900`) | **0개** (수정 전 10) · `observedTokenVolume` 10노드 합 48000 |
| `retrieve.py "multi-agent harness that spawns short-lived sub-agents"` | 후계 `Sub-agent spawn mode` **6.3** > 폐기 `Sub-agents ⚠ DEPRECATED` **2.835**. 폐기 노드는 **팩에 그대로 존재**(숨김 없음) + json에 `maturity` 구조화 필드 |
| 중앙 7하네스 materialize → `id:`/`core:`/`ho:` 토큰 | **0건** (트리 전체 grep, CLAUDE.md뿐 아니라 모든 산출 파일) · dangling 경고 stderr **0줄** |
| `h-coding`·`h-research`·`h-support` | **byte-identical** (직전 커밋 `f495c5a` worktree 빌드와 `diff -r` 무출력) |
| 변경된 4하네스 diff 성격 | CLAUDE.md는 **line-for-line 치환**(minus=plus, 총 줄 수 불변: 99/73/75/125) 이고 변경된 모든 old 줄이 IRI 토큰을 갖고 있었다. MANIFEST는 h-multiagent의 `tokenEstimate` 1줄 + 채널 definition 3줄뿐 |
| **recipe closure (연합)** | catalog 8 recipe 전부 federate **PASS** (`03-newsletter-engine`·`16-fullstack-webapp`·`21-code-reviewer`·`31-ml-experiment`·`46-product-manager`·`contract-demo`·`lpranging`·`techdoc`) |
| recipe 산출물 | `techdoc`: `core:h-research` → **"Research synthesis agent"**, 다른 diff 없음 · `21-code-reviewer`·`03-newsletter-engine`: 각 CLAUDE.md 3줄 + MANIFEST 2줄, 전부 라벨 치환, 산출 토큰 **0건** |

재검증은 repo를 건드리지 않고 수행했다 — `git worktree add --detach <scratch> HEAD`로 직전 커밋
트리를 만들어 old 산출물을 빌드하고 working tree 산출물과 `diff -r` 했다(시간 baseline 오염 회피).

**잔여(회귀 아님)**: `techdoc` 산출 CLAUDE.md 1곳에 `ho:artifactTemplate` 언급이 남는다. 이는
`ho:artifactTemplate` **본문 파일**(손저작 템플릿)에서 온 문자열로 수정 전후 동일하며, 설계상
의도적 미해소(템플릿 본문은 이미 산출물 청중을 위해 쓰였다는 계약)다. 별도 판단거리로 §후속에
남긴다.

## 적용 계획 / 적용 결과 (land)
- **commit `8aecd6f`** "Split observation volume off tokenEstimate; rank retired parts below successors"
  — `tools/retrieve.py` · `ontology/tbox/harness.ttl` · `ontology/shapes/harness-shapes.ttl` ·
  `ontology/abox/core/observational/observation.ttl` + developer 메모리
  `retrieve-pack-quality-budget-lifecycle.md`(및 `MEMORY.md` 인덱스 1줄).
- **commit `f71a033`** "Resolve ontology-internal IRI tokens when building a harness document"
  — `tools/materialize.py` + developer 메모리 `emitted-text-iri-token-projection.md`
  (및 `MEMORY.md` 인덱스 1줄). 공유 파일 `MEMORY.md`는 **hunk 단위로 분할 스테이징**해 각 커밋에
  자기 증분의 인덱스 줄만 담았다.
- **commit `6752de7`** "Record the two projection-quality fixes in the issue log and the audit plan"
  — `docs/plans/OPEN-ISSUES.md` · `docs/plans/disambiguation-audit.md`.
- push `f495c5a..6752de7` (origin/main). CI `validate-ontology` = **success**
  (run 30113743079 — validate + determinism 2 step).
- **커밋에서 의도적으로 제외**: `docs/plans/dispatch-consistency-cleanup.md` (본 세션 중 새로
  나타난 미추적 파일, 브리프 범위 밖 — orchestrator 소유이므로 미커밋으로 남겼다).

## 판정
**apply — 완료(land).** 두 소스 항목은 **inspection이 상신했고 frontmatter가 `status: open`**이다.
사용자 승인 태그가 없으므로 **refresh(제거)하지 않고 그대로 둔다** — 적용 사실은 이 보고서로
기록한다. `status` 태깅은 사용자 소관이며 agent가 대신하지 않는다. 사용자가 두 항목을
`approved`로 고치면 다음 사이클에 항목·본 보고서를 함께 refresh할 수 있다.

## 후속 (이번 재검증에서 확인·발견)
1. **`ho:supersededBy` 부재** (OPEN-ISSUES §B.9). 폐기→후계가 아직 산문(`DEPRECATED: superseded by
   id:mode-sub-agents`)뿐이라 0.35 배수는 **휴리스틱**이다. 엣지가 생기면 "후계보다 아래"를
   구조적으로 보장하고 폐기 노드 검색 시 후계를 함께 끌어올 수 있다.
2. **`ho:observedTokenVolume` capacity-fit는 여전히 무검증**. SHACL이 합을 못 세므로
   `Σ AoO observedTokenVolume ≤ Agent.cognitiveCapacity`는 tool/review 몫이다 — 지금은 그 tool이
   **없다**(실측 합 48000 vs capacity 150000이라 현재는 여유). 린터 후보.
3. **템플릿 본문의 `ho:` 언급**(위 잔여). 산출물 자기완결성 계약을 템플릿 본문까지 확장할지는
   저작 규약 결정 사항 — `ONTOLOGYSTYLE`에 1줄로 명문화하는 편이 맞다(§B.10 predicate order
   갱신과 함께 처리 가능).
