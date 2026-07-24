# import_corpus.py 독립 재검증 레시피 (tool land)

`tools/import_corpus.py`(코퍼스 harness → draft recipe TTL)를 발주 없이 실측 검증하는 절차.

## 4축 실측
- **결정성**: `--out run1`/`--out run2` 2회 → `diff -r` 0. + 코퍼스 dir md5(전파일) before/after 동일로
  read-only 확인(도구가 코퍼스를 안 건드림).
- **판단성 경계(★grep 함정)**: judgment 술어(`usesModel`/`roleTool`/`hasGuardrail`/`requiresCapability`
  등)의 **실제 트리플 배정 = 0**이어야 한다. 단 flag 헤더 주석이 이 술어 이름을 **6건 언급**한다 —
  `grep -vE '^\s*#'`로 주석줄을 먼저 버리고 세라. 안 그러면 주석 6건을 배정으로 오독(orchestrator가 실제로 오독할 뻔).
- **oracle 표본**: 파일럿(03/16/21/31/46)을 재생성해 손저작과 대조. 일치해야 하는 것: role/sp-role/sp/ins/h
  **id 집합**, `augmentsRole` 타깃, instruction `tokenEstimate`(=skill.md `wc -w`, 예: 21은 945/784/1019 정확일치).
  **유일한 정당한 불일치 = QA-gate collapse**(파일럿은 terminal QA를 `core:role-synthesizer`로 승격재사용,
  importer는 로컬유지+flag) → 결함 아님, 의도된 ② 판단. 파일럿이 augmentsRole를 **주석으로만** 가지면
  (pre-augmentsRole) importer가 더 정확 = supersession.
- **무변경**: 기존 파일럿 recipe TTL 5개 unchanged(git status·mtime), 중앙 `validate.py` PASS @223.

## GAP (다음 증분 전 처리 권고)
importer가 **TestScenario/FailurePolicy를 추출 안 함**(브리프 SHOULD 밖). 소스는 거의 전수 제공하고
Phase 0.7 backfill이 채웠다 → 대량 임포트(35×) 전 importer 다음 증분에 안 넣으면 같은 누락이 35× 복제.
OPEN-ISSUES에 GAP 등록 권고.

## 관측: refresh 함정
`inquiries/*.md`가 `status: closed`여도 본문에 "…보존"/참조기준 명시면 **제거 금지**(예: METHODOLOGY.md).
closed⇒delete로 가정하지 말고 본문을 읽어라(verify-then-proceed).
