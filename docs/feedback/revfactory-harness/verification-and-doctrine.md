# revfactory/harness 반영: 검증개념 정리 + doctrine 불일치 + 모델하지 말 것

> 출처: inspection dispatch 3-에이전트 분석(2026-07-23). 상위: `../revfactory-harness-reflection.md`.

## 1. 세 검증개념 정리 (비중복 — load-bearing)
소스가 요구하는 검증이 우리의 기존 `Contract`와 겹치는지가 핵심 질문. **subject/time 축이 달라 비중복**:

| | `ho:Contract`(빌드) | `ho:TestScenario`(행위, 신규) | QA 교차검증 |
|---|---|---|---|
| **대상** | 하네스가 emit한 **artifact 트리**(tools/*.py·SKILL.md·CLAUDE.md) | 조립된 하네스의 **런타임 행위**(현실 요청) | 실행 에이전트가 **유저에게 산출한 것**(예: API↔hook 경계) |
| **질문** | "빌드가 well-formed/runnable를 냈나?" | "빌드된 하네스가 대표입력에 옳게 행동하나?" | "산출물 경계 양쪽이 일치하나?" |
| **시점/주체** | 빌드타임, `verify_contract.py` 결정적 판정 | 설계/수용 시점, fixture(프롬프트+기대), Grader/스크립트 채점 | 에이전트 런타임, **하네스 내부 reviewer Role**이 수행 |
| **스키마 위치** | Capability에 `capabilityContract` | **Harness에 `hasTestScenario`** | `Role`+`Guardrail`(reviewer + `gr-integration-coherence`) |

**공존 규칙**: **artifact 구조 → Contract; 입력→출력 행위 → TestScenario.** executable Contract가 시나리오를
*돌릴 수도* 있으나 CWD=emit 트리 + exit-code 결정적인 것만; open-ended 행위 채점은 TestScenario(Role 채점).
**QA 교차검증은 둘과 직교** — 하네스에 대한 검사가 아니라 하네스가 *내부에 담아 downstream 작업물에 수행하는
방법론*(reviewer Role + guardrail). 셋을 각 Capability/Harness/content 위치에 두면 겹치지 않는다.
→ 3층: **Contract=artifact 빌드적합 · TestScenario=artifact 행위수용 · QA=하네스가 담은 reviewing 능력.**

## 2. Doctrine 불일치 (사용자 결정 필요)
소스를 충실 반영하되 우리 운영 harness(CLAUDE.md)와 저장 harness가 **일치**해야 하므로(gr-lang 절 원칙),
아래를 조용히 채택하면 안 됨:

1. **기본 실행모드가 반대**: 소스는 **peer Agent-Teams가 최우선 기본**. 우리 repo는 **central orchestrator-
   workers/dispatch가 기본**, `pat-peer-mesh`가 대안. → **양쪽을 selectable로 저장하되 repo의 central-dispatch
   기본을 명시 유지**(안 그러면 저장 harness가 운영 harness와 모순). **[결정 필요]**
2. **"Agent Teams" primitive ≠ 우리 dispatch 모델**: 소스 Teams=TeamCreate/SendMessage/TaskCreate(독립 Claude
   인스턴스 peer). 우리 기본=orchestrator 하 `Agent`-tool subagent spawn(`chan-dispatch`). 구조 매핑
   (`pat-peer-mesh`+`chan-peer`)은 맞으나 **우리 repo는 실제로 peer team을 운영하지 않음**(orchestrator+dispatch).
   모델은 둘 다 담되 live harness는 dispatch. **[기록]**
3. **`model:opus`는 이 repo엔 불일치 아님**(이전 `design-patterns-coverage.md`의 flag는 **harness-100 인스턴스**
   기준이라 stale). 이 repo doctrine은 이미 dispatch developer/vnv에 opus 강제 + `mc-opus` 바인딩 → 소스와 **일치**.
   권고: 레퍼런스를 규범으로 보고 옵션 `gr-opus-required`로 명시화. **[정정: 불일치 아님]**
4. **QA=general-purpose vs least-privilege 긴장**: 소스는 QA가 검증 스크립트 실행 필요로 general-purpose 요구
   (Explore=읽기전용). 우리 `gr-least-privilege` 기본과 긴장 → `agentType`(delta B) + **정당화된 `roleTool`
   실행 scope**로 해소(읽기전용 기본이 아니라 명시적 execute 부여). **[해소책 있음]**

## 3. 모델하지 말 것 (ABox promptText/artifactTemplate 또는 materialize convention)
세 에이전트 공통 — 스키마로 만들면 over-fitting:
- severity 마커 🔴🟡🟢, verdict/checklist 레이아웃 → artifactTemplate 내용.
- JSON 필드명(`eval_metadata`/`grading{text,passed,evidence}`/`timing{total_tokens,duration_ms}`) → Deliverable의
  artifactTemplate 내용(필드명 정확성=템플릿 제약, 어휘 아님).
- `_workspace/` 트리·`{phase}_{agent}_{artifact}` 파일명·iteration-N 넘버링·"삭제 금지" → materialize/runtime layout
  (감사보존 의도는 `gr-traceability`로 이미 커버).
- CLAUDE.md 포인터/변경이력 표 레이아웃 → emit 포맷(`AssemblySection` 순서 + `gr-traceability`+`derivedFrom`/
  `maturity`가 의미 담당).
- Phase 선택 매트릭스·dry-run 체크리스트·모드선택 트리 → workflow `skos:definition` prose.
- 유저 숙련도 감지·톤 조절 → 런타임 대화 행위(옵션 `gr-audience-tone`, 저가치).
- 500줄 제한·300줄 ToC·progressive-disclosure 3-tier 파일기제 → 저작 convention(원리 = `gr-bounded-context`+
  `tokenEstimate`로 이미).
- 팀크기 2~7·idle 알림·리더 고정·토큰비용높음 → Agent-Teams primitive 런타임 속성(비용은 `tokenEstimate` 축).
- description "pushy" 트리거 문구·should-NOT 작문 스타일 → skill 저작 craft(트리거 검증 *행위*는 wf-verify-harness step).
