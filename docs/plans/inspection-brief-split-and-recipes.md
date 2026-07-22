# Inspection 실행 브리프 — 중앙 타입별 분리 커밋 + harness-recipes repo

> 작성: orchestrator (2026-07-22). **실행 주체: inspection 세션** (git·GitHub 전담).

## 배경
- **Phase 1**: 중앙 `seed.ttl` → `ontology/abox/core/` 11개 타입별 유닛으로 분리(개체 64 불변, triple-무결성 검증됨). catalog/root 재배선, seed.ttl 삭제.
- **Phase 2**: `harness-recipes` repo 콘텐츠 로컬 제작 — `staging/harness-recipes/`(gitignored). 중앙 중립 부품을 import·조립한 lpranging 예시 레시피 포함. 중앙은 neutral 64 유지.
- vnv 독립검증 **pass-with-notes**(결함 0) — `docs/verify/split-and-recipes.md`.
- rename 대상: `cpark90/harness-data-lpranging`(현재 **archived**) → **`harness-recipes`**, 콘텐츠는 stale lpranging 하네스 → 레시피 모음으로 전면 교체.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # → PASS, 64 individuals
ls ontology/abox/core/                         # 11개 유닛, seed.ttl 없음
git status --short                             # Phase1 분리 + docs + staging(gitignore로 제외) 등
gh auth status                                 # cpark90
```

## Task 1 — 중앙 Phase 1 분리 커밋 + push
```bash
git add -A                                     # core/ 분리, seed.ttl 삭제(D), catalog/root, docs/recipes-design.md,
                                               # docs/federation-design.md, verify 리포트 등. /staging/ 는 gitignore로 제외
/usr/bin/python3 tools/validate.py             # PASS 64 (pre-commit gate)
git status --short | grep staging              # (아무것도 안 나와야 정상 — staging 미커밋)
git commit -m "Split central parts library into per-type units; add recipe-repo design

- ontology/abox/seed.ttl -> ontology/abox/core/{concepts,capabilities,constraints,
  model-configs,tools,guardrails,patterns,workflows,system-prompts,domains-tasks,harnesses}.ttl
  (64 individuals unchanged; catalog + root owl:imports rewired)
- docs/recipes-design.md: recipe/blueprint repo role (assemble neutral parts into harnesses)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Task 2 — repo unarchive → rename → 레시피 콘텐츠로 교체 → push
```bash
# 1) archived 상태라 push 전에 unarchive
gh repo unarchive cpark90/harness-data-lpranging --yes
# 2) rename
gh repo rename harness-recipes --repo cpark90/harness-data-lpranging
# 3) 로컬에서 콘텐츠 전면 교체
DST=/home/cpark/git/harness-recipes
rm -rf "$DST"
git clone https://github.com/cpark90/harness-recipes.git "$DST"
cd "$DST"
git rm -r --quiet . 2>/dev/null; true                        # 기존 stale 콘텐츠(구 lpranging 하네스) 제거
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/. "$DST"/   # 숨김파일 포함
rm -rf "$DST"/central 2>/dev/null; true                      # 혹시 모를 symlink 정리(.gitignore가 /central/ 무시)
# 4) federate 재검증(선택이나 권장): 중앙 clone 후 compose validate
git clone https://github.com/cpark90/harness-ontology.git central
HARNESS_CATALOG=$PWD/catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
  /usr/bin/python3 central/tools/validate.py   # → PASS, 75 individuals
rm -rf central
# 5) 커밋 + push
git add -A
git commit -m "Repurpose as harness-recipes: blueprints/examples assembled from harness-ontology

Replace the retired domain-harness data repo with a recipe repo. Each recipe
owl:imports the central neutral parts and composes a complete harness; domain
bindings live locally. First recipe: recipes/lpranging (composes h-lpranging).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## (선택·비차단) 검토 노트
- vnv note: `h-lpranging` maturity = `"reviewed"`(CLAUDE.md 산문은 draft-first 권장). 예시 레시피라 그대로 둬도 무방. draft로 낮추길 원하면 orchestrator→developer.
- `data/authored` catalog 매핑(파일 부재, BFS skip) — webui 잔재, 무해.

## 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] 중앙 push: cpark90/harness-ontology @ per-type split (commit: ____) / validate 64 PASS
- [ ] repo rename: harness-data-lpranging → **harness-recipes** (unarchived)
- [ ] 레시피 push: harness-recipes @ recipes/lpranging (commit: ____) / compose validate 75 PASS
- [ ] 최종: 중앙 = 중립 부품 64(11파일) · recipes repo = 조립 레시피 모음
