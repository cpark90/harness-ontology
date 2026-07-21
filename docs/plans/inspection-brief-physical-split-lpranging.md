> ⚠️ **SUPERSEDED (2026-07-21)** — 이 물리 분할(lpranging 파일럿) 브리프는 폐기됨. 사용자가
> 모델링 원칙을 정정("온톨로지는 특정 하네스 설명이 아니라 도메인 독립 중립 부품 저장")하여
> lpranging 도메인 노드를 제거하고 분할을 되돌렸다. 후속 git 작업은
> **`docs/plans/inspection-brief-neutral-parts-finalize.md`** 를 따른다. 아래 내용은 이력 보존용.

# Inspection 실행 브리프 — 물리 repo 분할 (lpranging 파일럿)

> 작성: orchestrator (2026-07-21). **실행 주체: inspection 세션** (git·GitHub 전담).
> orchestrator/developer/vnv는 git을 실행하지 않는다. 이 문서는 durable 핸드오프 채널이다.

## 목표 / 확정값
현 repo `/home/cpark/git/harness_ontology` → **중앙 schema+tooling repo**로 전환하고, `lpranging`
도메인 abox를 **외부 순수-data repo**로 분리(파일럿). 연합 로딩은 D1 owl:imports+catalog(구현·검증됨).

| 항목 | 값 |
|---|---|
| GitHub owner | `cpark90` |
| 중앙 repo | `cpark90/harness-ontology` (**public**) |
| data repo | `cpark90/harness-data-lpranging` (**public**) |
| data-repo payload (durable, on-disk) | `staging/lpranging-data-repo/` (중앙 `.gitignore`로 제외됨) |

## 안전 원칙 (verify-then-proceed) — 반드시 준수
- **외부 data repo가 push로 durable하게 확인되기 전에는 중앙에서 lpranging를 제거하지 않는다.**
  (이유: lpranging 하네스는 어떤 커밋에도 없어 git 복구 불가였음 — 삭제 선행은 유실 위험.)
- 중앙 제거(Step 5)는 **content 편집이라 developer 소관** → inspection이 직접 하지 않고
  orchestrator에 핸드백. inspection은 커밋만.
- 모든 커밋 전 `/usr/bin/python3 tools/validate.py` = **PASS** 확인.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # → PASS, all 62 individuals
gh auth status                                 # cpark90 로 로그인돼 있어야 함 (아니면 gh auth login)
git status --short                             # 대량 uncommitted(federation 작업). staging/ 는 안 보여야 정상(gitignored)
git log --oneline -3                           # 기존 3커밋(webUI 등) 위에 쌓는다
```

## Step 1 — 중앙 전체 상태 커밋 (lpranging를 git 히스토리에 durable화)
현재 워킹트리에 federation 전체 작업이 미커밋 상태다. 이걸 먼저 커밋해야 lpranging가 히스토리에 남는다.
```bash
git add -A                                     # /staging/ 는 gitignore라 자동 제외
git status --short                             # 확인: ontology/abox/lpranging-sysdesign.ttl = staged,
                                               #       staging/ = 미포함
/usr/bin/python3 tools/validate.py             # PASS 62 재확인 (pre-commit gate)
git commit -m "Add owl:imports+catalog federation, IRI sub-namespaces, and lpranging system-design harness

- D1 loader: catalog-v001.xml + root harness-ontology.ttl (owl:imports)
- D3 IRI: .../id/<domain>/<slug> (core, lpranging)
- lpranging system-design harness (composed from ~/git/agrtls/.../lpranging)
- CONTRIBUTING-ONTOLOGY.md + data-repo CI template (D4)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

## Step 2 — 중앙 GitHub repo 생성 + push
```bash
gh repo create cpark90/harness-ontology --public \
  --source=/home/cpark/git/harness_ontology --remote=origin --push
gh repo view cpark90/harness-ontology --web   # (선택) 확인
```
- 실패 시(이미 존재 등): `git remote add origin https://github.com/cpark90/harness-ontology.git && git push -u origin main`.

## Step 3 — lpranging data repo 생성 (durable payload에서)
payload를 중앙 밖 작업 디렉토리로 복사(숨김파일 포함), placeholder를 실제값으로 치환:
```bash
DST=/home/cpark/git/harness-data-lpranging
mkdir -p "$DST"
cp -a /home/cpark/git/harness_ontology/staging/lpranging-data-repo/. "$DST"/
cd "$DST"
# placeholder 치환: 개발자가 넣은 예시 owner를 실제 cpark90 값으로
grep -rl 'hhmm2728' . | xargs -r sed -i \
  -e 's#hhmm2728/harness_ontology#cpark90/harness-ontology#g' \
  -e 's#hhmm2728/harness-data-lpranging#cpark90/harness-data-lpranging#g'
grep -rn 'cpark90/harness' .                   # README·.github/workflows/validate.yml 에 반영 확인
ls -a                                          # lpranging.ttl catalog-v001.xml README.md LICENSE .gitignore .github/
```
커밋 + repo 생성 + push:
```bash
git init -b main
git add -A
git commit -m "Initial commit: lpranging system-design ontology (federated data repo)

Pure-data abox for domain 'lpranging', imports central schema+core by IRI.
Validated by composing the union against cpark90/harness-ontology.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
gh repo create cpark90/harness-data-lpranging --public --source=. --remote=origin --push
```

