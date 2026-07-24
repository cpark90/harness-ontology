---
status: approved            # 사용자만 approved로 바꾼다
targets: [id:mode-sub-agents, id:h-multiagent, id:chan-orchestrator-inspection]
kind: decision
related: [docs/feedback/verified/execution-mode-axis-finalize.md]
---
# 결정 요청 — `h-multiagent`의 실행모드가 inspection lane을 포괄하는가

## 배경
`d40c347`에서 실행모드가 1급 축이 되고 `id:h-multiagent`가 `ho:hasExecutionMode id:mode-sub-agents`를
선언했다. dispatch lane(developer·vnv) 기준으로는 정확하다 — `chan-dispatch` 정의가 "coordination
here is the spawn/return of the subagent invocation itself"이고, 워커는 cold-start로 브리프를 받아
수행 후 회수된다.

## 충돌 (실측)
`id:mode-sub-agents`의 정의: "an agent exists **only for the span of its delegated task** and reports
back through the lead, **which is the single integration point**".

그런데 같은 하네스가 `ho:hasRole id:role-inspection` + `ho:hasChannel id:chan-orchestrator-inspection`을
보유하고, 그 채널 정의는 "run in **SEPARATE sessions** and therefore cannot use chat or spawn return
values … each side scans the channel on its own cycle"라고 명시한다. inspection lane은 **spawn되지도,
lead를 통해 보고하지도 않으며, 태스크 수명에 묶이지도 않는다** — 즉 한 하네스 안에서 실행모드 정의와
채널 정의가 서로를 반증한다.

`id:mode-hybrid`도 해가 아니다: 그 정의는 **phase-varying**("VARIES BY PHASE … exploring vs
executing")인데, `h-multiagent`의 혼합은 phase가 아니라 **동시 병존하는 lane**이다.

## 선택지
- **(A) 범위 한정 (inspection 권고)**: `mode-sub-agents` 유지 + `h-multiagent`에 TTL 주석으로
  "실행모드는 **dispatch되는** 에이전트의 topology를 기술하며, inspection은 메인테이너측 상주 세션이라
  이 축 밖"이라고 범위를 못박는다. 문서 산출 영향 0. 어휘 증식 0.
- **(B) 모드 정의 정정**: `mode-sub-agents`의 "single integration point" 문구를 dispatch되는 워커에
  한정하도록 `skos:definition` 수정. → 이 모드를 쓰는 다른 하네스(`h-workspace-synthesis`)와
  materialized CLAUDE.md **2건의 본문이 바뀐다**(byte 회귀 발생, 의도된 변경이면 수용 가능).
- **(C) 신규 mode 개체**: lane-혼합 topology를 새 `ho:ExecutionMode` 개체로 추가(축이 개체 단위
  확장이라 schema·shape 변경 0). → 다만 소비자가 `h-multiagent` 하나뿐이라
  `gr-controlled-vocabulary`·`gr-reuse-first`와 마찰.

## 권고
**(A)**. 근거: 실행모드는 "하네스가 **띄우는** 에이전트를 어떤 위상으로 조율하는가"의 축이고,
inspection은 하네스가 띄우는 대상이 아니라 별도 세션의 메인테이너 lane이다. (B)는 산출물 회귀를
동반하고, (C)는 소비자 1인짜리 어휘를 늘린다.

## 판단 필요
어느 선택지로 갈지. 승인 시 `status: open` → `approved`로 고치면 orchestrator가 developer dispatch로
적용한다. (A)~(C) 외의 방향을 원하면 여기에 적어달라.

## 사용자 피드백
(A)
