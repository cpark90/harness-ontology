# 검증 lane (docs/feedback/verified)

inspection → orchestrator **판정 보고** 채널. inspection이 inbox(`docs/feedback/*.md`)의
피드백 항목을 `retrieve.py` projection + `validate.py`로 검증해 파급효과·정합성·적용 계획·
verdict를 여기에 쓴다. **온톨로지는 이 lane에서 바뀌지 않는다** — orchestrator가 승인·완료된
보고만 읽어 **developer dispatch로** `ontology/abox/`에 적용한다(직접 편집 아님).

- 작성 규약: `{item}.wip.md`로 Write → 완료 시 `{item}.md`로 rename (rename = 완료 선언).
  orchestrator는 `*.wip.md`를 처리하지 않는다.
- verdict: `apply` / `apply-with-changes` / `needs-decision`.
- 적용 게이트: **inbox 항목이 `status: approved`(사용자만 태깅)** + 보고 verdict가
  `apply`/`apply-with-changes` + 보고 완료(rename) — 셋 다일 때만 orchestrator가 developer
  dispatch로 적용한다.
- 적용 후 orchestrator가 이 보고서에 **적용 결과를 기록**하고, inspection이 다음 사이클에
  항목·보고서를 refresh(제거)한다.

보고 형식은 `.claude/agents/inspection.md` §B 참조.
