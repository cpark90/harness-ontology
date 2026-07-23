# Dispatch brief — harness-100 inc3: 파일럿 5 recipe (recipe-local)

> 작성: orchestrator (2026-07-23). 실행: **developer dispatch (opus), recipe당 1건 병렬**.
> 상위 결정 앵커: `docs/feedback/harness-100-augmentation.md`(inc3, 열린결정 확정본).
> 근거: `docs/feedback/harness-100/recipe-roadmap.md §1~3,6`, 참조-모델 포맷=`staging/harness-recipes/recipes/lpranging/lpranging.ttl`.

## 0. 게이트 (선결 — 반드시 먼저)
recipe는 중앙 `core:` 부품을 **published 중앙 clone**에 federate해 검증된다. inc1/inc2의 중앙
추가분(아래 "재사용 맵")은 **아직 미커밋 pile**(HEAD=batch3 `9c24873`)이다. 따라서:
- **federation 최종검증**(README의 clone+union validate)은 **inspection이 중앙 @126을 push한 뒤** 완결된다
  (`docs/plans/inspection-brief-CONSOLIDATED-since-batch3.md`).
- 단, recipe는 **recipe-local**(신규 중앙노드 0)이므로 **저작 자체는 working-tree 중앙에 대해 지금 가능**하다.
  → 저작은 working-tree union(중앙 소스 직접 import)으로 검증하고, remote-clone federation은 push 후 재확인.

## 1. 공통 규약 (5개 recipe 전부)
### 1a. 산출물 위치·형식
- `staging/harness-recipes/recipes/<name>/<name>.ttl` + `README.md` (lpranging와 동형).
- prefix: `id: <https://harness-ontology.dev/id/<name>/>`, `owl:imports <https://harness-ontology.dev/ontology>`.
- **본문 vendor 금지**: persona body·skill body·scaffold는 `ho:artifactTemplate`/`ho:scaffold`로 **코퍼스 파일 절대경로 외부참조**만
  (materialize가 build 시 fetch, 없으면 `.ref` stub). 코퍼스 루트:
  `/tmp/claude-1000/-home-cpark-git-harness-ontology/528b6512-abe6-402f-93d1-ad04a227d50b/scratchpad/harness-100/en/<harness>/`.
  ⚠ 이 절대경로는 임시 scratchpad다 — recipe에 박기 전 orchestrator에게 **영속 소스 경로 확정**을 확인할 것(미확정이면 브리프 경로 그대로 두고 flag).
- **attribution**(열린결정6): 각 harness 노드에 `dct:source "<코퍼스 harness 상대경로>"` ·
  `dct:license "Apache-2.0"`. README 상단에 `revfactory/harness-100` 크레딧 1줄.
- **maturity**: 신규 로컬노드 `ho:maturity "draft"`. harness도 `"draft"`.
- **tokenEstimate**: 텍스트 담는 노드(persona·instruction) 전부 부여(코퍼스 파일 `wc -w` 근사).
- 언어: `skos:prefLabel`/`skos:definition`/`promptText`는 **영어**(ONTOLOGYSTYLE §1d).

### 1b. 중앙 재사용 맵 (core: IRI — 로컬 재정의 금지, 바인딩만)
| 종류 | 재사용 core: IRI |
|---|---|
| workflow | `core:wf-multiagent` |
| pattern | `core:pat-orchestrator-workers` (+ 필요시 `core:pat-peer-mesh` — 아래 1d) |
| synthesizer 역할 | `core:role-synthesizer` (QA/reviewer gate; `providesCapability core:cap-synthesis`) |
| capability | `core:cap-synthesis` (harness `requiresCapability`, role-synthesizer가 충족) + 필요한 기존 cap(`cap-fileedit`←tool-editor, `cap-codeexec`←tool-shell, `cap-orchestration`←wf-multiagent) |
| tool | `core:tool-editor`, `core:tool-shell` (least-privilege slice로 role에 배분) |
| guardrail | `core:gr-lang`(필수), `core:gr-structured-output`(엄격 artifact 포맷), `core:gr-least-privilege`, `core:gr-report-over-prompt`, `core:gr-graceful-fallback`(코퍼스 Error Handling 절), 필요시 `core:gr-scale-modes` |
| channel | `core:chan-workspace`(`_workspace/NN_*.md` handoff — 전 코퍼스 공통), `core:chan-agent-user`, 필요시 `core:chan-peer`(SendMessage mesh) |
| model | `core:mc-opus` |
| lineage | `ho:derivedFrom core:h-multiagent` |

