# harness-100 inc3 파일럿 5 recipe — 저작 결과 (developer dispatch 취합)

> 작성: orchestrator (2026-07-23). developer 5 dispatch(opus) 산출 취합. 상위: `docs/feedback/harness-100-augmentation.md`(inc3), 브리프: `docs/plans/dispatch-inc3-pilot5-recipes.md`.
> **상태(2026-07-23 최종): 저작·vnv판정·영속경로 치환 완료 → BLOCKER 해소, PUSH-READY. 남은 것 = inspection push(별도 세션).**
> - **영속경로 치환 완료(developer)**: 코퍼스 `git clone --depth 1` → `/home/cpark/git/harness-100`(revfactory/harness-100, Apache-2.0). artifactTemplate 38건 → 로컬 영속경로, dct:source 5건 → GitHub canonical URL(`.../tree/main/en/<h>`). 재검증 **5/5 validate PASS + materialize stubs=0(persona resolve, abort 없음)·2회 diff IDENTICAL**. 잔여 scratchpad ref 0. → ★BLOCKER(아래) 해소.
> - **vnv 판정**: 5개 전부 **PASS-with-notes** (`docs/verify/inc3-pilot5-recipes.md`). validate 141/144/146/146/146, materialize 결정적(diff IDENTICAL), retrieve 5개 자기질의 TOP candidate(21=9.9,16=9.0,46=8.1,03=7.2,31=3.96). deviation(16 로컬 qa-engineer cap-synthesis 재사용, 03 websearch/no-shell) 부합 판정.
> - **사용자 결정(2026-07-23)**: ① 영속 소스=**로컬 안정 클론 `/home/cpark/git/harness-100`**(artifactTemplate 치환, dct:source=GitHub canonical URL). ② persona hard-fail=**유지**(경로치환으로 해소, 중앙 materialize 변경 안 함).
> - **진행 중(developer)**: 코퍼스 영속 클론 + 5 recipe ref 일괄 치환 + 재검증(materialize resolve 0-stub 확인).
> - **비차단 note N1**(vnv): emitted `.claude/agents/<role>.md`가 graph frontmatter + corpus body frontmatter **2블록 중첩**. 기능 무해, output-fidelity 정리 별도 후속 검토.

## 산출물 (staging/harness-recipes/recipes/)
| recipe | 로컬 id: | per-recipe closure | materialize |
|---|---|---|---|
| 21-code-reviewer | 15 | PASS 141 | green(byte-identical·결정적·stub 확인) |
| 16-fullstack-webapp | 18 | PASS 144 | green(tool-scope 변이 반영) |
| 31-ml-experiment | 20 | PASS 146 | green |
| 03-newsletter-engine | 20 | PASS 146 | green |
| 46-product-manager | 20 | PASS 146 | green |

각 recipe는 `<name>.ttl` + `README.md` + 전용 `catalog-<name>.xml`(자기검증용) 보유. `staging/harness-recipes/central` = working-tree 심링크(gitignored).
검증 = per-recipe closure(중앙 126 + 그 recipe) 1개씩 — **all-recipes union 안 함**(roadmap §5).

## QA-gate(synthesizer) 매핑 — promote-once 실전 검증
`core:role-synthesizer`(inc2 중앙승격) 재사용이 5개 중 4개 clean fit:
- ✅ 재사용: review-synthesizer(21) · experiment-reviewer(31) · quality-reviewer(03) · pm-reviewer(46).
- ⚠ deviation(정당): **16 qa-engineer** = test-engineering worker + gate 하이브리드(Vitest/Playwright 실행 → shell·distinct persona 필요). 로컬 `id:role-qa-engineer` 저작하되 `ho:providesCapability core:cap-synthesis`(**cap IRI 재사용, 신규 cap 0**)로 harness 요구 충족.
- 03 editor-in-chief = 로컬 worker role(publish-ready 산출물 생산, 게이트 아님) — quality-reviewer와 구별.
→ 결론: 중앙 role-synthesizer 승격이 실전 검증됨. 하이브리드役은 "cap 재사용 + 로컬 role"로 흡수 가능.

