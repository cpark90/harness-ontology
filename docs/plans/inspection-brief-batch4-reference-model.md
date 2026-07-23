# Inspection 실행 브리프 — batch 4: 레시피 참조-모델 (구체물 미저장)

> 작성: orchestrator (2026-07-23). **실행 주체: inspection 세션** (git 전담).
> batch 1~3 land 완료. 이건 그 다음 batch.

## 배경 (developer 저작 → vnv **pass-with-notes**, 결함 0 — `docs/verify/lpranging-reference-model.md`)
모델링 원칙 정정: 온톨로지/레시피는 **일반화된 부품 + 방법론 + 조립 설명**만 보유하고 **구체 build 문서는 저장하지 않는다**. lpranging을 vendoring→**외부 참조 + 설명**으로 재작업, materialize는 참조를 **fetch(없으면 stub)**.
- **중앙 tooling**: `tools/materialize.py` — `_resolve_ref_path`(repo→recipe→absolute→None) 단일 resolver로 impl/scaffold/skill 모두 **fetch-or-stub** 통일. 결정론·validate 게이트 유지.
- **docs**: `recipes-design`·`materialize-design`·`composition-methodology`에 원칙 명문화(레시피=조립 spec+설명+외부참조; materialize가 fetch).
- **레시피(lpranging)**: vendor된 `impl/`·`scaffold/` 본문·`skills/*/SKILL.md` **삭제**, 참조는 외부 절대경로, README는 설명서로 재작성. 레시피 dir = `lpranging.ttl` + `README.md`만.

**게이트 실측**: 중앙 validate **PASS 96** · lpranging compose **119**(불변) · materialize 소스 present→8파일 byte-identical fetch, absent→stub(exit 0) · 결정론.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # PASS 96
git status --short | grep -v staging          # Task1 대상
gh auth status                                 # cpark90
```

## Task 1 — 중앙 커밋 + push
미커밋(non-staging): `tools/materialize.py`, `docs/{recipes-design,materialize-design,composition-methodology}.md`, `docs/verify/lpranging-reference-model.md`, `.claude/agent-memory/**`. (신규 피드백 `docs/feedback/finer-domain-design-graph.md`는 별도 처리 — 아래 참고, 이 커밋에 포함해도 무방.)
```bash
git add -A
/usr/bin/python3 tools/validate.py             # PASS 96 (pre-commit gate)
git commit -m "Recipes store references+explanation, not concrete build docs (materialize fetch-or-stub)

- materialize: unified _resolve_ref_path; impl/scaffold/skill fetch-or-stub (no stored copies)
- docs: recipe = composition spec + explanation + external refs; ODR INV-1 at recipe layer

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Task 2 — harness-recipes: lpranging에서 vendor 파일 삭제 + 참조-모델 push
원격 lpranging엔 아직 `impl/`·`scaffold/`·`skills/*/SKILL.md`가 있음 — staging(참조-모델: TTL+README만)으로 **full-sync**(삭제 반영).
```bash
DST=/home/cpark/git/harness-recipes
[ -d "$DST/.git" ] || git clone https://github.com/cpark90/harness-recipes.git "$DST"
cd "$DST" && git pull
rm -rf recipes/lpranging                                   # vendor 파일 포함 전부 제거
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/recipes/lpranging recipes/   # 이제 TTL+README만
# federate 재검증(권장): 중앙 clone 후 lpranging union(119) + materialize fetch(소스 있는 환경에서)
git clone https://github.com/cpark90/harness-ontology.git central
HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging /usr/bin/python3 central/tools/validate.py   # PASS 119
rm -rf central
git add -A && git commit -m "lpranging recipe: references + explanation only (drop vendored build artifacts)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" && git push
```
- push 후 Actions(`validate-recipes`)가 lpranging(119)·contract-demo(107)·techdoc(101) green인지 확인.
- **주의**: materialize fetch는 외부 소스(`~/git/agrtls/...`)가 있는 환경에서만 실제 파일을 가져옴 — CI(소스 없음)에선 validate만 게이트(정상). materialize 산출 자체는 CI 대상 아님.

## 비차단 노트 (vnv)
- N1 외부 절대참조는 소스 있는 환경에서만 resolve(공개 사용자 환경 고려 시 후속: 안정 IRI resolver/공개 소스). N2 contract-demo greeter는 INV-4 합성 fixture(유지 or `fixtures/` 표시). N3 recipe≠전체 프로젝트(도메인 콘텐츠는 모델 밖, 정상).

## 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] 중앙 push: cpark90/harness-ontology @ reference-model (commit: ____) / validate 96 / CI green
- [ ] recipes push: harness-recipes @ lpranging refs-only (commit: ____) / compose 119·107·101 / Actions green
