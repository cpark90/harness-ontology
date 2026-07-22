# ODR BIND axis + Lock — implementation candidates & reproducible builds

materialize 증분: 하나의 중립 SPEC(tool+capability)을 시대별 **여러 구현으로 치환**하되
**재현 가능**하게. METHODOLOGY.md(ODR) BIND축(②)+Lock(③). 설계 원본 `docs/odr-bind-lock.md`.

## TBox vocab (중앙, 중립)
- `ho:Candidate ⊑ HarnessComponent` — Tool의 구현 옵션 1개(ref+version+tag).
- `ho:implementationCandidate` Tool→Candidate (plain object prop, NOT subPropertyOf hasComponent).
- `ho:candidateVersion`/`ho:candidateTag` (Candidate→string, domain Candidate 안전).
- `ho:selectionPolicy` (Tool 또는 Harness→string) — domain 없음(둘 다 or이라 conjunctive domain 불가).
- `ho:implementationRef` — domain 제거. Candidate가 지님(어느 파일) OR Tool 직접(degenerate
  1-candidate). 우선순위: 명시 candidates > 직접 ref > stub. Tool domain 유지시 이 ref 지닌
  Candidate가 prp-dom로 Tool 오타입되므로 domain 제거 필수(inference만 감소·검증 불변·중앙 64 유지).

## ★핵심 함정: candidate 도달성 = property chain (subPropertyOf 아님)
Candidate⊑HarnessComponent라 ComponentConnectivityShape(inverse hasComponent≥1) 대상.
`implementationCandidate ⊑ hasComponent`로 하면: hasComponent domain=Harness → tool
implementationCandidate cand ⟹(prp-spo1) tool hasComponent cand ⟹(prp-dom) **tool a Harness**
→ HarnessShape(targetsDomain/task/wf 필요) trip. (rolePersona domain-trip의 역방향, 메모리 기존).
**해결**: `ho:hasComponent owl:propertyChainAxiom ( ho:hasComponent ho:implementationCandidate )`.
harness hasComponent tool ∧ tool implementationCandidate cand ⟹ harness hasComponent cand.
후보가 **harness**(정상 Harness)의 component로 roll-up → orphan-free, tool 무오염, **새 shape 불요**.
owlrl가 propertyChainAxiom(prp-spo2) 지원 확인. probe로 tool NOT Harness·SHACL conforms 검증.
ontology_lib: INSTANCE_CLASSES+=Candidate, INSTANCE_LINK_PREDICATES+=implementationCandidate.

## materialize.py (BIND resolution + lock)
- resolution/tool: lock pin > candidates+policy > 직접 ref > stub.
- `_bound_impl_tools`는 **RDF.type Tool로 제한**: 후보가 chain으로 hasComponent-reachable하고
  implementationRef 지녀서 `_iter_components`(hasComponent 포함)로 후보가 tool로 오검출됨. type Tool 필터.
- policy 결정적: `pinned:<tag>`(그 tag만, 없으면 hard error), `latest-stable`(stable 우선, 최고 ver),
  `conservative`(stable 우선, 최저 ver). tie=ver key then IRI. tool-level policy > harness-level > 기본.
  `_version_key`: `.`/`-`/`+`/`_` split, 숫자 세그먼트는 int·비숫자보다 상위(1.10>1.9).
- **harness.lock.json**(매 빌드 작성): lockVersion, spec{harness IRI, prefLabel, individualCount},
  tools{iri→{selected(cand IRI|null), ref, version, tag, policyApplied, contentHash=sha256}}.
  무타임스탬프·sort_keys → 그 자체 byte-identical.
- `--lock`: strict 재현. spec identity(harness+individualCount)·후보 존재·ref·contentHash 전부
  대조, mismatch=hard FAIL(exit1, 아무것도 안 씀). lock이 validate 게이트 완화 못함(gate 여전히 실행).
  **policyApplied는 lock서 원본값 유지**(lock으로 relabel 금지)→A와 B(--lock A) diff -r IDENTICAL.
- 후보-backed tool은 **안정 파일명**: tool stem(strip `tool-`)+선택ref 확장자(tool-docgraph→
  docgraph.py). candidate 바꿔도 파일명 불변(callers 안 깨짐=행위 동등성). 직접-ref tool은 ref basename 유지(증분 호환).

## 데모/게이트(lpranging)
tool-docgraph=2 candidates(cand-docgraph-stable=impl/docgraph.py tag stable v1.4.0,
cand-docgraph-next=impl/docgraph_v2.py tag next v2.0.0), policy latest-stable. tool-simulator=직접 ref.
compose union 83(=81+2). docgraph_v2.py=진짜 별개 compact rewrite 신규작성(선택 관찰가능).
- A(no lock)=stable(docgraph.py). B(--lock A) diff -r A B IDENTICAL(INV-2). A vs A2 identical(결정성).
- INV-4: policy→pinned:next면 tools/docgraph.py=v2 내용, compose validate+emit 여전히 PASS(교체 무해).
  테스트후 policy latest-stable 복원(pushed recipe 기본값).
- lock tamper(contentHash/individualCount)→refuse exit1.
- 데모 compose는 staging catalog + `central`심링크(→repo root), **실행후 rm**(payload symlink-free).
- ODR 성숙도 level 2(재현 via lock) 도달. level 3/4(계약-VERIFY)는 미해결(validate는 그래프 정합만).

## 완결 ODR 예시 = 레시피가 LOCK도 vendor (SPEC+BIND+LOCK 동봉)
- 재현성 커밋(ODR §4-③): emit된 `harness.lock.json`을 레시피에 **`recipes/<name>/harness.lock.json`**
  으로 복사해 둔다. 레시피가 SPEC(ttl)+BIND(impl/candidates)+pinned LOCK을 함께 ship → 완결 ODR 예시.
  증명: `--lock recipes/<name>/harness.lock.json`로 재빌드가 no-lock 빌드와 `diff -r` byte-identical(INV-2),
  vendored lock의 contentHash가 vendored `impl/` 파일 sha256과 일치. staging/은 gitignore(빌드산출물은
  scratchpad에만·커밋 안 함)지만 **vendored lock은 레시피 파일이라 유지**(gitignore /staging/ 무관—커밋 주체는 inspection).
- consolidation/build-confirm dispatch 패턴: 중앙 무수정(ontology/·tools/ 손대지 않음), 임시 `central`
  심링크(→repo root)로 compose validate+materialize 후 rm. git상 ontology/tbox·tools/materialize·ontology_lib이
  `M`으로 보여도 그건 선행 ODR 작업의 미커밋분(mtime이 세션전)—내 세션이 만든 게 아님을 mtime+무write로 확인.
