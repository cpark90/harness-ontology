# lpranging faithful-reflection 검증 재현 절차 + 함정

recipe가 REAL source harness(`~/git/agrtls/device_harvest_lp/lpranging/`)를 충실히
재반영했는지 판정. 판정: `docs/verify/lpranging-faithful-reflection.md` (pass-with-notes).
전부 `/usr/bin/python3`. odr-bind-lock의 후속 — synthetic 제거 후 single direct ref.

## 핵심 축 = source와 cmp (재반영 진위)
- **primary axis는 validate PASS가 아니라 cmp-against-source**. materialize 산출물을 실제 원본과
  byte-cmp: emitted `tools/docgraph.py` == source `tools/docgraph.py`(32560B), emitted
  `tools/sim_grid_reservation.py` == source `reference/sim_grid_reservation.py`(11309B),
  scaffold `DESIGN_HARNESS_STANDARD.md`/`CODESTYLE.md`/`docs/ONTOLOGY.md` == source. 모두 identical.
- **agent .md는 byte-differ가 정상**: ontology role persona(영어 graph-data)에서 render되므로
  source의 한글 파일과 byte 다름 → cmp 말고 **sanity-read로 persona/scope 의미 대조**.
  set은 정확히 {developer,vnv,inspection}. orchestrator는 role 파일 아님(main agent) = 정답.
- CLAUDE.md operating-rules는 source 6원칙(traceable records / escalate-as-issue /
  verify-then-proceed / design-for-loss / least-privilege / K-E language)을 grep으로 대조.

## synthetic 제거 확인 (odr→faithful 전환)
- recipe dir: `find -iname '*_v2*' -o -iname '*lock*'` = none (docgraph_v2.py + vendored
  harness.lock.json 삭제). ttl grep `Candidate|selectionPolicy` = 주석 1줄만 OK.
- 각 tool은 **single direct repo-relative** `ho:implementationRef "recipes/lpranging/impl/…"`.
- **central TBox는 BIND/lock vocab 그대로 유지**(harness.ttl: Candidate/implementationCandidate/
  selectionPolicy/propertyChainAxiom/implementationRef) — recipe가 안 쓸 뿐 결함 아님.
  implementationRef 정의가 "직접 Tool에 단일 candidate로" 경로를 명시적으로 허용.
- materialize 출력의 `harness.lock.json`은 **build 산출물**(fresh lock written), 삭제된
  vendored recipe 파일과 별개 — residue 아님.

## 재현 (compose+materialize, 심링크 dance)
- 심링크는 **repo root**를 가리켜야: `cd staging/harness-recipes; ln -sfn /repo/root central`.
  주의: `cd` 후 `ln -sfn "$(pwd)" central`은 staging 자신을 가리켜 `central/tools/…` 없음 → 실패.
- union validate = **81** (odr 시절 83에서 2 candidate 빠짐), central = 64.
- materialize tree: CLAUDE.md(+`## Roles`)/MANIFEST/.claude/agents/{3}/tools/{2}/scaffold{3}/
  harness.lock.json. determinism `diff -r A B` IDENTICAL. 끝나면 `rm -f central`.

