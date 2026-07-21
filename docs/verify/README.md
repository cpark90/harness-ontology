# 검증 산출물 (docs/verify)

vnv 에이전트의 **평가 리포트·증거** 위치. composition된 harness가 규격대로
(verification = `validate.py` PASS)·올바르게(validation = `retrieve.py` 재검색·capability
gap 충족·`HarnessShape` 최소구성) 만들어졌는지의 판정과 근거를 여기에 남긴다.

- **온톨로지 그래프 밖**이다 — `validate.py`/`retrieve.py`는 `ontology/`만 스캔한다.
- vnv만 쓴다(정의: `.claude/agents/vnv.md`). 온톨로지 수정은 orchestrator, git은 inspection.
- 리포트에는 **실행한 명령(인터프리터 포함)·기준·측정값(도구 출력)**을 그대로 적는다 —
  근거 없는 통과 판정 금지.
