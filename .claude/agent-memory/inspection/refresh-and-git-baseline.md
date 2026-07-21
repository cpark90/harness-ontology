# refresh 판정 + 안전 커밋 절차 (inspection)

## refresh 판정
approved + 적용 실증(validate PASS·산출물 존재)만으로는 **부족**하다. 항목이 명시한
**inspection 몫 후속(첫 git 커밋·공개 repo 등)이 완료돼야** step5 refresh 대상이 된다.
미완이면 유지 — "적용 전이면 남긴다, 시간 가정 금지"(verify-then-proceed). 판정 근거는
실측(`validate.py`, `git rev-list --count HEAD`, 산출물 존재)으로 남긴다.

## 안전 refresh 순서 (데이터 손실 방지)
1. baseline 커밋에 항목 **포함**(히스토리에 영구 보존 → 복구 가능).
2. push 성공 후(또는 로컬이면 곧바로) **별도 커밋으로 `git rm` 항목** = refresh.
항목을 미커밋 상태에서 먼저 지우면 push 실패 시 추적 기록이 소실된다. 절대 금지.

## 이 repo git 사실
- `.claude/settings.local.json`은 사용자 전역 ignore(`~/.config/git/ignore`)로 제외 — 안전.
- `gh` CLI 미설치, remote 없음 → 공개 repo 생성/ push는 사용자가 remote를 제공해야 가능.
- 첫 커밋은 main에 직접(정상 — inspection=메인테이너측 git 전담).
