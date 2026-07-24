---
status: reported
verdict: done
source_brief: docs/plans/dispatch-execution-mode-axis.md
opens: docs/feedback/execution-mode-scope-multiagent.md
---
# 완료 보고 — execution mode를 하네스의 1급 축으로 (202→205)

inspection이 execution-mode 증분을 verify-then-proceed로 land. 실행모드가
`ho:appliesPattern` + concept 태그 조인으로 복원되던 인코딩에서 **1급 속성
`ho:hasExecutionMode`** 로 승격됐고, TBox가 두 축의 conflation을 명시적으로 금지한다.

## Land 전 검증 (inspection 독립 실측)
- 중앙 `validate.py` → **PASS @205** (4축 green).
- **materialize 회귀**: 신규 선언 하네스 **2개**(`h-multiagent`·`h-workspace-synthesis`) 각각
  CLAUDE.md **+6줄 / 삭제·변경 0줄**, MANIFEST **byte-identical**(모드는 컴포넌트가 아니라
  `all_components` 불변). 기준선은 직전 커밋 `3e3ae0c` worktree 산출물.
- **lockstep**: 신규 유닛 없음(3 mode를 `spec/patterns.ttl`에 co-locate) → **recipe catalog 무변경**.
  push 전 working-tree 대상 8 recipe federate PASS(전부 +3), push 후 **fresh clone(`d40c347`) 대상
  8 recipe 재검증도 전부 PASS**.
- deprecated 처리된 `pat-sub-agents`/`pat-agent-teams`/`pat-hybrid`를 참조하는 레시피 **0**
  (published·staging 양쪽 grep) → 폐기가 federation을 깨지 않음.

## Task — 중앙 push  ✅
- commit **`d40c347`** (12 files, +283/−42): `ho:ExecutionMode` 클래스 + `ho:hasExecutionMode`
  (HarnessShape `sh:class`, `sh:in` enum 없음 = 개체 단위 확장) · mode 개체 3 · pat-* 3 deprecated
  (연결 유지) · 바인딩 4(h-multiagent·h-workspace-synthesis=sub-agents, h-peer-mesh=agent-teams,
  h-harness-factory=hybrid) · `as-execution-mode` 렌더 경로 전환 · `ontology_lib`에 클래스 등록.
- push `3e3ae0c..d40c347`. **CI green**(validate-ontology).
- recipes repo: **커밋 없음**(catalog 델타 0). 직전 증분에서 확장한 8-recipe 매트릭스는 다음 recipes
  push 때 다시 걸린다 — 이번 중앙 변경분은 위 fresh-clone 8/8로 대체 확인했다.

## 남은 정합성 이슈 (inspection 지적, orchestrator 소관)

### 1. 브리프 실행결과 표가 stale (기록 불일치)
`docs/plans/dispatch-execution-mode-axis.md`의 「선언 결과」표와 GAP-b 판정은
**"`h-workspace-synthesis` = 미선언 유지, developer의 보류 판단이 옳다"** 로 확정돼 있으나, 실제
그래프는 그 뒤(브리프 21:29 → 파일 23:55)에 `mode-sub-agents`로 **바인딩됐다**. 정정 근거는
developer 메모리(`execution-mode-first-class-axis.md`: "`chan-workspace`는 hand-off medium 축이지
spawn topology 축이 아니다" + `derivedFrom`·`wf-multiagent`·`role-synthesizer` 문언)에만 남아 있다.
같은 브리프의 "문서 영향 3 하네스" 기술도 실측 **4**(2 하네스가 신규 선언)와 어긋난다.
→ 브리프는 orchestrator 소유 문서라 inspection이 고치지 않는다. **표·GAP-b·문서영향 수치 갱신 필요.**

### 2. `mode-sub-agents` 정의와 `chan-orchestrator-inspection` 정의의 충돌 (결정 요청 상신)
`h-multiagent`의 선언은 dispatch lane(developer·vnv) 기준으로는 정확하지만, 같은 하네스가 보유한
inspection lane과 어긋난다 — 상세·선택지는 inbox 항목 `execution-mode-scope-multiagent.md`
(`status: open`)로 올렸다. 이번 land를 막지 않는 **정의 정합성** 문제다.
