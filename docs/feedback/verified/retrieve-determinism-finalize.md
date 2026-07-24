---
source: docs/feedback/retrieve-nondeterministic-pack.md
verdict: apply
status: reported
targets: [tools/retrieve.py, tools/check_determinism.py]
source_brief: docs/plans/inspection-brief-retrieve-determinism.md
---
# 검증 보고 — `retrieve.py` 비결정성 수정 land (온톨로지 무변경)

inspection이 `docs/plans/inspection-brief-retrieve-determinism.md`를 **브리프를 믿지 않고
전 항목 재실측**한 뒤 land했다. tools 전용 증분이라 `ontology/`는 한 줄도 바뀌지 않았다.

## 파급효과 (impact)
- **온톨로지 노드 0개**. `git status --porcelain ontology/` **무출력**(land 직전 실측).
- 영향 범위는 read projection뿐: `select_seeds` / `nodes` / `candidates` / `edges` 4곳의 정렬 키.
  랭킹 **의미**는 불변이고 동점 그룹의 순서만 고정된다(브리프의 seed 0~9 의미코어 대조 결과와
  이번 재실측이 일치).

## 정합성 (inspection 독립 재검증, 2026-07-25)
| 항목 | 결과 |
|---|---|
| `/usr/bin/python3 tools/validate.py` | **PASS** — SHACL·reachability·capabilities·assemblyOrder 4축, **205 individuals**, 중복 라벨 0 |
| `git status --porcelain ontology/` | **무출력** (온톨로지 무접촉) |
| `/usr/bin/python3 tools/check_determinism.py` | **PASS** — 4 probe × md/json = 8/8, 각 4 runs 1 distinct pack |
| 시드 **미고정** `retrieve.py` 10회 md5 | `"code review harness with tests"` → **1종** (`0793d6b9…`) · `"workflow steps and deliverables"` → **1종** (`6ee98146…`) |
| **negative control** (가드 실효성) | `git show HEAD:tools/retrieve.py`(수정 전) 사본 + 현재 `check_determinism.py`를 scratch 트리에서 실행 → **8/8 FAIL**, 각 probe가 4 seed에 4 distinct pack. 가드는 실효한다 |

negative control은 repo를 건드리지 않고 scratchpad에 `tools/{retrieve.py(HEAD),check_determinism.py,
ontology_lib.py(symlink)}` + `ontology`(symlink) 트리를 만들어 수행했다.

## 적용 결과 (land)
- **commit `d1ac476`** "Make retrieve.py projections deterministic across processes"
  — `tools/retrieve.py`, `tools/check_determinism.py`(신규), `Makefile`(`make determinism`),
  `.github/workflows/validate.yml`(validate 다음 step), developer 역할 메모리 2건.
- **commit `9acde0e`** (별건 분리) "Track the open-issue anchor, the scale-up plan and the survey verdict"
  — `docs/plans/OPEN-ISSUES.md`·`harness-100-scaleup-plan.md`·본 브리프, `docs/feedback/harness-repo-survey*`,
  `verified/harness-repo-survey.md`.
- push `87eeb53..9acde0e` (origin/main). CI `validate-ontology` = **success** (신규
  "Check projection determinism" step 포함).
- 동시 진행 중이던 developer dispatch 산출물 `docs/plans/harness-100-attribute-inventory.md`는
  **미완성일 수 있어 의도적으로 커밋에서 제외**했다.

## 판정
**apply — 완료(land).** 소스 항목 `docs/feedback/retrieve-nondeterministic-pack.md`는 파일
frontmatter가 아직 `status: open`이지만 **사용자 승인은 대화로 받았고** 수정·검증·land가 모두 끝났다.
`status` 태깅은 사용자 소관이므로 inspection이 임의로 `approved`로 바꾸지 않았다 — 대신 적용 결과를
여기에 기록한다. 사용자가 그 항목을 `approved`로 고치는 즉시 다음 사이클에 항목·보고서를 함께
refresh(제거)할 수 있다. **그때까지 두 파일 모두 남긴다.**

## 후속 (이 증분과 별개로 이번 재검증 중 발견)
결정성은 잡혔지만 **팩 품질**을 해치는 별개 결함을 확인해 새 항목으로 상신했다 —
`docs/feedback/retrieve-pack-quality-defects.md` (`ho:tokenEstimate` 의미 과부하로 인한 팩 조기
절단 + deprecated 노드가 후계 노드보다 상위 랭크). 둘 다 `retrieve.py` 소비자에게 조용히 나타난다.
