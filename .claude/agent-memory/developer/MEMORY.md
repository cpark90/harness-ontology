# developer 역할 메모리

온톨로지 노드 저작 에이전트의 역할 특화 메모리 인덱스. 역할 정의는
`.claude/agents/developer.md`. 노드 종류별 함정·모델링 패턴·capability 배선을 파일로 추가하고
아래에 한 줄로 인덱스한다.

- 완결 brief로 받은 배정분만 구현: 온톨로지 노드(`ontology/abox/`) 또는 배정 소스(`tools/**` 등).
  TBox·shapes·brief 밖 경로는 안 만짐. 검증(vnv)·커밋(inspection)은 안 함. 온톨로지 노드 스타일은
  `ONTOLOGYSTYLE.md` [지킴], 소스는 기존 컨벤션·언어 표준.
- 도구는 `rdflib` 등이 있는 인터프리터로(예: `/usr/bin/python3`). 셸 기본 python3엔 없을 수 있음.

<!-- 학습 인덱스 (한 줄씩) -->
- [neutral-parts-decomposition](neutral-parts-decomposition.md) — 온톨로지 = domain-INDEPENDENT
  재사용 PART 라이브러리(특정 harness 서술 아님): governance doc→중립 Guardrail/Pattern/Workflow/
  SystemPrompt로 분해, gr-lang 재사용·도메인 명사 제거·domain tool dependsOn strip. anti-orphan
  때문에 파트를 중립 harness(h-multiagent) 하나에 배선 필수. seed.ttl(core)에 append(plumbing 불요).
  도메인 split 은퇴: catalog/root infra 유지·엔트리만 drop·NOTE는 retired로·staging 삭제·grep은 노드만(주석 허용).
- [model-external-harness](model-external-harness.md) — 외부 멀티에이전트/설계 하네스를 abox로
  모델링: role split→Workflow+pat-orchestrator-workers, tool→Tool+cap, CLAUDE 규칙→Guardrail,
  gr-lang 재사용, 캡 requires↔provides 짝, 개념 reachability(ho:tagged 필수·topConceptOf 부족).
- [webui-svelte-frontend](webui-svelte-frontend.md) — tools/webui 프론트 Svelte+Vite 재작성:
  vite outDir=../static·emptyOutDir, compose ./tools 마운트 제거(shadowing), Dockerfile 멀티스테이지,
  Svelte5 mount/a11y, /api/* 응답 형태·retrieve id는 full URI.
- [federation-owl-imports-catalog](federation-owl-imports-catalog.md) — GitHub 연합(D1–D4):
  glob→owl:imports+catalog 로더(glob fallback 유지·shapes skip·env override로 data repo CI),
  IRI `.../id/<domain>/<slug>` 마이그(prefix 바인딩만·cross-domain은 core: prefix·union에서 병합),
  webui flat id/ 베이스 core화, Write 툴 stray `</content>` 제거 gotcha.
