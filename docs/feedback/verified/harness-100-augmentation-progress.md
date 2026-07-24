---
source: harness-100-augmentation.md
verdict: apply
targets: [central-vocab-archetypes, staging-recipes-run-behaviour]
status-of-item: approved — APPLICATION IN PROGRESS, do NOT refresh
---
# 검증 보고 (진행 기록) — harness-100 augmentation

이 항목(`approved`)의 적용은 **여러 Phase로 나뉘어 진행 중**이다. inspection refresh 규약은
"approved + 적용 결과가 보고서에 기록됨"일 때만 항목을 제거하는데, **아직 importer·대량 임포트가
남아 있으므로 제거하지 않는다**. 여기까지의 적용 결과를 기록한다 (verify-then-proceed — 시간으로
완료를 가정하지 않는다).

## 적용된 Phase (실측 확인)
- **Phase 0.5 — 인벤토리** (`4575e11`). 코퍼스 100 하네스 속성 전수 인벤토리 +
  scaleup 계획(`docs/plans/harness-100-scaleup-plan.md`, `harness-100-attribute-inventory.md`).
- **Phase 0.6 — 중앙 어휘 GAP 18 개체** (`27c6582`). 코퍼스가 요구하나 중앙 라이브러리에 담을
  그릇이 없던 Role/Guardrail/FailurePolicy/Concept 원형 18개를 승격. `validate.py` PASS,
  개체수 **205 → 223**. 8 recipe federate 전부 **+18** 균일(ID 충돌 0 — closure 델타가 충돌 탐지기).
- **Phase 0.7 — recipe run-behaviour 3축 보정** (recipes repo commit, 이 사이클에 land).
  land된 8 recipe 전부 `hasExecutionMode`/`TestScenario`/`FailurePolicy`가 **0이던 것**을
  소스에서 보정. coverage-audit(CLAUDE.md step-7)이 잡았어야 할 누락으로, 대량 임포트 前
  차단요소였다(같은 누락을 35× 복제 방지). 상세·재검증 수치는 아래.

### Phase 0.7 재검증 실측 (inspection 독립 측정)
- 중앙 무회귀: `git status --porcelain ontology/` 무출력 · `validate.py` **PASS @223** ·
  중앙 산출물 byte-identical(ontology/ = HEAD이므로 구조적으로 자명).
- recipe federate **8/8 PASS** (per-recipe closure): 03=246 · 16=245 · 21=243 · 31=249 ·
  46=246 · contract-demo=234 · lpranging=246 · techdoc=228.
- materialize: 그룹 A(newsletter) = Execution mode/Data flow/Error handling/**Test scenarios**
  4섹션 렌더 · lpranging = Execution mode/Error handling(**Test scenarios 없음** → 조건부
  early-return 정상). 2회 결정성 byte-identical(lock 제외).
- 그룹 B 미표현 = **정당한 미표현**(은폐 아님): techdoc·contract-demo는 0-role 단일에이전트
  + dct:source 없음(reflect할 소스 표 자체가 없음), 3축 미표현에 **in-recipe 수용 사유 주석**이
  영속. lpranging은 4-role 다중에이전트, `derivedFrom core:h-multiagent`(양쪽 모드 선언)에서
  **mode-sub-agents**(spawn-and-reclaim)를 골라 cold-start dispatch 구조와 일치 + `fp-validation-fail`
  재사용. **날조 없음.**
- 어휘 통제: local FailurePolicy 6종(16 build-error · 21 language-undetected/large-codebase ·
  31 data-unavailable/no-gpu/training-divergence)은 중앙 `core:fp-*` 원형의 **근사 동의어 아님** —
  조건+복구 기계가 도메인 특수(복구 전략이 원형과 다른 machinery). 최근접은 `id:fp-data-unavailable`
  vs `core:fp-source-unavailable`/`fp-insufficient-input`이나, 31이 두 원형을 **별도로 함께 바인딩**하고
  복구가 synthetic-data 생성이라 **추가 특화지 대체가 아님** — 수용. 전부 `id:` 접두사 준수.

## 남은 일 (아직 미적용 — 항목 유지 근거)
- **P0-b**: catalog/CI glob 생성(손 나열 → 재귀 glob). batch 임포트 전 차단요소.
  계획: `docs/plans/dispatch-p0b-catalog-ci-glob.md`.
- **importer**: 코퍼스 → recipe TTL 임포터.
- **대표 ~35 임포트**: 코퍼스에서 대표 하네스 대량 반영.

## 판정
**apply — 진행 중.** Phase 0.5·0.6·0.7 적용 완료. **refresh(제거) 보류** — importer·대량 임포트
완료 후 별도 사이클에서 재판정한다. 항목 `status: approved` 유지.
