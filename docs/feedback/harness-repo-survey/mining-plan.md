# 반영 계획 — wave·게이트·검증

원칙은 기존과 같다: **작게 반복**(ODR §8), wave마다 `validate.py` PASS + federate 회귀 0 + coverage
게이트. 새 소스라고 예외를 두지 않는다.

## 선행 정리 (새 소스 착수 전)
지금 미완인 것부터 닫는 편이 낫다 — 둘 다 승인된 항목의 잔여다.
1. `revfactory-harness-reflection` **P3/P4** (augmentsRole·agentType 활용, skill 거버넌스, role-qa).
2. `harness-100-augmentation` **inc4 importer**(`import_corpus.py`).
새 코퍼스는 이 importer의 **첫 재사용처**가 되므로, inc4를 먼저 하면 아래 wave 비용이 크게 준다.

## Wave 0 — 커버리지 대조 (부품 저작 0, 가장 싸고 가장 정보량 큼)
`awesome-harness-engineering`(CC0)의 12 Design Primitives × 우리 205 개체 대조표 작성.
산출: 12행 판정표 + GAP 목록. **여기서 나온 GAP이 이후 wave의 우선순위를 정한다.**
담당: inspection 조사(부품 저작 없음) 또는 vnv. 실패 조건 없음(판정만).

## Wave 1 — orchestrator/실행모드 축 (wshobson `agents`의 16 orchestrators)
가장 얇은 축(`ExecutionMode` 3, `DesignPattern` 15)을 외부 실증으로 검증·확장한다.
- 16개 orchestrator를 읽고 **중립 패턴/모드로 원형화** → 기존 15 pattern·3 mode와 중복 제거 후 신규만 저작.
- 완료 게이트: `validate.py` PASS · 신규 노드 전부 `tokenEstimate`+`maturity "draft"` · 기존
  `h-*` 산출물 **byte-identical**(새 개체는 어느 하네스에도 자동 결합되지 않아야 한다).
- 예상 규모: pattern/mode 5~15. **소규모로 시작**.

## Wave 2 — role 원형 확장 (VoltAgent 154 + wshobson 203)
- **그대로 넣지 않는다.** 두 코퍼스를 합쳐 **원형(archetype)으로 클러스터링**한 뒤, 현재 8개 role로
  덮이지 않는 원형만 채택(예상 10~20, 언어·프레임워크 특화는 전부 제외).
- frontmatter 매핑이 기계적이므로 **inc4 importer 재사용**이 자연스럽다.
- 완료 게이트: Wave 1과 동일 + `retrieve.py`로 신규 role이 검색되는지 확인(anti-orphan 실증).

## Wave 3 — guardrail·skill 보강 (toolkit rules 15 · skills, 조건부 agent-rules-books)
- 기존 34 guardrail과 **중복·근사 동의어 제거가 주 작업**(drift 위험이 가장 큰 wave).
- `agent-rules-books` 채택 여부는 §license-gate의 회색지대 결정에 달렸다.

## Wave 4 — GAP 처리 (hook / permissions / observability)
Wave 0 결과로 확정된 GAP만 TBox 확장. **범주 신설은 같은 커밋에서 연결**(orphan 금지 규율).
`ho:Hook`이 채택되면 assembly section·materialize 렌더러까지 한 세트로 계획해야 한다
(GAP-4 전례: 개체만 만들고 렌더러가 없으면 그래프에만 존재하는 부품이 된다).

## 매 wave 공통 검증 (lockstep)
1. 중앙 `validate.py` PASS + 개체 수 증감 기록.
2. **push 전 로컬 federate**: staging 공유 catalog로 8 recipe 전부 PASS(신규 유닛을 만들면 catalog 동반).
3. `materialize` 회귀: 기존 하네스 산출물 diff — 의도한 섹션 외 변경 0.
4. NOTICE·`dct:source` 갱신(§license-gate).
5. 완료 보고 `docs/feedback/verified/`.

## 위험
- **카탈로그화**: 200+ role을 그대로 흡수하면 "중립 부품 라이브러리"가 "에이전트 목록"으로 변질된다.
  Wave 2의 원형화 상한(10~20)을 지키는 것이 이 저장소의 정체성 방어선이다.
- **retrieve 예산**: 개체가 늘수록 팩 경쟁이 심해진다. 지금 `retrieve.py`는 **동점 tie-break가
  비결정적**이라(별건 `retrieve-nondeterministic-pack.md`) 개체 증가 전에 그 결함을 닫는 편이 좋다 —
  안 그러면 "새 부품이 검색되는가"라는 wave 게이트 자체를 신뢰할 수 없다. **Wave 1 착수 전 처리 권고.**
