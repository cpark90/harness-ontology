# Dispatch brief — Phase 0.6: 중앙 어휘 GAP 저작 (코퍼스 전수 속성값 반영)

> 작성: orchestrator (2026-07-25). 상위: `docs/plans/harness-100-scaleup-plan.md` §5c ·
> 근거: `docs/plans/harness-100-attribute-inventory.md` §2B~2F (전수 실측).
> 사용자 지시: **"온톨로지에는 전체 속성값들을 다 반영"** — 100개를 다 임포트하지 않아도 **어휘 커버리지는 100%**여야 한다.
> 실행: **developer dispatch (opus)**. ★**선행: 작업트리 clean일 때 fire**(진행 중 dispatch와 abox 충돌 방지).

## 이 증분의 목적
코퍼스 100개에서 관측된 속성값 중 **중앙에 담을 그릇이 없는 것**(분류 ①)을 중립 부품으로 저작하고,
**기존 개체로 흡수 가능한 것**(분류 ②)은 `skos:altLabel`로 붙인다. 분류 ③(코퍼스 특수·도메인 내용)은
**중앙에 넣지 않는다** — 중립 부품 라이브러리를 도메인 카탈로그로 변질시키는 것이 이 작업의 최대 위험이다.

## A. 신규 Role 6 (①, 인벤토리 §2B)
정량 근거: 파일럿 5개가 **로컬 Role 21개를 저작하고 중앙 Role은 1개만 재사용**했다. 35 recipe로 가면 로컬 Role
약 140개가 되며 대부분이 아래 5원형의 도메인 변형이다.

| slug | 원형 | 규모 | 기존과 왜 다른가 (definition에 반영할 것) |
|---|---|---|---|
| `id:role-analyst` | 평가·진단하고 발견을 severity와 함께 보고 | 78 agent/64 harness | `role-research`는 *수집*, `role-vnv`는 *하네스 산출물 판정* |
| `id:role-author` | 발견을 구조화된 문서로 **생산** | 63/51 | `role-synthesizer`는 terminal convergence **gate**(판정+통합). 이쪽은 **생산자** |
| `id:role-implementer` | 사양을 실제 산출물로 구현 | 74/46 | ★아래 주의 |
| `id:role-planner` | 계획·일정·로드맵을 산출하는 **워커** | 50/44 | `role-orchestrator`는 "performs no substantive work itself" — 정반대 |
| `id:role-strategist` | 선택지·권고를 제시 | 30/26 | 대응 없음 |
| `id:role-tester` | 테스트 케이스·시뮬레이션 산출 | 9/7 | 판정형과 다르나 규모 작음 — **우선순위 낮음, 저작하되 salience 낮게** |

**★`role-implementer` 주의 (orchestrator 결정)**: 기존 `core:role-developer`의 definition이
*"authors the ontology nodes (abox individuals) assigned in a brief"* — **이 repo 전용이라 중립이 아니다**.
그러나 **definition을 고치지 않는다.** 이유는 byte-identity가 아니라 **의미**다: `role-developer`는 이 repo의
harness가 실제로 쓰는 구체 역할이고, `role-implementer`는 도메인 무관 원형으로 **서로 다른 노드**다.
→ **중립 sibling 신설**이 옳다. 두 definition이 서로를 구별하도록 **disambiguation 문장**을 넣어라
(`disambiguation-audit.md` 관례. 단 IRI 참조는 emit 시 라벨로 해소되므로 자유롭게 써도 된다).

## B. 신규 Guardrail 4 (①, 인벤토리 §2C)
| slug | 규율 | 규모 | 최근접 기존과 왜 다른가 |
|---|---|---|---|
| `id:gr-cross-validation` | 리뷰어가 전 deliverable을 교차검증하고 severity 등급으로 표기, 최상위만 강제 재작업 | 68/100 | `gr-discriminating-eval`은 *baseline differential* 평가법, `gr-bounded-iteration`은 루프 횟수 |
| `id:gr-declared-routes` | 각 role이 자기 outbound hand-off 상대를 **명시 선언** | 469/489 agent · 1818 route | `chan-peer`는 *매체*, `channelParticipant`는 *엔드포인트 집합* — "각자 라우트를 선언한다"는 **정책**이 없다 |
| `id:gr-sequenced-artifacts` | 워크스페이스 산출물에 서수 접두사(`{NN}_{type}.{ext}`) | 419/432 (97%) | `gr-absolute-paths`는 경로 규율. 이 규약이 있어야 producer→consumer 해소가 결정적 |
| `id:gr-three-flow-acceptance` | normal/existing-input/error **세 fixture를 모두** 갖춘다 | 90/100 | `scenarioKind` 값은 있으나 "셋을 다 갖춰라"는 정책 노드가 없다. `gr-structural-coverage`는 소스→표현 매핑 |

Guardrail은 관례상 `ho:promptText`(정책 본문)를 갖고 `skos:definition`은 생략 가능하다(기존 34개 전부 그렇다) —
**기존 파일의 지역 컨벤션을 그대로 따르라.** `ho:tokenEstimate` 필수.

## C. 신규 FailurePolicy 5 (①, 인벤토리 §2D-D1)
`fp-agent-failure-retry`(91) · `fp-insufficient-input`(64) · `fp-review-critical-rework`(52) ·
`fp-source-unavailable`(49) · `fp-conflict-contradiction`(25). 기존 중앙 2개는 **이 repo 방법론 전용**이라
도메인 무관 원형이 없다. `ho:failureCondition` / `ho:recoveryStrategy` 사용.

