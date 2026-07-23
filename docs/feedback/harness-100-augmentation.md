---
status: approved            # 사용자만 approved로 바꾼다
targets: [core:h-multiagent, core:wf-multiagent, core:pat-orchestrator-workers]
kind: proposal
related: [docs/feedback/finer-harness-decomposition-assembly.md]
---
# harness-100 코퍼스로 harness-recipes 대폭 증강 (결정 앵커)

## 요청 (사용자)
`revfactory/harness-100`(Apache-2.0, 100 하네스·10도메인) 분석해 **harness-recipes 보강 작업**을 만들라.
dispatch 진행, 여러 문서 제안 OK. → inspection이 **3개 분석 에이전트(opus) dispatch** 후 아래로 합성.

## 분석 결과 (companion 문서 4편)
- **`harness-100/part-taxonomy.md`** — 부품 taxonomy + neutral/domain 분류(role 원형·skill archetype·빈도).
- **`harness-100/tbox-gaps.md`** — 스키마 gap 5개 + delta(GAP-1 Deliverable+DAG … GAP-5 augmentsRole).
- **`harness-100/recipe-roadmap.md`** — 매핑·중앙성장·파일럿/wave·importer·scale·attribution.
- **`harness-100/design-patterns-coverage.md`** — (추가 2026-07-23) `revfactory/harness`의
  `agent-design-patterns.md`(방법론 레퍼런스) 커버리지 판정 — **부분 반영**. 미반영분(패턴 taxonomy 6종·
  agent-type·복잡도 guardrail 등)은 **중앙 패턴·거버넌스 축**으로 별도 inc 권고. 아래 addendum 참조.

## inspection addendum (2026-07-23) — design-patterns 레퍼런스 반영 여부
사용자 질의("`agent-design-patterns.md` 내용도 다 반영되나?")에 대한 판정: **"다"는 아니다(부분).**
내 제안은 harness-100 **인스턴스 실측** 기반이라 지배 구조·role/skill/guardrail 원형은 담았으나, 이
레퍼런스가 정의하는 **named 패턴 taxonomy**(Pipeline·Fan-out/Fan-in·Expert-Pool·Producer-Reviewer·
Supervisor·Hierarchical-Delegation), **agent-type**(general-purpose/Explore/Plan), **설계 거버넌스**
(분리/재사용/depth≤2/no-nested-teams/bottleneck)는 **미/부분 반영**. 이는 recipe가 아니라 **중앙 중립
라이브러리(패턴·guardrail·agent-type) 강화**라 인스턴스 임포트와 직교 → **로드맵에 "패턴·거버넌스 축"을
별도 inc로 추가** 권고. orchestrator의 "pluggable coordination" 확정과 정합(그 6패턴이 정확히 그 축).
불일치 1건: 레퍼런스는 `model:opus 필수`인데 코퍼스 인스턴스는 model 미선언 — SPEC 기준 확인 필요.

## 한 문장 결론
코퍼스 100개는 **구조적으로 균일**(orchestrator + 4~5 worker + reviewer/QA, SendMessage mesh)하고
**form은 중립·content는 도메인**이다. 따라서 (1) 재발 부품을 **중앙 라이브러리에 1회 승격**, (2) 각
하네스를 **recipe로 임포트**(importer 반자동), (3) 코퍼스 메커니즘(task-DAG·scale-mode 등)을 담도록
**TBox 소폭 확장**하면 recipes가 3개→수십·100개로 확장되며 중립 라이브러리가 실전 검증된다.

## 이 작업이 기존 방향과 만나는 지점
- **이미 승인된 `finer-harness-decomposition-assembly.md`(범위 c)의 실증 근거**다: 그 WorkflowStep/조립
  축을 코퍼스가 요구하며, **GAP-1(Deliverable + stepProduces/stepConsumes/stepDependsOn)**은 그 WorkflowStep의
  직접 확장이다. → 두 이니셔티브를 **하나의 로드맵으로 통합** 권고(finer가 선행 기반, 코퍼스가 검증 코퍼스).

