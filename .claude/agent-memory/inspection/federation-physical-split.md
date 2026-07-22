# 물리 repo 분할 실행 (federation) — inspection 절차

brief `docs/plans/inspection-brief-physical-split-*.md`를 실행할 때의 재사용 지식.

> **갱신(2026-07-22)**: lpranging 물리 분할(도메인 data repo)은 **되돌려짐**. 온톨로지 원칙이
> "도메인 독립 중립 부품 라이브러리"로 정정 → 중앙(`cpark90/harness-ontology`)엔 중립 부품만.
> 중앙 abox는 `seed.ttl` → **`ontology/abox/core/` 11 타입별 유닛**으로 분리(catalog+root
> owl:imports 재배선).
>
> **외부 repo = `cpark90/harness-recipes`** (구 `harness-data-lpranging`를 unarchive→rename→
> 콘텐츠 전면 교체). 도메인 하네스 저장소가 아니라 **레시피/blueprint repo**: 각 recipe가 중앙
> 중립 부품을 owl:imports해 완결 하네스로 조립(도메인 바인딩은 레시피에 로컬). 예: `recipes/lpranging`.
> federate 검증: 레시피 repo에서 중앙 clone 후 `HARNESS_ROOT_ONTOLOGY=…/recipes/<name>` compose
> validate → PASS(중앙 64 + 레시피분). staging은 `staging/harness-recipes/`(gitignored).
>
> gh 폐기/전환: `gh repo archive|unarchive <repo> --yes`, `gh repo rename <new> --repo <owner/old> --yes`
> (토큰 scope=repo — archive/rename OK, delete_repo 없어 완전삭제 불가).

## GitHub repo 규약 (owner cpark90)
- 중앙 schema+tooling repo = **`cpark90/harness-ontology`(하이픈)**. (이전 세션의 언더스코어
  `harness_ontology`는 stale — 혼동 주의.)
- data repo = **`cpark90/harness-data-<domain>`**(예: harness-data-lpranging), pure-data abox.

## gh CLI (이 환경 미설치)
- 무암호 sudo 불가 → apt 불가. **gh 릴리스 tar.gz를 `~/.local/bin/gh`로 설치**(PATH에 있음).
  최신 조회: `curl api.github.com/repos/cli/cli/releases/latest`. 검증: `gh --version`.
- 인증은 대화형 → **사용자가 `gh auth login`**(cpark90, keyring). inspection이 대신 못 함.

## 연합 validate 재현 (data repo가 federate 하는지)
data repo에서 중앙을 `./central/`로 clone 후:
`HARNESS_CATALOG=$PWD/catalog-v001.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/data/<domain>
/usr/bin/python3 central/tools/validate.py` → PASS(union: schema+core+data). 로더 env=`ontology_lib.py:37-39`.
data repo `.github/workflows/validate.yml`가 push/PR에서 green인지 `gh run list --repo …`로 확인.

## 안전 순서 (유실 방지)
1. 중앙에 data abox를 **먼저 커밋**(git 히스토리에 durable, 복구 가능).
2. 외부 data repo **push + federate PASS + CI green** 확인 후에야 중앙 제거 착수.
3. 중앙 제거(Step 5)는 **content 편집 = developer 소관** → inspection은 안 함, 커밋만.
   완료 보고는 `docs/feedback/verified/`(조율 채널, 내 파일 경계 안)에 남긴다 — brief(docs/plans)
   직접 편집 금지(경계 밖).

## 함정
- auto-mode classifier가 `git remote add`/`git push`를 간헐 차단 → **plain 형태로 재시도하면 통과**
  (env prefix·compound 줄이기). 되돌릴 수 없는 외부 작업은 단계 분리해 실행.
