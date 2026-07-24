# harness-100 전수 속성 인벤토리 (Phase 0.5)

> 작성: developer dispatch (2026-07-25). 상위 계획: `harness-100-scaleup-plan.md` §5(D3 두 축 분리).
> 근거 분석: `docs/feedback/harness-100/part-taxonomy.md` · `recipe-roadmap.md` §1.
> 소스: `/home/cpark/git/harness-100/en/` **100 전수**(읽기 전용). 중앙 대조: `ontology/abox/core/` 206 individuals.
>
> **이 문서는 인벤토리·GAP 보고서이며 저작물이 아니다.** 여기서 제안하는 신규 개체는 하나도 저작되지 않았다.
> 신설 여부는 orchestrator의 설계 결정이다(ONTOLOGYSTYLE §1b anti-drift — 발명 금지, 보고).

---

## 0. 방법과 측정 신뢰도

- 100개 하네스의 `.claude/CLAUDE.md` + `agents/*.md` + `skills/*/skill.md` 전 904 파일을 **스크립트로 파싱**해
  frontmatter·섹션 헤딩·표 헤더·표 행·bullet을 구조 추출했다. 전문 정독은 표본 3개(71/21/16)만.
- **실측**(파일에서 직접 센 값)과 **정규화 실측**(regex 사전으로 값을 묶은 뒤 센 값)을 구분해 표기한다.
  정규화는 사람이 만든 사전이므로 ±약간의 오차가 있다 — 표에 `(정규화)` 로 표시.
- **판정**(내가 내린 매핑 판단)은 `판정` 으로 표시하며 근거를 함께 적는다.
- 코퍼스 영문판은 기계번역 흔적이 있어 헤딩 문자열이 13종까지 변형된다(예: `Workflow` / `workflow` /
  `flow` / `data before as`). 따라서 **헤딩 문자열이 아니라 표 헤더·본문 시그널**을 1차 근거로 삼았다.

### 0a. 규모 실측 (전수)

| 항목 | 값 |
|---|---|
| harness | **100** |
| agent 정의 파일 | **489** (5개짜리 89, 4개짜리 11) |
| skill 파일 | **315** = orchestrator **100** + agent-extending **215** (3-skill 85, 4-skill 15) |
| agent frontmatter 키 | `name`, `description` **만** — 489/489. `tools:`·`model:` **0/489** |
| skill frontmatter 키 | `name`, `description` **만** — 315/315 |
| agent body 중앙값 | 450 words (min 230 / max 796) |
| orchestrator skill 중앙값 | 876 words (min 356 / max 1049) |
| extending skill 중앙값 | 656 words (min 307 / max 1122) |

---

## 1. 축별 속성값 전수 인벤토리

브리프가 지정한 11축 + 소스에서 추가 발견한 3축(§1L~1N).

### 1A. Role 원형 (agent 이름·역할 유형)

489 agent 중 **unique name 429**, 2개 이상 하네스에 같은 이름으로 재등장하는 것은 **46종뿐**
(최다 `doc-writer` 5회). 즉 **이름 인스턴스의 재사용률은 거의 0** — 원형(archetype)만 재사용된다.

이름 마지막 토큰 상위 실측: `analyst 65 · reviewer 52 · designer 40 · writer 39 · architect 21 ·
engineer 20 · manager 19 · planner 16 · strategist 15 · builder 14 · specialist 10 · developer 8 ·
assessor 8 · researcher 6`.

정규화 후 **14 원형** (정규화):

| # | 원형 | agents | harness 도달 |
|---|---|---|---|
| 1 | reviewer-qa (reviewer/assessor/auditor/validator/verifier/checker/proofreader) | 80 | 68/100 |
| 2 | analyst (analyst/analyzer/evaluator/investigator/detector/profiler) | 78 | 64/100 |
| 3 | implementer-engineer (engineer/architect/builder/developer/integrator/generator) | 74 | 46/100 |
| 4 | writer-synthesizer (writer/editor/copywriter/summarizer/reporter/drafter/narrator) | 63 | 51/100 |
| 5 | coordinator-planner (manager/planner/coordinator/scheduler/director/producer) | 50 | 44/100 |
| 6 | designer (designer/stylist/illustrator/storyboarder/visualizer) | 44 | 43/100 |
| 7 | strategist-advisor (strategist/advisor/coach/mentor/tutor) | 30 | 26/100 |
| 8 | researcher-collector (researcher/searcher/collector/explorer/curator/monitor) | 24 | 23/100 |
| 9 | modeler-calculator (modeler/classifier/matcher/tracker/estimator/engine) | 11 | 11/100 |
| 10 | specialist-domain (specialist/expert) | 11 | 9/100 |
| 11 | tester-simulator (tester/simulator/debater/quiz-master) | 9 | 7/100 |
| 12 | data-preparer (extractor/preprocessor/cleaner/parser/linker) | 6 | 5/100 |
| 13 | optimizer-tuner (optimizer/tuner/refiner) | 5 | 5/100 |
| 14 | transformer-localizer (translator/localizer/harmonizer) | 3 | 1/100 |
| — | 미분류 잔여 | 1 (`adr-author`) | 1/100 |

**팀 규모·구성** (실측): 5-agent **89/100**, 4-agent **11/100**. 6 이상·3 이하 **0**.
reviewer 원형 보유: 0개 32/100 · 1개 56/100 · 2개 12/100.

### 1B. Tool 사용 패턴 (least-privilege slice)

**핵심 실측: agent 파일에 `tools:` 선언이 없다(0/489).** 도구 범위는 본문에서 **추론**해야 한다.
본문 시그널로 slice를 재구성한 결과 (정규화):

| slice | agents | harness 도달 |
|---|---|---|
| file only (`_workspace/`에 산출물 저장) | 333 | — |
| file + websearch | 94 | — |
| file + message(SendMessage 명시) | 59 | — |
| file + message + websearch | 1 | 09-documentary-research |
| code + file (코드펜스 보유) | 1 | 69-privacy-engineer, 98-academic-paper |
| 무 시그널 | 1 | 16-fullstack-webapp |

축별 도달: **file 488 agents / 100/100 harness** · **websearch 95 agents / 57/100** ·
**codeexec 사실상 0** (agent 파일에 code fence가 있는 harness는 **2/100**; skill 파일까지 넓혀도 25/100).