**★host 결정 (orchestrator)**: `ho:hasFailurePolicy`는 Harness 직결이라 host 배선이 필수다.
**`core:h-workspace-synthesis`에 물려라.** 이유: 그 definition이 스스로 *"wires the recurring central-library
parts a multi-agent worker team reuses … exists to make those parts connected, reusable components
(anti-orphan)"* — **정확히 이 용도의 library carrier**다. `h-multiagent`(중립 base template)에 물리지 말 것.
그 하네스의 CLAUDE.md가 바뀌는 것은 **정상**이다(carrier의 목적이 그것). 다른 하네스 산출물은 불변이어야 한다.

## D. 짝 Concept (①, 인벤토리 §2D-D4)
신규 Guardrail·Role이 `ho:tagged`로 가리킬 Concept가 없으면 **orphan**이 된다(기존 관용: Guardrail→Concept).
필요한 만큼만 신설하고 **반드시 같은 커밋에서 `skos:broader` 부모에 걸거나 무언가를 tag**하라(ONTOLOGYSTYLE §1b).
후보: cross-validation · deliverable-artifact · trigger-boundary. **기존 35개 Concept를 먼저 재사용 시도**할 것.

## E. altLabel 흡수 8 (②) — **신규 개체를 만들지 말 것**
근사 동의어 노드를 만드는 것이 이 repo가 막는 drift다. 아래는 **기존 개체에 `skos:altLabel` 추가**로만 처리한다.
- `role-synthesizer`/`role-vnv` ← reviewer-qa 변종("cross-validator", "quality reviewer")
- `role-design` ← 시각·교안 designer 포괄(definition이 "system/architecture design"에 치우침 → altLabel 보강)
- `role-analyst`(신규) ← modeler-calculator · `role-implementer`(신규) ← data-preparer/optimizer-tuner
- `gr-bottleneck-avoidance` ← "parallel-first" · `gr-grounding` ← assumption/limitation disclosure ·
  `gr-cite`+`gr-grounding` ← no-fabrication · `gr-scale-modes` ← "full pipeline"·"review mode"

## F. 중앙 금지 (③) — **저작하지 말 것**
domain-specialist role · localizer · compliance/security/a11y/l10n 원칙 문장 · TestScenario prompt 실체 ·
extending skill 209종 · 도메인 scale-mode 라벨 · Task 100종. 전부 recipe-local이다.

## G. 이번 범위에서 **의도적으로 제외**한 것 (coverage-audit 명시 사유)
- **D2 Deliverable 원형 3종**: Deliverable은 `stepProduces`로만 도달하므로 workflow step 배선이 필요하고,
  `wf-multiagent`를 건드리면 `h-multiagent` 산출물이 바뀐다. **별도 증분**으로 분리(host workflow 설계 필요).
- **D3 PromptSection 원형 5종**: recipe의 persona 본문은 외부 `artifactTemplate` 참조라 **분해의 소비자가 없다**
  → YAGNI(ONTOLOGYSTYLE §1c). 소비자가 생기면 그때 저작한다.
- **T1 scale mode 클래스**: TBox 확장이라 **별도 브리프**(`harness-100-scaleup-plan.md` §5c에서 (i) 신설로 확정).

## 저작 규약
`ONTOLOGYSTYLE.md` 전면 적용 — predicate 순서 §3 · 4칸 들여쓰기 · `skos:prefLabel` 클래스 내 유일 ·
definition은 **"왜 존재하고 언제 고르는가"** · **`ho:tokenEstimate` 필수** · 신규 노드 `ho:maturity "draft"` ·
파일은 DA-4 그룹 디렉토리(`organization/roles.ttl` · `behavioral/guardrails.ttl` · `verification/verification.ttl` ·
`vocab/concepts.ttl`). **새 unit 파일을 만들지 말 것**(기존 unit에 append — catalog·imports 무변경).
**어휘 발명 금지**: 새 `ho:` 클래스·프로퍼티 0. 필요하면 저작 말고 **GAP 보고**.

## 완료 게이트
```bash
/usr/bin/python3 tools/validate.py     # PASS. 개체 205 + 신규분
/usr/bin/python3 tools/check_determinism.py
/usr/bin/python3 tools/retrieve.py "who analyses findings and reports them by severity"   # role-analyst
/usr/bin/python3 tools/retrieve.py "reviewers cross-validate every deliverable"           # gr-cross-validation
/usr/bin/python3 tools/materialize.py h-multiagent ...   # ★CLAUDE.md byte-identical 이어야 함
/usr/bin/python3 tools/materialize.py h-workspace-synthesis ...  # FailurePolicy 5 렌더(정상 변경)
```
**불변식**: 신규 부품은 `h-workspace-synthesis`에만 물린다 → **`h-multiagent`·`h-peer-mesh`·`h-harness-factory`·
`h-coding`/`h-research`/`h-support` 산출물은 전부 byte-identical**이어야 한다. 깨지면 배선이 잘못된 것이다.

## 금지
TBox·shapes 변경 · 새 unit 파일 · `docs/**` 편집 · **git 조작**(inspection 전담).

## 반환 보고
① 저작한 개체 IRI 전량(클래스별) ② 각 개체 연결 edge(무엇이 어디에 물렸나) ③ altLabel 추가분
④ 게이트 로그 + **byte-identity 6하네스 증명** ⑤ 재사용 시도했으나 못 쓴 기존 개체와 이유 ⑥ GAP.
