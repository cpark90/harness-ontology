---
status: reported
verdict: done
source_briefs: [docs/plans/dispatch-revfactory-p1-residual.md, docs/plans/dispatch-gap345-parallel.md]
refreshed: docs/feedback/finer-harness-decomposition-assembly.md
---
# 완료 보고 — revfactory P1 잔여 + GAP-3/4/5 land (185→202)

inspection이 두 dispatch 증분(둘 다 orchestrator 독립검증 완료, "git land는 inspection 소관"으로
핸드오프됨)을 verify-then-proceed로 land. 파일이 얽혀(workflows.ttl을 P1이 추가하고 GAP-3가
relocate) 분리 커밋이 무의미 → 통합 커밋 1건.

## Land 전 검증 (inspection 독립 실측)
- 중앙 `validate.py` → **PASS @202** (4축 green, 기본 조립순서 **12 sections**).
- **lockstep federate dry-run** (staging 공유 catalog + working-tree 중앙): 8 recipe 전부 PASS —
  lpranging 225 · techdoc 207 · contract-demo 213 · 21 217 · 16 220 · 31 222 · 03 222 · 46 222
  (전부 기존 대비 +17 = 중앙 185→202 증분과 일치).
- **전용 per-recipe catalog 4개**(잠복 결함 1의 복구분) 재실행: 222/220/222/222 **PASS** —
  결함 시절의 조용한 부분 closure(41 individuals)가 아님을 확인.
- **materialize 회귀 독립검증**: HEAD(`a8e835a`) worktree 산출물 대비 `h-multiagent` CLAUDE.md
  **삭제·변경 줄 0 / `## Data flow`만 append**. 2회 실행 **byte-identical**(결정성). 신규 렌더러는
  `h-harness-factory`에서 `## Error handling`·`## Test scenarios`·`## Data flow` 실제 출력 확인.

## Task 1 — 중앙 push  ✅
- commit **`c2b7e47`** (18 files, +732/−17): P1 잔여 13개체(생애주기·검증 workflow 2 + step 7 +
  scn 2 + fp 2, host=`h-harness-factory`) · GAP-3 `abox/core/verification/verification.ttl` 신설
  relocation(IRI 불변) · GAP-4 AssemblySection 4(order 9–12) + materialize 렌더러 4 +
  `INSTANCE_LINK_PREDICATES` · GAP-5 ONTOLOGYSTYLE 네이밍표 +11행/그룹 12→13 · per-recipe catalog 4 복구.
- push `a8e835a..c2b7e47`. **CI green**(validate-ontology).

## Task 2 — harness-recipes catalog 동기화  ✅
- 신규 `core-verification` 유닛 매핑 추가(델타는 이 3줄뿐). push된 중앙 클론 대상 재검증 8/8 PASS.
- commit **`209b3a8`** → push `829aa87..209b3a8`. **CI green**, 확장된 매트릭스로 **8 job 전부 ✓**
  (지난 증분의 매트릭스 확장이 여기서 처음 실효 — 신규 유닛 회귀축을 6개 recipe에서 자동 검출).

## 피드백 항목 refresh — `finer-harness-decomposition-assembly.md` ✅ 제거
승인 범위 **(c) 전체**가 land 완료로 실측됨 → refresh(제거). 근거:
- WorkflowStep **10개체** + `hasStep` 사용, `stepByRole` 10 · `stepGuardedBy` 9 · `stepUsesTool` 3
  (항목의 "부품-대-부품 조립 edge 부재" 해소).
- PromptSection **3개체**(SystemPrompt blob 분해).
- 조립순서 **그래프-구동**: `hasAssemblySection`/`assemblyOrder`로 12 sections, materialize는
  `resolve_assembly_order`로 읽기만 하고 미규정 시 **error**(승인된 결정2 = silent fallback 금지).
  `validate.py`에 total-order 축 상시 게이트.
- 결정성(byte-identity)은 위 독립검증으로 유지 확인.

## 유지 (refresh 대상 아님)
- `revfactory-harness-reflection.md`: P1·P2 완료이나 **P3**(augmentsRole/agentType 활용·skill 거버넌스)
  · **P4**(role-qa) 미착수 → 유지.
- `harness-100-augmentation.md`: inc4 importer(`import_corpus.py`) 미착수 → 유지.

## 후속 (orchestrator 소관)
- `execution-mode` 섹션(order 9)이 **어느 중앙 하네스에서도 미출력** — `pat-agent-teams`/
  `pat-sub-agents`/`pat-hybrid`를 `appliesPattern`으로 채택한 하네스 0. 렌더러는 검증됐고 남은 것은
  **모델링 결정**(어느 하네스가 실행모드를 선언하는가).
- `tools/ontology_lib.py:INSTANCE_CLASSES`에 `TestScenario`/`FailurePolicy` 미등록 → MANIFEST에서
  `HarnessComponent`로 표기(MANIFEST 변경을 유발하므로 별도 증분 권장).
