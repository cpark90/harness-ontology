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

---

## 적용 결과 (orchestrator, 2026-07-25) — 파이프라인 step 4

### 이슈 2 → **해결됨**. 사용자가 선택지 **(A) 범위 한정**을 승인(`status: approved` + "사용자 피드백: (A)").
developer dispatch로 적용. **트리플 0 변경, TTL 주석 11줄만 추가** (`ontology/abox/core/wholes/harnesses.ttl`의
`id:h-multiagent` 블록 배너):
> 실행모드는 이 하네스가 **DISPATCH하는** 에이전트의 조율 topology를 기술한다. `id:role-inspection`은
> dispatch되는 에이전트가 아니라 **자체 상주 세션의 메인테이너측 lane**이며(`id:chan-orchestrator-inspection`의
> 파일 채널 + 상태 마커로 연동) **이 축의 범위 밖**이다.

- 기각된 선택지 미수행 확인: **(B) definition 수정 0** · **(C) 신규 개체 0**.
- **orchestrator 독립검증**: `git diff ontology/`가 전부 `+#` 주석 라인(비-주석 변경 **0**) ·
  `validate.py` **PASS @205**(triple count 불변 — 주석은 파서가 버림) ·
  `materialize.py h-multiagent` 산출 **트리 전체 byte-identical**(HEAD 버전을 stash로 뽑아 `diff -r` 대조).
- **알려진 트레이드오프**((A)의 의도된 성질): 범위 한정이 `h-multiagent` **로컬 주석**이라 `mode-sub-agents`를
  읽는 다른 소비자(`h-workspace-synthesis`, retrieve pack)에는 노출되지 않는다. 같은 충돌이 다른 하네스에서
  재발하면 (B)/(C) 재검토 신호.

### inspection 사후 검증 (2026-07-25) — 적용분 독립 실측
per-item 검증 보고서 `verified/execution-mode-scope-multiagent.md`(refresh로 제거됨)의 결론을 여기 보존한다.
inspection이 (A)를 worktree에서 먼저 시뮬레이션한 뒤 orchestrator 적용분을 재측정했고 결과가 일치했다:
`git diff ontology/`의 **비-주석 변경 줄 0** · `validate.py` **PASS @205** · `materialize.py` 4 하네스
(`h-multiagent`·`h-workspace-synthesis`·`h-peer-mesh`·`h-harness-factory`) **전부 byte-identical** ·
`retrieve.py` 투영 동일(시드 고정 비교) · 기각 선택지 (B) definition 수정 0, (C) 신규 개체 0 ·
권고했던 옵션 TBox 범위 문장은 **미채택**(승인 문언이 (A)이므로 정당 — 다만 범위 한정이 로컬 주석에만
존재한다는 트레이드오프는 위 orchestrator 기록과 동일 인식).
**부수 발견**: 이 검증 중 `retrieve.py` 산출이 **비결정적**임을 확인(같은 질의 10회 → 10종, 시드 고정 시 동일).
별도 항목 `docs/feedback/retrieve-nondeterministic-pack.md`(`status: open`)로 상신 — 파급효과를
retrieve diff로 검증하는 방법의 신뢰성에 직결되므로 우선 처리 권고.

### 이슈 1 → **해결됨**. `docs/plans/dispatch-execution-mode-axis.md` 갱신 완료
「선언 결과」표·GAP-b 판정은 이미 최종 상태(`h-workspace-synthesis` = `mode-sub-agents`)로 갱신돼 있었고,
이번에 남아 있던 **문서영향 수치(3 → 4 하네스)** 를 정정하고 정정 사유를 명시했다.

> 이 증분은 **미커밋**이다(orchestrator는 git을 만지지 않는다). inbox 항목 `execution-mode-scope-multiagent.md`의
> `status`/verified 이동은 **inspection 소관** — 적용 결과가 위에 기록됐으므로 다음 사이클에 refresh 가능하다.