## 판정 = pass-with-notes (note는 결함 아닌 경계 한계)
- N1 language shift: emitted prose 영어(§1d graph-data) vs source 한글 — 의미충실, byte-copy 아님.
- N2 recipe≠full project: source의 domain design docs(ARCHITECTURE/CONCEPT/SYSTEM_DESIGN,
  docs/{feedback,issues,requirements,...}), .claude/skills, agent-memory, exports/*.manifest,
  reference/ 하위트리는 ontology 표현 없음 → tree에 부재. harness만 모델링하므로 정답이나
  overclaim 방지 위해 한계로 명시.
- N3 vnv role이 simulator tool 추가(source vnv frontmatter엔 없음) — domain 검증하네스로 적정, 결함 아님.

## 후속: coverage/completeness 감사 (2026-07 update) → docs/verify/lpranging-coverage.md
- **BLOCKER 회귀**: central이 `ontology/abox/core/roles.ttl`(7 role, 다 prefLabel 有) 신설 +
  `h-multiagent hasRole` 7 core role 배선. 그런데 **recipe catalog + lpranging.ttl owl:imports가
  `core-roles` unit을 안 넣음**. lpranging은 derivedFrom 위해 core-harnesses import→h-multiagent와
  그 hasRole 7개가 union에 bare IRI로 들어옴→prefLabel shape 7 violation→union FAIL→
  `materialize.py` REFUSE(아무것도 emit 안 함). 증상: validate 출력에 `id2:role-{orchestrator,
  research,inspection-worker,design,...}` prefLabel 없음. **central 자체 validate.py는 PASS**
  (repo-root catalog는 core-roles 매핑함) — 결함은 recipe closure에만.
- **fix(검증됨)**: recipe catalog에 core-roles uri 추가 + lpranging.ttl owl:imports에
  `.../data/core/roles` 추가 = 2줄. scratch 사본에 이것만 넣으면 PASS + materialize 성공.
  → orchestrator에 P0 developer dispatch. techdoc도 같은 잠복 가능성.
- **재현 우회**: repo 파일 못 고치므로 staging 전체를 scratch로 cp → catalog+ttl 패치 →
  central 심링크는 repo root → materialize. build-lpr tree 얻어 coverage 매핑.
- **coverage 결론**: 모델링은 complete enough(persona/9 guardrail/wf/pat/mc/3 role+persona+
  scope+memoryPolicy/2 tool byte-identical/3 scaffold byte-identical). 단 as-shipped는
  materialize 안 됨(B1). GAP-A=domain 설계그래프 content(docs 261+, reference 126, exports,
  agent-memory content, settings.local.json) 전부 out-of-model 정당. GAP-B2(low)=
  .claude/skills 3개(check-docs/new-design-doc/resolve-issue) 미모델 — ho:Instruction/Workflow로
  가능하나 capability(design-graph)는 이미 tool-docgraph+scaffold에 있음.
- source 총 385 파일. .claude/commands는 source에 없음(skill만).

## 후속2: coverage re-audit — P0 해소 + channels 반영 (2026-07-22) → docs/verify/lpranging-coverage-final.md
- **verdict = pass** (BLOCKER 해소). P0 fix = **Option A**(내가 권한 2줄 개별enum보다 깔끔):
  recipe lpranging.ttl가 이제 `owl:imports <.../ontology>`(central ROOT) **하나만**. root가
  schema+모든 core unit(roles line31, channels line32) 재귀 import → 새 core unit이 recipe
  closure를 다시는 조용히 깨지 못함. catalog는 root(id=root)+core-roles+core-channels 매핑.
- union validate = **94**(회귀 전 81/candidate시 83 → roles+channels 합류로 94). PASS.
- **channels 반영**: central `ontology/abox/core/channels.ttl` 3개(chan-agent-user[involvesUser
  true]/chan-orchestrator-inspection/chan-dispatch) — 각 ho:Channel + channelParticipant(roles)+
  involvesUser+channelMedium. h-multiagent(harnesses.ttl:100)·h-lpranging 둘 다 hasChannel 3개.
  recipe엔 local channel 정의 0(재사용만). `hasChannel ⊑ hasComponent`=True → orphan-free.
- materialize: 25 components(22→+3 channel), deterministic. **channel은 MANIFEST components[]에만
  롤업**(type HarnessComponent), 전용 file-emitter 없음 = honest state(projection 미완, 모델 완).
- 잔여 GAP: A(domain content out-of-model 정당)+B2(skills 3 미모델 low). **NEW gap 없음**.
- prevention landed: gr-structural-coverage(guardrails.ttl:41, h-multiagent:96 배선)+CLAUDE.md
  step-7 Coverage-audit gate(56-62)+docs/lessons/coverage-gap-channels.md.
