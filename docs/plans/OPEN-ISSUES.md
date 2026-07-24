# 열린 이슈 추적 (자율 루프 앵커)

> 작성: orchestrator (2026-07-25). **30분 주기 자율 루프(`/loop 30m`, job `1562b40d`)가 매 사이클 이 문서를
> 먼저 읽고 갱신한다.** 사이클마다 상태를 실측으로 재확인할 것 — 시간 경과를 완료로 가정하지 않는다.

## 사용자 설정 목표 (2026-07-25)
> "남은 피드백과 열린 이슈가 없을 때까지 수행. 또한 온톨로지의 내용들이 **통일성과 건전성**있게 정리되고
> **충분히 세분화**되어야 함."

두 축이다. **(1) 채널 배수** — inbox·verified·inquiries에 미처리가 없을 때까지. **(2) 품질 축** — 배수만으로는
목표가 아니며, 온톨로지가 일관되고(통일성) 정합하며(건전성) 충분히 분해돼야(세분화) 한다. 이 축은
`validate.py` PASS로 증명되지 않는다 — PASS는 그래프 정합성만 본다. 따라서 **품질 감사(Q1~Q3)가 별도 작업 항목**이다.

---

## A. 승인된 피드백 (적용 대기/진행 중)

| 항목 | 상태 | 남은 일 |
|---|---|---|
| `harness-100-augmentation.md` | **진행 중** | Phase 0.5 전수 속성 인벤토리 **dispatch 실행 중** → 중앙 어휘 GAP 저작 → P0-b catalog/CI glob 생성 → importer → 대표 recipe 임포트. 계획: `harness-100-scaleup-plan.md` |
| `harness-repo-survey.md` | **미착수** (승인+답변 완료) | ①전체 로드맵(c) ②**`ho:Hook` 신설** ③agent-rules-books는 온톨로지에만 ④role 원형: 온톨로지 전량 + 예제 10~20. 계획: `harness-repo-survey/mining-plan.md` Wave 0~4 |
| `revfactory-harness-reflection.md` | **거의 완료** | P1·P2 land 완료. **잔여 확인 필요** — delta-inventory 대조로 미반영분이 정말 없는지 1회 감사 |
| `retrieve-nondeterministic-pack.md` | **land 완료** (`d1ac476`, CI green) | 파일 태그만 `open` 유지 — 사용자가 `approved`로 고치면 즉시 refresh 가능. 근거: `verified/retrieve-determinism-finalize.md`. negative control로 가드 실효 확인(8/8 FAIL) |

## B. 기술 GAP (이번 세션에서 판정 보류한 것)

1. **P0-b — catalog/CI glob 생성**: 현재 catalog·CI matrix가 손 나열. batch 임포트 **전 차단요소**.
   누락이 에러가 아니라 **조용한 부분 closure**로 나타나는 실패 양식을 이미 한 번 겪었다.
2. **retrieve tie-break 정책**: 지금은 IRI 사전순(재현성 확보용). 동점 17개에 슬롯 5개인 질의가 실재하므로
   **검색 품질** 관점의 정책(maturity/salience/tokenEstimate 가중)은 미결. → Q2와 함께 다루면 좋다.
3. **`INSTANCE_CLASSES` 미등록 — 범위 정정(inspection 실측)**: 2개가 아니라 **7클래스·32개체**
   (`Agent` 5 · `AreaOfInterest` 5 · `AreaOfObservation` 10 · `ObservationSpace` 5 · `Memory` 3 ·
   `TestScenario` 2 · `FailurePolicy` 2). MANIFEST type 표기뿐 아니라 카운트·reachability·retrieve 노출에 영향.
5. **★`tokenEstimate` 의미 과부하 → 팩 조기 절단** (`docs/feedback/retrieve-pack-quality-defects.md` 결함 A).
   `retrieve.py "what does the inspection agent observe"` → **nodes=3, budget 125/900**. 원인 ① 같은 프로퍼티가
   "팩 비용"과 "1회 추론 관측량"(12000 등) 두 뜻 ② `traverse()`가 예산 초과 노드에서 `break`. → **수정 dispatch 진행 중.**
6. **★deprecated 노드가 후계보다 상위 검색** (같은 항목 결함 B). `retrieve.py`가 `ho:maturity`를 안 읽어
   폐기된 `pat-sub-agents`가 rel 8.1로 1위, 후계 `mode-sub-agents` 6.3. **→ 같은 dispatch에서 수정 중.**
7. **산출 하네스 문서로 내부 IRI 유출** (`docs/feedback/emitted-harness-iri-leak.md`). `materialize.py`가
   definition/promptText를 그대로 렌더해 CLAUDE.md에 `id:`/`ho:` dangling reference — 21노드·50회
   (h-peer-mesh 10 · h-harness-factory 9 · h-workspace-synthesis 7 · h-multiagent 1). **미착수.**
4. **execution-mode 범위 한정이 로컬 주석에만 존재** — `mode-sub-agents`를 읽는 다른 소비자에겐 안 보인다.
   같은 충돌이 다른 하네스에서 재발하면 (B)정의정정/(C)신규모드 재검토 신호.