도구 이름 언급의 harness 도달(실측): `SendMessage 100/100` · `Task 93/100` ·
`TaskCreate/TaskUpdate 60/100` · `Write 64/100` · `WebSearch 41/100` · `WebFetch 40/100` ·
`Read 18/100` · `Edit 5/100` · `Glob/Grep 2/100` · `Bash 0/100`.

> **놀라운 점**: 코퍼스의 tool-scope 변이는 사실상 **이진**(file / file+web)이다. 파일럿
> `16-fullstack-webapp`가 보여준 "role마다 다른 tool slice"는 코퍼스에서 **전형이 아니다**.

### 1C. Skill 유형

- **orchestrator skill**: 100/100. 디렉토리명 = 하네스 basename, 예외 0. 실제 제어 문서.
- **extending skill**: 215개, unique 209. **2개 하네스에 같은 이름으로 등장하는 것은 6종뿐**
  (`data-visualization-guide`·`scoring-optimizer`·`roi-calculator`·`financial-ratio-analyzer`·
  `win-theme-builder`·`research-methodology`), **3개 이상은 0** → 인스턴스 재사용률 ≈ 0.
- extending skill의 **내용 형태**(실측): 표 210/215 · 코드블록 201/215 · 수식/계산 150/215 ·
  예시 129/215 · 절차 128/215 · 체크리스트 101/215 · 템플릿 79/215 · python 27 · json 8.
- 이름 기반 type-archetype (정규화, part-taxonomy §3의 5분류를 확장):
  `calculator-engine 48 · pattern-template-catalog 36 · framework-methodology 21 ·
  knowledge-reference-base 17 · visualization-reporting 5 · linker-mapper 3 · 미분류 85`.
  → 미분류 85가 크다는 사실 자체가 **"extending skill 이름은 도메인 payload"**의 실증이다.
- **skill → 대상 agent 매핑은 명시적**: 96/100이 "Agent Extension Skills" 표를 갖는다.
  표 헤더가 깔끔한 59개에서 130행을 추출했고, 그 중 **114행이 대상 agent를 2개 이상 나열**한다
  → `ho:augmentsRole`은 **반복 가능해야 한다**(현재 cardinality shape 없음 → 충족 ✓).

### 1D. Guardrail / 원칙 문장

두 층으로 나타난다.

**(a) 구조적 규율** — agent 파일 섹션 존재(실측):

| 섹션 | 보유 agent |
|---|---|
| Core Responsibilities (변형 포함) | **489/489** |
| Working Principles (변형 포함) | **489/489** |
| Team Communication Protocol | **469/489** (총 outbound route 1818, 중앙값 4) |
| Output/Deliverable Format | **443/489** |
| Error Handling | **441/489** |
| Verification/Validation Checklist | 62/489 |

**(b) 원칙 문장 테마** — Working Principles bullet 6130개 분류 (정규화, agent 수 / harness 도달):

| 테마 | agents | harness |
|---|---|---|
| prioritize by impact/severity | 183 | 89/100 |
| consistency / terminology discipline | 116 | 66/100 |
| assumption & limitation disclosure | 110 | 57/100 |
| quantified / measurable claims | 55 | 33/100 |
| audience adaptation / readability | 50 | 25/100 |
| compliance / regulatory alignment | 50 | 25/100 |
| evidence-grounding / cite source | 46 | 27/100 |
| actionable / concrete over abstract | 44 | 33/100 |
| security / privacy by design | 44 | 15/100 |
| bounded iteration (2~3 rounds) | 31 | 31/100 |
| accessibility / inclusive design | 30 | 18/100 |
| structured-output (bullet로 명시된 경우) | 25 | 16/100 |
| reproducibility / versioning | 17 | 12/100 |
| no fabrication / flag unverified | 12 | 9/100 |

> structured-output이 bullet 기준으로 낮은 것은 **문장이 아니라 구조**(Output Format 섹션 443/489)로
> 강제되기 때문이다 — 두 측정을 함께 읽어야 한다.

**(c) orchestrator skill 수준 규율** (실측, harness 도달):
`retry 언급 98/100` · `error-type 표 95/100` · `bounded 2 rounds 75/100` · `cross-validation 68/100` ·
`parallel 65/100` · `🔴 severity emoji 64/100` · `explicit out-of-scope 74/100` · `single-agent mode 31/100`.

### 1E. 조율 메커니즘 (coordination)

| 메커니즘 | harness 도달 (실측) |
|---|---|
| 파일 workspace (`_workspace/NN_*.md`) | **100/100** |
| SendMessage peer mesh | **100/100** |
| task board (`TaskCreate`/`TaskUpdate`) | **60/100** |
| 최종 사용자 보고 (Phase 3 report to user) | **100/100** (Phase 3 섹션 100/100) |

Data Transfer Protocol 표 헤더 `strategy / method / purpose` 66/100에서 직접 확인. 3 전략의
조합은 2가지뿐: `file+message` 40/100, `file+message+task-board` 60/100.

### 1F. 실행 topology 신호

**실측: `Agent Team` 100/100.** `sub-agent` 표기 **0/100**, `hybrid` **1/100**(문맥상 무관한 단어).
"Execution Mode" 섹션 첫 줄이 전부 `**Agent Team** — N members communicate directly via SendMessage
and cross-validate` 계열이다(문구 변형 15종, 의미 동일).

패턴 신호: task-DAG 표(`Order/Task/Owner/Depends On/Deliverable`) **91/100** · `parallel` 명시
65/100 · Phase 1/2/3 3단 구성 **100/100** · reviewer 수렴 게이트 68/100.

> DAG 표가 없는 8개: `12·13·14·15·27·28·29·30` (번역 변형으로 헤더가 깨진 경우 포함, 판정).

### 1G. Scale mode (요청 범위 → agent 부분집합)

"User Request Pattern / Execution Mode / Agents" 표 **95/100**. 모드 개수 실측:
**5개 67/100 · 6개 27/100 · 7개 1/100**.

