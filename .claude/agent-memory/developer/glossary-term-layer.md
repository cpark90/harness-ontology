# 용어(glossary) 레이어 저작 — Concept를 정의된 term으로

거버넌스 원칙(least-privilege, verify-then-proceed 등)이 guardrail `promptText` 안에만
녹아 있고 독립 term이 아니던 갭을 메운 작업. `ho:Term` 새 클래스 발명 금지 — `skos:Concept`가
곧 term(prefLabel+definition)이다(그게 SKOS의 본래 용도, 새 클래스면 drift).

## 핵심 사실 (검증기 기계 동작 — 재확인 불요)
- `tools/ontology_lib.py` `INSTANCE_LINK_PREDICATES`: `ho:tagged, skos:broader, skos:narrower,
  skos:related`는 reachability edge. **`skos:topConceptOf`는 edge 아님** + `skos:ConceptScheme`
  (id:scheme)는 INSTANCE_CLASSES 아님 → topConceptOf만으론 Concept가 reachable하지 않다.
  top concept가 살아있는 건 누군가 `ho:tagged`하거나 자식이 `skos:broader`로 가리키기 때문.
- SHACL `ho:ConceptConnectivityShape`(harness-shapes.ttl): Concept는 prefLabel 필수 +
  {inverse ho:tagged | skos:broader | inverse skos:broader | skos:related} 중 1개 이상.
  **topConceptOf는 이 shape도 만족 못 시킴** — 추상 top concept는 자식의 broader(inverse)로 산다.
- 중복 label 검사(`check_duplicates`)는 **(class, casefold prefLabel)** 단위 + **advisory(빌드
  실패 아님)**. 그래서 Guardrail "Verify then proceed"와 Concept "Verify then proceed"가 같은
  문자열이어도 클래스가 달라 충돌 아님(term=원칙, guardrail=정책, 라벨 겹쳐도 OK).

## 관용 패턴 (이번에 확립)
- 원칙 term 1개 = guardrail 1개(1:1). guardrail을 generic top(c-safety 등)에서 특정 term으로
  `ho:tagged` 재지정. promptText/다른 트리플은 안 건드림(Edit anchor를 promptText **tail**로 —
  `ho:tagged id:c-safety ; ho:tokenEstimate NN`는 tokenEstimate 값이 겹쳐 unique 아님, 앞
  promptText 문장으로 앵커).
- 계층: cross-cutting 운영 규율(verify-proceed/design-for-loss/least-privilege/escalation/
  bounded-context)은 새 top `c-agent-methodology`(topConceptOf + 자식 broader로 연결) 밑에,
  도메인 특정 원칙은 기존 top 밑(root-cause/simplicity→c-design, grounding/structural-coverage→
  c-traceability, report-over-prompt/controlled-vocabulary→c-communication, dispatch/delegation→
  c-multiagent). generic top에 남길 guardrail은 그게 정말 그 원칙일 때만(gr-nodestruct/gr-cite→
  c-safety, gr-lang→c-communication). generic top은 남은 tag 1개+자식 broader로 계속 연결됨.
- definition은 §1d대로 "왜/언제 고르나"(원칙 서술), 영어 한 문장. altLabel로 검색성 보강
  (YAGNI, anti-drift, anti-context-rot 등 — 클래스 내 유일하면 됨).
- 게이트: 새 term 수만큼 individual 증가(77→91), SHACL/reachability/dup 그린, retrieve로 term
  표면화 확인. `/usr/bin/python3`.
