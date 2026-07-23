# harness-100 inc3 파일럿 5 recipe 검증 재현 절차 + 함정

recipe-local blueprint 5개(21-code-reviewer/16-fullstack-webapp/31-ml-experiment/03-newsletter-engine/
46-product-manager)를 harness-100 corpus에서 파생. 판정: `docs/verify/inc3-pilot5-recipes.md` = 5개 전부
**PASS-with-notes** + 1 known BLOCKER(persona-ref hard-fail). 전부 `/usr/bin/python3`.

## per-recipe closure(union 금지) 재현
- `cd staging/harness-recipes`; `central`은 **pre-existing working-tree 심링크**(내가 안 만들었으면 rm 금지).
- `HARNESS_CATALOG=<cat> HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/<name>
  /usr/bin/python3 central/tools/validate.py`. 21→catalog-v001.xml, 나머지→catalog-<name>.xml.
- catalog에 다른 recipe URI 매핑돼 있어도 `HARNESS_ROOT_ONTOLOGY`가 owl:imports closure를 그 recipe로 한정 →
  **union 아님**. 확증 신호: validate "1 harness declares assembly order"(2개면 union 샌 것).
- individuals: 21=141, 16=144, 31/03/46=146 (중앙 126 + 로컬 15/18/20/20/20). capabilities 체크 green =
  모든 requiresCapability가 provider 컴포넌트로 충족(권위 기준, retrieve gaps 아님).

## materialize round-trip (recipe별 분리 out, 병렬 오염 주의)
- `materialize.py h-<name> --out <scratch>/<name>-A` (CLI = harness + `--out` 필수). corpus 존재 시 exit 0.
- 결정성 = 2회 백투백 `diff -r A B` IDENTICAL. tree = agents 5(worker 4 + synthesizer) + skills 3~4 +
  CLAUDE.md + MANIFEST.json + harness.lock.json. skill SKILL.md는 corpus skill.md와 **byte-identical**(cmp).
  MANIFEST skills status=resolved, `.ref` stub 0(corpus present).
- **out은 내 scratchpad에만**, 판정 후 rm. staging/repo에 out/.ref/MANIFEST 잔재 0 확인(git status).

## ★persona-ref hard-fail 비대칭 실증 (핵심)
- **skill/impl/scaffold** artifactTemplate unresolvable → emitter가 `<dest>.ref` stub, **exit 0**.
- **persona** rolePersona artifactTemplate unresolvable → `render_component`→`render_from_template`→
  `resolve_template`(materialize.py:129) **FileNotFoundError raise, exit 1, out dir 미생성(atomic)**. stub 대체 없음.
- **graph PASS엔 영향 0**(ref는 노드 add/remove 안 함) → validate green이어도 build는 hard-fail 가능. 두 축 분리.
- 실증 재현(실 recipe 미편집): 21 ttl을 scratch 복사 → 1개 persona ref만 nonexistent로 sed = exit1/no-out ;
  1개 skill ref만 sed = exit0/stub. scratch catalog는 catalog-v001을 sed로 `uri="central/`→절대경로,
  recipe uri→scratch ttl 절대경로 치환(catalog uri는 os.path.join(base,uri), 절대경로면 base 무시).
- **이번 5 recipe 함정**: persona ref 43개(8/9/9/9/8) 전부 임시 세션 scratchpad 절대경로
  (`/tmp/claude-1000/.../<UUID>/scratchpad/harness-100/en/<h>/...`). 그 scratchpad 소멸 = 전 recipe
  materialize exit1 build blocker. finalize/push 前 영속경로 확정+치환(developer) or persona graceful-stub化 필요.

## retrieve gaps 오판 금지 (N2)
- retrieve `gaps` = **pack 전역**: in-scope 모든 harness의 requiresCapability 중 provider가 budget에 안
  딸려온 것. candidate-specific 아님. 기본 budget(900)에선 recipe 자신 cap도 gap으로 뜸(projection 산물).
- 검증법: `--budget 6000`로 올리면 recipe 자신 cap gap 소멸. 잔여 gaps(예 16/31/03의 Document retrieval/
  Web search/Code execution)는 **co-scope 중앙 harness** 소유(그 recipe가 미요구) → 결함 아님.
- discoverability 판정 = recipe harness가 자기 질의에 **TOP candidate**인지(21=9.9/16=9.0/03=7.2/46=8.1/
  31=3.96). 31은 rank#1이나 relevance 낮음(prefLabel lexical distinctiveness 약함, N3, 비차단).

## 관찰 (non-blocking)
- N1 output fidelity: emitted agent .md = graph frontmatter + fetched corpus body인데 corpus md 자체가
  YAML frontmatter로 시작 → **frontmatter 중첩 2블록**. persona에 artifactTemplate 준 부산물(faithful 시절엔
  persona=promptText inline이라 없던 문제). 소비자는 최상위만 읽어 무해하나 정리 권고.
- deviation 정당 판정: 16 로컬 `id:role-qa-engineer`가 `providesCapability core:cap-synthesis`(cap IRI 재사용,
  신규 cap 0) = Golden Rule #2 부합. 03 `core:tool-websearch`+`core:cap-websearch` 재사용, shell 미바인딩 =
  least-privilege 정직반영. 신규 로컬 dom/task는 scheme(topConceptOf/broader) 접붙임으로 orphan 0.
- tokenEstimate: promptText·artifactTemplate 보유 노드 전부 완비(누락 0) — subjects(HO.promptText)/
  subjects(HO.artifactTemplate) 중 tokenEstimate 없는 것 스캔.
