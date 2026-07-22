# ODR VERIFY axis — capability contracts + artifact judgment (maturity 3–4)

ODR level 3(부합 검증)/4(기술 독립 실증). capability에 검증가능 contract를 붙이고 materialize
산출 트리를 그 contract로 판정. 설계 원본 `docs/odr-contract-verify.md`.

## TBox vocab (중앙, 중립)
- `ho:Contract ⊑ HarnessComponent` — capability의 spec contract(검증 단위).
- `ho:capabilityContract` Capability→Contract (plain object prop).
- `ho:contractKind` Contract→string: "executable" | "structural".
- `ho:contractCheck` Contract→string: executable=트리 root서 실행할 셸 명령(exit0=pass),
  structural=선언 assertion(grammar 아래).
- Contract는 tokenEstimate 안 붙임(Candidate 선례: bind/verify 메타데이터, promptText 없음.
  §1c 규칙은 promptText-bearing+Tool/Workflow만). prefLabel+definition은 필수(ComponentConnectivityShape).

## ★핵심: Contract 도달성 = 3-link property chain (mistype 함정)
Contract⊑HarnessComponent라 orphan shape 대상. Candidate 선례처럼 hasComponent에 chain 추가:
`ho:hasComponent owl:propertyChainAxiom ( ho:hasComponent ho:providesCapability ho:capabilityContract )`.
→ harness hasComponent comp ∧ comp providesCapability cap ∧ cap capabilityContract contract ⟹
harness hasComponent contract. **반드시 hasComponent로 시작(3-link)**: 2-link `(providesCapability
capabilityContract)`면 결론이 `comp hasComponent contract`→prp-dom(hasComponent domain Harness)로
**provider comp가 Harness로 오타입**→HarnessShape trip. (Candidate trap의 판박이.)
hasComponent에 propertyChainAxiom **2개 공존 가능**(candidate용+contract용, owlrl prp-spo2가 각각 처리).
probe로 검증: contract가 harness(들)의 hasComponent로 roll-up + provider NOT Harness + SHACL conforms.
ontology_lib: INSTANCE_CLASSES+=Contract, INSTANCE_LINK_PREDICATES+=capabilityContract. 중앙 96 불변.

## tools/verify_contract.py (VERIFY dual)
- CLI: `verify_contract.py <harness-id> --tree <out> [--format text|json]`. env override 존중(materialize와 동일 load).
- 대상 contract 수집: harness requiresCapability ∪ (컴포넌트 providesCapability) → 각 cap의 capabilityContract.
  IRI-sort로 결정적. contract 없으면 vacuous 0/0 PASS.
- executable: `subprocess.run(shell=True, cwd=tree, capture_output, timeout=120)`, exit0=pass.
- structural grammar(트리-상대 경로, `..`/절대 escape 거부=commonpath 체크):
  `file-exists:<path>` / `file-contains:<path>::<substring>` / `section:<path>::<heading>`.
  section은 **hash-strip한 heading 텍스트**로 비교→`::Coordination channels`와 `::## Coordination channels`
  둘 다 `## Coordination channels` 라인 매치(arg의 leading # lstrip). partition(':')로 op, partition('::')로 인자.
- 판정: 하나라도 fail→exit1. text는 volatile stdout 미포함(결정적), json은 detail 포함.
- gate 아님: validate 게이트 안 돌림(artifact vs spec 판정 전용, reason=True로 load만).

## 데모/게이트
- **Level 3 = faithful lpranging**: cap-designgraph에 contract 2개(structural file-exists:tools/docgraph.py
  + executable AST parse-check `python3 -c "import ast; ast.parse(open('tools/docgraph.py').read())"`),
  cap-simulation에 file-contains:MANIFEST.json::cap-simulation. **contract만 추가, 합성 candidate 금지**
  (faithful 유지). docgraph는 no-arg시 exit2(docs/ 필요)라 parse-check가 안전한 executable. materialize→verify 3/3 PASS.
  주의: contract가 hasComponent-reachable라 MANIFEST components 목록에 뜸(+N)=정상(파일 emit은 안 됨, 어떤 emitter도 안 건드림).
  CLAUDE.md/tools/skills는 불변→source fidelity 유지(MANIFEST는 build 부기, 실소스에 없음).
- **Level 4 = INV-4 candidate swap**: 별도 데모 recipe `recipes/contract-demo/`(lpranging 오염 방지).
  tool-greeter 2 candidate(greeter_v1 stable 직접print / greeter_v2 next 함수빌드, **출력 동일·소스 상이**)
  +selectionPolicy. cap-greet contract=file-exists + executable behavioral `python3 tools/greeter.py | grep -q 'hello world'`.
  A(latest-stable→v1) verify PASS → policy sed→pinned:next(rebuild→v2, emit파일 differ) verify **동일 PASS** →
  복원. 증거: emitted greeter.py diff differ + per-contract verdict identical(json에서 tree경로 제외 비교).
  candidate-backed tool은 stable 파일명(tool-greeter→tools/greeter.py)이라 swap=내용만 바뀜.
- 게이트: 중앙 validate PASS·96불변·양 로더 동치, recipe compose PASS, materialize 2런 IDENTICAL,
  verify PASS(exit0)·tamper(파일삭제)→FAIL(exit1), no-contract harness(h-coding)=vacuous PASS.
- 중앙 neutral: ontology/abox/ 무변경(grep contract=0), TBox vocab+tools+docs만. staging(recipes repo)은
  gitignore=lpranging/contract-demo/catalog 변경분은 recipe-side(중앙 커밋 대상 아님). central 심링크 실행후 rm.
