# harness-100 코퍼스 분석 — 부품 taxonomy (neutral vs domain)

> 출처: inspection dispatch 분석(2026-07-23). 코퍼스 `revfactory/harness-100`(Apache-2.0), `en/` 100
> 하네스·489 agent·315 skill. 전 10카테고리 ~30하네스 정독 + 100개 구조 grep. 상위 제안: `../harness-100-augmentation.md`.

## 1. 템플릿 해부 (매우 균일)
각 하네스 = `.claude/` 트리 3파일종:
- `CLAUDE.md` — **얇은 overview**(Structure 87/100·Usage 87·Deliverables 74). 오케스트레이션 로직 없음.
- `agents/*.md` **4~5개**(89/100=5, 11/100=4): frontmatter `name`+`description`만, body =
  Core Responsibilities(≈전수)·Working Principles(≈전수)·Deliverable Format(≈전수)·**Team
  Communication Protocol(469/489, 다중에이전트 훅)**·Error Handling(≈전수). 전부 `general-purpose`.
- `skills/{harness-name}/skill.md` = **오케스트레이터 스킬(실 제어문서)**: Execution Mode(77)·Agent
  Roster(82)·**Workflow+task-DAG(83)**·Scale modes(~96)·Data Transfer Protocol(77)·Error Handling(82)·
  **Test Scenarios 3종(77)**. + 2~3 **agent-extending 스킬**(도메인 payload). **trigger boundary는
  스킬 description frontmatter**(positive 트리거 + 명시적 out-of-scope).

## 2. Agent-role 원형 (빈도) — 489 agent
| 중립 원형 | 근거(name head) | ~수 | 하네스 도달 |
|---|---|---|---|
| **Reviewer/QA/Cross-validator** | reviewer 52·assessor 8·auditor 4·validator/verifier/judge/critic | ~71 | **71/100** 명시(교차검증은 사실상 전수) |
| **Analyst/Evaluator** | analyst 65 | ~65 | 대부분 |
| **Synthesizer/Writer/Reporter** | writer 39·editor·synthesizer·summarizer | ~55 | 대부분(최종 컴파일) |
| **Implementer/Builder/Engineer** | engineer 20·architect 21·builder 14·developer 8 | ~63 | SwDev/Data 집중, 그 외도 |
| **Designer** | designer 40 | ~40 | 흔함(instances는 도메인) |
| **Coordinator/Manager/Planner** | manager 19·planner 16·coordinator 4 | ~40 | **24/100** 명시(나머지는 스킬에 내재) |
| **Strategist/Advisor/Coach** | strategist 15·advisor/coach | ~24 | Business/Legal/Edu |
| **Researcher/Collector** | researcher 6·searcher/collector/mapper | ~20 | **21/100** 전담(45/100이 WebSearch 참조) |

→ **중앙 라이브러리 seed 후보 role 원형**: Reviewer/QA(최고 신뢰)·Analyst·Synthesizer/Writer·
Coordinator·Researcher·Implementer·Strategist/Advisor·Designer. **Domain-Specialist 슬롯만 recipe-side**.

## 3. Skill 원형 — form 중립 / instance 도메인
- 오케스트레이터 스킬 **shape는 100/100 재발**(중립 구조 원형).
- extending 스킬 **instance 재사용은 거의 0**(6개 이름만 정확히 2하네스, 3+ 없음) → **전부 recipe-side**.
- 단 type-archetype으로 군집(중립 form): **Calculator/Engine · Framework/Methodology ·
  Pattern/Template-Catalog · Knowledge/Reference-Base · Visualization/Reporting**.

## 4. 오케스트레이션 패턴 (중립·near-universal)
- **Agent-Team via SendMessage 100/100**. **Task DAG**(Order/Owner/Depends-On/Deliverable, 병렬 분기).
- **Scale/execution modes ~96/100**(full/reduced/single, 요청범위→에이전트 부분집합).
- **Data-transfer 3종**: 파일(`_workspace/NN_agent.ext`)·메시지(SendMessage)·태스크(TaskCreate/Update 60/100).
- **수렴**: reviewer가 전 deliverable 교차검증 → "🔴 Must Fix"면 소유 에이전트에 재작업 요청, **bounded(≈2라운드)**.

## 5. Guardrail 패턴 (중립·재발)
structured-output(deliverable 템플릿, ≈전수) · trigger-boundary(positive+out-of-scope) ·
error-fallback(실패유형별 표, 82/100) · cross-validation+severity(🔴🟡🟢) · team-communication(469/489) ·
evidence-grounding(web-search, 45/100) · bounded-iteration(≈2라운드).

## 6. 핵심 결론 (라이브러리 성장 근거)
- **form은 중립, content는 도메인** — 세 각도 공통. 중립 라이브러리는 **skill 원본이 아니라
  type-archetype(Calculator/Framework/…)을 Pattern/Concept로** 담아야 함.
- 강한 중앙 후보(구조 100/100 전 도메인): orchestrator-skill **Pattern** · agent-file **Role 템플릿** ·
  Task-DAG+scale-mode **Workflow** · `_workspace` data-transfer **Pattern** · guardrail 5종.
- recipe-side 유지: 모든 concrete skill instance · domain-specialist agent · domain deliverable 템플릿
  (교차도메인 재사용 ≈0 → "도메인 특정은 recipe-local" 분리 실증).
