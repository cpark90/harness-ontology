# ODR BIND + Lock 검증 재현 절차 + 함정

`ho:Candidate`/`implementationCandidate`/`selectionPolicy` (BIND) + `materialize.py`
lock(③) 증분 판정. 판정: `docs/verify/odr-bind-lock.md` (pass-with-notes). 전부 `/usr/bin/python3`.

## 심링크/PYTHONPATH 함정 (중요)
- 각 Bash 호출은 **별도 셸** — `trap 'rm central' EXIT`를 걸면 그 블록 끝에 심링크가 사라져
  다음 블록에서 core 미해소 → union이 recipe-local만(예 lpranging 19 individuals). 심링크는
  **한 블록에서 만들고, 검증 다 끝난 마지막 블록에서 rm** 하라 (trap 쓰지 말 것).
- 심링크 없거나 core 안 붙으면 union 개수로 즉시 탐지: lpranging full union = **83** (central 81
  effektiv + 2 candidates; validate는 "all 83 reachable"). recipe-local만이면 19.
- ad-hoc 파이썬으로 union 로드 시 import: validate.py는 `import ontology_lib as lib` (스크립트
  dir). staging cwd에서 one-liner는 `PYTHONPATH=central/tools`(심링크 상대경로 OK, 단 심링크가
  존재해야) 필요. `tools.ontology_lib`(패키지경로)는 tools/__init__.py 없어서 실패.

## 핵심 검증 = property-chain 타입체크 (ratified deviation)
- brief 원안 `implementationCandidate rdfs:subPropertyOf hasComponent`는 **틀림**: hasComponent
  `rdfs:domain ho:Harness` → prp-dom로 Tool subject가 Harness로 추론 → HarnessShape trip
  (rolePersona domain-trip의 거울상, developer memory에 기록됨).
- 채택안 = `ho:hasComponent owl:propertyChainAxiom ( ho:hasComponent ho:implementationCandidate )`.
  증명: `load_graph(reason=True)` 후 `tool-docgraph` rdf:types = `[HarnessComponent, Thing, Tool]`
  (**Harness 아님**), `(harness, hasComponent, cand)` = True (chain roll-up), cand는 Candidate만
  (Tool/Harness 아님). shapes 무변경(`git status ontology/shapes` empty, `sh:closed` 0). → 건전, ratify.
- `implementationRef`·`selectionPolicy` **rdfs:domain 제거**도 정답(Tool domain이면 Candidate 오타입 /
  selectionPolicy는 Tool+Harness 공용이라 단일 conjunctive domain 불가). 모든 user 명시 타입 → central 64 불변.

## 정책 선택 + lock 재현 (materialize)
- no-lock build A → `latest-stable` = tag==stable 중 최고 version. lpranging: cand-docgraph-stable
  (v1.4.0) 선택 → emitted `tools/docgraph.py` **cmp**로 `impl/docgraph.py`와 byte-identical,
  `impl/docgraph_v2.py`와 differ. 파일명은 tool-derived **stable**(`tools/docgraph.py`, 후보 바꿔도 불변).
- vendored `harness.lock.json` == fresh A lock (byte-identical; lock에 timestamp 없음).
- 재현: `--lock <vendored> --out B` → `diff -r A B` empty (INV-2). 결정성: A2 == A.
- vendored lock contentHash sha256 == vendored impl 파일 재계산 해시로 대조.

## tamper 테스트 함정 — 부분쓰기 (N1)
- **scratch 복사본에만** tamper (vendored lock 절대 수정 금지; 끝나면 git status로 pristine 확인).
- `individualCount` tamper → `_verify_lock_spec`가 **쓰기 전** 실패 → out dir 비어있음(clean).
- `contentHash` tamper → `emit_implementations`의 per-tool 해시게이트가 **copyfile 이후** 실행 →
  exit 1이지만 out dir에 부분물(role .md들 + 복사된 tools/docgraph.py) 남음, CLAUDE.md/MANIFEST/
  lock는 없음. `docs/odr-bind-lock.md`의 "nothing half-written"과 불일치 = **N1 note**(재현계약은
  유지 — 완결 build 절대 안 나옴). 원하면 emit 전 전량 해시검증 or temp+atomic move 권고.

## INV-4 정책스왑
- scratch recipe 복사 → `selectionPolicy "latest-stable"`→`"pinned:next"` 치환(shipped 무수정).
  주의: ttl 주석에 이미 `"pinned:next"` 있어 grep count 2 나옴(정상). materialize → emitted
  docgraph.py == docgraph_v2.py, 파일명 여전히 tools/docgraph.py, compose validate+emit 둘 다 PASS.

## 판정
pass-with-notes. 7항목 전부 통과. N1(contentHash tamper 부분쓰기 vs "nothing half-written" 문구),
N2(unrecognised policy가 latest-stable로 soft-fallback — pinned만 hard-error). 성숙도 level 2
(재현가능) 정당 도달; level 3-4(contract-VERIFY)는 문서가 open으로 정직히 선언.