모드 라벨 정규화 빈도 상위: `full pipeline 86 · review mode 36 · analysis mode 19 · strategy mode 7 ·
budget mode 6 · test/design/report mode 각 5 · security/checklist mode 각 4` … 이후는 전부 ≤3
(도메인 고유명). **중립 라벨은 사실상 `full pipeline`과 `review mode` 둘뿐**이고 나머지는 도메인 값.

### 1H. 도메인 / 카테고리

코퍼스 README의 공식 10 카테고리 (실측):

| 카테고리 | 하네스 수 |
|---|---|
| 1 Content Creation & Creative (01–15) | 15 |
| 2 Software Development & DevOps (16–30) | 15 |
| 3 Data & AI/ML (31–42) | 12 |
| 4 Business & Strategy (43–55) | 13 |
| 5 Education & Learning (56–65) | 10 |
| 6 Legal & Compliance (66–72) | 7 |
| 7 Health & Lifestyle (73–80) | 8 |
| 8 Communication & Documents (81–88) | 8 |
| 9 Operations & Process (89–95) | 7 |
| 10 Specialized Domains (96–100) | 5 |

Task(하네스가 다루는 use-case)는 하네스마다 1개씩 사실상 고유 — 100종.

### 1I. Model 선언 유무

**실측: 0/100.** frontmatter에 `model:`이 없고, 본문 어디에도 `opus`/`sonnet`/`haiku`/`claude-*`
문자열이 없다. 대신 roster 표의 Type 열이 **`general-purpose` 100/100** — 이는 Claude Code의
`subagent_type`이지 모델이 아니다.

> 결과: **ModelConfig 바인딩은 소스에 근거가 없는 판단성 결정**이다. roadmap §4의 MUST NOT
> ("model/guardrail 의미적 배정은 사람")과 정확히 일치 — importer가 추측하면 안 된다.

### 1J. Deliverable / artifact 유형

- `_workspace/` 참조 **distinct path 432종**, 총 참조 668회.
- 확장자(실측): **`.md` 632회 / 99·100 harness**. 그 외 `.yaml` 2 · `.sql` 2 · `.srt` 1 · `.html` 1,
  디렉토리 참조 32.
- **파일명 규약: `NN_` 서수 접두사 419/432 (97%)** — `{sequence}_{document_type}.{extension}`.
- 의미 분류 (정규화, distinct path 기준):
  `analysis 58 · final-report 41 · design-spec 40 · plan 33 · guide-doc 28 · review-report 26 ·
  draft-content 22 · input-brief 10 · checklist 6 · data 6 · code 5 · 기타 157`.
- 사실상 보편 산출물 3종(판정): `00_input.md`(orchestrator가 Phase 1에서 생성) ·
  중간 워커 산출물 `NN_<topic>.md` · 마지막 `NN_review_report.md`.

> **놀라운 점**: 이 코퍼스는 **코드 생산 코퍼스가 아니라 문서 생산 코퍼스**다(.md 99/100,
> 코드펜스 보유 agent 2/100). `cap-codeexec`/`tool-shell`은 거의 필요하지 않다.

### 1K. 검증 / QA gate 유형

- **Test Scenarios**: 90/100이 **정확히 3개**(총 prompt 270개), 10/100은 헤딩 파손으로 미검출.
  3종 = Normal Flow(73) / Existing-File·Partial Flow(72) / Error Flow(89) — **TBox
  `ho:scenarioKind`의 `normal`/`existing-input`/`error`와 1:1 대응** ✓.
- **Error Handling 표** 95/100, 총 470행. 조건 정규화 (harness 도달):

  | failure 조건 원형 | harness |
  |---|---|
  | agent failure → retry 1회 후 누락 표기 | **91/100** |
  | 입력 정보 부족 → 일반 기준으로 진행 + 보완 필요 표기 | 64/100 |
  | 리뷰에서 🔴 발견 → 담당 agent 재작업(최대 2회) | 52/100 |
  | 외부 소스/검색 불가 → 대체 근거 사용 | 49/100 |
  | 포맷/파싱 오류 | 27/100 |
  | 문서 간 모순 → 리뷰어가 해소 방향 제시 | 25/100 |
  | 범위 초과 | 6/100 |

- **수렴 게이트 형태**(판정): DAG 종단 소유자를 뽑을 수 있었던 92개 중 **45개는 reviewer/QA류**,
  **47개는 synthesizer/reporter/planner류**. 즉 종단 게이트는 **"판정형 reviewer"와 "통합형
  synthesizer"의 두 원형**으로 갈린다 — 중앙 `role-synthesizer`는 두 성격을 한 노드에 합쳐 놓았다.

### 1L. (추가 발견) Trigger boundary

- orchestrator skill description의 **positive trigger phrase 총 963개**, 하네스당 중앙값 **10개**
  (min 7 / max 14). `Use this skill for ... including: '...', '...'` 형식 78/100.
- **명시적 out-of-scope 문장 74/100** (`Note: ... are outside the scope of this skill.`).
- extending skill description에도 out-of-scope 132/215.
→ TBox `ho:triggerPhrase` / `ho:outOfScope`(Harness+Instruction 공용)로 **완전 충족** ✓.

### 1M. (추가 발견) Agent persona 섹션 구조

agent 파일 body는 **5-섹션 고정 shape**다(§1D(a) 표). 이는 `ho:PromptSection` + `ho:sectionOrder`로
표현 가능한 구조이며, **100개 전수에 걸쳐 동일**하다 — 즉 도메인이 아니라 **form**이다.

### 1N. (추가 발견) CLAUDE.md 자체는 얇다

헤딩 실측: `Structure 87+13 · Usage 87+13 · Deliverables 51+19(Outputs)+13+4(Artifacts)`.
오케스트레이션 로직이 없다 → **우리 materialize 출력이 소스 CLAUDE.md보다 정보량이 많다**.
소스 CLAUDE.md는 저장 대상이 아니라 **버려도 되는 파생물**(roadmap §1과 일치) ✓.

---

## 2. 중앙 어휘 대조 → GAP 목록

대조 기준: `ontology/abox/core/` **206 individuals** (Role 8 · Tool 4 · Capability 8 · Channel 6 ·
Guardrail 34 · Concept 35 · DesignPattern 15 · ExecutionMode 3 · Domain 4 · Task 6 · Workflow 7 ·
WorkflowStep 10 · Deliverable 2 · TestScenario 2 · FailurePolicy 2 · ModelConfig 2 · Memory 3 · …).