### 1c. 로컬(id:) 저작 대상 (recipe별)
- **worker Role ×4**: 각 `id:role-<x>` — `rolePersona id:sp-role-<x>`, `roleTool`(least-privilege slice),
  `roleGuardrail`(중앙), `roleMemoryPolicy`(코퍼스에 memory 없음 → 역할에 맞게 **합성**), `tagged`, `maturity "draft"`.
- **worker persona ×4**: 각 `id:sp-role-<x>` (`ho:SystemPrompt`) — `promptText`는 짧은 중립 요약 1~2문장으로
  **직접 작성**하되, 원문 상세 body는 harness `ho:scaffold` 대신 **role md 재생성이 필요하면** `artifactTemplate` 외부참조.
  (lpranging 방식: persona는 `promptText` 보유 + materialize가 `.claude/agents/<role>.md`로 렌더. 코퍼스 원문 agent md를
  충실 재현하려면 `sp-role-<x>`에 `ho:artifactTemplate "<코퍼스 agents/<x>.md>"` 추가 — 본문 fetch용.)
- **orchestrator persona ×1**: `id:sp-<name>` — harness 최상위 persona(도메인 명시). `promptText` 직접 작성.
- **Instruction(skill) ×3~4**: 각 `id:ins-<skill>` (`ho:Instruction`) — `skos:notation "<skill dir name>"`(슬래시 트리거),
  `skos:definition`(요약), `ho:artifactTemplate "<코퍼스 skills/<skill>/skill.md>"`(본문 외부참조), `tokenEstimate`.
  - orchestrator skill(harness명과 동일, 예 `code-reviewer`)은 workflow=composition spec.
  - **extending skill**(특정 agent 확장, 예 `vulnerability-patterns`→security-analyst): **GAP-5 `augmentsRole` 미도입**이므로
    당장은 harness-level `hasInstruction` 바인딩 + `skos:definition`에 **타깃 agent를 명시**해 기록(로드맵 §1). GAP-5는 파일럿이 요구하면 별도 TBox inc.
- **Domain / Concept**: 아래 recipe별 표 참조. **기존 중앙 도메인이 맞으면 재사용**, 신규는 recipe-local(`id:`), scheme는
  `core:scheme`에 `skos:topConceptOf`/`skos:broader`로 접붙여 orphan 금지. **신규 도메인 concept는 Golden Rule #2** — 로컬로만.
- **harness ×1**: `id:h-<name>` — 위 전부 조립. `hasSystemPrompt`(persona 전부), `usesTool`, `hasWorkflow`,
  `hasGuardrail`, `usesModel`, `hasInstruction`, `hasRole`(worker 4 + `core:role-synthesizer`), `hasChannel`,
  `appliesPattern`, `requiresCapability`, `derivedFrom core:h-multiagent`, `targetsDomain`, `addressesTask`, `tagged`,
  `dct:source`/`dct:license`, `maturity "draft"`. **모든 `requiresCapability`는 바인딩 컴포넌트가 `providesCapability`로 충족**(HarnessShape).

### 1d. coordination (열린결정1 = pluggable, both)
코퍼스는 analyst 간 **SendMessage peer-mesh** + review-synthesizer **convergence gate**다. 파일럿 기본은
`core:pat-orchestrator-workers`(orchestrator+workers+terminal gate). analyst 간 직접 메시지가 원문에 뚜렷하면
`core:pat-peer-mesh` **함께 바인딩** + `core:chan-peer` 추가(예: 21-code-reviewer의 "Team Communication Protocol··· via SendMessage").
gate/handoff는 `core:chan-workspace`가 담는다.

