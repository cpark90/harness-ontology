---
source: docs/feedback/execution-mode-scope-multiagent.md
verdict: apply
targets: [id:h-multiagent, id:mode-sub-agents, ho:hasExecutionMode]
---
# 검증 보고 — `h-multiagent` 실행모드 범위 한정 (선택지 A 승인)

사용자 승인: **(A) 범위 한정**. 아래는 그 선택을 실제 편집으로 시뮬레이션해 측정한 파급효과와,
orchestrator가 developer dispatch로 그대로 실행할 적용 계획이다.

## 파급효과 (impact)
- **그래프**: TTL 주석은 파서에 진입하지 않으므로 트리플 증감 0, 개체 수 **205 불변**.
- **대상 노드를 참조하는 이웃**: `id:h-multiagent`를 `ho:derivedFrom`하는 하네스 3
  (`h-peer-mesh`·`h-workspace-synthesis`·`h-harness-factory`) — 상속되는 것은 트리플이지 주석이
  아니므로 영향 없음. 실측으로 4 하네스 산출물 전부 무변경(아래).
- **레시피**: `hasExecutionMode`·`mode-*`를 참조하는 published/staging 레시피 **0** → federation 무영향.

## 정합성 (실측, HEAD `3c41dd9` 기준 worktree 시뮬레이션)
- `validate.py` → **PASS @205** (주석 + 아래 옵션 TBox 문장을 함께 적용한 상태에서도 동일).
- `materialize.py` 4 하네스(`h-multiagent`·`h-workspace-synthesis`·`h-peer-mesh`·`h-harness-factory`)
  → CLAUDE.md·MANIFEST **완전 동일(byte-identical)**. 즉 (A)는 산출물 회귀 0 — 승인 근거였던
  "(B)는 산출물 2건 본문이 바뀐다"와 대비되는 (A)의 이점이 실측으로 확인됐다.
- `retrieve.py` 투영: **동일**(단, 아래 §부수 발견의 이유로 `PYTHONHASHSEED` 고정 비교 필요).
- drift 없음: 신규 클래스·프로퍼티·개체 0, 근사 동의어 0, 중복 prefLabel 0.

## 적용 계획 (orchestrator 실행용)

### 필수 — `ontology/abox/core/wholes/harnesses.ttl`, `id:h-multiagent a ho:Harness ;` 바로 위에 주석 삽입
```
# SCOPE of ho:hasExecutionMode below: the execution mode describes the topology
# of the agents this harness itself SPAWNS and coordinates (the dispatch lane:
# developer / vnv, spawned per brief and reclaimed). The inspection lane is
# deliberately outside this axis -- id:role-inspection runs as a separate,
# standing maintainer session that is never spawned by the lead and coordinates
# over durable file channels (id:chan-orchestrator-inspection), so the "only for
# the span of its delegated task / single integration point" wording of
# id:mode-sub-agents is not contradicted by it -- it simply does not range over it.
```
(ONTOLOGYSTYLE의 산문-한글/그래프값-영어 규칙에 따라 주석도 영어. 기존 harnesses.ttl 주석 스타일과 동일.)

### 권고(선택) — `ontology/tbox/harness.ttl:595` `ho:hasExecutionMode`의 `skos:definition` 끝에 1문장 추가
```
SCOPE: the mode ranges over the agents the harness itself spawns and coordinates; a standing
maintainer session that the harness never spawns and that coordinates over durable file channels
instead of spawn/return is outside this axis.
```
- **왜 권고하는가**: 주석은 저작자만 본다. 같은 혼동이 다른 하네스에서 재발하지 않으려면 범위 규정이
  **속성 정의(스키마)** 에 한 번 있어야 한다. 실측상 산출물·투영 영향 **0**이라 (A)의 무회귀 성질을
  깨지 않는다.
- **왜 필수가 아닌가**: 사용자가 승인한 (A)의 문언은 "`h-multiagent`에 주석"이다. 스키마 문구 추가는
  범위 확장이므로 orchestrator 판단으로 채택/보류한다. 보류해도 결정은 이행된다.

### 적용 후 검증
```bash
/usr/bin/python3 tools/validate.py                              # PASS 205
for H in h-multiagent h-workspace-synthesis h-peer-mesh h-harness-factory; do
  /usr/bin/python3 tools/materialize.py $H --out /tmp/x_$H; done # 직전 산출물과 diff 0
```

## 판정
**apply** — 승인된 (A)를 위 편집 그대로 적용하면 된다. 그래프·산출물 회귀 0, 결정 요청 잔여 없음.

## 적용 확인 (2026-07-25, orchestrator가 병행 적용 → inspection 사후 검증)
이 보고서를 쓰는 사이 orchestrator가 (A)를 이미 적용했다(문구는 위 계획과 다르나 **내용 동치** —
"실행모드는 이 하네스가 DISPATCH하는 에이전트의 topology이고 `role-inspection`은 상주 세션이라 축 밖").
inspection이 적용분을 독립 실측한 결과:
- `git diff ontology/`의 **비-주석 변경 줄 0** (순수 주석 11줄 추가) → 트리플 불변.
- `validate.py` **PASS @205**.
- `materialize.py` 4 하네스 전부 **byte-identical** (기준 HEAD `3c41dd9`).
- `retrieve.py` 투영 **동일**(`PYTHONHASHSEED=0` 고정 비교).
- 기각된 선택지 미수행 확인: (B) `skos:definition` 수정 **0**, (C) 신규 개체 **0**.
- **권고했던 옵션 TBox 문장은 미채택**(`ontology/tbox/harness.ttl` 변경 0). 승인 문언이 (A)이므로
  정당한 선택이며, 그 결과 범위 한정은 `h-multiagent` **로컬 주석에만** 존재한다 — 같은 충돌이 다른
  하네스에서 재발하면 (B)/(C) 재검토 신호라는 점을 orchestrator도 적용 결과에 기록했다.

⇒ 항목 `docs/feedback/execution-mode-scope-multiagent.md`는 approved + 적용 완료. **git land 후**
inspection이 항목과 이 보고서를 refresh한다(적용은 됐으나 아직 미커밋 — 시간으로 가정하지 않는다).

## 부수 발견 (별건, 이 적용을 막지 않음) — `retrieve.py` 산출이 비결정적
이 검증 중 발견: **같은 트리·같은 질의로 10회 실행하면 10개 산출이 모두 다르다**(md5 10종).
`PYTHONHASHSEED=0`으로 고정하면 3회 모두 동일 → 원인은 파이썬 문자열 해시 랜덤화가 **동점 정렬의
tie-break**로 새는 것. 근거: `tools/retrieve.py:103`·`177`·`185`가 `key=lambda x: x[1]`처럼
**점수만** 키로 쓰므로 동점 노드의 순서가 set/dict 순회 순서에 좌우된다. 노드 수(예산 34)는 같지만
**어떤 동점 노드·엣지가 팩에 실리는지가 실행마다 달라진다.**
- **왜 중요한가**: "요청 → 예산 캡 팩"이 이 repo의 context-rot 방어인데, 같은 요청이 실행마다 다른
  컨텍스트를 준다(재현 불가). 또한 **파급효과 검증을 `retrieve` diff로 하는 방법 자체가 무효**가 된다 —
  이번에도 시드 고정 전에는 무영향 편집이 유의미한 diff로 보였다.
- 제안 수정: 정렬 키에 안정적 2차 키를 추가(`key=lambda x: (-score, str(node))`). 별도 항목
  `docs/feedback/retrieve-nondeterministic-pack.md`(`status: open`)로 상신했다.
