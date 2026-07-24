# 소스 → 온톨로지 매핑과 스키마 gap 후보

중앙 현황(실측 @205): `Concept` 35 · `Guardrail` 34 · `DesignPattern` 15 · `AssemblySection` 12 ·
`WorkflowStep` 10 · `AreaOfObservation` 10 · `Role` **8** · `Capability` 8 · `Workflow` 7 · `Harness` 7 ·
`Channel` 6 · `Task` 6 · `Agent` 5 · `Tool` **4** · `SystemPrompt` 4 · `Domain` 4 · `ExecutionMode` 3.

얇은 축은 **`Role`(8)·`Tool`(4)**이고, 후보 코퍼스가 정확히 그 두 축을 수백 개 규모로 들고 있다.

## 1. 기존 어휘로 그대로 들어오는 것 (스키마 변경 0)

| 소스 | 소스 단위 | 매핑 | 비고 |
|---|---|---|---|
| VoltAgent subagents (154) · wshobson agents (203) | subagent 파일 | `ho:Role` (+`ho:roleTool`←frontmatter `tools`, `ho:usesModel`←`model`, `ho:rolePersona`←body role 서술) | frontmatter가 우리 role 모델과 거의 1:1. **중립화가 관건** — 언어별·프레임워크별 특화 200종을 그대로 넣으면 부품 라이브러리가 아니라 카탈로그가 된다 |
| wshobson skills (175) · toolkit skills (35) | skill 파일 | `ho:Instruction` | lpranging recipe에서 이미 `.claude/skills`를 `ho:Instruction`으로 모델링한 전례 있음 |
| wshobson **orchestrators (16)** | 다중 에이전트 조율 워크플로 | `ho:Workflow`+`ho:WorkflowStep`, `ho:DesignPattern`, `ho:ExecutionMode` | **최우선 광맥**. 우리 `ExecutionMode`가 3개뿐이라 외부 실증으로 이 축을 검증·확장할 유일한 소스 |
| toolkit rules (15) · agent-rules-books | 자연어 규칙 | `ho:Guardrail` | 34개 기존 guardrail과 중복 제거가 주 작업 |
| VoltAgent body의 "communication protocol" 절 | 에이전트 간 통신 규약 | `ho:Channel` | 현재 6채널이 전부 우리 자체 운영에서 나온 것 — 외부 사례로 중립성 검증 가능 |
| awesome-harness-engineering의 12 Design Primitives | 축의 목록 | `ho:Concept`/`ho:Capability` **대조표** | 부품이 아니라 **커버리지 감사 기준**으로 쓴다(아래 §3) |

## 2. 스키마 gap 후보 (TBox 확장이 필요할 수 있는 것)

- **GAP-H (hook / lifecycle trigger)** — toolkit의 20 hooks는 `SessionStart`·`UserPromptSubmit`·
  `PostToolUse`·`Stop` 같은 **실행 시점 이벤트에 걸리는 트리거**다. 우리 `ho:Guardrail`은 *정책*(무엇을
  지켜라)이고 `ho:WorkflowStep`은 *절차의 한 단계*라, "이 이벤트가 발생하면 이것이 실행된다"는
  **트리거 축을 담을 범주가 없다**. CLAUDE.md step-7 규율상 **조용히 건너뛰지 말고 TBox 확장을
  먼저 트리거**해야 하는 전형적 사례. → 신규 범주 후보 `ho:Hook`(⊑`ho:BehavioralComponent`?) +
  `ho:hookEvent`. **결정 필요**(항목 결정 2).
- **GAP-E (다중 타깃 emit)** — wshobson은 하나의 부품 정의를 **5개 harness-native 포맷**으로 낸다.
  우리 `materialize.py`는 CLAUDE.md+MANIFEST 단일 타깃이다. 부품 쪽 스키마 변경 없이 **emitter 축**의
  확장으로 볼 수도 있어, TBox 문제인지 tools 문제인지 판정이 필요하다. → **조사 후 결정**.
- **GAP-P (permissions/authorization)** — harness-engineering의 12 primitive 중 "Permissions &
  Authorization"은 우리에게 `gr-least-privilege`(guardrail) + `roleTool`(부분집합)로 **부분 존재**한다.
  도구 호출을 가로채 정책 평가·승인 라우팅하는 축(Veto류)은 미표현. 신규 범주까지 갈지, 기존 guardrail로
  충분한지 판정 필요.
- **GAP-O (observability/tracing)** — 12 primitive 중 미표현이 가장 뚜렷한 축. 우리는 관측을
  `ObservationSpace`/`AreaOfInterest`/`AreaOfObservation`(에이전트가 **무엇을 보는가**)으로 모델링했는데,
  harness-engineering이 말하는 observability는 **운영자가 실행을 어떻게 관측·추적하는가**로 방향이 반대다.
  같은 단어로 다른 축이므로 **disambiguation 대상**(drift 위험 높음 — 기존 `disambiguation-audit.md` 연장).

## 3. 커버리지 감사 용도 (부품 수확이 아닌 사용법)
`awesome-harness-engineering`(CC0)의 **12 Design Primitives**를 축으로 우리 205 개체를 대조하면,
"소스의 구조 요소를 빠짐없이 열거해 표현에 매핑"하라는 CLAUDE.md step-7 게이트를 **외부 기준**으로
한 번 더 돌릴 수 있다. 산출은 12행 표 — 각 primitive가 (a) 표현됨(노드 id 제시) (b) 부분 표현
(c) 미표현+GAP (d) 의도적 범위 밖 중 무엇인지. 위 GAP-H/P/O는 이 대조의 예비 결과다.

## 반증 참조 (부품화하지 않음)
- `open-multi-agent`: coordinator가 **런타임에 task DAG를 계획**한다 — 우리 `Deliverable` DAG는 저작
  시점에 고정된다. "계획 시점"이 축으로 필요한지 검토 재료.
- `agentscope-ai/AgentTeams`: Matrix room을 채널로 쓰는 human-in-the-loop 조율 — `chan-agent-user`의
  외부 대응물.
