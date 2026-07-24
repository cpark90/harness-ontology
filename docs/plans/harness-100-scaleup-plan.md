# 계획 — harness-100 코퍼스 스케일업 (8 → 100 recipe)

> 작성: orchestrator (2026-07-25). 상위(승인): `docs/feedback/harness-100-augmentation.md`(`status: approved`).
> 근거 분석: `docs/feedback/harness-100/recipe-roadmap.md`(§1 매핑 · §4 importer · §5 scale · §6 attribution).
> 이 문서는 **wave 계획**이다. 각 Phase는 별도 dispatch brief로 쪼개 실행한다.

## 0. 착수 시점 실측 (2026-07-25)

| 로드맵 항목 | 상태 |
|---|---|
| §2 중앙 라이브러리 선(先)성장 | **완료** — `role-synthesizer`·`chan-workspace`·`chan-peer`·`gr-structured-output`·`gr-scale-modes`·`gr-graceful-fallback`·`cap-synthesis` 전부 land |
| §1 GAP-5 `ho:augmentsRole` | **완료** — TBox에 존재(skill→특정 agent 타깃 표현 가능) |
| §3 파일럿 5 | **완료** — 21·16·31·03·46 + lpranging·techdoc·contract-demo = **published 8 recipe**, 전부 federate PASS |
| §4 importer `tools/import_corpus.py` | **미착수** |
| §5 scale 인프라 | **미착수** — catalog 11엔트리·CI matrix 8엔트리 모두 **손으로 나열** |
| §6 attribution | **부분** — published repo에 `NOTICE` 있음, 파일럿 TTL에 `dct:source` 있음 |
| 코퍼스 | `/home/cpark/git/harness-100` 클론됨, `en/` **100 하네스**(각 `.claude/CLAUDE.md` + `agents/*.md` + `skills/*/skill.md`) |

**남은 임포트 대상 = 95 하네스** (100 − 파일럿 5).

## 1. Phase 0 — 선행 차단요소 (batch 前 반드시)

### P0-a. `retrieve.py` 결정성 수정 — **진행 중** (별도 dispatch, 사용자 승인 완료)
wave 게이트가 "retrieve sanity(신규 하네스가 gap 없이 후보로)"를 쓴다. 계측기가 비결정적인 채로 95× 판정하면
**잘못된 신호를 대량 생산**한다. 이것이 green이 되기 전에는 batch를 시작하지 않는다.

### P0-b. catalog · CI matrix **생성 자동화** (§5)
현재 둘 다 손으로 나열한다(catalog 11 / CI matrix 8). 95개를 손으로 추가하면 누락이 **조용한 부분 closure**로
나타난다 — 이 실패 양식은 이미 한 번 겪었다(전용 recipe catalog 4개가 REORG에서 누락돼 41 individuals만
로드되고도 에러가 안 났다). 따라서 **`recipes/*/` glob에서 catalog와 CI matrix를 생성하는 build step**을
batch 시작 前에 넣는다. CI는 100 entry면 과금·시간이 커지므로 **path-filtered(변경 recipe만) 또는 shard**로.
- 게이트: 생성물이 현재 수기 파일과 **동등**함을 8 recipe로 확인(회귀 0) → 그 다음 자동생성으로 전환.

## 2. Phase 1 — importer (`tools/import_corpus.py`)

로드맵 §4의 SHOULD/MUST NOT를 그대로 계약으로 삼는다.
- **SHOULD(결정적)**: `.claude/` walk → `id:h-<name>` skeleton · `agents/<x>.md`→`Role`+`SystemPrompt`
  (본문은 **외부 `artifactTemplate` 참조**, vendor 금지) · `skills/*`→`Instruction`(orchestrator/extending 판별,
  타깃 agent는 `augmentsRole`) · `tokenEstimate`(wc) · catalog/CI 엔트리 · `ho:maturity "draft"`.
- **MUST NOT(사람/developer에게 넘길 것)**: 어휘 신설(Concept/Capability/Guardrail/Domain **금지**, 기존 IRI
  바인딩만) · capability 충족 **추측**(미충족 = hard stop) · 본문 vendor · model/guardrail 의미적 배정.
  판단성 edge는 draft 산출 후 **developer 리뷰**가 채운다.

### ★수용 시험 (importer의 oracle) — 이 계획의 핵심 안전장치
**파일럿 5개는 이미 손으로 저작돼 검증까지 끝났다.** importer로 그 5개를 **재생성**해 기존 산출물과 대조한다.
- 기계적 부분(role/persona/instruction 골격·tokenEstimate·catalog 엔트리)이 **일치**해야 한다.
- 불일치는 두 종류로 분류해 보고: ① importer 결함 ② 사람이 넣은 **판단성 결정**(= MUST NOT 영역, 자동화 대상 아님).
  ②의 목록이 곧 **"recipe당 사람이 해야 하는 일"의 실측 명세**가 되며, Phase 2의 리뷰 비용 추정 근거가 된다.
- 이 대조가 통과하기 전에는 95개에 돌리지 않는다.

## 3. Phase 2 — batch wave (95 recipe)

로드맵 §3의 카테고리 분할을 따른다: **A** dev/infra 16–30 · **B** data/ml 31–42 · **C** content 01–15 ·
**D** business 43–55 · **E** edu/research 56–65 · **F** legal 66–72 · **G** lifestyle/ops/comms/misc 73–100.

