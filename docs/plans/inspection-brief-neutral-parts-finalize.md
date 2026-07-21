# Inspection 실행 브리프 — 중립 부품 재작업 git 마무리

> 작성: orchestrator (2026-07-21). **실행 주체: inspection 세션** (git·GitHub 전담).
> 이전 물리 분할 브리프(`inspection-brief-physical-split-lpranging.md`)는 SUPERSEDED.

## 배경
사용자 원칙 정정: 온톨로지는 특정 하네스의 "설명"이 아니라 **도메인 독립 중립 부품 라이브러리**.
→ developer가 lpranging governance 문서를 중립 부품으로 재작업(도메인 노드 전부 제거),
분할 되돌리기 완료. vnv 독립검증 **pass-with-notes**(차단 없음, `docs/verify/neutral-parts-rework.md`).
현재 로컬 상태(미커밋): core 64 individuals, validate PASS, 도메인 잔재 0.

## 결정 반영
- 분할 중단 + 되돌리기: 중앙에 중립 부품 유지, 별도 data repo 없음(연합 D1/D3 infra는 유지).
- **`cpark90/harness-data-lpranging`(공개, stale 도메인 하네스 보유) 폐기** — 저장 전제가 사라짐.

## 선결 확인
```bash
cd /home/cpark/git/harness_ontology
/usr/bin/python3 tools/validate.py            # → PASS, 64 individuals
git status --short                             # 대량 변경(재작업). D ontology/abox/lpranging-sysdesign.ttl 포함,
                                               # staging/ 는 삭제됨
gh auth status                                 # cpark90
grep -rniE 'uwb|rtls|lpranging|docgraph|simulator' ontology/abox/ | wc -l   # → 0 (도메인 잔재 없음)
```

## Task 1 — 재작업 커밋 + 중앙 push
현재 워킹트리 전체가 최종 상태(연합 infra + 중립 부품 라이브러리 + lpranging 도메인 제거)다.
```bash
git add -A                                     # seed.ttl(중립 부품), catalog/root(분할 되돌림 NOTE),
                                               # docs/*, lpranging-sysdesign.ttl 삭제(D) 등 포함
/usr/bin/python3 tools/validate.py             # PASS 64 재확인 (pre-commit gate)
git commit -m "Rework: store neutral domain-independent parts, not a domain harness

Decompose harness governance docs into reusable neutral parts (guardrails,
orchestrator-workers pattern, multi-agent workflow, methodical persona,
bounded-context/anti-rot), assembled by a neutral h-multiagent template.
Remove all lpranging domain-specific nodes; revert the physical split
(federation D1/D3 infra retained, no external data unit).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

## Task 2 — stale data repo 폐기
안전 기본 = **archive**(비파괴, 되돌리기 가능). 완전 삭제를 원하면 대신 delete.
```bash
# 권장: archive (읽기전용 보존)
gh repo archive cpark90/harness-data-lpranging --yes
# 또는 완전 삭제 (되돌릴 수 없음; delete_repo 스코프 필요)
# gh repo delete cpark90/harness-data-lpranging --yes
```
- 로컬 클론 디렉토리(`/home/cpark/git/harness-data-lpranging`)가 있으면 정리.

## (선택) Note D — 문서 cosmetic
`docs/federation-design.md`에 `lpranging`을 네이밍 예시로 쓴 줄이 남아 있음(파일럿 주장 아님).
정리를 원하면 orchestrator에 요청 → developer dispatch(문서 저작). 미관 사항, 비차단.

## 완료 보고 (inspection → orchestrator, 아래 append)
- [ ] 중앙 push: cpark90/harness-ontology @ neutral-parts rework (commit: ____) / validate 64 PASS
- [ ] data repo 폐기: harness-data-lpranging = archived / deleted
- [ ] 최종: 중앙 = core 중립 부품 64, 도메인 잔재 0
