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

## 병렬 dispatch 중 scoped land (자율 루프 E-1 상시 상황)
같은 작업트리에서 developer 2~3인이 동시에 편집한다 ⇒ **`git add -A` 절대 금지**, brief가
명시한 파일만 개별 add. 절차:
1. `git status --porcelain`으로 브리프의 "진행 중 dispatch 파일 목록"과 실제를 **대조**한다 —
   목록이 어긋날 수 있다(예: 브리프는 `tools/ontology_lib.py`인데 실제는
   `ontology/shapes/harness-shapes.ttl`이 dirty). 내 5파일 외는 무조건 손대지 않는다.
2. **공유 파일 `.claude/agent-memory/developer/MEMORY.md`** 는 여러 dispatch가 같이 고친다 →
   커밋 전 `git diff <파일>`로 **추가된 줄이 인덱스 한 줄뿐인지** 확인. 다른 dispatch의
   인덱스 줄이 섞여 있어도 함께 커밋 무해(메모 포인터일 뿐), 미완성 본문이면 보류.
3. `git add` 후 `git status --porcelain`으로 스테이지가 정확히 그 파일들인지 재확인 →
   커밋 → push → 다시 porcelain으로 **타 dispatch 작업분이 미커밋으로 온전한지** 보고.
4. 문서만 커밋할 때 `validate.py` 실패는 차단 사유가 아니다(스테이지에 그래프 파일이 없으므로
   CI가 보는 트리는 이전 그래프 + 문서). 단 과도기라는 사실을 보고에 남긴다.

## 이 repo git 사실
- `.claude/settings.local.json`은 사용자 전역 ignore(`~/.config/git/ignore`)로 제외 — 안전.
- `gh` CLI 미설치, remote 없음 → 공개 repo 생성/ push는 사용자가 remote를 제공해야 가능.
- 첫 커밋은 main에 직접(정상 — inspection=메인테이너측 git 전담).
