# vnv 역할 메모리

verification & validation 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/vnv.md`. 검증 노하우를 파일로 추가하고 아래에 한 줄로 인덱스한다.

- composition 결과물의 검증(규격 부합 = `validate.py` PASS)·평가(목적 부합 = `retrieve.py`로
  재검색·capability gap 충족·`HarnessShape` 최소구성) 판정만. 온톨로지·설계 편집 없음.
- 리포트는 `docs/verify/`에. 근거 없는 통과 금지 — 실행한 명령·측정값(도구 출력)을 명시.
- 도구는 `rdflib` 등이 있는 인터프리터로(예: `/usr/bin/python3`). 셸 기본 python3엔 없을 수 있음.

<!-- 학습 인덱스 (한 줄씩) -->
- [webui 검증 재현 절차](webui-smoke.md) — Svelte/Vite+FastAPI web UI 빌드·서버·Docker 스모크, 무결성 sha256 대조, ttl_writer dry 라운드트립, static-missing/dockerignore 결정거리.
