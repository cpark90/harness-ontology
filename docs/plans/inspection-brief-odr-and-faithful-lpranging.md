# Inspection 실행 브리프 — ODR(BIND+Lock) + 거버넌스 guardrail + lpranging 충실 재반영

> 작성: orchestrator (2026-07-22). **실행 주체: inspection 세션** (git 전담).

## 배경 (모두 developer 저작 → vnv 검증 완료)
- **ODR EMIT/BIND/Lock**: `tools/materialize.py`(P1–P5 + 정책·lock), TBox BIND 어휘(`ho:Candidate`·
  `implementationCandidate`[propertyChain]·`candidateVersion`·`candidateTag`·`selectionPolicy`·
  `implementationRef` domain 제거), `ontology_lib` 등록. vnv **pass** — `docs/verify/odr-bind-lock.md`.
- **거버넌스 guardrail 2건**(중앙 중립): `gr-dispatch-execution`(작업 agent는 dispatch로만 실행),
  `gr-delegated-orchestration`(orchestrator는 직접 실작업 안 함, 수행 agent 통해서만) → `h-multiagent`에 wire.
- **에이전트 역할 taxonomy**(중앙 중립): TBox `ho:userFacing`(Role→boolean) + 신규 core 유닛
  `ontology/abox/core/roles.ttl`(catalog+root 배선) — 7 `ho:Role`: 유저소통 {orchestrator, inspection},
  worker {developer, research, inspection-worker, vnv, design}. `h-multiagent`에 `hasRole`로 wire.
- **lpranging 충실 재반영**: 실 소스(`~/git/agrtls/device_harvest_lp/lpranging`)를 레시피에 충실 반영
  — 합성물(docgraph_v2·candidates·stale lock·스텁 scaffold) 제거, 실 코드/표준문서 vendor, 단일 direct ref.
  materialize 트리가 실 소스와 **cmp-identical**. vnv **pass-with-notes** — `docs/verify/lpranging-faithful-reflection.md`.
- **METHODOLOGY 조사항목** `closed`(ODR 채택·성숙도 level 2 기록).
- 중앙 validate **PASS 73**(64 + guardrail 2 + role 7). 중앙 abox neutral 유지(BIND/candidate 개체는 recipe-side; role taxonomy는 중립 governance라 core).

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # PASS, 73 individuals
git status --short | grep -v staging          # 아래 Task1 대상(17건)
gh auth status                                 # cpark90
```

## Task 1 — 중앙 커밋 + push
미커밋(non-staging): `ontology/tbox/harness.ttl`, `ontology/abox/core/{guardrails,harnesses,roles}.ttl`,
`catalog-v001.xml`, `ontology/harness-ontology.ttl`,
`tools/{materialize.py,ontology_lib.py}`, `docs/{materialize-design.md,odr-bind-lock.md}`,
`docs/verify/{odr-bind-lock.md,lpranging-faithful-reflection.md}`, `docs/feedback/inquiries/METHODOLOGY.md`,
`docs/plans/*`, `.claude/agent-memory/**`.
```bash
git add -A                                     # /staging/ 는 gitignore로 제외
/usr/bin/python3 tools/validate.py             # PASS 73 (pre-commit gate)
git commit -m "ODR BIND+Lock axis + dispatch-governance guardrails

- materialize.py: candidate/selection-policy resolution + harness.lock.json (write/--lock reproduce)
- TBox: ho:Candidate/implementationCandidate(propertyChain)/candidateVersion/candidateTag/selectionPolicy
- core guardrails: gr-dispatch-execution, gr-delegated-orchestration (wired into h-multiagent)
- agent role taxonomy: ho:userFacing + core/roles.ttl (7 roles: orchestrator/inspection user-facing;
  developer/research/inspection-worker/vnv/design workers), wired into h-multiagent
- ODR methodology adopted (maturity level 2: reproducible via lock); METHODOLOGY inquiry closed

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Task 2 — harness-recipes: lpranging를 faithful 버전으로 **full-sync**
원격 lpranging은 stale(impl/ 없음·합성 `scaffold/docs/README.md`). staging의 faithful 버전으로 **완전 치환**
(추가+삭제 동기화). staging tree: `lpranging.ttl · README.md · impl/{docgraph.py,sim_grid_reservation.py} ·
scaffold/{DESIGN_HARNESS_STANDARD.md,CODESTYLE.md,docs/ONTOLOGY.md}`.
```bash
DST=/home/cpark/git/harness-recipes
[ -d "$DST/.git" ] || git clone https://github.com/cpark90/harness-recipes.git "$DST"
cd "$DST" && git pull
rm -rf recipes/lpranging                                   # 기존 stale 트리 제거(합성 scaffold 포함)
cp -a /home/cpark/git/harness_ontology/staging/harness-recipes/recipes/lpranging recipes/
# federate 재검증(권장): 중앙 clone 후 lpranging union(81) + materialize 충실성
git clone https://github.com/cpark90/harness-ontology.git central
HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/lpranging \
  /usr/bin/python3 central/tools/validate.py               # → PASS, 81
rm -rf central
git add -A                                                 # impl/ 추가, 실 표준문서, docgraph_v2/README 삭제 반영
git commit -m "lpranging recipe: faithful re-reflection of the real source harness

Mirror ~/git/agrtls/device_harvest_lp/lpranging: real .claude/agents roles,
vendored real tool code (docgraph.py, sim_grid_reservation.py), real standard
docs scaffold (DESIGN_HARNESS_STANDARD.md, CODESTYLE.md, docs/ONTOLOGY.md).
Remove synthetic demo content (docgraph_v2, BIND candidates, stub scaffold, lock).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```
- push 후 harness-recipes Actions(`validate-recipes`)가 lpranging(81)·techdoc(69) 모두 green인지 확인.

## 참고 (비차단 후속 — 별도 대기)
- materialize 하드닝(vnv 노트): **N1** lock content-hash tamper가 일부 파일 emit 후 실패(부분 산출물) → temp-dir+atomic move 권장; **N2** 미인식 policy 문자열이 error 아닌 silent fallback. 둘 다 재현 계약 자체는 유지.
- `ontology_lib.most_specific_types` reflexive-subclass 중앙 수정(retrieve/webui type noisy; materialize는 로컬 우회).
- ODR 로드맵 후속: level 3~4 **계약-VERIFY축**(capability contract + artifact 판정) → 이중 타깃.
- 충실성 경계(비결함): 소스 도메인 docs/skills/memory/exports/reference는 하네스 모델 밖이라 materialize 대상 아님; 산문은 §1d로 영어(의미적 반영).

## 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] 중앙 push: cpark90/harness-ontology @ ODR+guardrails+role-taxonomy (commit: ____) / validate 73 / CI green
- [ ] recipes push: harness-recipes @ lpranging faithful (commit: ____) / compose 81 / Actions green
