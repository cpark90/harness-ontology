# harness-100 → harness-recipes 증강 로드맵

> 출처: inspection dispatch 분석(2026-07-23). 상위 제안: `../harness-100-augmentation.md`.
> 근거: recipes-design.md, 기존 3레시피, materialize.py/retrieve.py, catalog/CI.

## 0. 핵심 관찰
코퍼스 100개가 **구조적으로 동일한 composition**(orchestrator + 4~5 worker, 병렬 fan-out → synthesis/QA
gate) = 우리 `core:pat-orchestrator-workers` + `core:wf-multiagent`와 정확히 일치. → **importer 템플릿
1개로 ~90% 커버**, 재발 부품은 100× 중복 대신 **중앙에 1회 승격**.

## 1. 매핑 (코퍼스 항목 → recipe .ttl)
| 코퍼스 | 온톨로지 노드 | 비고 |
|---|---|---|
| `agents/<x>.md` name | `id:role-<x>`(`ho:Role`) prefLabel/slug | materialize가 `.claude/agents/<slug>.md`로 round-trip |
| name description | `Role skos:definition` | build_role_md가 frontmatter로 |
| persona body | `id:sp-role-<x>`(`SystemPrompt`), `rolePersona` | body는 **외부 `artifactTemplate` 참조**(vendor 금지, recipes-design §refs). tokenEstimate |
| tool 사용 | `roleTool core:tool-editor/shell/websearch` | least-privilege slice, 중앙 tool로 충족 |
| 원칙/제약 | `roleGuardrail`(중앙 gr-*) + `roleMemoryPolicy` | 코퍼스에 memory policy 없음→합성 |
| orchestrator skill | `hasWorkflow core:wf-multiagent`+`appliesPattern core:pat-orchestrator-workers`; `id:ins-<harness>`(`Instruction`, `skos:notation`=슬래시 트리거) | 워크플로 표=composition spec; 본문=외부 ref |
| extending skill | `id:ins-<x>`(`Instruction`), notation, 외부 ref | **GAP-5**: 특정 agent 타깃 → `augmentsRole` 필요(그 전엔 harness-level 바인딩+definition에 타깃 기록) |
| `CLAUDE.md` | **materialize 출력**(미저장) | build_claude_md가 그래프에서 재생성 |
| 5-agent 팀 | `hasRole`(5) + `derivedFrom core:h-multiagent` | 중립 템플릿 직접 적합 |

**Worked sketch `21-code-reviewer`**: harness 1 + role 5 + persona 5 + instruction 3 + local concept 2 =
**로컬 ~16노드**, 나머지 IRI 재사용(`core:dom-coding`·`core:task-codereview` 이미 존재 → coding 카테고리는
도메인 어휘 거의 무추가).

## 2. 중앙 라이브러리 선(先)성장 (promote-once, 임포트 前)
- **Role**: `core:role-synthesizer`(전 하네스의 최종 QA/reviewer gate; 기존 role-vnv보다 광의 → 중립 sibling).
- **Channel**: `core:chan-workspace`(`_workspace/NN_*.md` 파일 handoff, 전수) · `core:chan-peer`
  (SendMessage mesh). ※ **코퍼스는 peer-mesh** — lpranging의 dispatch 규율과 실질 차이(→ 아래 열린 결정).
- **Guardrail**: `core:gr-structured-output` · `gr-scale-modes` · `gr-graceful-fallback`(+각 짝 Concept).
- **Capability**: `core:cap-synthesis`(synthesizer requiresCapability 충족용) · (옵션)`cap-authoring`.
- **주의(도메인)**: 10 카테고리 도메인이 각 ~10~15 recipe에서 재발 → 재사용 pull은 "중앙", neutral-parts
  규칙은 "recipe-local". **권고: 도메인은 recipe-local 유지, 단 기존 중앙 도메인**(`dom-coding`/`dom-research`/
  `dom-support`/`dom-design`)**은 맞으면 재사용**. → 열린 결정(중앙 도메인 신설 여부).
- 중앙 성장은 **임포트 前 별도 reviewed 변경**(developer dispatch + validate PASS)으로 먼저 land.

## 3. Phasing
**파일럿 5개(변이 span, hand-author, importer 前)**: `21-code-reviewer`(dev·최고 재사용·skill→agent gap 시험)
· `16-fullstack-webapp`(5 role별 상이 tool scope) · `31-ml-experiment`(4-skill 변이) · `03-newsletter-engine`
(content·신규 로컬 도메인) · `46-product-manager`(4-agent 변이·프레임워크 로컬 concept). 5개 통과=템플릿 검증.
**Batch wave(파일럿 green 후, 카테고리별)**: A dev/infra 16-30 · B data/ml 31-42 · C content 01-15 · D
business 43-55 · E edu/research 56-65 · F legal 66-72 · G lifestyle/ops/comms/misc 73-100.
**wave별 게이트(양방향)**: 각 recipe federate validate PASS · materialize round-trip(agents/skills/CLAUDE.md
emit, 외부 ref resolve/stub) · retrieve sanity(신규 하네스가 gap 없이 후보로).

## 4. Importer (semi-automated 권장)
`tools/import_corpus.py` — 코퍼스 균일 → ~90% 기계적, 100× 수작업은 drift 유발.
- **SHOULD(결정적)**: `.claude/` walk → skeleton `id:h-<name>` 바인딩; agent→Role+SystemPrompt(body=외부
  ref); skill→Instruction(orchestrator vs extending 판별, 타깃 agent 기록); tokenEstimate(wc); catalog `<uri>`
  + CI matrix 라인 추가; `ho:maturity "draft"`.
- **MUST NOT(drift/orphan → 사람/developer)**: 어휘 신설(Concept/Capability/Guardrail/Domain **금지**, 기존
  IRI 바인딩만; 신규 도메인 concept는 **flag** — Golden Rule #2) · capability 충족 추측(미충족=hard stop) ·
  본문 vendor · model/guardrail 의미적 배정. → **draft 산출 후 developer 리뷰가 판단성 edge 바인딩 + reviewed 승격.**

## 5. Scale / anti-rot (100 recipe + 중앙 성장)
- **retrieve seed 품질**: 100개 near-identical orchestrator-workers가 lexical 충돌 → prefLabel/definition·
  domain/task edge를 distinctive하게(코퍼스 description 활용), wave별 `retrieve.py` spot 확인.
- **union 크기**: 검증은 **per-recipe closure 1개씩**(중앙+1 recipe), **절대 all-recipes union 금지**.
- **catalog+CI matrix**: 현재 손으로 각 recipe 나열 → 100개는 **glob(`recipes/*/`)에서 생성**하는 build step,
  CI는 path-filtered(변경 recipe만) 또는 shard.
- **중앙 blast radius**: 모든 recipe가 중앙 root import → 나쁜 중앙 edit=100 union 동시 파손. 중앙 변경은
  **전 recipe matrix로 게이트**(D4 불변), §2 중앙 추가를 batch 前 안정 land.
- **maturity 규율**: draft로 임포트, 리뷰 후 승격 — 100 미검토 하네스가 authoritative로 보이지 않게.

## 6. Attribution (Apache-2.0)
코퍼스=Apache-2.0, recipes repo도 Apache-2.0(호환). **NOTICE**에 `revfactory/harness-100` 크레딧 +
각 임포트 recipe README 한 줄. TTL에 `dct:source`(코퍼스 경로)·`dct:license "Apache-2.0"`(템플릿 lineage
`derivedFrom`와 구별). 본문을 참조로 두면 재배포 표면 최소; fetch-commit 시 헤더/NOTICE 동반.
