# lpranging reference-model 검증 재현 절차 + 함정

principle 검증: **recipe는 generalized parts + methodology + explanation만 저장, concrete
build document는 저장 안 함**; materialize가 external ref를 build time에 **fetch**(없으면
`.ref` stub). faithful-reflection의 후속 전환(in-recipe vendoring → external absolute ref).
판정: `docs/verify/lpranging-reference-model.md` = **pass-with-notes**. 전부 `/usr/bin/python3`.

## 핵심 축 = 저장물 vs fetch (principle 부합)
- **no-stored-artifacts proof**: recipe dir가 정확히 `{lpranging.ttl, README.md}` 2개뿐
  (`find` = no .py/SKILL.md/scaffold body/impl/). `grep -nE '"recipes/'` TTL = NONE
  (repo-relative in-recipe ref 잔존 0). 모든 impl/scaffold/artifactTemplate ref는 external
  absolute `/home/cpark/git/agrtls/device_harvest_lp/lpranging/...`.
- **fetch = byte-identical**: materialize 후 emitted 8개(2 impl+3 scaffold+3 skill)를 real
  source와 `cmp` → 전부 identical. MANIFEST status=resolved. **주의**: scaffold `docs/ONTOLOGY.md`는
  경로에 `scaffold/` marker 없어 `_scaffold_dest`가 basename fallback→ tree root `ONTOLOGY.md`.
- faithful-reflection 시절엔 agent .md가 render라 byte-differ였는데, 이번 rework는 skill을
  **artifactTemplate로 byte-copy fetch**하므로 SKILL.md도 byte-identical(전환 포인트).

## fetch-or-stub (source ABSENT 재현)
- `_resolve_ref_path`(materialize.py:445) = **단일 공유 resolver**(repo→recipe→absolute→None)
  for impl/scaffold/skill 모두. None이면 emitter가 `<dest>.ref` stub(fail-safe, no crash).
- 재현: **real recipe 안 건드림** — staging 전체 scratch cp → **central 심링크 재생성 함정**:
  `cp -rL`은 central 심링크를 dir로 deref함 → scratch에서 `rm -rf central; ln -sfn <repo-root> central`
  다시 만들어야(안 그럼 union FAIL). scratch ttl에서 impl/scaffold/skill 각 1개 ref를
  nonexistent path로 치환 → materialize **exit 0**, 정확히 3 stub(`tools/x.ref`,
  `<name>.md.ref`, `.claude/skills/<n>/SKILL.md.ref`), status=stub, resolved ref는 여전히 fetch.
- **build-only literal**: bogus ref여도 union validate PASS(ref는 node 추가/제거 안 함).

## 재현 (symlink dance)
- `cd staging/harness-recipes; ln -sfn "$(cd ../.. && pwd)" central` (repo ROOT여야 함).
  validate/materialize with `HARNESS_CATALOG=catalog-v001.xml
  HARNESS_ROOT_ONTOLOGY=.../recipes/lpranging`. 끝나면 **`rm -f central`**(at-rest 심링크 0 hygiene,
  `find staging -type l` 확인). 재현 python one-off는 `sys.path.insert(0,'central/tools')` 필요
  (`import tools.ontology_lib`는 ModuleNotFoundError).
- union = **119**(faithful 시절 94에서 skill instructions 등 합류로 증가). central = 96.
  determinism `diff -r lpr1 lpr2` IDENTICAL(lock/manifest no timestamp).
- tokenEstimate 감사: `subjects(HO.promptText,None)` 중 tokenEstimate 없는 것 = NONE.

## techdoc/contract-demo principle 판정 (§6)
- **techdoc = aligned**: recipe dir = README+ttl만. 유일 artifactTemplate가
  `tools/materialize_templates/persona.md.tmpl` = **central 재사용 tool asset**(repo root 해소,
  recipe 안 아님). generalized central template를 reference = principle 정확 부합.
- **contract-demo = acceptable/noted tension**: `impl/greeter_v{1,2}.py`를 여전히 in-recipe 저장
  (repo-relative ref) = 표면상 vendoring 안티패턴. 그러나 **synthetic demo fixture, external
  source 無**(INV-4 재바인드 데모용 2 divergent candidate; recipe가 authoritative home). principle
  의도는 "다른 곳에 authoritative하게 있는 문서의 copy를 vendoring 말라" — 이건 copy도 아니고
  generalized part도 아닌 데모 자체의 subject. **결함 아님**. 권고(non-blocking): README/recipes-design.md에
  test-fixture 예외로 명시하거나 `fixtures/` marker로 이동.

## 판정 = pass-with-notes (note는 경계한계)
- N1 portability tradeoff(external absolute ref는 source 있는 box에서만 해소, off-box는 stub —
  README에 명시된 의도적 user choice "설명서 중심+참조 fetch"). N2 contract-demo fixture(위).
  N3 recipe≠full project(domain design docs/exports/agent-memory content out-of-model 정당).
- README-as-explanation = PASS: §1 which parts / §2 which methodology(+ODR axes) / §3 how
  (references not artifacts + tradeoff callout) / §4 what result — 4 movement 다 있음, 설명서로 읽힘.
- 6 checkpoint(central gate 96 / no-stored proof / fetch byte-identical / stub fail-safe /
  regression techdoc+contract-demo / principle judgment) 전부 통과.
