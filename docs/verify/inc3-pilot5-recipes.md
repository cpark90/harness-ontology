# vnv 판정 — harness-100 inc3 파일럿 5 recipe

> 판정: vnv dispatch (2026-07-23). 독립 재실행(developer self-check 불신뢰). 전부 `/usr/bin/python3`.
> 대상: `staging/harness-recipes/recipes/{21-code-reviewer,16-fullstack-webapp,31-ml-experiment,03-newsletter-engine,46-product-manager}`.
> 상위: `docs/plans/inc3-pilot5-results.md`(저작취합), 브리프 `docs/plans/dispatch-inc3-pilot5-recipes.md §1e`.

## 종합 verdict (1줄)

**5 recipe 전부 PASS-with-notes** — graph verification(validate 4체크)·composition validation
(materialize round-trip·retrieve 후보·HarnessShape·tokenEstimate·Golden Rule #2) 전부 green.
단 **1개 알려진 BLOCKER**(persona-ref hard-fail, 임시 scratchpad 경로 의존 — recipe 범위 밖
central materialize.py 동작)는 **inspection push 前 선결**이며 여기서 **독립 재확인**됨.

## 재현 명령 (per-recipe closure)

```bash
cd /home/cpark/git/harness_ontology/staging/harness-recipes
HARNESS_CATALOG=<catalog> HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<name> \
/usr/bin/python3 central/tools/validate.py        # per-recipe closure = 중앙 126 + 그 recipe 1개
# 21-code-reviewer → catalog-v001.xml ; 나머지 → catalog-<name>.xml
```
catalog에 다른 recipe URI가 매핑돼 있어도 `HARNESS_ROOT_ONTOLOGY`가 해당 recipe만 owl:imports
closure에 넣으므로 **union 아님**(각 validate가 "1 harness declares assembly order"로 확증).

---

## Recipe별 판정

각 항목: (1) closure validate, (2) materialize round-trip, (3) retrieve, (4) persona-blocker.

### 21-code-reviewer — PASS-with-notes
- **(1) validate PASS** — SHACL·reachability·capabilities·assemblyOrder 4/4 ✓. individuals=**141**
  (중앙 126 + 로컬 15, results.md 일치). 1 harness assembly order(8 sections). 모든
  `requiresCapability`(cap-fileedit/cap-codeexec/cap-orchestration/cap-synthesis) 내부 provider로 충족.
- **(2) round-trip** — `materialize.py h-code-reviewer` exit 0. 2회 백투백 `diff -r` **IDENTICAL**
  (결정적). tree = agents(5: 4 worker + synthesizer) + skills(3) + CLAUDE.md + MANIFEST.json + harness.lock.json.
  skill 3개 corpus `skill.md`와 **byte-identical**(cmp). MANIFEST skills status=**resolved**, `.ref` stub 0개
  (corpus 존재). persona = graph frontmatter + fetched corpus body.
- **(3) retrieve** — "Automated code-review agent team"가 **TOP candidate**(relevance 9.9;
  runner-up 4.5 대비 뚜렷). 기본 budget의 `gaps`는 provider 노드가 pack에 안 딸려온 projection 산물 —
  `--budget 6000`에서 **gaps=[]**로 소멸(재확인). discoverability PASS.
- **(4) persona-blocker** — 아래 §BLOCKER. persona ref 8개 전부 임시 scratchpad 절대경로.

### 16-fullstack-webapp — PASS-with-notes
- **(1) validate PASS** — 4/4 ✓. individuals=**144**(로컬 18). deviation: **로컬 `id:role-qa-engineer`**
  (test-engineering worker + gate 하이브리드)가 `ho:providesCapability core:cap-synthesis` — **cap IRI 재사용**
  (신규 cap 0), hasRole 바인딩으로 harness cap-synthesis 충족. HarnessShape/Golden Rule #2 부합 → **정당 deviation**.
  tool-scope 변이: architect/frontend=editor-only, backend/devops/qa=editor+shell(least-privilege slice).
- **(2) round-trip** — exit 0, `diff -r` IDENTICAL. agents(5) + skills(3) + CLAUDE/MANIFEST/lock. stub 0.
- **(3) retrieve** — "Fullstack web-app delivery agent team" **TOP**(9.0). budget6000 잔여 gaps(Document
  retrieval/Web search)는 **co-scope 중앙 harness 소유**(16은 그 cap 미요구) — recipe 결함 아님(§N2).
- **(4) persona-blocker** — persona ref 9개 임시 scratchpad 경로. §BLOCKER.

### 31-ml-experiment — PASS-with-notes
- **(1) validate PASS** — 4/4 ✓. individuals=**146**(로컬 20). 신규 로컬 `id:dom-ml`·`id:task-mlexperiment`
  (중앙 부적합), concept는 `skos:topConceptOf core:scheme`/`skos:broader`로 접붙여 orphan 0(reachability 확증).
- **(2) round-trip** — exit 0, IDENTICAL. agents(5) + **skills(4)** + CLAUDE/MANIFEST/lock. stub 0.
- **(3) retrieve** — "ML-experiment agent team" **TOP**(3.96; rank #1이나 절대값 낮음 — §N3). budget6000
  잔여 gaps는 co-scope 중앙 harness 소유.
- **(4) persona-blocker** — persona ref 9개. §BLOCKER.

### 03-newsletter-engine — PASS-with-notes
- **(1) validate PASS** — 4/4 ✓. individuals=**146**(로컬 20). 신규 로컬 `id:dom-content`·`id:task-newsletter`.
  tool 변이: curator/analyst가 **`core:tool-websearch`+`core:cap-websearch`**(재사용 core, 신규 0),
  **tool-shell/cap-codeexec 미바인딩**(PM성 산출) — least-privilege 정직반영. editor-in-chief=로컬 worker role.
- **(2) round-trip** — exit 0, IDENTICAL. agents(5) + skills(4) + CLAUDE/MANIFEST/lock. stub 0.
- **(3) retrieve** — "Newsletter-production agent team" **TOP**(7.2). budget6000 잔여 gaps(Code execution 등)는
  co-scope 중앙 harness 소유(03은 cap-codeexec 미요구) — 결함 아님.
- **(4) persona-blocker** — persona ref 9개. §BLOCKER.

### 46-product-manager — PASS-with-notes
- **(1) validate PASS** — 4/4 ✓. individuals=**146**(로컬 20). 신규 로컬 `id:dom-product`·`id:task-productplanning`.
  editor-only 전체, cap-codeexec 없음.
- **(2) round-trip** — exit 0, IDENTICAL. agents(5) + skills(3) + CLAUDE/MANIFEST/lock. stub 0.
- **(3) retrieve** — "Product-management planning agent team" **TOP**(8.1). budget6000 **gaps=[]**.
- **(4) persona-blocker** — persona ref 8개. §BLOCKER.

---

## §BLOCKER — persona-ref hard-fail 비대칭 (독립 재확인)

results.md ★주장(persona ref 부재→abort / skill ref 부재→stub)을 **scratch 복제본에서 실증**
(실 recipe 미편집). 21-code-reviewer ttl을 scratch로 복사해 각 1개 ref만 nonexistent로 치환:

| 변이 | 결과 |
|---|---|
| **skill** artifactTemplate 깨짐 | **exit 0** + `.claude/skills/vulnerability-patterns/SKILL.md.ref` stub 생성 (graceful) |
| **persona** artifactTemplate 깨짐 | **exit 1**, `FileNotFoundError` at `materialize.py:129` (`resolve_template`), **out dir 미생성**(atomic) |

- 원인: persona는 `render_component`→`render_from_template`→`resolve_template`(strict, stub 대체 없음),
  skill/impl/scaffold emitter만 unresolvable 시 `<dest>.ref` stub로 감쌈.
- **graph-level PASS에는 영향 없음**: ref는 노드를 추가/제거하지 않으므로 validate 4체크 전부 green(위 5개 확인).
- **scratchpad 소멸 후 build blocker**: 5 recipe의 persona ref 43개(8+9+9+9+8)가 전부
  `/tmp/claude-1000/.../528b6512.../scratchpad/harness-100/en/<h>/...` 임시경로 → 이 세션 scratchpad가
  지워지면 **모든 recipe materialize가 exit 1로 hard-fail**. (현재는 corpus 존재 → 위 round-trip green.)
- 범위: 중앙 `materialize.py` 동작이라 recipe 범위 밖. **inspection push 前 선결**: 영속 corpus 경로 확정 +
  5 recipe artifactTemplate 일괄 치환(developer dispatch), 또는 persona도 graceful-stub化. (판정만 — 미수정.)

## 추가 검증 (validation 축)

- **tokenEstimate**: 5 recipe 전부 `promptText`·`artifactTemplate` 보유 노드에 tokenEstimate 완비(누락 0).
- **Golden Rule #2**: 5 pilot recipe 신규 capability **0**(16=`core:cap-synthesis` 재사용, 03=`core:cap-websearch`
  재사용). `id:cap-*` 로컬정의는 lpranging/contract-demo(범위 밖)에만 존재.
- **drift**: 각 closure 내 duplicate prefLabel 0(validate 경고체크 green). 신규 로컬 dom/task/concept는
  scheme 접붙임으로 orphan 0(reachability green).
- **HarnessShape 최소구성**: SHACL conforms가 1 SystemPrompt + ≥1 Workflow + tool + guardrail + ModelConfig
  강제 — 5개 전부 통과.

## Notes (non-blocking 관찰)

- **N1 (output fidelity)**: emitted `.claude/agents/<role>.md`가 **graph-생성 frontmatter + fetched corpus
  body** 순인데, corpus agent md 자체가 YAML frontmatter로 시작 → 산출 파일에 **frontmatter 블록 2개**(중첩).
  소비자(Claude Code)는 최상위 frontmatter를 읽으므로 기능상 무해하나, 충실도 관점 관찰. persona에
  artifactTemplate를 준 이번 방식(브리프 1c 허용)의 부산물. → 후속 정리 검토 권고(권고, 비차단).
- **N2 (retrieve gaps 의미)**: retrieve `gaps`는 **pack 전역**(in-scope 모든 harness의 requiresCapability 중
  provider가 budget에 안 딸려온 것)이라 candidate-specific 아님. 기본 budget의 gaps·budget6000 잔여 gaps
  (16/31/03의 Document retrieval/Web search/Code execution)는 **co-scope 중앙 harness 소유**이거나 projection
  산물 — recipe 결함 아님. 권위 기준은 validate의 per-harness capability 체크(green).
- **N3 (31 relevance margin)**: 31-ml-experiment TOP relevance 3.96 — rank #1이나 절대값이 낮음(prefLabel/
  definition의 lexical distinctiveness가 질의어 대비 약함). discoverable(PASS)이나 향후 batch에서 ML 도메인
  질의어와의 매칭 강화 여지 관찰(비차단).
