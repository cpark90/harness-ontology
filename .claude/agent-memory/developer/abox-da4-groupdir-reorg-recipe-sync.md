# REORG-2: recipe staging catalog → DA-4 그룹경로 동기화

REORG-1이 중앙 ABox를 `core/<group>/<type>.ttl`로 옮김 → recipe federation catalog가 옛
평면 `central/ontology/abox/core/<type>.ttl`를 참조하므로 동기화. 파일 배타:
`staging/harness-recipes/catalog-v001.xml` + docs 3(federation-design·recipes-design·ci/data-repo-validate.yml).

## catalog 경로 매핑 (root catalog와 동일 그룹, `central/` prefix만 추가)
- 13 core: concepts→vocab · capabilities/constraints/patterns/domains-tasks→spec ·
  model-configs→substrate · tools→operational · guardrails/system-prompts→behavioral ·
  workflows→process · harnesses→wholes · roles/channels→organization.
- 신규 4: observation→observational/ · memory→state/ · information-space→information-space/ ·
  assembly-sections→assembly/.
- 논리 IRI `.../data/core/<type>`는 위치독립 → `uri=` 경로만 갱신, 툴 하드코딩 無.

## ★함정: 공유 catalog에 pilot recipe 누락
- 공유 `catalog-v001.xml`엔 recipe uri 4개(lpranging·21·techdoc·contract-demo)만 있고
  pilot 03/16/31/46은 **dedicated `catalog-<name>.xml`에만** 존재.
- self-verify는 per-recipe closure(`HARNESS_ROOT_ONTOLOGY=recipe IRI` + 공유 catalog).
  recipe IRI가 공유 catalog에 없으면 owl:imports 해석 실패 → 5 pilot 검증 불가.
- 해결: 공유 catalog에 8 recipe uri 전부 consolidate(dedicated catalog는 임시·삭제가능).
  recipe uri 값 자체는 dedicated에서 그대로 복사(불변).

## 검증
`central` 심링크(→repo root) 확인 후 per-recipe closure 8건 PASS.
5 pilot: 21=200 · 16=203 · 31/03/46=205 individuals (185 중앙 신규레이아웃 + recipe-local).
lpranging/techdoc/contract-demo도 PASS. 실패 시 catalog 경로/신규유닛 매핑 점검.

## stale docs (평면→그룹 서술, 논리 IRI 위치독립 명시)
- federation-design.md: L88 표, L179 산문(`**/*.ttl`), L249 data-repo 검증 경로.
- recipes-design.md: L13 `<group>/<type>.ttl`.
- ci/data-repo-validate.yml: L16 주석, L21 예시 uri(tools→operational).
- `docs/verify/**`·`docs/feedback/**`는 immutable — 안 건드림.
