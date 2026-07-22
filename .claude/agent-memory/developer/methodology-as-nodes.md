# 메소돌로지(process)를 first-class 노드로 반영

CLAUDE.md 워크플로("Composing a new harness")처럼 산문으로만 있던 **절차/방법론**을 온톨로지
노드로 반영한 작업(harness-composition methodology). glossary-term-layer.md(원칙→term+guardrail)의
확장판: 원칙 하나가 아니라 **process 하나**를 반영할 때의 관용 조합.

## 관용 조합 (한 methodology = 4~5 노드)
- **Workflow** (`wf-<slug>`): 절차 자체 = 번호 매긴 step들을 `skos:definition`에. 텍스트 있으니
  `ho:tokenEstimate` 필수. capability는 필요할 때만(단순 절차면 생략, wf-multiagent는 provides함).
- **DesignPattern** (`pat-<slug>`): 그 절차가 체현하는 **접근/전략**(왜 이렇게 조립하나). 기존
  patterns.ttl 개체엔 maturity 없지만 추가 무방(brief가 요구하면 `ho:maturity` 붙임, SHACL 무관).
- **Guardrail** (`gr-<slug>`): 그 절차의 **규율**(anti-drift/anti-orphan 등) = promptText 1개.
- **Concept term ×N** (`c-<slug>`, `skos:broader c-agent-methodology`): 절차명·규율명을 검색가능
  term으로. cross-cutting이면 c-agent-methodology 밑.
- **배선**: 전부 중립 템플릿 `core:h-multiagent`에 연결해야 non-orphan. Harness는 **hasWorkflow·
  appliesPattern를 ≥2개 가질 수 있음** — 기존 값에 콤마로 append(wf-multiagent+wf-compose-harness,
  pat-orchestrator-workers+pat-ontology-composition). guardrail도 hasGuardrail 리스트에 append.
  개념은 guardrail의 `ho:tagged`로 reachable(+broader).

## 사실 재확인
- **prefLabel은 (class,label) 단위 dup 검사**라 Workflow "Harness composition"과 Concept
  "Harness composition"이 같은 문자열이어도 클래스 달라 충돌 아님(advisory이기도). 굳이 다르게
  안 지어도 되지만, 검색 랭킹상 term은 명사구(Harness composition)·wf도 동일 라벨 OK.
- 91→96(+5: wf+pat+gr+2 concept). 두 로더 parity·SHACL·reachability 그린. retrieve로 5노드 표면화.
- ODR 연계: composition=SPEC 저작/검증, ODR BIND/EMIT/Lock=render/reproduce. step7 coverage-audit
  뒤 materialize가 EMIT 진입점. 설계문서는 `docs/composition-methodology.md`(sibling=odr-bind-lock.md).
