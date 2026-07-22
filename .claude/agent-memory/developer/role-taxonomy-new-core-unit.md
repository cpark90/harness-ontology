# Role taxonomy as `ho:Role` individuals + adding a NEW core unit

멀티에이전트 역할 분류를 중앙 중립 온톨로지에 `ho:Role` 개체로 반영한 작업 노트.
새 core data unit(`ontology/abox/core/roles.ttl`)을 추가하고 boolean 분류 프로퍼티를 다는 패턴.

## userFacing 분류 프로퍼티 (TBox 확장)
- `ho:userFacing` = `owl:DatatypeProperty`, `rdfs:domain ho:Role`, `rdfs:range xsd:boolean`.
  기존 datatype prop 스타일(roleMemoryPolicy 옆) 모방: label + skos:definition 1줄. 새 prop이지만
  role 개체들이 실제로 쓰므로 anti-orphan/anti-drift OK. shapes는 이 prop을 거부하지 않음
  (HarnessShape·ComponentConnectivityShape는 prefLabel/inverse-hasComponent만 요구, closed 아님).
- boolean 리터럴은 `true`/`false`(따옴표 없이) — turtle 네이티브. `"true"^^xsd:boolean` 불필요.

## 새 core unit 배선 (split 노트의 restructure와 달리 진짜 신규 유닛 추가)
1. `ontology/abox/core/roles.ttl`: 자기 `owl:Ontology` 헤더 문서IRI `.../data/core/roles`, schema만 import.
2. `catalog-v001.xml`(repo root, ontology/ 아님!)에 `<uri id="core-roles" name=".../data/core/roles"
   uri="ontology/abox/core/roles.ttl"/>` 추가.
3. root `ontology/harness-ontology.ttl` owl:imports 목록에 `.../data/core/roles` 추가.
- **두 로더 경로 반드시 동시 갱신**: imports+catalog 경로는 2·3 둘 다 있어야 resolve. glob 경로
  (`abox/**/*.ttl`)는 파일만 있으면 자동. 둘 다 갱신하면 parity(개체집합·triple수 동일) 성립.
  검증: `HARNESS_CATALOG=/nonexistent`로 glob 강제 vs 기본 catalog → `load_graph(reason=False)`
  두 그래프의 typed-individual set·len(g)이 identical해야 함.

## Role 개체 (분류 전용, lean)
- `ho:Role` ⊑ HarnessComponent. `ho:hasRole` ⊑ hasComponent → h-multiagent에 `ho:hasRole`로
  묶으면 reachable(orphan 아님)·ComponentShape 자동 충족. rolePersona/roleTool/roleMemoryPolicy는
  **optional** — 순수 분류 태스크면 붙이지 않는다(YAGNI; persona 없어도 shape 통과, SystemPrompt만
  promptText 필수라 Role엔 무관).
- 각 role: prefLabel(클래스내 유일)·definition 1줄·`ho:userFacing` bool·`ho:tagged core:c-multiagent`
  (+도메인 맞으면 c-design)·`ho:maturity`. 태그로 retrieve 노출.
- 7 roles: orchestrator/inspection = userFacing true(사용자와 소통); developer/research/
  inspection-worker/vnv/design = false(dispatch 전용 worker). inspection(user-facing)과
  inspection-worker는 **별개 role**.

## 게이트
validate 73 individuals PASS(id:scheme는 count 제외라 id/ subject는 74). retrieve "design agent"·
"user-facing ... roles" 로 role-* 노출.