## 제안 작업 묶음 (orchestrator가 브리프로 분해)
1. **TBox 확장**(developer): GAP-1(최우선, finer WorkflowStep과 통합) → GAP-2~5 additive. `tbox-gaps.md` delta.
2. **중앙 라이브러리 성장**(developer, 임포트 前 별도 reviewed): role-synthesizer · chan-workspace/peer ·
   gr-structured-output/scale-modes/graceful-fallback · cap-synthesis (+짝 Concept). `recipe-roadmap.md §2`.
3. **파일럿 5 recipe**(hand-author): 21-code-reviewer·16-fullstack-webapp·31-ml-experiment·03-newsletter-engine·
   46-product-manager → federate + materialize round-trip + retrieve 확인.
4. **importer 도구**(파일럿 green 후): `import_corpus.py`(SHOULD/MUST-NOT 경계는 roadmap §4) → draft 산출.
5. **batch wave**(카테고리별) + catalog/CI matrix **glob 생성** 전환 + Apache-2.0 NOTICE/`dct:source`.

## 열린 결정 (승인 시 지정 — 사용자/orchestrator)
1. **fidelity vs doctrine (핵심)**: 코퍼스는 **peer SendMessage mesh**인데 우리 repo는 **orchestrator-only
   dispatch 규율**. (a) 코퍼스 충실 → 중앙에 `chan-peer` 추가하고 그대로 모델링, vs (b) 우리 규율 강제 →
   각 코퍼스 하네스를 strict orchestrator-workers로 재모델. `chan-peer`와 100 recipe가 무엇을 주장하는지가 갈림.
2. **도메인 배치**: 10 카테고리 도메인을 중앙 신설? vs recipe-local 유지(+기존 중앙 도메인 재사용). 추천=후자.
3. **TBox 확장 범위**: GAP-1만(최대가치+finer 통합) vs GAP-1~5 전체. 추천=GAP-1 선행, 나머지 additive 순차.
4. **importer**: 반자동 `import_corpus.py` 빌드 vs 전량 hand-author. 추천=반자동(draft-only, 판단은 사람).
5. **batch 범위**: 파일럿 5 → 전 100? vs 우선 카테고리 부분집합. 추천=파일럿 후 재평가.
6. **attribution**: Apache-2.0 NOTICE + `dct:source`/`dct:license`. 추천=그대로(저위험).

## 열린 결정 — 확정 (orchestrator 기록, 2026-07-23)
1. **fidelity vs doctrine**: **둘 다 + 확장성** — coordination을 pluggable 차원으로(orchestrator-workers[기본] + peer-mesh, 향후 확장). ✅ inc1에서 `pat-peer-mesh`+`chan-peer`+`h-peer-mesh`로 반영.
2. **도메인 배치**: **recipe-local**(중앙 재사용 + 로컬 도메인). (inc3 적용)
3. **TBox 범위**: **GAP-1 선행**(✅ inc1: task-DAG), 나머지(GAP-2~5)는 파일럿이 요구할 때 additive.
4. **importer**: **반자동 draft-only**(`import_corpus.py`) — 파일럿 green 후.
5. **batch 범위**: **파일럿 5 후 재평가**.
6. **attribution**: **Apache-2.0 NOTICE + `dct:source`/`dct:license`** (recipe 저작 시).
- inc1(GAP-1+coordination)·inc2(중앙부품 §2) ✅ 완료·vnv 검증. **inc3 파일럿 5**: 21-code-reviewer·16-fullstack-webapp·31-ml-experiment·03-newsletter-engine·46-product-manager (recipe-local·Apache-2.0). **선결: batch3 이후 미커밋 pile을 inspection이 land한 뒤 clean base에서 inc3 진행**(`docs/plans/inspection-brief-CONSOLIDATED-since-batch3.md`).

## 범위 / 핸드오프
inspection은 **조사·제안까지**(3 에이전트 dispatch 완료, 4문서 산출). TBox·중앙부품·recipe·importer 저작은
orchestrator가 노드단위 dispatch brief로 계획해 **developer** 수행(schema 변경=coverage-audit gate +
"Adding vocabulary" 규율). 승인 = 이 항목 `status: open`→`approved` + 위 열린결정 1~6 지정.

> 코퍼스 로컬 클론: scratchpad `harness-100/`(임시). 실제 임포트 시 소스 경로/IRI를 recipe `dct:source`로.