분류 기호:
**①** 중앙에 신규 개체로 담아야 함 · **②** 기존 개체의 `skos:altLabel`/기존 개체로 흡수 가능 ·
**③** 코퍼스 특수/도메인 내용 — 중앙에 넣으면 안 됨(recipe-local).

### 2A. 충족되는 축 (GAP 0)

| 관측값 | 충족 IRI | 근거 |
|---|---|---|
| 파일 workspace hand-off 100/100 | `core:chan-workspace` | definition이 "shared file workspace … named artifact file in a common directory" |
| SendMessage peer mesh 100/100 | `core:chan-peer` + `core:pat-peer-mesh` | "peer agents coordinate DIRECTLY … message mesh" |
| task board 60/100 | `core:chan-task-board` | "shared task list over which workers claim tasks" |
| 사용자 보고 100/100 | `core:chan-agent-user` | — |
| Agent Team topology 100/100 | `core:mode-agent-teams` (+`pat-agent-teams`) | ExecutionMode 축 완전 충족 |
| orchestrator + 병렬 워커 + 수렴 | `core:pat-orchestrator-workers`·`pat-fanout-fanin`·`pat-producer-reviewer`·`pat-pipeline` | 4 패턴으로 전 조합 표현 가능 |
| 파일 편집 100/100 | `core:tool-editor` / `cap-fileedit` | — |
| 웹 검색 57/100 | `core:tool-websearch` / `cap-websearch` / `cap-citation` | — |
| 코드 실행 2/100 | `core:tool-shell` / `cap-codeexec` | — |
| trigger boundary 74/100 + 963 phrase | `ho:triggerPhrase` / `ho:outOfScope` | Harness+Instruction 공용 |
| skill → 대상 agent | `ho:augmentsRole` (repeatable) | 다중 타깃 114행 수용 가능 |
| skill 주입 방식 | `ho:integrationMode "invoke"` | orchestrator skill = 슬래시 트리거 |
| test scenario 3종 | `ho:scenarioKind normal/existing-input/error` | 값 집합 1:1 대응 |
| structured output ≈전수 | `core:gr-structured-output` (alt "deliverable template") | — |
| scale mode 정책 95/100 | `core:gr-scale-modes` (alt "full/reduced/single modes") | 정책 자체는 충족 |
| error fallback 95/100 | `core:gr-graceful-fallback` (alt "error fallback") | — |
| bounded 2 rounds 75/100 | `core:gr-bounded-iteration` (alt "retry cap") | "at most two to three rounds" |
| least-privilege 슬라이스 | `core:gr-least-privilege` + `ho:roleTool` | — |
| 근거 제시 27/100 | `core:gr-cite` · `core:gr-grounding` | — |
| skill 형식 규율 | `core:gr-well-formed-skill` | — |
| 역할 단일책임 | `core:gr-single-responsibility` | — |
| workspace 경로 규율 | `core:gr-absolute-paths` | — |
| per-role 채널 참여 | `ho:channelParticipant` (Channel→Role) | 채널 쪽에서 표현됨 |
| model 선언 없음 | — | 소스에 정보가 없음(§1I). `mc-*`는 판단 배정 |
| `general-purpose` type 100/100 | — | **정보량 0의 상수** → 표현 불요(명시적 수용 사유) |

### 2B. GAP — Role (총 12건: ① 5 · ② 4 · ③ 3)

| # | 관측 원형 | 규모 | 분류 | 판단 근거 |
|---|---|---|---|---|
| R1 | **analyst** (평가·진단하고 발견을 severity와 함께 보고) | 78 agents / 64 harness | **①** | 중앙 Role 8개 중 대응 없음. `role-research`는 *수집*, `role-vnv`는 *하네스 산출물 판정*이라 둘 다 다르다 |
| R2 | **author/writer** (발견을 구조화된 문서로 *생산*) | 63 / 51 | **①** | `role-synthesizer`는 "terminal convergence gate"(판정+통합)로 정의됨. 코퍼스 writer는 게이트가 아니라 **생산자**다(파일럿이 `role-copywriter`·`role-prd-writer`를 로컬 저작한 이유) |
| R3 | **implementer** (사양을 실제 산출물로 구현) | 74 / 46 | **①** | `role-developer`의 definition이 **"authors the ontology nodes (abox individuals) assigned in a brief"** — 이 repo 전용이라 중립이 아니다. ⚠️ definition 수정은 `h-multiagent`의 CLAUDE.md byte-id를 깨므로 **수정 대신 중립 sibling 신설**을 권고 |
| R4 | **planner** (계획·일정·로드맵을 산출하는 *워커*) | 50 / 44 | **①** | `role-orchestrator`는 "user-facing planner … performs no substantive work itself". 코퍼스 planner/manager는 산출물을 만드는 워커라 반대다 |
| R5 | **strategist-advisor** (선택지·권고를 제시) | 30 / 26 | **①** | 대응 없음. Business/Legal/Edu 카테고리 전반에 재발 |
| R6 | reviewer-qa | 80 / 68 | **②** | `role-synthesizer`(통합형)와 `role-vnv`(판정형)가 두 변종을 이미 덮는다. altLabel 후보: "cross-validator", "quality reviewer" |
| R7 | designer | 44 / 43 | **②** | `role-design`으로 충족하되 definition이 "system/architecture design"에 치우쳐 있다. 시각·교안 designer까지 포괄하려면 altLabel 추가 권고 |
| R8 | modeler-calculator | 11 / 11 | **②** | R1(analyst)에 altLabel로 흡수 |
| R9 | data-preparer / optimizer-tuner | 11 / 10 | **②** | R1·R3에 흡수. 독립 개체로 만들면 근사 동의어 drift |
| R10 | tester-simulator | 9 / 7 | **①(낮음)** | 산출물이 *테스트 케이스/시뮬레이션*이라 판정형과 다르다. 다만 규모가 작아 우선순위 낮음 — orchestrator 판단 |
| R11 | specialist-domain (`tos-specialist`, `privacy-specialist` …) | 11 / 9 | **③** | part-taxonomy §2가 이미 "Domain-Specialist 슬롯만 recipe-side"로 결론 |
| R12 | transformer-localizer, `adr-author` 등 잔여 | 4 / 2 | **③** | 1~2 harness 특수 |

