# Inspection 실행 브리프 — languageCondition + materialize 증분1 커밋

> 작성: orchestrator (2026-07-22). **실행 주체: inspection 세션** (git 전담).

## 배경
두 변경(둘 다 vnv **pass-with-notes**, 차단 0 — `docs/verify/materialize-and-language.md`):
- **(A) 언어조건**: TBox `ho:languageCondition` + 중앙 `gr-lang`에 3항목(산문 한글/용어 영어/코드·커밋 영어).
- **(B) materialization 증분1** (approved 피드백 `recipe-to-buildable-harness.md`): TBox `ho:artifactTemplate` + `tools/materialize.py`(retrieve의 BUILD dual, 검증 게이트·결정론) + `tools/materialize_templates/` + `docs/materialize-design.md`. techdoc 레시피의 `sp-techdoc`에 template ref(레시피 쪽, 중앙 neutral 유지).
- 중앙 validate **PASS 64**, retrieve 무영향.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # PASS 64
git status --short | grep -v staging          # 아래 Task1 대상 확인
gh auth status                                 # cpark90
```

## Task 1 — 중앙 커밋 + push
대상(미커밋): `ontology/tbox/harness.ttl`(2 프로퍼티), `ontology/abox/core/guardrails.ttl`(gr-lang),
`tools/materialize.py`, `tools/materialize_templates/`, `docs/materialize-design.md`,
`docs/verify/materialize-and-language.md`, `docs/feedback/recipe-to-buildable-harness.md`,
`.claude/agent-memory/**`.
```bash
git add -A                                     # /staging/ 및 scratch build 출력은 gitignore/외부라 제외
/usr/bin/python3 tools/validate.py             # PASS 64 (pre-commit gate)
git commit -m "Add materialize build-projection + language-condition guardrail items

- TBox: ho:languageCondition (guardrail language rule items), ho:artifactTemplate (component template path)
- core:gr-lang: prose=Korean / terms=English / code+identifiers+commits=English
- tools/materialize.py: recipe union -> CLAUDE.md + MANIFEST.json (dual of retrieve;
  gates on validate; deterministic; template-fragment rendering)
- docs/materialize-design.md (P3/P4/P5 follow-ups noted)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Task 2 — harness-recipes에 techdoc template-ref 반영
```bash
DST=/home/cpark/git/harness-recipes
[ -d "$DST/.git" ] || git clone https://github.com/cpark90/harness-recipes.git "$DST"
cd "$DST" && git pull
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/recipes/techdoc/techdoc.ttl "$DST"/recipes/techdoc/
# federate 재검증(권장)
git clone https://github.com/cpark90/harness-ontology.git central
HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/techdoc \
  /usr/bin/python3 central/tools/validate.py   # PASS 69
rm -rf central
git add -A && git commit -m "techdoc recipe: wire ho:artifactTemplate on sp-techdoc (materialize persona)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" && git push
```

## 참고 (커밋 안 함)
- `materialize.py` 빌드 산출물(scratchpad `build-techdoc/`)은 빌드 결과물이라 커밋 대상 아님.
- approved 피드백 `recipe-to-buildable-harness.md`은 **증분1(P1 spine + P2 template-ref)만 반영**됨.
  P3(impl 참조)·P4(역할 1급)·P5(scaffold)는 미반영 → 항목을 지우지 말고 남겨둘 것(후속 대기).

## 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] 중앙 push: cpark90/harness-ontology @ materialize+language (commit: ____) / validate 64 PASS / CI green
- [ ] recipes push: harness-recipes @ techdoc template-ref (commit: ____) / compose 69 PASS