**wave별 게이트(양방향)** — 하나라도 실패하면 그 wave를 land하지 않는다:
1. recipe별 **federate validate PASS**(중앙 + 그 recipe **1개** closure). **all-recipes union 금지**(§5).
2. **materialize round-trip**: `agents/*.md`·`skills/*`·CLAUDE.md emit, 외부 ref resolve/stub, 2회 실행 결정성.
3. **retrieve sanity**: 신규 하네스가 capability gap 없이 후보로 뜨는가(P0-a 이후라야 의미 있음).
4. **중앙 무회귀**: 중앙 하네스 4종 materialize **byte-identical**(recipe 추가가 중앙을 흔들지 않음).

## 4. 주요 리스크 (계획에 이미 반영)

- **retrieve seed 품질 붕괴 (anti-rot 본질)**: 100개가 거의 동일한 orchestrator-workers 구성이라 lexical
  충돌이 난다. → prefLabel/definition·domain/task edge를 코퍼스 description으로 **distinctive**하게 만들고,
  wave마다 spot 확인. 이것이 나빠지면 "무엇을 재사용할지 못 찾는" 상태가 되어 repo의 목적이 훼손된다.
- **중앙 blast radius**: 모든 recipe가 중앙 root를 import → 나쁜 중앙 edit 하나가 100 union을 동시 파손.
  중앙 변경은 **전 recipe matrix로 게이트**(D4 불변). 중앙 성장은 batch 前에 안정 land(이미 완료).
- **union 크기**: 검증은 항상 per-recipe closure 1개씩.
- **maturity 규율**: 전량 `draft`로 임포트. 미검토 95개가 authoritative로 보이지 않게 한다.
- **리뷰 비용**: 95 × developer 리뷰는 이 계획 최대의 인적 비용이다 → 아래 열린 결정 D2.

## 5. 사용자 확정 결정 (2026-07-25) — **두 축을 분리한다**

> "온톨로지에는 전체 속성값들을 다 반영해주고, 하네스 예제 추가는 대표적인 30~40개 반영해줘"

**D3 확정**: 범위를 **어휘 축**과 **인스턴스 축**으로 나눈다. 이 분리가 이 계획의 중심 원리다.

| 축 | 소스 범위 | 산출 | 근거 |
|---|---|---|---|
| **어휘(속성값)** | **100 전수** | 중앙 중립 부품(`ontology/abox/core/`)이 코퍼스에서 관측되는 **모든 속성값을 커버** | 부품 라이브러리의 완결성 — 나중에 어떤 하네스를 조립하든 필요한 부품이 이미 있어야 한다 |
| **인스턴스(예제)** | **대표 30~40** | recipe (`staging/harness-recipes/recipes/`) | 코퍼스가 구조적으로 균일해 인스턴스의 한계효용은 체감. 예제는 변이 span만 보이면 충분 |

**핵심**: 100개를 다 임포트하지 않아도 **어휘 커버리지는 100%**여야 한다. 즉 61~70번 하네스만 쓰는 role
원형·guardrail 원칙·tool·skill 유형이 있다면, 그 하네스를 recipe로 넣지 않더라도 **그 부품은 중앙에 있어야 한다**.
→ 그래서 아래 **Phase 0.5(전수 속성 인벤토리)** 가 신설되며, 이것이 대표 선정의 근거도 함께 만든다.

**대표 30~40 선정 기준(coverage-driven)**: 임의 표본이 아니라 **어휘 커버리지를 최대화**하도록 고른다 —
10 카테고리 전부 대표 + role 원형·skill 유형·tool scope·팀 규모의 변이를 span. 파일럿 5개는 이미 포함된 것으로 친다.

## 5b. 남은 열린 결정 (Phase 1 착수 전까지)

- **D1. 도메인 정책**: 10 카테고리 도메인이 재발한다. 로드맵 권고는 "**recipe-local 유지**, 단 기존 중앙
  도메인(`dom-coding`/`dom-research`/`dom-support`/`dom-design`)이 맞으면 재사용". 단 D3 확정으로 **어휘는
  전수 커버**가 되었으므로, 카테고리 도메인은 중앙 승격 후보로 재검토할 여지가 생겼다 → Phase 0.5 인벤토리
  결과(도메인 값의 실제 분포·중복도)를 보고 판단한다.
- **D2. 리뷰 깊이**: importer 산출은 `draft`다. (a) 30~40 전수 developer 리뷰 후 `reviewed` 승격, (b) 표본
  리뷰 + 나머지 `draft` 유지, (c) 전량 `draft`. Phase 1 수용 시험이 ②로 분류한 "판단성 결정" 목록의 크기를
  보고 정하는 것이 합리적이다. (D3가 95→30~40으로 줄어 이 비용은 이미 크게 낮아졌다.)

## 6. 실행 순서 (요약)
```
P0-a retrieve 결정성 (진행 중)  ─┐
P0-b catalog/CI 자동생성        ─┴→ P1 importer + 파일럿 5 재생성 대조 → D1/D2/D3 확정 → P2 wave A…G
```
각 단계는 완료 후 **inspection land**(git은 inspection 소관)를 거쳐 다음 단계로 간다.