> **실증 근거**: 파일럿 5개는 **로컬 Role 21개를 저작하고 중앙 Role은 `role-synthesizer` 1개만
> 재사용**했다(`21-code-reviewer`: style-inspector/security-analyst/performance-analyst/
> architecture-reviewer — 4개 모두 R1 analyst·R6 reviewer 원형). 35 recipe로 확장하면 로컬 Role은
> **약 140개**가 되며 그 대부분이 위 5개 원형의 도메인 변형이다. 이것이 R1~R5 승격의 정량 근거다.

### 2C. GAP — Guardrail (총 8건: ① 4 · ② 3 · ③ 1)

| # | 관측 규율 | 규모 | 분류 | 판단 근거 |
|---|---|---|---|---|
| G1 | **cross-validation + severity triage** — 리뷰어가 전 deliverable을 교차검증하고 🔴/🟡/🟢로 표기, 🔴만 강제 재작업 | 68/100 (severity 64/100) | **①** | 중앙 최근접은 `gr-discriminating-eval`인데 그건 *baseline differential* 평가법이라 다른 규율. `gr-bounded-iteration`은 루프 횟수만 다룬다 |
| G2 | **declared communication routes** — 각 role이 자기 outbound hand-off 상대를 명시 선언 | 469/489 agent, 1818 route | **①** | `chan-peer`는 *매체*, `ho:channelParticipant`는 *엔드포인트 집합*. "각 역할이 자기 라우트를 선언한다"는 **정책**을 담는 Guardrail이 없다 |
| G3 | **sequenced workspace artifact naming** — `{NN}_{type}.{ext}` 서수 접두사 | 419/432 path (97%) | **①** | `gr-absolute-paths`는 절대/상대 경로 규율로 다른 축. 이 규약이 있어야 producer→consumer 해소가 결정적이 된다 |
| G4 | **three-flow acceptance coverage** — 모든 하네스가 normal/existing-input/error 3 fixture를 갖춘다 | 90/100 (정확히 3개) | **①** | TBox `scenarioKind` 값은 있으나 "세 종류를 모두 갖춰라"는 정책 노드가 없다. `gr-structural-coverage`는 소스→표현 매핑 규율이라 다르다 |
| G5 | parallel-first scheduling (독립 태스크 병렬, 선언된 의존만 직렬) | 91/100 DAG, 65/100 명시 | **②** | `gr-bottleneck-avoidance`("Do not funnel every hand-off through a single coordinator when the work is parallelisable")가 이미 덮는다 → altLabel "parallel-first" 추가로 충분 |
| G6 | assumption & limitation disclosure | 110 agent / 57 harness | **②** | `gr-grounding`("link every derived artifact to its grounding decision")의 확장 해석으로 흡수 가능. 독립 노드는 근사 동의어 위험 |
| G7 | no fabrication / flag unverified (`[Verification Required]`) | 12 agent / 9 harness | **②** | `gr-cite`+`gr-grounding`에 흡수. 규모도 작다 |
| G8 | compliance/regulatory · security · accessibility · localization 원칙 문장 | 각 15~25/100 | **③** | **도메인 내용**이다("GDPR 준수", "WCAG 충족"). 중립 추상("지배 표준에 정렬하고 조항을 인용하라")은 만들 수 있으나 **소비자가 없으므로 YAGNI**(ONTOLOGYSTYLE §1c 권장). recipe-local 권고 |

### 2D. GAP — 그 밖의 클래스

| # | 관측값 | 규모 | 분류 | 판단 |
|---|---|---|---|---|
| D1 | **FailurePolicy 원형 5종** (agent-failure-retry 91 / insufficient-input 64 / review-critical-rework 52 / source-unavailable 49 / conflict-contradiction 25) | — | **①** | 중앙 FailurePolicy는 `fp-dispatch-timeout`·`fp-validation-fail` 2개뿐이고 둘 다 **이 repo의 방법론 전용**이다. 위 5종은 도메인 무관하게 재발 → 중립 승격 대상. ⚠️ `ho:hasFailurePolicy`는 Harness 직결이라 **host harness 배선 필수**이며, `h-multiagent`에 물리면 그 CLAUDE.md가 변한다(기존 학습: byte-id) → **중립 host 선택은 orchestrator 결정** |
| D2 | **Deliverable 원형 3종** (input-brief `00_input.md` / 중간 워커 산출물 / review-report) | 100·100·26 | **①(중간)** | 중앙 Deliverable 2개(`dlv-dispatch-brief`·`dlv-verified-result`)는 방법론 전용. ⚠️ Deliverable은 `stepProduces`로만 도달하므로 **workflow step에 물려야** 하고, `wf-multiagent` 손대면 `h-multiagent` CLAUDE.md/MANIFEST가 변한다 → 신중 |
| D3 | **PromptSection 원형 5종** (responsibilities / principles / output-format / comm-protocol / error-handling) | 441~489/489 | **①(중간)** | part-taxonomy §6의 "agent-file Role 템플릿" 중앙 후보에 해당. 다만 recipe에서 persona 본문은 외부 `artifactTemplate` 참조라 **분해가 중복일 수 있다** → 소비자 유무를 orchestrator가 판단 |
| D4 | **Concept 태그** — cross-validation, task-DAG/data-flow, deliverable-artifact, trigger-boundary, skill type-archetype(calculator-engine / framework-methodology / pattern-template-catalog / knowledge-reference-base / visualization-reporting) | — | **①(낮음)** | 중앙 Concept 35개에 대응 없음. G1·G4 신설 시 짝 Concept는 **필수**(Guardrail은 `ho:tagged`로 Concept를 가리키는 것이 기존 관용). skill archetype 5종은 part-taxonomy §6이 "중립 라이브러리는 type-archetype을 담아야" 라고 권고한 지점 |
| D5 | **TestScenario 인스턴스** (270 prompt) | — | **③** | prompt/expected는 하네스별 내용 → recipe-local. 값 **종류**는 TBox가 이미 덮음 |
| D6 | **extending skill 인스턴스** 209종 | — | **③** | 재사용률 ≈0 (2회 6종, 3회 0). part-taxonomy §3 결론 재확인 |
| D7 | **scale mode 라벨** (`analysis mode`, `budget mode` …) | ~100종 | **③** | 도메인 값. 단 `full pipeline`(86)·`review mode`(36)는 중립 → **②**로 `gr-scale-modes`의 altLabel/definition 예시에 흡수 가능 |
| D8 | **Task 100종** | — | **③** | 하네스별 use-case. 중앙 Task 6개와 겹치는 것은 `task-codereview`(21) 정도 |
| D9 | **Domain 10 카테고리** | — | **판단 보류 → §4** | D1(도메인 정책) 결정 사항. 수치는 §4 |

