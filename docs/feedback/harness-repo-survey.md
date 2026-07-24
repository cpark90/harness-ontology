---
status: approved            # 사용자만 approved로 바꾼다
targets: [core:h-multiagent, core:role-developer, core:pat-orchestrator-workers, core:mode-sub-agents]
kind: proposal
related: [docs/feedback/harness-100-augmentation.md, docs/feedback/revfactory-harness-reflection.md, docs/feedback/retrieve-nondeterministic-pack.md]
---
# 외부 harness repo 조사 → 온톨로지 반영 계획 (결정 앵커)

## 요청 (사용자)
"하네스와 관련된 git repo들 검색해서 찾고 온톨로지에 반영하기 위한 문서들 만들어줘."
→ inspection이 4개 검색축으로 조사, 실측(`gh api`) 기반으로 아래 companion 4편 작성.

## Companion 문서
- **`harness-repo-survey/candidate-inventory.md`** — 후보 9종 실측표(license·규모·내용·수확 추정) +
  후보에서 뺀 것과 이유.
- **`harness-repo-survey/license-gate.md`** — 소스별 채택 가부와 조건. **`hesreallyhim/awesome-claude-code`
  (CC BY-NC-ND)는 채택 불가**, leaked prompt 모음도 불가.
- **`harness-repo-survey/ontology-mapping.md`** — 소스 단위 → `ho:` 범주 매핑 + **스키마 gap 후보 4건**
  (hook·다중 emit·permissions·observability).
- **`harness-repo-survey/mining-plan.md`** — Wave 0~4, 게이트, 위험.

## 핵심 발견 3가지
1. **얇은 축과 코퍼스가 정확히 맞물린다.** 중앙은 `Role` 8 · `Tool` 4로 얇은데, MIT 코퍼스 두 곳이
   role 350여 개를 frontmatter(`tools`/`model`/description) 형태로 들고 있다 — 우리 role 모델과 거의 1:1.
2. **가장 값진 것은 부품이 아니라 축이다.** `wshobson/agents`의 **16 orchestrator**는 우리
   `ExecutionMode`(3개)·`DesignPattern`(15개)을 외부 실증으로 검증·확장할 유일한 소스다.
   `awesome-harness-engineering`(**CC0**)의 12 Design Primitives는 **커버리지 감사 기준**으로 쓸 수 있다.
3. **표현 범주가 없는 것이 실제로 나왔다.** toolkit의 20 hooks(`SessionStart`/`PostToolUse`/`Stop`)는
   "이벤트 발생 시 실행"이라는 **트리거 축**인데, 우리 `Guardrail`(정책)·`WorkflowStep`(절차)로는 담기지
   않는다. CLAUDE.md step-7이 "담을 어휘 범주가 없으면 TBox 확장을 먼저 트리거하라"고 규정한 사례다.

## 권고 순서
**Wave 0(커버리지 대조, 저작 0) → 결함 정리 → Wave 1(orchestrator/실행모드) → Wave 2(role 원형)**.
선행으로 `harness-100` inc4 importer를 닫으면 Wave 2 비용이 크게 준다(그 importer의 첫 재사용처가 된다).
또한 `retrieve.py` 비결정성(별건 항목)을 **Wave 1 전에** 닫기를 권고한다 — 안 그러면 "새 부품이
검색되는가"라는 wave 완료 게이트 자체를 신뢰할 수 없다.

## 결정 필요 (사용자)
1. **범위**: (a) Wave 0만 먼저(가장 싸고, 이후 우선순위를 데이터로 정함) / (b) Wave 0+1 / (c) 전체 로드맵 승인.
   — inspection 권고: **(a)**.
2. **`ho:Hook` 신설 여부**: 트리거 축을 1급 범주로 만들 것인가, 아니면 기존 `Guardrail`/`WorkflowStep`으로
   흡수할 것인가. (신설 시 개체·assembly section·materialize 렌더러를 한 세트로 계획해야 한다 — GAP-4 전례.)
3. **`mattpocock/agent-rules-books` 채택 여부**: repo는 MIT지만 규칙 내용이 유명 서적 요약이라
   회색지대(§license-gate). inspection 권고: **제외**(보수 노선).
4. **role 원형화 상한**: Wave 2에서 350여 개를 원형 **10~20개**로 압축하는 상한에 동의하는가.
   (상한이 없으면 중립 부품 라이브러리가 에이전트 카탈로그로 변질된다.)

## 한계 (정직한 표시)
후보 repo들을 **README·디렉토리 구조 수준**까지만 판독했다. 파일 단위 전수 정독은 하지 않았으므로
"수확 추정" 수치(예상 pattern 5~15, role 원형 10~20)는 **추정**이다. 채택된 wave의 첫 단계에서
실제 파일을 열어 확정해야 한다.

## 사용자 피드백
1. (c)
2. 신설
3. 온톨로지에만 반영
4. 온톨로지에는 모두 반영하고, 예제는 10~20개로 압축해서 반영.
