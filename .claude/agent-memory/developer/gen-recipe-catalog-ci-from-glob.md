# recipe catalog + CI matrix 를 glob에서 생성 (레지스트리 표류 대책의 recipe판)

recipe 나열이 3곳(공유 `catalog-v001.xml` · published `validate.yml` matrix · 중앙
`docs/ci/data-repo-validate.yml`)에 손으로 중복 → REORG 때 dedicated catalog 4개 누락으로
**부분 closure**가 에러 없이 통과한 전례. `tools/gen_recipe_catalog.py`가 디스크
`recipes/*/`를 단일 진실로 삼아 catalog(양블록) + CI matrix를 생성.

## 핵심 함정 (재발 주의)
- ★**XML 주석에 `--`(연속 하이픈) 금지** — well-formed 위반. 게다가 `_parse_catalog`은
  `ET.ParseError`를 **삼키고 {} 반환**→`_load_via_imports` False→**glob fallback**으로
  조용히 떨어진다(recipe 안 로드=federation 파손, 에러 0). 그래서 malformed catalog는
  치명적 silent-fail. 생성기 주석에서 `--repo`/`--check`를 프로즈로 풀어 씀. **생성 후
  반드시 `ET.fromstring(gen_text)`로 well-formedness 자체를 assert**.
- 로더는 `<uri>`의 `name`/`uri` 속성만 읽음 → 주석·정렬·엔트리 순서는 federation에
  무관, **오직 `--check` 멱등성**에만 영향. 그래서 "생성물==수기"의 진짜 잣대는 byte가
  아니라 **{name→uri} dict 동일 + 8 federate 개체수 동일**(회귀 0). 실측: 29 entry
  (21 central + 8 recipe) dict 완전 일치, 8/8 PASS 카운트 baseline과 동일.

## 설계 결정 (단일소스 2블록 다 생성)
- catalog는 **central 블록도** 생성기가 소유: 생성기가 `central/catalog-v001.xml`을
  읽어 각 엔트리에 `central/` prefix만 붙여 재emit. 이게 원래 REORG 버그(central 블록
  손-동기화 표류)의 근본 수리 — central이 core unit 늘면 regenerate 한 방에 전파, `--check`
  가드. 생성기는 CENTRAL repo `tools/`에 둠(데이터 repo가 central 툴 pull = D4 철학,
  `__file__.parent.parent`=central checkout, CI에선 `central/tools/…`로 호출·`--repo .`).
- recipe root IRI는 **디렉토리명 가정 금지**: rdflib로 각 `<name>.ttl` 단독 parse(파싱은
  owl:imports 따라가지 않음)→`owl:Ontology` subject 1개를 읽고 `.../recipes/<dirname>`
  관례와 **불일치 시 hard error**(silent guess 금지).
- 결정성=recipe는 dirname 정렬, central은 문서순 보존. 멱등=재실행 diff 0.

## 가드 실효(negative control) 2종 다 확인
- catalog에서 recipe 1줄 삭제 → `--check` exit 1(diff에 빠진 uri 표시).
- recipe dir 추가 후 regenerate 안 함 → disk 9 vs catalog 8 → exit 1. (둘 다 CI
  `discover` job의 `--check` step이 잡음.)

## CI 스케일 (path-filter + shard, D4 2경로)
- `validate.yml`: `discover` job(central+recipe checkout, `--check` 가드 step, 그다음
  `--print-matrix`로 전 IRI JSON) → `validate` job이 `fromJSON`으로 matrix. 세번째
  손-복사본 없음(생성기 라이브 호출).
- **PR이 recipe dir만 건드리면** 그 recipe만(path-filter, git diff base…head basename
  매칭); **catalog/워크플로/recipes 밖** 변경이면 **전 recipe full**(central-affecting).
  push[main]·`workflow_dispatch`도 full. → union 불변식은 전체에서만 성립(D4).
- ★**B19**: `workflow_dispatch: {}` 트리거 추가 — central만 바뀐 라운드에 `gh workflow
  run`으로 연합 full gate 발동(없으면 422). shard=`max-parallel: 20`.
- inline python-in-bash 함정: `python3 - <<'PY'`(stdin=스크립트)와 `<<<`(stdin=data)는
  **동시 불가**. discover pick은 순수 python heredoc + env(EVENT/BASE_SHA/HEAD_SHA) +
  subprocess git diff로. 진단은 stderr로(`$GITHUB_OUTPUT`엔 `recipes=` 만).

## 남은 GAP (inspection/후속)
- dedicated `catalog-<recipe>.xml` 4개(03/16/31/46)는 이제 vestigial 잉여 드리프트원 —
  공유 catalog가 8 전부 담음. **inspection이 삭제**(git 전담). 생성기는 안 만듦.
- 중앙 `docs/ci/data-repo-validate.yml`은 stale(`HARNESS_ROOT_ONTOLOGY=…/data/lpranging`,
  retired) — recipe와 무관한 generic data-repo 템플릿이라 이번 범위 밖, 별건 보고.
- 100 스케일: matrix 개별 job은 GitHub 256 한도 내 OK지만 runner 분 과금 → PR path-filter가
  상시 방어, full gate만 `max-parallel` bound. 더 크면 shard grouping(N recipe/job) 필요.