### 1e. 검증 (developer가 저작 후 자기검증 → vnv 최종판정)
1. **working-tree union validate** (remote clone 대신 로컬 중앙 소스로 federate):
   ```bash
   cd /home/cpark/git/harness_ontology
   HARNESS_CATALOG=staging/harness-recipes/catalog-v001.xml \
   HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<name> \
   /usr/bin/python3 tools/validate.py     # PASS 기대 (중앙+이 recipe closure 1개)
   ```
   (catalog에 recipe `<uri>` 라인 없으면 추가. **per-recipe closure 1개씩만** — 절대 all-recipes union 금지, roadmap §5.)
2. **materialize round-trip**: `materialize.py h-<name>` → `.claude/agents/<role>.md`(5) · `.claude/skills/<skill>/`(3~4) ·
   `CLAUDE.md` emit, 외부 ref resolve 또는 `.ref` stub 확인.
3. **retrieve sanity**: 신규 harness가 관련 요청에 gap 없이 후보로 뜨는지(prefLabel/definition distinctive, roadmap §5).
- developer는 1~2를 자기검증하고 결과를 브리프에 append. **최종 PASS 판정·retrieve 재검색은 vnv dispatch**(`docs/verify/`).

## 2. Recipe별 노드 명세

### 2a. `21-code-reviewer` (1순위 — 최고 재사용·skill→agent gap 시험) ★ 완전전개(템플릿)
- **domain/task**: 재사용 `core:dom-coding` + `core:task-codereview` (신규 0).
- **local concept ×2**: `id:c-security-review`(`skos:broader` 코딩계열 or `topConceptOf core:scheme`),
  `id:c-code-quality`. (OWASP·refactoring 계열 태그용.)
- **worker Role ×4** (+ reused `core:role-synthesizer` = review-synthesizer QA gate):
  | role | persona sp- | roleTool (slice) | 비고 |
  |---|---|---|---|
  | `id:role-style-inspector` | `id:sp-role-style-inspector` | `core:tool-editor` (read/write review) | 스타일·네이밍·가독성 |
  | `id:role-security-analyst` | `id:sp-role-security-analyst` | `core:tool-editor`, `core:tool-shell` | OWASP Top10; ins-vulnerability-patterns 타깃 |
  | `id:role-performance-analyst` | `id:sp-role-performance-analyst` | `core:tool-editor`, `core:tool-shell` | 복잡도·메모리·쿼리 |
  | `id:role-architecture-reviewer` | `id:sp-role-architecture-reviewer` | `core:tool-editor` | SOLID·결합도; ins-refactoring-catalog 타깃 |
  - synthesizer: **`core:role-synthesizer` 재사용**(별도 로컬 role 저작 안 함 — promote-once 실증). 코퍼스 review-synthesizer의
    최종판정 로직은 `core:role-synthesizer` 정의로 충족. (도메인 persona 필요성 낮음 — 재사용으로 gap 시험.)
- **Instruction ×3**:
  | ins | notation | artifactTemplate (외부) | 타깃 |
  |---|---|---|---|
  | `id:ins-code-reviewer` | `code-reviewer` | `.../skills/code-reviewer/skill.md` | orchestrator(팀 조율·워크플로) |
  | `id:ins-vulnerability-patterns` | `vulnerability-patterns` | `.../skills/vulnerability-patterns/skill.md` | **extending → security-analyst**(definition에 명시) |
  | `id:ins-refactoring-catalog` | `refactoring-catalog` | `.../skills/refactoring-catalog/skill.md` | **extending → architecture/performance**(definition 명시) |
- **coordination**: `core:pat-orchestrator-workers` + `core:pat-peer-mesh`(analyst SendMessage mesh 명시적) ;
  channel `core:chan-workspace`(`_workspace/00~05_*.md`) + `core:chan-peer` + `core:chan-agent-user`.
- **guardrail**: `core:gr-lang`, `core:gr-structured-output`(엄격 artifact 포맷), `core:gr-least-privilege`,
  `core:gr-report-over-prompt`, `core:gr-graceful-fallback`(Error Handling 절).
- **capability**: `requiresCapability core:cap-fileedit, core:cap-codeexec, core:cap-orchestration, core:cap-synthesis`.
- **harness** `id:h-code-reviewer`: 위 조립. `dct:source ".../en/21-code-reviewer"`, `dct:license "Apache-2.0"`.
- 예상 로컬노드: harness1 + role4 + persona5(sp-<name> + sp-role×4) + concept2 + instruction3 ≈ **15**.