### 2E. TBox 확장 후보 (담을 어휘 범주 자체가 없는 것) — **1건**

**T1. Scale mode를 1급 값으로 담을 클래스가 없다.**

- 관측: "요청 패턴 → 실행 모드 → 활성 role 부분집합" 표가 **95/100**, 모드 5~7개.
- 중앙에 있는 것: `gr-scale-modes`(정책 문장) + `c-scale-modes`(개념). **개별 모드**(이름 + 트리거
  패턴 + 활성 role 집합)를 담을 그릇은 없다.
- `ho:ExecutionMode`는 **쓸 수 없다** — 그 definition이 "runtime coordination topology … ORTHOGONAL
  to ho:DesignPattern"으로 못박혀 있고, 코퍼스의 모든 모드는 topology가 동일한 `agent-teams`다.
  여기에 `mode-review-only` 같은 개체를 넣으면 두 축을 conflate하는 drift다.
- **기존 어휘로의 우회는 가능하지만 무리다**: 모드마다 `ho:Workflow`를 하나씩 만들고 각 step에
  `stepByRole`로 부분집합을 표현할 수 있다. 그러나 (a) recipe당 workflow 5~7개(35 recipe면 200개
  내외)로 비대해지고, (b) "어떤 요청 패턴이 이 모드를 켜는가"를 담을 술어가 없다
  (`ho:triggerPhrase`는 Harness+Instruction 전용으로 definition에 명시됨).
- **따라서 발명하지 않고 보고한다.** 선택지는 셋: (i) `ho:ScaleMode` 클래스 + `hasScaleMode` +
  `modeActiveRole` 신설, (ii) `ho:triggerPhrase`의 적용 범위를 Workflow까지 확장, (iii) 표현하지
  않고 **명시적 수용 사유**("scale mode는 실행시 정책이며 `gr-scale-modes`로 충분")를 남긴다.
  → **orchestrator 결정 사항**. (CLAUDE.md step 7 coverage-audit 기준상 (iii)도 적법한 결론이지만,
  95/100 재발하는 harness-구조 요소이므로 조용히 넘기면 안 되는 항목이다.)

**T1 외에 TBox 확장이 필요한 축은 없다** — 나머지 관측값은 전부 기존 클래스·술어로 담긴다.

### 2F. GAP 요약

| 분류 | 건수 | 내역 |
|---|---|---|
| **①** 신규 개체 필요 | **17** | Role 6(R1~R5, R10) · Guardrail 4(G1~G4) · FailurePolicy 5(D1) · Deliverable 1군(D2) · PromptSection 1군(D3) — 여기에 짝 Concept D4가 동반 |
| **②** 기존 개체로 흡수(altLabel/정의 예시) | **8** | R6~R9(4) · G5~G7(3) · D7(1) |
| **③** 중앙 금지(recipe-local) | **7** | R11·R12 · G8 · D5·D6·D7(도메인 라벨)·D8 |
| **TBox 확장 후보** | **1** | T1 scale mode |

> ①을 개체 수로 환산하면 대략 **Role 6 + Guardrail 4 + Concept 4~9 + FailurePolicy 5 + Deliverable 3
> + PromptSection 5 ≈ 27~32 individuals**. 중앙 206 → 233~238 규모. (추정)

---

## 3. 대표 30~40 선정안 (coverage-driven)

### 3a. 세 개의 값 우주(universe)

선정을 정직하게 평가하려면 "무엇을 커버하는가"를 먼저 고정해야 한다. 실측으로 세 우주를 세었다.

| 우주 | 정의 | 크기 | 성격 |
|---|---|---|---|
| **U1 구조·중립값** | §1의 정규화된 구조 속성값 전체 (role 원형 14 · tool slice 6 · skill archetype 7 · 원칙 테마 18 · failure 원형 7 · artifact 클래스 10 · 섹션 시그널 8 · 팀규모 2 · extending skill 수 2 · data-transfer 2 · 카테고리 10) | **85** | **중앙 라이브러리가 담아야 할 축** |
| **U2 role 이름 어휘** | agent 이름 마지막 토큰 | **102** | 원형과 도메인의 중간층 |
| **U3 extending skill 인스턴스** | extending skill 디렉토리명 | **209** | **순수 recipe-local payload** |

### 3b. 선정 알고리즘 (재현 가능)

1. 파일럿 5개를 **강제 포함**(`21`·`16`·`31`·`03`·`46`).
2. 카테고리 비례 쿼터: cat01 5 · cat02 5 · cat03 4 · cat04 5 · cat05 3 · cat06 3 · cat07 3 ·
   cat08 3 · cat09 2 · cat10 2 = **35** (코퍼스 카테고리 분포에 비례).
3. 쿼터 안에서 greedy set-cover, 점수 = `3×|new U1| + 2×|new U2| + 1×|new U3|`.
   동점은 하네스 번호 오름차순으로 결정적 tie-break.

### 3c. 선정 결과 — 35 recipe

```
cat01 Content     02-podcast-studio  03-newsletter-engine*  07-comic-creator
                  09-documentary-research  14-translation-localization
cat02 SwDev       16-fullstack-webapp*  17-mobile-app-builder  18-api-designer
                  21-code-reviewer*  28-security-audit
cat03 Data/ML     31-ml-experiment*  32-data-analysis  33-text-processor
                  35-api-client-generator
cat04 Business    43-startup-launcher  46-product-manager*  48-sales-enablement
                  51-investor-report  55-rfp-responder
cat05 Education   56-language-tutor  60-debate-simulator  62-adr-writer
cat06 Legal       69-privacy-engineer  70-legal-research  72-regulatory-filing
cat07 Lifestyle   73-meal-planner  74-fitness-program  75-tax-calculator
cat08 Comms/Docs  81-technical-writer  82-report-generator  87-crisis-communication
cat09 Operations  90-hiring-pipeline  95-procurement-docs
cat10 Specialized 96-real-estate-analyst  100-ip-portfolio
```
`*` = 기존 파일럿.

