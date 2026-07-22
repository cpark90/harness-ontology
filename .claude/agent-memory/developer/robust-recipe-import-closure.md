# robust-recipe-import-closure

recipe(staging/harness-recipes) 하네스가 중앙 core를 `owl:imports`할 때 **개별 core 유닛을
열거하면 fragile**: 중앙이 새 core 유닛(roles.ttl/channels.ttl 등)을 추가하고 seed harness가
그걸 `hasRole`/`hasChannel`로 참조하면, 그 개체들이 `derivedFrom core:h-multiagent` 계보를
타고 recipe union에 **bare IRI**로 들어오는데 recipe catalog+imports엔 그 유닛이 없어 정의
triple이 안 실려 → SHACL missing prefLabel → validate FAIL, materialize refuse. 중앙 자체
validate.py는 root catalog가 완결이라 PASS라 조용히 recipe만 깨진다(P0 회귀).

## robust fix = 중앙 ROOT 온톨로지를 import (열거 대신)
- recipe ttl: 개별 `.../data/core/<type>` 나열 전부를 **단일** `owl:imports
  <https://harness-ontology.dev/ontology>`(중앙 root IRI, `ontology/harness-ontology.ttl`가
  선언—주의: `.../ontology`지 `.../harness-ontology` 아님)로 교체. root가 schema+모든 core
  유닛+authored를 import하므로 **전체 중앙 스토어가 transitive 해소** → 새 core 유닛 자동 전파,
  다시는 조용히 안 깨짐.
- recipe catalog(`staging/harness-recipes/catalog-v001.xml`): root IRI + schema + 모든 core
  유닛(roles/channels 포함) + `data/authored`를 `central/...`로 매핑. **중앙 root
  catalog-v001.xml과 같은 목록 유지**가 규칙. 없는 파일(authored.ttl 미존재)은 loader가
  `os.path.exists` false로 graceful skip(하드페일 아님)이라 매핑해둬도 안전·미래대비.
- loader(`tools/ontology_lib._load_via_imports`)는 root IRI서 BFS로 owl:imports 해소, 미매핑
  IRI는 `catalog.get`→None→skip. 그래서 root import 방식이 안전.

## 게이트 실행 함정
- gate cmd는 **repo root에서** 실행: `HARNESS_CATALOG=staging/harness-recipes/catalog-v001.xml`는
  cwd 상대라 `cd staging/...` 하면 이중경로로 catalog 못찾아 glob fallback(중앙만 76 로드)→
  위양성 PASS. 반드시 repo root cwd.
- 테스트 fixture: `ln -sfn ../.. staging/harness-recipes/central`(→repo root), 게이트 후 `rm`.
  payload는 symlink-free 유지.
- `staging/`는 **git-ignored**(`git check-ignore staging/` 확인). 그래서 recipe 편집은 git에
  안 보이고 "central untouched" git 게이트는 자동 충족. 반대로 recipe 변경은 커밋 대상 아님.

## 검증 수치(이번 회귀)
- fix 전 lpranging union: SHACL FAIL(id2:role-vnv 등 bare central role/channel prefLabel 없음).
- fix 후: lpranging 94 individuals PASS, materialize 성공(CLAUDE.md+3 agent md+실 tool code
  docgraph.py/sim_grid_reservation.py byte-match impl+scaffold 3), 2런 byte-identical.
  techdoc 82 individuals PASS, materialize 성공. 중앙 validate 불변 PASS(수치는 중앙 진화 따라감).
- 주의: docs/recipes-design.md(중앙)는 아직 "열거" 패턴을 서술 → Option A 채택 시 문서 drift.
  중앙 문서 수정은 developer 경계 밖(orchestrator 소관)이라 보고만.
