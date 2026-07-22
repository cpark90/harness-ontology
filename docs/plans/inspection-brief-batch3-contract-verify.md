# Inspection 실행 브리프 — batch 3: ODR 계약-VERIFY축 (level 3~4)

> 작성: orchestrator (2026-07-22). **실행 주체: inspection 세션** (git 전담).
> batch 1(methodology), batch 2(materialize emitters/bugfix/hardening)는 이미 land. 이건 그 다음 batch.

## 배경 (developer 저작 → vnv 검증 pass-with-notes, 결함 0 — `docs/verify/odr-contract-verify.md`)
ODR **VERIFY축** = capability에 검증가능 contract + 산출물 판정. 성숙도 **level 3(부합 검증) + level 4(기술 독립 실증/INV-4)** 실증.
- **TBox**(중앙): `ho:Contract`(⊑HarnessComponent), `ho:capabilityContract`(Capability→Contract, 3-link propertyChain로 reachability·mistype 회피), `ho:contractKind`(executable/structural), `ho:contractCheck`. `ontology_lib` INSTANCE_CLASSES 등록.
- **도구**(중앙): `tools/verify_contract.py` — materialize 트리를 계약으로 판정(실행=cwd에서 명령 exit 0 / 구조=file-exists·file-contains·section), validate/materialize의 VERIFY dual.
- **레시피 데모**: lpranging `cap-designgraph`/`cap-simulation`에 계약 3개(구조+실행 AST parse) = level 3(verify 3/3 PASS, 툴 삭제 시 FAIL). 신규 `recipes/contract-demo/`(greeter 후보 2종·동일출력/상이소스+행위계약) = level 4(스왑해도 동일 verdict PASS).
- 중앙 abox neutral(계약/candidate는 recipe-side; abox 계약항 0).

**게이트 실측**: 중앙 validate **PASS 96**(불변) · lpranging compose **119**(+3 contracts) · contract-demo compose **107** · techdoc **101**. verify_contract 결정론.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # PASS 96
git status --short | grep -v staging          # Task1 대상
gh auth status                                 # cpark90
```

## Task 1 — 중앙 커밋 + push
미커밋(non-staging): `ontology/tbox/harness.ttl`, `tools/ontology_lib.py`, `tools/verify_contract.py`(신규), `docs/{materialize-design,odr-bind-lock,odr-contract-verify,verify/odr-contract-verify}.md`, `.claude/agent-memory/**`.
```bash
git add -A
/usr/bin/python3 tools/validate.py             # PASS 96 (pre-commit gate)
git commit -m "ODR contract-VERIFY axis: capability contracts + verify_contract.py (maturity 3-4)

- TBox: ho:Contract / capabilityContract (3-link propertyChain) / contractKind / contractCheck
- tools/verify_contract.py: judge materialized tree against spec contracts (executable + structural)
- demonstrates level 3 (contract-checked) and level 4 (INV-4: impl-independent verify)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Task 2 — harness-recipes: lpranging 계약 + 신규 contract-demo push
lpranging에 계약 추가, `contract-demo/`는 신규. staging catalog에 contract-demo 매핑 + CI matrix에 root IRI 추가돼 있어야 함(staging 반영분 그대로 복사).
```bash
DST=/home/cpark/git/harness-recipes
[ -d "$DST/.git" ] || git clone https://github.com/cpark90/harness-recipes.git "$DST"
cd "$DST" && git pull
rm -rf recipes/lpranging recipes/contract-demo catalog-v001.xml .github/workflows/validate.yml
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/recipes/lpranging     recipes/
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/recipes/contract-demo recipes/
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/catalog-v001.xml .
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/.github/workflows/validate.yml .github/workflows/
# federate 재검증(권장)
git clone https://github.com/cpark90/harness-ontology.git central
for R in lpranging contract-demo techdoc; do
  HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/$R /usr/bin/python3 central/tools/validate.py 2>&1 | grep -E "individuals|PASS|FAIL"; done
rm -rf central
git add -A && git commit -m "Recipes: lpranging capability contracts + contract-demo (INV-4 candidate swap)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>" && git push
```
- push 후 Actions(`validate-recipes`)가 lpranging(119)·contract-demo(107)·techdoc(101) green인지 확인.

## 비차단 노트 (vnv, 운영/문서)
- N1 구조계약은 wiring/presence 검사 — 강한 보장엔 executable 계약 병행. N2 executable 계약은 그래프에서 임의 shell 실행 → `verify_contract`는 신뢰된 recipe 그래프에만(=CI test 명령과 같은 신뢰면). N3 INV-4 재바인딩은 recipe `selectionPolicy` 편집(현재 `--policy` CLI 없음, `pinned:<tag>`로 동작).

## 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] 중앙 push: cpark90/harness-ontology @ contract-verify (commit: ____) / validate 96 / CI green
- [ ] recipes push: harness-recipes @ contracts+contract-demo (commit: ____) / compose 119·107·101 / Actions green
