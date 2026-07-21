# inspection 역할 메모리

조사 + 피드백 파급효과 검증 + git 담당 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/inspection.md`. 그래프 지도·함정·규약을 파일로 추가하고 아래에 한 줄로 인덱스한다.

- 조사 전용: `docs/feedback/**`와 이 메모리 외 파일 생성·수정 금지. git(add/commit/branch/push)
  전담(사용자 요청 시). 피드백 파급효과는 `retrieve.py` projection + `validate.py`로 검증해
  `docs/feedback/verified/`에 보고. 조사는 `retrieve.py` pack에서 시작(전체 로드 금지).

<!-- 학습 인덱스 (한 줄씩) -->