### 3d. 커버리지 (실측)

| 선정 규모 | U1 구조값 | U2 role 이름 | U3 skill 인스턴스 |
|---|---|---|---|
| 파일럿 5 | 66/85 = **77.6%** | 15/102 = 14.7% | 12/209 = 5.7% |
| 11 (카테고리 1개씩) | 80/85 = 94.1% | 36.3% | 12.0% |
| **29** | **85/85 = 100.0%** | 75.5% | 31.6% |
| **35 (제안)** | **85/85 = 100.0%** | **82/102 = 80.4%** | 78/209 = **37.3%** |

증분 로그(주요 구간):

```
 6 +75-tax-calculator          U1gain=5  U1=83.5%
 7 +56-language-tutor          U1gain=3  U1=87.1%
 8 +09-documentary-research    U1gain=2  U1=89.4%   (유일한 file+msg+web slice)
 9 +90-hiring-pipeline         U1gain=2  U1=91.8%
12 +14-translation-localization U1gain=1 U1=95.3%   (유일한 transformer-localizer 원형)
13 +62-adr-writer              U1gain=1  U1=96.5%   (유일한 미분류 role)
15 +81-technical-writer        U1gain=1  U1=97.6%
17 +100-ip-portfolio           U1gain=1  U1=98.8%
29 +69-privacy-engineer        U1gain=1  U1=100.0%  (코드펜스 보유 2개 중 하나)
30~35                          U1gain=0  → U2/U3만 증가
```

**희소값 전수 포함 확인**(U1에서 ≤2 harness에만 나타나는 값 5종): `file+msg+web`(09) ·
`no-signal`(16) · `code+file`(69, 98) · `transformer-localizer`(14) · `role-other`(62)
→ **5종 모두 선정 안에 포함**된다.

### 3e. 커버되지 않는 값 (= recipe 없이 중앙 어휘로만 존재할 부품)

**U1: 0건.** 35 recipe가 구조·중립 값 공간을 **100% 커버**한다.
→ D3(어휘 전수 vs 인스턴스 대표)의 핵심 주장이 실측으로 확인된다: **중앙 어휘의 완결성은
35개 예제만으로도 예시 근거를 잃지 않는다.**

**U2: 20/102 미커버** (role 이름 마지막 토큰) —
`automator · detector · diagnostician · differentiator · director · examiner · identifier · lead ·
mentor · operator · organizer · producer · profiler · prompter · proofreader · reconstructor ·
simulator · storyteller · taker · worldbuilder`.
→ 전부 §2B의 ①/② 원형(analyst·implementer·writer·coordinator)의 **도메인 변형**이다. 중앙 Role
원형이 승격되면 어휘적으로 이미 담긴다. **추가 recipe가 필요한 값은 없다**(판정).

**U3: 131/209 미커버** (extending skill 인스턴스) — 정의상 recipe-local이고 재사용률 ≈0이므로
**중앙에 담지 않는 것이 옳다**(③). 커버 안 되는 것이 결함이 아니다.

**그 밖에 recipe로는 예시되지 않지만 중앙에 있어야 하는 부품**:
- G8(compliance·security·accessibility·localization 원칙)의 도메인 인스턴스 → ③이므로 애초에 중앙 대상 아님.
- 65개 미선정 하네스의 Domain/Task 개체 → §4의 결정에 따름.
- `core:tool-retriever`·`core:pat-react`·`pat-planexec`·`mode-sub-agents`·`mode-hybrid`·`mem-*` 등은
  **코퍼스가 전혀 쓰지 않는다**(관측 0). 코퍼스 커버리지와 무관하게 중앙에 남는 부품이다.

---

## 4. D1 판단 근거 — 도메인 값의 분포·중복도 (실측)

### 4a. 기존 중앙 도메인이 덮는 범위

중앙 Domain은 4개(`dom-coding`·`dom-research`·`dom-support`·`dom-design`)이고 **넷 다
`skos:definition`이 없다**(prefLabel + altLabel + salience 뿐, `dom-design`만 `scopedFrom` 보유).
경계 판정이 label에만 의존한다는 뜻이다. 매핑 판정:

| 중앙 도메인 | 매핑되는 하네스 | 수 |
|---|---|---|
| `dom-coding` | cat02 전체(16–30) | 15 |
| `dom-research` | 09·44·58·63·70·98 | 6 |
| `dom-design` | 06·13·15·36·77 | 5 |
| `dom-support` | 49 (·93 경계) | 1~2 |
| **합계** | | **27~28 / 100** |

→ **72~73/100 하네스는 중앙에 대응 도메인이 없다.**

### 4b. 카테고리 값의 중복도

| 정책 | 35 recipe에서 저작될 Domain 개체 수 | 서로 다른 개념 수 | 중복 배수 |
|---|---|---|---|
| recipe-local 유지 | **30** (cat02 5개만 `core:dom-coding` 재사용) | 9 (cat02 제외 9 카테고리) | **3.3×** |
| 100 전량 임포트 가정 | 85 | 9 | **9.4×** |
| 카테고리 9개 중앙 승격 | **0** | 9 | 1× |

### 4c. 파일럿의 실제 선택 (실증)

| recipe | targetsDomain | 카테고리 | 관계 |
|---|---|---|---|
| 16-fullstack-webapp | `core:dom-coding` | cat02 | 중앙 재사용 ✓ |
| 21-code-reviewer | `core:dom-coding` | cat02 | 중앙 재사용 ✓ |
| 03-newsletter-engine | `id:dom-content` "Content production" | cat01 | 카테고리와 **1:1** |
| 31-ml-experiment | `id:dom-ml` "Machine-learning experimentation" | cat03 | 카테고리와 **1:1** |
| 46-product-manager | `id:dom-product` "Product management" | cat04 | 카테고리의 **부분집합** |

