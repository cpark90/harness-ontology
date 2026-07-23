# Agent memory 3-tier model (firmware/cache/long-term) — schema + ABox

3종 에이전트 memory를 온톨로지에 additive로 반영한 저작. 소스 3요소 → 표현:
firmware=always-read durable baseline, cache=task-scoped ephemeral working store,
long-term=trigger-gated durable selective store.

## 모델링 (mirror hasChannel/hasRole 패턴)
- `ho:Memory ⊑ ho:HarnessComponent`, `ho:hasMemory ⊑ ho:hasComponent`
  (domain Harness, range Memory). subject IS the Harness → **직접 subPropertyOf
  hasComponent**(hasRole/hasChannel/hasAssemblySection 꼴), propertyChain 아님
  (chain은 intermediate subject일 때만 — WorkflowStep/Candidate/Contract). ⇒
  기존 `ComponentConnectivityShape`(targetClass HarnessComponent)가 그대로 적용,
  bespoke reachability shape 불요.
- reachability anchor = `id:h-multiagent`에 `ho:hasMemory mem-firmware,mem-cache,
  mem-longterm` 1줄 → 파생 harness(h-peer-mesh/workspace-synthesis/전 recipe) 상속.
- 구분 datatype props (domain Memory, range xsd:string, closed set은 definition+SHACL sh:in):
  `memoryReadTiming`(every-execution/task-continuous/conditional),
  `memoryPersistence`(durable/ephemeral), `memoryReadScope`(full/selective),
  `memoryActivationCondition`(long-term만, optional). AssemblySection의
  assemblyOrder/sectionKind 판박이.

## 파일 배치 (신규 core unit 금지 — blast-radius 회피)
새 unit(memory.ttl)은 root owl:imports+중앙 catalog+**모든 recipe catalog** 동기화
요구. 대신 **기존 unit에 additive** → 스키마·기존 ABox 경유로 recipe union에 카탈로그
변경 0으로 전파: TBox=`tbox/harness.ttl`, shape=`shapes/harness-shapes.ttl`(MemoryShape:
prefLabel/definition/readTiming/persistence/maturity min1 + readTiming/persistence sh:in),
Memory 개체 3개=`abox/core/roles.ttl`(roleMemoryPolicy와 co-locate=agent-state 인접;
roleMemoryPolicy 단일 free-text가 3-tier 못 담는 게 GAP 근거), concept c-memory=
`concepts.ttl`(topConceptOf scheme + related c-autonomy; inverse-tagged로 non-orphan),
hasMemory 부착=`harnesses.ttl` h-multiagent(hasChannel 다음, hasAssemblySection 앞).

## 검증
- 중앙 validate PASS, 130 individuals(+4). recipe 21-code-reviewer closure PASS
  145(=141+4, mem 상속 확인). ★mem 3개가 recipe union에도 나타나되 안 깨짐.
- ★materialize 무크래시(out of scope지만 regression guard): `_concrete_type`가
  INSTANCE_CLASSES 없는 클래스는 "HarnessComponent"로 **safe fallback**(raise 아님).
  mem 3개=MANIFEST components에 type="HarnessComponent"로 기록, CLAUDE.md엔 memory
  섹션 0(prose byte-identical). **FLAG(후속)**: 정밀 표현하려면 `ontology_lib.INSTANCE_CLASSES`에
  `HO.Memory` 등록 + materialize에 memory 섹션 renderer + AssemblySection sectionKind에
  "memory" enum 추가(shape sh:in + emitter SECTION_RENDERERS). 이번엔 온톨로지 표현이 핵심이라 미실행.
