# materialize 출력 회귀 독립검증 레시피 (inspection)

developer/orchestrator가 "byte-identical" 또는 "append-only"를 주장하는 증분을 land할 때, 그
주장을 **직접** 재현하는 방법. 작업 트리를 건드리지 않는다.

```bash
SP=<scratchpad>
git worktree add -q --detach $SP/head <직전_커밋>          # 예: a8e835a
(cd $SP/head && /usr/bin/python3 tools/materialize.py <harness> --out $SP/m_head)
/usr/bin/python3 tools/materialize.py <harness> --out $SP/m_new   # working tree
diff $SP/m_head/CLAUDE.md $SP/m_new/CLAUDE.md | grep -c '^<'   # 0 = append-only
git worktree remove --force $SP/head && git worktree prune
```
- **★`harness.lock.json`은 byte-identity 불변식에서 제외해야 한다.** `build_lock()`의
  `spec.individualCount = len(lib.instance_nodes(g))`는 **union 전체 카운터**(하네스 스코프가
  아니다, `materialize.py:1232`) — 중앙에 개체가 하나라도 늘면 **배선과 무관하게 모든**
  하네스의 lock이 바뀐다. 게다가 `_verify_lock_spec()`(:1209)이 불일치 lock을 **에러로**
  거부하므로 "lock 고정"은 불가능할 뿐 아니라 틀린 요구다. 따라서 올바른 불변식은
  **"lock 제외 산출 트리 diff 0"**. 실측 시 `diff -r -q` 결과가 lock **한 줄**
  (`individualCount`)뿐인지 반드시 눈으로 확인할 것 — "lock만 다르다"와 "lock의 그 한 줄만
  다르다"는 다른 주장이다.
- **결정성**은 같은 트리에서 2회 `--out`을 다른 경로로 뽑아 `diff -r`(0 = byte-identical).
- **인자 형식 함정**: harness 인자는 **bare slug**(`h-multiagent`). `id:core/h-multiagent`처럼
  prefixed IRI를 주면 `✗ no harness matches`로 exit 2 (알려진 하네스 목록을 에러가 출력해준다).
- 섹션이 늘어난 증분은 **다른 하네스에서도** 확인한다 — 조건부 가드 때문에 하네스마다 출력
  섹션이 다르다(예: `h-harness-factory`만 Error handling/Test scenarios를 낸다).
- materialize는 union이 PASS일 때만 산출하므로, 성공 자체가 부가 검증이다.

## 관련
[[federation-lockstep]] (recipe federate 게이트), [[refresh-and-git-baseline]] (커밋 순서).