## 신규 로컬 노드 (결정2=recipe-local 유지; 중앙승격 후보 flag)
- Domain: `id:dom-ml`(31) · `id:dom-content`(03) · `id:dom-product`(46). (21·16은 `core:dom-coding` 재사용.)
- Task: `id:task-mlexperiment`(31) · `id:task-newsletter`(03) · `id:task-productplanning`(46). 중앙 task 부적합.
- → batch wave가 재발 확인 시 중앙승격 재평가(현재는 recipe-local, Golden Rule #2 준수).

## tool 축 변이 (least-privilege 충실반영)
- 16: 5役 상이 slice — architect/frontend=editor-only, backend/devops/qa=editor+shell(ORM migration·dev server 실행 원문 명시).
- 03: curator/analyst가 WebSearch → `core:tool-websearch`+`cap-websearch` 바인딩, **shell 없음**(`tool-shell`/`cap-codeexec` 미바인딩).
- 46: editor-only 전체, `cap-codeexec` 없음(PM은 markdown 산출).
→ harness의 requiresCapability set이 role tool 실사용에서 정직하게 도출됨(추측 배정 아님).

## coordination (결정1=pluggable both)
전 recipe: `core:pat-orchestrator-workers` + `core:pat-peer-mesh` 공존, channel `core:chan-workspace`(`_workspace/NN_*.md` handoff)+`core:chan-peer`(SendMessage mesh)+`core:chan-agent-user`. (03·16은 원문에 "communicate directly via SendMessage" 강함.)

## ★ BLOCKER — persona-ref hard-fail 비대칭 (✅ 해소됨 2026-07-23: 영속경로 치환 완료. 아래는 이력)
- materialize resolver: skill/impl/scaffold `artifactTemplate` 부재 → graceful `.ref` stub(exit 0). **그러나 persona `rolePersona`의 `artifactTemplate` 부재 → `render_component`→`resolve_template` strict 경로가 FileNotFoundError raise, build abort.**
- 5 recipe 전부 persona ref가 **임시 scratchpad 절대경로**(`/tmp/claude-1000/.../528b6512.../scratchpad/harness-100/en/<h>/...`)를 가리킴 → scratchpad 소멸 시 materialize **hard-fail**.
- ⇒ **영속 corpus 소스 경로 확정·치환이 finalize/push 前 build 선결조건**(단순 fidelity 손실 아님). 중앙 materialize.py 동작이라 recipe 범위 밖 — **orchestrator/사용자 결정 필요**(경로 확정 or persona도 graceful stub化).

## 공유 catalog 통합 대기 (5줄 — inspection push 시 `catalog-v001.xml`에 통합)
21-code-reviewer는 이미 공유 catalog에 추가됨. 나머지 4줄(각 developer가 문자열만 리포트, 공유 catalog 미편집):
```xml
<uri id="recipe-16-fullstack-webapp" name="https://harness-ontology.dev/recipes/16-fullstack-webapp" uri="recipes/16-fullstack-webapp/16-fullstack-webapp.ttl"/>
<uri id="recipe-31-ml-experiment"    name="https://harness-ontology.dev/recipes/31-ml-experiment"    uri="recipes/31-ml-experiment/31-ml-experiment.ttl"/>
<uri id="recipe-03-newsletter-engine" name="https://harness-ontology.dev/recipes/03-newsletter-engine" uri="recipes/03-newsletter-engine/03-newsletter-engine.ttl"/>
<uri id="recipe-46-product-manager"  name="https://harness-ontology.dev/recipes/46-product-manager"  uri="recipes/46-product-manager/46-product-manager.ttl"/>
```

## 다음 단계
1. **vnv dispatch**(진행): 5 recipe 각 per-recipe closure PASS 재확인 + materialize round-trip 재현 + retrieve sanity → `docs/verify/inc3-pilot5-*.md`. (저작·판정 분리 — 개발자 self-check 신뢰 아닌 독립 판정.)
2. **영속 소스경로 결정**(사용자): 코퍼스 영구 클론 위치 확정 → 5 recipe의 artifactTemplate/dct:source 일괄 치환(developer dispatch). persona hard-fail 해소.
3. **inspection push**(별도 세션): (a) 중앙 pile @126 land(`inspection-brief-CONSOLIDATED-since-batch3.md`), (b) vnv green + 경로치환 후 recipes repo에 5 recipe + catalog 5줄 통합 push + Apache-2.0 NOTICE.
4. inc3 green → **importer(inc4)** 착수 재평가(결정5: 파일럿 후 batch 범위).