## Step 4 — 연합 검증 (data repo가 실제로 federate 하는지, D4 시나리오 로컬 재현)
data repo 디렉토리에서 중앙을 `./central/`로 clone 후 중앙 validate를 union에 실행:
```bash
cd /home/cpark/git/harness-data-lpranging
git clone https://github.com/cpark90/harness-ontology.git central
HARNESS_CATALOG=$PWD/catalog-v001.xml \
HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/data/lpranging \
  /usr/bin/python3 central/tools/validate.py    # → PASS, all 62 individuals (schema+core+lpranging)
rm -rf central                                   # .gitignore가 /central/ 무시하지만 정리
```
- GitHub Actions(데이터 repo의 `.github/workflows/validate.yml`)가 첫 push/PR에서 green인지도 확인.

## Step 5 — (핸드백) 중앙에서 lpranging 제거 — **지금 하지 말 것**
Step 2–4로 외부 repo가 durable히 확인된 뒤에만 진행. **content 편집이라 developer 소관**:
1. inspection이 아래 "완료 보고"를 이 문서 하단(또는 조율 채널)에 남긴다 (외부 repo URL + federate PASS).
2. orchestrator가 그 보고를 확인 → developer dispatch로 중앙에서 lpranging 제거
   (`ontology/abox/lpranging-sysdesign.ttl` 삭제 + `catalog-v001.xml`/`ontology/harness-ontology.ttl`
   import 제거 + docs를 "split executed"로 갱신) → validate 41 PASS.
3. inspection이 그 제거를 커밋·push (중앙 = schema+core).
- 파일럿 성공 판정은 Step 4까지로 충분하다(외부 repo 존재 + federate). 제거는 "clean split" 마무리.

## 완료 보고 (inspection → orchestrator, 이 문서 하단에 append)
- [ ] 중앙 push: https://github.com/cpark90/harness-ontology (commit hash: ____)
- [ ] data repo push: https://github.com/cpark90/harness-data-lpranging (commit hash: ____)
- [ ] Step 4 federate validate: PASS / FAIL
- [ ] data repo Actions: green / ____
- [ ] 남은 것: Step 5(중앙에서 lpranging 제거) 핸드백 대기

---

# Step 5 실행 (git 마무리) — 콘텐츠 준비 완료, inspection이 실행

> orchestrator 확인(2026-07-21): Step 1–4 검증 완료 — 중앙/`cpark90/harness-data-lpranging` 모두
> public push됨, `origin/main`(=HEAD)에 opus/reviewed lpranging가 durable히 커밋됨.
> **정합성 수정**: data repo가 stale(sonnet/draft)였음 → developer가 (A) payload를 opus/reviewed로
> 동기화, (B) 중앙에서 lpranging 제거(validate 41 PASS)까지 **콘텐츠 완료**. 아래 git 2단계만 남음.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # → PASS, 41 individuals (schema+core)
git status --short                             # D ontology/abox/lpranging-sysdesign.ttl,
                                               # M catalog-v001.xml, harness-ontology.ttl, docs/federation-design.md 등
grep -E "usesModel|reviewed" staging/lpranging-data-repo/lpranging.ttl | head  # opus + reviewed 확인
gh auth status                                 # cpark90
```

## Step 5a — 동기화된 payload를 data repo에 push (중앙 제거보다 먼저)
data repo 워킹디렉토리를 최신 payload로 갱신(placeholder는 이미 치환돼 있으면 skip):
```bash
DST=/home/cpark/git/harness-data-lpranging     # Step 3에서 만든 디렉토리 (없으면 git clone)
[ -d "$DST/.git" ] || git clone https://github.com/cpark90/harness-data-lpranging.git "$DST"
cp -a /home/cpark/git/harness_ontology/staging/lpranging-data-repo/lpranging.ttl "$DST"/lpranging.ttl
cd "$DST"
grep -E "usesModel|reviewed" lpranging.ttl     # opus + reviewed 확인
# federate 재검증
git clone https://github.com/cpark90/harness-ontology.git central 2>/dev/null || (cd central && git pull)
HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/data/lpranging \
  /usr/bin/python3 central/tools/validate.py    # → PASS, 62 individuals
rm -rf central
git add lpranging.ttl
git commit -m "Sync lpranging harness to opus tier + reviewed maturity

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Step 5b — 중앙 제거 commit + push (data repo 동기화 확인 후에만)
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # → PASS, 41 (pre-commit gate)
git add -A                                     # 삭제(D)·수정(M) 포함, /staging/ 는 gitignore로 제외
git status --short                             # lpranging-sysdesign.ttl = 삭제 스테이징 확인
git commit -m "Execute lpranging pilot split: externalize to cpark90/harness-data-lpranging

Central now = schema + core (41 individuals). Full federated union (62)
recomposed by cloning the external data repo. Completes docs/federation-design.md.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Step 5 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] data repo 동기화 push: harness-data-lpranging @ opus/reviewed (commit: ____) / federate PASS 62
- [ ] 중앙 제거 push: harness-ontology @ schema+core 41 (commit: ____)
- [ ] 최종: 중앙 41 PASS · data repo federate 62 PASS · data repo Actions green
- 완료 시 이 브리프 + `docs/verify`·`docs/feedback` 관련 항목 refresh는 inspection refresh 사이클 규약대로.