### 2b. `16-fullstack-webapp` (role별 상이 tool scope 시험)
- agents: architect · frontend-dev · backend-dev · devops-engineer · **qa-engineer**(→ `core:role-synthesizer` 재사용? qa-engineer는
  QA gate 성격 → 재사용 검토; 파이프라인 성격이 강하면 로컬 `id:role-qa-engineer`). **판단은 developer가 원문 보고**, 애매하면 flag.
- skills(3): `fullstack-webapp`(orch) · `api-security-checklist`(→backend/devops ext) · `component-patterns`(→frontend ext).
- domain: 재사용 `core:dom-coding` + `core:task-architecture`; 로컬 concept(web/api/deploy) 2~3.
- **핵심 변이**: 4 worker의 tool scope가 상이 — frontend/backend(editor), devops(shell 강함), architect(editor). least-privilege slice를 role별로 다르게.

### 2c. `31-ml-experiment` (4-skill 변이 + 신규 도메인)
- agents: data-engineer · model-designer · training-manager · evaluation-analyst · **experiment-reviewer**(QA gate → `core:role-synthesizer` 재사용 검토).
- skills(4): `ml-experiment`(orch) · `feature-engineering-cookbook` · `model-selection-guide` · `experiment-tracking-setup`(각 extending 타깃 기록).
- domain: **신규 로컬** `id:dom-ml`("Machine-learning experimentation") — `core:dom-research`와 구별(실험 lifecycle ≠ 문헌조사). 로컬 concept(feature/model/eval) 3.
- task: 로컬 `id:task-mlexperiment` 또는 재사용 `core:task-architecture` — developer 판단, 신규면 recipe-local.

### 2d. `03-newsletter-engine` (content — 신규 로컬 도메인)
- agents: curator · analyst · copywriter · editor-in-chief · **quality-reviewer**(QA gate → `core:role-synthesizer` 재사용 검토).
- skills(4): `newsletter-engine`(orch) · `email-copywriting` · `audience-segmentation` · `deliverability-optimization`.
- domain: **신규 로컬** `id:dom-content`("Content/newsletter production"). 로컬 concept(curation/copywriting/deliverability) 3.
- 파이프라인(curation→writing→A/B→send) — `core:pat-orchestrator-workers` 기본, peer-mesh는 원문에 약하면 생략.

### 2e. `46-product-manager` (4-agent 변이·프레임워크 로컬 concept)
- agents: strategist · prd-writer · story-writer · sprint-planner · **pm-reviewer**(QA gate → `core:role-synthesizer` 재사용 검토).
- skills(3): `product-manager`(orch) · `rice-prioritizer` · `story-point-estimator`.
- domain: **신규 로컬** `id:dom-product`("Product management"). 로컬 concept(roadmap/PRD/RICE/story-point) 3~4 — PM 프레임워크 용어.

## 3. Dispatch 계획 (orchestrator)
- **recipe 5개 = 독립**(recipe-local, 공유 신규 중앙노드 0) → **developer 5 dispatch 병렬 가능**. 단 2a를 **먼저 1건**
  실행해 템플릿·검증파이프(1e)를 확정한 뒤 2b~2e를 병렬로 여는 것을 권장(파일럿 취지=템플릿 검증).
- 각 dispatch에 넘길 것: 이 브리프의 §1 전체 + 해당 recipe §2 항목 + lpranging.ttl 포맷 예시.
- developer 산출: `<name>.ttl` + `README.md` + 자기검증(1e-1,2) 결과. **git·중앙 push 안 함**.
- **vnv dispatch**: 5 recipe 각 per-recipe closure PASS + materialize round-trip + retrieve sanity 판정 → `docs/verify/inc3-pilot5-*.md`.
- **inspection(별도 세션)**: vnv green 후 recipes repo push(각 recipe federate against pushed 중앙 @126) + attribution NOTICE.

## 4. 완료 정의 (inc3)
5 recipe 전부: (1) per-recipe closure validate PASS(remote clone), (2) materialize round-trip green(ref resolve/stub),
(3) retrieve sanity(gap 없이 후보). → 통과 시 **importer(inc4)** 착수 재평가(열린결정5: 파일럿 후 batch 범위 결정).
