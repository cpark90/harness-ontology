# recipe catalog/CI를 glob 생성으로 전환 — land 재검증 + 형상관리 (inspection)

P0-b(§B16 recipe판, `dispatch-p0b-catalog-ci-glob.md`) land 시 재사용 지식. 2026-07-25.

## 구조 (진실 = 디스크 `recipes/*/`)
`tools/gen_recipe_catalog.py`(중앙 tool, recipe repo가 validate.py처럼 pull)가 recipe repo의
catalog-v001.xml + CI matrix를 생성. root IRI는 각 recipe TTL `owl:Ontology` 헤더에서 rdflib로
읽음(dirname 가정 아님). central 블록은 **중앙 자신의 catalog-v001.xml을 `central/` prefix 붙여 복사** →
중앙 core 유닛 추가 시 재생성만으로 전파(REORG 드리프트 근본 수리).
- `--check` = 드리프트 가드(디스크≠catalog면 exit1). `--print-matrix` = JSON(CI `fromJSON`). `--repo <dir>`로 대상 지정.

## land 순서 (★중앙 먼저 — CI 의존성)
published `validate.yml`의 `discover` job이 **`central/tools/gen_recipe_catalog.py --check`**를 돌린다
(central@main을 checkout). 따라서 **① 중앙 push(생성기)** → **② published push** 순서 필수.
published 먼저 push하면 그 CI가 central@main에서 생성기를 못 찾아 실패.

## published harness-recipes repo에는 dedicated catalog가 애초에 없다 (브리프 정정)
브리프가 "잉여 `catalog-{03,16,31,46}.xml` 4개를 published에서 삭제"라 했지만, **published repo엔
catalog-v001.xml + validate.yml뿐**이다(clone 후 `git ls-files|grep catalog` = 1건). 그 4개는
**staging 작업트리 전용 leftover**(gitignored, 한 번도 push된 적 없음) → published 삭제 대상 없음.
staging은 자체 git repo가 아니라 중앙에 gitignore된 디렉토리(`git -C staging …`는 중앙 .git으로 walk-up).
published는 clone해서 파일 copy→commit→push.

## push 전 CI 재현 (verify-then-proceed)
push 전 중앙에서 `/usr/bin/python3 tools/gen_recipe_catalog.py --repo <published-clone> --check`로
CI 드리프트 가드를 그대로 재현(exit0 확인). validate.yml은 `yaml.safe_load`로 문법 확인.

## 가드 negative control (파이프 금지 — `cmd>out 2>&1; rc=$?`)
① catalog에서 recipe 1줄 제거 → `--check` exit1. ② 디스크에 recipe dir 추가(catalog 미재생성) →
exit1. 둘 다 복원 후 exit0. (파이프로 exit code 재면 오측정.)

## B19 해소 확인 = 실제 dispatch 발동
`gh workflow run validate.yml --repo cpark90/harness-recipes`가 **수락**되면(이전엔 422) B19 해소.
dispatch run은 full-gate(9 jobs = discover 1 + validate 8), event=workflow_dispatch, success.
push run도 9 jobs green. central 5084827 / published d9ebf0c.

## 발견(미수리, 보고만): `docs/ci/data-repo-validate.yml` 이중 stale
retired **pure-data-repo** 패턴 템플릿(레시피 repo 패턴이 대체). 두 곳 stale:
- L38 `HARNESS_ROOT_ONTOLOGY: …/data/lpranging` — lpranging은 이제 **recipe**(`…/recipes/lpranging`), data 도메인 아님.
- L35 `CENTRAL_REPO: hhmm2728/harness_ontology` — 소유자·언더스코어 모두 stale(정답 `cpark90/harness-ontology`).
developer는 L38만 지목, L35는 추가 발견. 파일은 clean(committed).