## C. 품질 축 작업 항목 (목표 (2) — `validate.py`가 못 보는 축)

- **Q1. 통일성 감사**: 같은 종류의 노드가 같은 방식으로 저작됐는가 — definition 문체("왜/언제 고르나"),
  `tokenEstimate` 누락, `maturity` 분포, 접두사 규약(ONTOLOGYSTYLE §2 표) 준수, 배너 스타일.
  기계 점검 가능한 항목이 많으므로 **린터성 스크립트**로 만들면 재발 방지가 된다.
- **Q2. 건전성 감사**: 중복/근사동의어(drift) 탐지 — `validate.py`의 duplicate-label 검사는 **완전일치만** 본다.
  의미 중복(예: 같은 원칙을 다른 문장으로 적은 guardrail 2개)은 못 잡는다. 또 deprecated 노드가 실제로
  아무도 참조하지 않는지, capability 짝이 의미적으로도 맞는지.
- **Q3. 세분화 감사**: 아직 blob인 노드가 남았는가. 이미 분해된 축(Workflow→WorkflowStep, SystemPrompt→
  PromptSection, Harness→AssemblySection)과 달리, **한 노드가 여러 책임을 지고 있는 곳**을 찾는다
  (ONTOLOGYSTYLE §1 "노드는 작고 단일 책임"). 코퍼스 인벤토리 결과가 여기 근거를 준다.

### C-0. 초벌 감사 실측치 (inspection, 2026-07-25) — 다음 저작 브리프의 근거
> **방법론**: 품질 감사는 **그래프 스캔만으로 부족하다** — `retrieve.py`·`materialize.py`를 **실제로 돌려야**
> 드러나는 결함군이 있다(예산 절단·랭킹·유출). 위 §B.5~7이 전부 그렇게 발견됐다.

- **Q1**: `tokenEstimate` 누락 **98/189**(예산 과소계상 ~5,200토큰; 최악 `chan-peer` ~212·`h-harness-factory` ~204) ·
  `maturity` 누락 **58**(전부 SpecConcept 계열 — shapes가 일부 클래스에만 minCount를 거는 **비대칭**이 원인) ·
  `definition` 누락 **56**(`Guardrail` 34/34는 관례상 `promptText`가 본문) · **접두사 위반 0**.
  → 진단 정정: ONTOLOGYSTYLE §1c의 **명시 범위 위반은 0**이다. "규칙 위반"이 아니라 **규칙 범위가 좁다**.
- **Q2**: 라벨 근사중복 J≥0.5 **81쌍**(대부분 `os-*`/`as-*` 작명 패밀리 노이즈) · 정의 근사중복 J≥0.55 **9쌍**
  (전부 `AreaOfObservation` internal 패밀리, 최고 J=0.86 `oa-developer-internal`↔`oa-synthesizer-internal`
  — **템플릿 저작인지 복붙 blob인지 판단 필요**) · deprecated 3개 inbound 참조 0(그래프는 clean).
- **Q3**: definition 길이 median 210 / p90 485 / **max 1019**(`wf-compose-harness`). blob 후보: `chan-peer` 832 ·
  `h-harness-factory` 818 · `h-workspace-synthesis` 771 · `pat-peer-mesh` 770 · `h-multiagent` 746.
  **다중정책 Guardrail 10/34** — 특히 `gr-design-for-loss`는 한 문장에 정책 4개.

## D. 현재 건전성 기준선 (2026-07-25)
`validate.py` **PASS** · 205 individuals · TBox 클래스 44 · abox 18파일 · 기본 assembly order 12 sections ·
`check_determinism.py` PASS. **미커밋**: 결정성 증분(tools/CI) + 계획 문서들.

## E. 사이클 규약
- 실행 중인 dispatch가 있으면 **그 파일 범위를 건드리지 않는다**(병렬 충돌 방지). 특히 **inspection이 git을
  다루므로, 다른 dispatch가 쓰는 중인 파일을 커밋하지 않도록 매 dispatch에 진행 중 목록을 알려준다.**
- 저작은 반드시 developer dispatch 경유. orchestrator는 계획·통합확인만. **git은 inspection 전담.**
- 대규모/비가역 작업은 사용자 부재 중 착수하지 않는다 — 계획·감사·검증까지 진행하고 대기.

### E-1. inspection dispatch 허용 (사용자 지시, 2026-07-25)
> "goal이 완료될 때까지 inspection agent도 dispatch해서 진행해줘."

CLAUDE.md의 **"inspection은 별도 세션 — orchestrator가 spawn하지 않는다"** 규칙은 **이 목표가 완료될 때까지
이 지시로 대체**된다. orchestrator가 `subagent_type: inspection`, `model: opus`로 직접 dispatch한다.
역할 경계는 그대로다 — inspection은 **판정·검증·git만** 하고 `ontology/**`·tools를 편집하지 않는다.
이로써 land 병목(별도 세션 대기)이 사라져 루프가 자립적으로 돈다: **저작(developer) → 확인(orchestrator) →
검증·land(inspection)** 가 한 사이클 안에서 닫힌다.
