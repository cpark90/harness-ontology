# 후보 repo 인벤토리 (실측)

조사: inspection, 2026-07-25. 수치는 **GitHub API 실측**(`gh api repos/<r>`), 구조는 README 판독.
**한계**: 파일 단위 전수 정독은 하지 않았다 — 아래 "수확 추정"은 README·디렉토리 구조 기반 추정이며,
채택 wave에서 실제 파일을 열어 확정해야 한다.

| repo | license (실측) | stars | size | last push | 내용 | 온톨로지 수확 추정 |
|---|---|---|---|---|---|---|
| `ai-boost/awesome-harness-engineering` | **CC0-1.0** | 3.2k | 433KB | 2026-07-24 | harness engineering을 하나의 분야로 정리한 큐레이션. **12 Design Primitives**(agent loop, planning/task decomposition, context delivery & compaction, tool design, skills & MCP, permissions & authorization, memory & state, task runners & orchestration, verification & CI, observability & tracing, debugging & DX, human-in-the-loop) + evals/security/templates | `ho:Concept`·`ho:Capability` **커버리지 대조표**. 부품이 아니라 **축의 목록** — 우리 taxonomy에 빠진 축(observability, permissions, compaction)을 찾는 데 최적 |
| `wshobson/agents` | **MIT** | 38.2k | 5.6MB | 2026-07-22 | 203 agents · 175 skills · 109 commands · **16 orchestrators**(multi-agent coordination workflows) · 94 plugins. **5개 플랫폼용 harness-native 산출**(Claude Code, Codex, Cursor, OpenCode, Gemini CLI) | `ho:Role` 원형·`ho:Instruction`(skill)·`ho:Workflow`. **16 orchestrator = `ho:DesignPattern`/`ho:ExecutionMode` 증거의 최대 광맥**. 다중 타깃 emit은 `materialize` 확장 근거 |
| `VoltAgent/awesome-claude-code-subagents` | **MIT** | 23.7k | 811KB | 2026-07-10 | 154+ subagent, 10 카테고리. 파일당 frontmatter(`name`/`description`/`tools`/`model`) + body(role·checklist·**communication protocol**·workflow) | `ho:Role`(+`roleTool`·`rolePersona`) 원형. frontmatter가 **우리 role 모델과 거의 1:1** — `tools`→`roleTool`, `model`→`usesModel`. "communication protocol" 절은 `ho:Channel` 증거 |
| `rohitg00/awesome-claude-code-toolkit` | **Apache-2.0** | 2.4k | 1.1MB | 2026-05-12 | 135 agents · 35 skills · 42 commands · **20 hooks**(SessionStart/UserPromptSubmit/PostToolUse/Stop) · 15 rules · 7 templates | **hooks가 핵심** — 라이프사이클 이벤트에 걸리는 실행 트리거. 우리 TBox에 이 축이 없다(§ontology-mapping GAP-H). rules→`ho:Guardrail` 보강 |
| `mattpocock/agent-rules-books` | **MIT** | 333 | 5.8MB | 2026-05-13 | Clean Code·Refactoring·DDD·Clean Architecture·DDIA에서 뽑은 AGENTS.md rule/skill 세트 | `ho:Guardrail`(현재 34개)의 **도메인 중립 확장** 후보. 단 출처가 서적이라 표현(문구) 아닌 **규칙의 취지**만 중립화해 재저작 필요 |
| `tallesborges/agentic-system-prompts` | MIT(**편찬물만**) | 180 | 166KB | 2025-08-04 | 7개 프로덕션 코딩 에이전트(Claude Code·Gemini CLI·Cline·Aider·Roo Code·Zed·Codex)의 system prompt·tool 정의 + 출처·회수일 | `ho:SystemPrompt`/`ho:PromptSection` 구조 **관찰용**. §license-gate 참조 — 본문 텍스트는 원저작자 소유라 **복사 금지, 구조만 관찰** |
| `hesreallyhim/awesome-claude-code` | **CC BY-NC-ND 4.0** | 50.8k | 34MB | 2026-07-24 | 최대 규모 큐레이션(skills·agents·statuslines·tooling·plugins) | **채택 불가** — NoDerivatives. §license-gate |
| (기 반영) `revfactory/harness` | Apache-2.0 | 8.5k | 9.3MB | 2026-07-20 | 방법론 repo | 이미 Wave A+B1 반영, P3/P4 잔여(`revfactory-harness-reflection.md`) |
| (기 반영) `revfactory/harness-100` | Apache-2.0 | 1.2k | 3.4MB | 2026-03-22 | 100 하네스 코퍼스 | pilot 5 recipe 반영, inc4 importer 잔여(`harness-100-augmentation.md`) |

## 파일 수 실측 정정 (2026-07-25, git tree API)
위 표의 개수는 README 주장치였다. `gh api repos/<r>/git/trees/main?recursive=1`로 실측한 결과:

| 소스 | README 주장 | 실측 경로 수 | **이름 기준 고유** |
|---|---|---|---|
| VoltAgent subagents | 154+ | `categories/**.md` **164** | **155** (카테고리 README 포함분 제외) |
| wshobson agents | 203 | `**/agents/**.md` **204** | **139** — 경로가 많은 것은 5개 플랫폼 디렉토리에 **같은 에이전트가 중복 배치**되기 때문 |
| wshobson skills | 175 | `**/skills/**.md` **397** | (미측정 — 같은 중복 구조로 추정) |

**두 코퍼스 합집합(이름 기준) = 253**, **교집합 = 41**(`code-reviewer`·`data-engineer`·`cloud-architect`·
`python-pro`류가 양쪽에 동명으로 존재). 즉 "350여 개"가 아니라 **고유 원형 후보는 253**이고, 그중
41은 두 소스가 같은 이름으로 각자 정의한 **병합 대상**이다. 이름에 언어·프레임워크가 박힌 것만 세도
최소 30(보수적 패턴 매칭이라 실제 도메인 특화 비율은 더 높다).

## 검색 경로 (재현용)
`"agent harness" 큐레이션` · `awesome claude code subagents/skills` · `multi-agent orchestration framework
roles channels guardrails` · `AGENTS.md / agent rules 컬렉션` 4개 축으로 검색 → 상위 결과에서 **부품이
파일 단위로 분리 저장된** repo만 후보로 남겼다(블로그·SaaS 랜딩·프레임워크 코드 제외).

## 후보에서 뺀 것과 이유
- **에이전트 프레임워크 코드**(CrewAI·AgentTeams·open-multi-agent 등): 부품이 **코드 추상**이라 텍스트
  부품으로 뽑아내는 비용 대비 수확이 낮다. 다만 `open-multi-agent`의 "coordinator가 런타임에 task DAG를
  계획" 구조와 `AgentTeams`의 Matrix room 기반 조율은 **`ho:Channel`·`ho:ExecutionMode`의 외부 반증
  사례**로 §ontology-mapping에서만 참조한다.
- **leaked system prompt 모음**(`dontriskit/awesome-ai-system-prompts` 등): 출처가 프로덕트 유출물이라
  라이선스 근거가 없다. 채택하지 않는다.
