# ODR contract-VERIFY 축 검증 재현 절차 + 함정

`ho:Contract`/`capabilityContract`/`contractKind`/`contractCheck` + `tools/verify_contract.py`
(ODR level 3~4) 판정. 판정: `docs/verify/odr-contract-verify.md` (pass-with-notes). 전부 `/usr/bin/python3`.

## 핵심 = property-chain 3링크 타입체크 (Candidate rollup의 거울상)
- `ho:hasComponent owl:propertyChainAxiom ( ho:hasComponent ho:providesCapability ho:capabilityContract )`.
  3링크(hasComponent 접두)라 추론 subject가 항상 **Harness**. 2링크(`providesCapability capabilityContract`)면
  `component hasComponent contract` → hasComponent domain=Harness(prp-dom)로 provider component를
  Harness로 오타입 → HarnessShape trip. Candidate(implementationCandidate) rollup과 동일 패턴.
- 증명(reason=True union): tool-docgraph/tool-simulator types=Tool/HarnessComponent(**Harness 아님**),
  cap-designgraph/cap-simulation=Capability만, contract 3개 types=Contract/HarnessComponent이고
  `(h-lpranging, hasComponent, contract)`=True(rollup). shapes diff empty, sh:closed 무변경.

## 중립성/구조 (level 1~2 회귀 없음)
- central validate PASS 96 reachable. **both loader paths=96**: 기본(catalog owl:imports 클로저) vs
  glob fallback(`HARNESS_CATALOG=/nonexistent`)로 강제. contract 어휘는 central abox에 0
  (`grep ontology/abox/ = 0`, central Contract instance 0). retrieve pack에 build-only prop
  (contractCheck/contractKind/capabilityContract/implementationRef/selectionPolicy) leakage 0.
- lpranging union 119 reachable / contract-demo union 107 reachable (contract가 orphan 아님).
- TBox diff는 harness.ttl만(+25/-1): Contract/capabilityContract/contractKind/contractCheck + chain 1줄.

## verify_contract 실행 (materialize의 dual)
- `verify_contract.py <hid> --tree <t>` — union의 capability contract(harness requires ∪ 컴포넌트
  provides) 수집, contractKind로 dispatch. IRI정렬(결정적). exit≠0 iff 하나라도 fail. no-contract=vacuous 0/0 PASS.
- **executable**: `contractCheck`를 shell=True, cwd=tree, timeout 120s로 run, exit0=pass.
- **structural** grammar: `file-exists:<p>` / `file-contains:<p>::<sub>` / `section:<p>::<heading>`
  (heading은 `#` strip 후 텍스트 비교). `_safe_join`이 `..`/절대경로 escape 거부(normpath+commonpath).
  in-tree `tools/../tools/x`는 정규화되어 허용(정상).

## level 3 (lpranging) — artifact 판정이 validate와 별개임을 증명
- materialize h-lpranging → verify 3/3 PASS(exit0). **tree COPY에서 `rm tools/docgraph.py`** →
  structural+executable 계약 둘 다 FAIL(exit1), MANIFEST 계약만 PASS = 1/3 FAIL. union은 여전히
  validate PASS인데 tree는 FAIL → verify는 산출물을 본다(원리3/§5). 결정성: diff -r 트리 동일,
  같은 tree 재실행 byte-identical. JSON은 `tree` 절대경로 필드만 빌드간 다름(verdict 아님) → contracts 배열은 동일.

## level 4 / INV-4 (contract-demo) — 핵심 주장
- cap-greet에 structural(file-exists:tools/greeter.py)+executable(`python3 tools/greeter.py | grep -q 'hello world'`).
  tool-greeter에 후보 2개(stable v1 bare print / next v2 fn+__main__), selectionPolicy shipped=latest-stable.
- **재바인드 방법**: --policy CLI 없음. staging 전체를 scratch로 cp → central 심링크 재생성 → scratch
  recipe의 `ho:selectionPolicy "latest-stable"`→`"pinned:next"` sed(shipped 무수정). materialize demoB.
- build A(latest-stable→v1) 2/2 PASS, build B(pinned:next→v2) 2/2 PASS. **소스 v1≠v2, emitted greeter.py
  A≠B(diff), 파일명 slot tools/greeter.py 불변**, 둘 다 실행시 hello world, verdict 동일 → INV-4 실증.

## refusal/hygiene
- bogus harness id exit2, --tree 비디렉토리 exit2, vacuous PASS exit0.
- 심링크는 한 블록에서 만들고 마지막에 rm(trap 금지, 각 Bash 별도 셸). 끝나면 `find staging -type l`=empty 확인.

## 판정
pass-with-notes. level 3(auto-judged lpranging)·level 4(candidate swap 동일 verdict) 정당 도달.
N1(structural 계약은 얕음·wiring만; 강보장은 executable 필요), N2(executable=graph발 arbitrary shell,
trusted recipe에서만 실행해야—CI test와 동급 신뢰경계), N3(재바인드 CLI flag 없음, 정책은 graph fact라 recipe 편집). 전부 문서/운영 노트, ontology 결함 아님.