→ 5개 중 **2개는 이미 중앙 재사용**, 3개는 로컬 저작했고 그중 2개는 카테고리와 정확히 1:1이다.
카테고리 granularity가 실제 저작 선택과 대체로 맞는다(46만 더 좁음).

### 4d. developer 소견 (결정은 orchestrator)

- **중복 3.3×는 이 repo가 막으려는 drift의 정의에 부합한다** — `dom-content`라는 사실상 동일한
  개념이 5개 recipe 네임스페이스에 독립 저작되면, per-recipe closure 검증에서는 prefLabel 중복
  검사가 걸리지 않아 **조용히** 다섯 갈래로 갈라진다.
- 승격 비용은 낮지만 **0은 아니다**(실측): `ho:Domain`을 target으로 하는 SHACL shape는 **없다**
  (`EnvironmentSpace stays shape-free … like a Domain`). 그러나 `HO.Domain`은
  `tools/ontology_lib.py`의 `INSTANCE_CLASSES`에 등록돼 있어 **전역 reachability BFS의 대상**이다
  → 중앙에 새 Domain을 놓으면 같은 변경 안에서 **누군가가 `targetsDomain`(또는 `describesDomain`/
  `scopedFrom`)으로 가리켜야** 한다. 중앙에는 그 도메인을 겨냥한 하네스가 없으므로, 이전에
  `chan-*`·`gr-*`를 승격할 때 쓴 **중립 host harness 패턴**(`h-workspace-synthesis`·`h-peer-mesh`)이
  다시 필요하다. `ho:HarnessShape`는 `targetsDomain` **최소 1개**만 요구하므로 host 1개가 9 도메인을
  동시에 겨냥해도 통과한다(판정 — 실검증은 vnv 소관).
- 반대 논거: `dom-product`(46)처럼 카테고리보다 좁은 선택이 실제로 나왔다 → 카테고리 승격이
  **모든** recipe의 필요를 덮지는 않는다. 혼합안(카테고리 9개 중앙 + 필요 시 recipe-local 세분)이
  중복도(3.3→1×)와 표현력을 동시에 취한다 — **이것이 수치가 가리키는 방향이다**(판정, 결정 아님).

---

## 5. 계획 수정이 필요한 발견 (놀라운 점)

1. **U1 커버리지는 15개에서 이미 포화한다.** 카테고리 쿼터 없이 파일럿 5개에서 순수 greedy로
   돌리면 **15 recipe에서 U1 100%**에 도달한다(실측 경로: `+75 +56 +09 +69 +90 +14 +25 +62 +81 +96`).
   16번째부터 구조 증분이 0이다. 즉 "30~40"의 근거는
   *구조 커버리지*가 아니라 **카테고리 대표성·도메인 어휘 예시**다. 계획 §5의 "변이 span" 표현을
   이 수치로 교정하는 것이 정직하다.

2. **실행 topology 축의 변이가 0이다.** 코퍼스 100/100이 `Agent Team`이고 sub-agents/hybrid는
   **한 건도 없다**. 계획이 "topology 판별 근거"를 wave 게이트에 넣는다면 판별할 것이 없다 —
   전 recipe가 `core:mode-agent-teams` 단일 값이다. 반대로 `mode-sub-agents`/`mode-hybrid`는
   이 코퍼스로는 **검증되지 않는다**.

3. **파일럿 5개가 이미 land된 recipe들에 `hasExecutionMode`·TestScenario·FailurePolicy가 하나도
   없다**(실측: 8 recipe 전체에서 `hasExecutionMode` 0건, `a ho:TestScenario` 0건,
   `a ho:FailurePolicy` 0건). 그런데 소스는 셋 다 **거의 전수 제공**한다(Agent Team 100/100,
   3-flow scenario 90/100, error 표 95/100). 이는 **어휘 GAP이 아니라 바인딩 누락**이며,
   CLAUDE.md step 7 coverage-audit 기준으로는 **기존 파일럿 5개도 아직 GAP 상태**다.
   → 95개를 임포트하기 전에 **파일럿 5개의 coverage-audit 재실행**을 계획에 넣기를 권고한다.
   (importer가 이 세 축을 기계적으로 채울 수 있는지도 Phase 1 수용시험 항목으로.)

4. **코퍼스는 코드가 아니라 문서를 만든다.** 산출물 `.md` 99/100, agent 파일에 code fence 2/100,
   `Bash` 언급 0/100. 따라서 `tool-shell`/`cap-codeexec` 바인딩은 대부분 recipe에서 **부적절**하다
   (파일럿 중 `16`·`21`·`31`이 `core:tool-shell`을 걸었는데, 소스 근거는 약하다 — 재검토 권고).

5. **tool scope 변이가 이진이다.** 계획·roadmap이 "role별 상이 tool scope"를 파일럿 16번의 선정
   근거로 삼았지만, 코퍼스 전체에서 slice는 `file` / `file+web`의 둘이 지배적(427/489)이다.
   least-privilege 시연 가치는 여전하지만 **대표성 근거로는 약하다**.

6. **agent 파일에 `tools:`도 `model:`도 없다.** 즉 roadmap §1 매핑 표의 "tool 사용 → `roleTool`"은
   **소스 데이터가 아니라 추론**이다. importer의 SHOULD(결정적) 영역이 아니라 MUST NOT(판단성)
   영역에 가깝다 — Phase 1 계약 문구 조정 권고.

7. **`role-developer`의 definition이 이 repo 전용이다**("authors the ontology nodes (abox
   individuals) assigned in a brief"). 중립 부품 라이브러리에 도메인 특정 정의가 들어가 있는
   사례다. 다만 이미 `h-multiagent`에 바인딩돼 있어 **definition 수정은 CLAUDE.md byte-id를
   깬다** → 수정이 아니라 중립 sibling 신설로 처리할 것을 권고(§2B R3).

8. **번역 품질이 파싱을 오염시킨다.** 영문판 헤딩이 13종까지 변형되고(`data before as`,
   `inthisbefore setup` 등) 10/100은 Test Scenarios 헤딩이 파손됐다. importer는 **헤딩 문자열
   기반 파싱을 하면 안 되고** 표 헤더·본문 시그널을 써야 한다. 이 인벤토리의 모든 수치도 그렇게 냈다.
