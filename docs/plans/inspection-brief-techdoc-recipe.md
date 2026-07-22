# Inspection 실행 브리프 — techdoc 레시피를 harness-recipes에 추가

> 작성: orchestrator (2026-07-22). **실행 주체: inspection 세션** (git 전담).

## 배경
조립 시연: "기술문서 작성·리뷰 에이전트"를 중앙 중립 부품으로 조립한 새 레시피.
- 로컬 산출: `staging/harness-recipes/recipes/techdoc/{techdoc.ttl,README.md}` + 갱신된
  `staging/harness-recipes/catalog-v001.xml`·`.github/workflows/validate.yml`(techdoc를 CI matrix에 추가).
- `id:h-techdoc` = `derivedFrom core:h-research`, 중앙 부품 ~13개 IRI 재사용 + 로컬 4노드(sp/dom/c/task-techdoc).
- vnv **pass-with-notes**(결함 0) — `docs/verify/techdoc-assembly.md`. 중앙 neutral 64 불변, compose 69 PASS, lpranging 75 무회귀.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # 중앙 → PASS 64 (불변)
ls staging/harness-recipes/recipes/           # lpranging  techdoc
gh auth status                                 # cpark90
```
- 중앙 `ontology/` 는 이번 라운드 변경 없음(조립은 recipes 쪽만). 중앙 커밋 불필요.
  (verify 리포트 `docs/verify/techdoc-assembly.md` + 이 브리프만 미커밋 docs — 원하면 중앙에 함께 커밋 가능, 선택.)

## Task — harness-recipes에 techdoc 추가 push
```bash
DST=/home/cpark/git/harness-recipes
[ -d "$DST/.git" ] || git clone https://github.com/cpark90/harness-recipes.git "$DST"
cd "$DST" && git pull
# staging의 신규/갱신분 반영 (techdoc 레시피 + 갱신된 catalog + CI matrix)
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/recipes/techdoc "$DST"/recipes/
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/catalog-v001.xml "$DST"/
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/.github/workflows/validate.yml "$DST"/.github/workflows/
# federate 재검증(권장): 중앙 clone 후 techdoc union validate
git clone https://github.com/cpark90/harness-ontology.git central
HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/techdoc \
  /usr/bin/python3 central/tools/validate.py   # → PASS, 69
HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
  /usr/bin/python3 central/tools/validate.py   # → PASS, 75 (무회귀)
rm -rf central
git add -A
git commit -m "Add techdoc recipe: technical-documentation agent assembled from core parts

Demonstrates composing a complete harness from the neutral library with minimal
local specialization (h-techdoc derivedFrom core:h-research; reuses retriever/
websearch/editor tools, cite/lang/grounding/traceability/report guardrails,
plan-execute workflow, opus). Local: techdoc persona/domain/concept/task only.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```
- push 후 GitHub Actions(`validate-recipes`)가 두 레시피(lpranging·techdoc) 모두 green인지 확인.

## (선택·비차단) 검토 노트
- vnv N1: `task-techdoc`(인용 저작+정확성 리뷰)은 일반화하면 core Task로 승격 후보. 데모라 로컬 유지 무방.
  같은 패턴 반복 시 orchestrator→developer로 core 승격 검토. `sp/dom/c-techdoc`은 도메인 특정이라 로컬이 맞음.

## 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] recipes push: harness-recipes @ recipes/techdoc (commit: ____)
- [ ] federate: techdoc 69 PASS · lpranging 75 PASS · Actions green
