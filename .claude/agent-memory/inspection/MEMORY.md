# inspection 역할 메모리

조사 + 피드백 파급효과 검증 + git 담당 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/inspection.md`. 그래프 지도·함정·규약을 파일로 추가하고 아래에 한 줄로 인덱스한다.

- 조사 전용: `docs/feedback/**`와 이 메모리 외 파일 생성·수정 금지. git(add/commit/branch/push)
  전담(사용자 요청 시). 피드백 파급효과는 `retrieve.py` projection + `validate.py`로 검증해
  `docs/feedback/verified/`에 보고. 조사는 `retrieve.py` pack에서 시작(전체 로드 금지).

<!-- 학습 인덱스 (한 줄씩) -->
- [refresh 판정 + 안전 커밋 절차](refresh-and-git-baseline.md) — refresh는 inspection 후속 완료까지 유지; 항목은 baseline 커밋에 보존 후 별도 커밋으로 git rm; **병렬 dispatch 중 scoped land 절차**(add -A 금지·공유 developer/MEMORY.md diff 확인·문서만 커밋이면 validate 과도기 무관)
- [물리 repo 분할 실행 (federation)](federation-physical-split.md) — cpark90/harness-ontology(중앙)+harness-data-<domain>; gh를 ~/.local/bin에 설치; 연합 validate 재현(catalog env); 중앙 커밋 선행 후 외부 확인 뒤 제거(Step5=developer); classifier git 차단은 재시도
- [연합 lockstep](federation-lockstep.md) — 중앙 core 추가·**파일 이동** 모두 recipe catalog 동반 필요; push 전 로컬 8-recipe federate 게이트(staging central symlink); recipe 추가 시 catalog+CI 매트릭스 둘 다 갱신(1:1 점검 명령 포함)
- [materialize 회귀 독립검증](materialize-regression-check.md) — worktree(직전 커밋) vs working tree 산출물 diff로 append-only/byte-identity 자체 재현; harness 인자는 bare slug
- [품질 축 감사 레시피(Q1/Q2/Q3)](quality-axis-audit-recipes.md) — validate가 못 보는 축 측정법: `reason=True` 필수(173 vs 205)·`INSTANCE_CLASSES` 미등록 7클래스/32개체·tokenEstimate fallback 15가 예산을 갉는 계산·라벨 Jaccard는 작명 패밀리 노이즈; 도구를 돌려야만 보이는 3결함(예산 조기 break·deprecated 무자각 랭킹·산출물 IRI 유출)·negative control 트리 구성법
- [web UI 쓰기 경로 감사](webui-write-path-audit.md) — 저장=삭제(82/205·375트리플) 를 **read-only**로 재현하는 3층(plan_upsert·그래프집계·개체별 SHACL); 게이트 분류 27 조용/55 거부; 브리프 수치 불신(chan-dispatch 9→**6**줄); **레지스트리 표류**가 반복 패턴이라는 진단과 불변식 1줄 처방; 개체계수 수정의 파급=worktree materialize diff + recipe별 전용 catalog로 8건 federate
- [어휘 증가 증분(원형 추가) 재검증](vocab-growth-increment-audit.md) — 연합 closure 델타 **+N 균일**이 ID충돌 탐지기; 원형↔로컬 인스턴스를 잇는 **술어가 없다**(`ho:specializes`는 Harness 전용)는 TBox GAP; `id:` 참조는 materialize만 해소하고 **retrieve 팩엔 그대로 샌다**(32/17→41/24); carrier 산출물은 "정확히 기대만큼" 바뀌었는지도 셀 것; recipes CI는 `workflow_dispatch`가 없어 중앙 push로 안 돈다
- [recipe catalog/CI glob 생성 land](recipe-catalog-glob-land.md) — `gen_recipe_catalog.py`가 디스크 `recipes/*/`에서 catalog+CI matrix 생성(central 블록은 중앙 catalog `central/` prefix 복사=REORG 드리프트 근본수리); ★land 순서 **중앙 먼저**(published CI가 central@main 생성기로 `--check`); published repo엔 dedicated catalog 애초에 없음(staging leftover, 삭제대상 0); push 전 `--repo <clone> --check`로 CI 재현; 가드 negative control 파이프 금지; B19=`gh workflow run` 수락(이전 422)+full-gate 9jobs; `docs/ci/data-repo-validate.yml` 이중 stale(L38 data/lpranging·L35 hhmm2728 owner) retired 템플릿
- [외부 소스 repo 조사·라이선스 게이트](external-source-survey.md) — NOASSERTION은 LICENSE 본문을 직접 읽어야(CC0/NC-ND/MIT 혼재); NC-ND는 채택 불가; 수확 우선순위는 우리 얇은 축
