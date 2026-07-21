# 조사 lane (docs/feedback/inquiries)

orchestrator ↔ inspection **조사 채널**. 세션이 분리되어 대화·spawn 반환값을 쓸 수 없으므로,
orchestrator가 그래프·문서 조사가 필요한 질문을 항목으로 남기고 inspection이 같은 파일에
답을 쓴다. **사용자 피드백 lane과 다른 어휘**를 쓴다 — 섞지 않는다.

수명주기: `open` → (inspection) `answered` → (orchestrator, 소비 후) `closed` →
(inspection, 다음 사이클) 제거.

- **orchestrator**: `{q}.md`에 `status: open`으로 질문을 남긴다(관련 노드·맥락 포함).
  inspection이 `answered`로 채운 답을 소비한 뒤 `status: closed`로 태깅한다.
- **inspection**: 사이클마다 `status: open`을 스캔해 `retrieve.py` pack 기반으로 조사하고,
  같은 파일에 `## 답`(결론 + 근거 node id 또는 `file:line`)을 채운 뒤 `answered`로 바꾼다
  (쓰기는 wip→rename). 불명확하면 추측하지 말고 답에 한계를 명시한다.
  `closed` 항목만 다음 사이클에 제거한다 (**closed 전 제거 금지** — custody transfer).

## 항목 형식

```
---
status: open        # open → answered(inspection) → closed(orchestrator)
targets: [id:…]     # 조사 대상 노드(있으면)
---
# 질문: {한 줄}
{맥락}

## 답
(inspection이 채움: 결론 + 근거 node id / file:line)
```
