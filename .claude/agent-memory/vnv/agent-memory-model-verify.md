# agent memory 3-tier schema 확장 검증 재현 절차

`ho:Memory ⊑ ho:HarnessComponent` + `ho:hasMemory ⊑ ho:hasComponent`(direct subProp, subject=Harness)
+ 4 discriminator datatype props(memoryReadTiming/-Persistence/-ReadScope/-ActivationCondition)
+ `ho:MemoryShape` + ABox(c-memory, mem-firmware/-cache/-longterm, h-multiagent hasMemory×3).
판정: docs/verify/agent-memory-model.md. → **PASS + 2 non-blocking REC**.

## 핵심 검증 포인트 (재사용)
- **component 패턴 정합 = hasRole/hasChannel 관례**: subject가 Harness면 direct subPropertyOf
  hasComponent(propertyChain 아님)이 옳다. 그러면 bespoke shape 없이 `ComponentConnectivityShape`
  (targetClass HarnessComponent)가 그대로 적용돼 orphan-free·reachable. reachability "all N
  reachable"에 mem이 포함됨이 곧 subPropertyOf OWL RL 전파의 실증(별도 쿼리 불필요).
- **shape sh:in ↔ 개체값 오타 대조**: closed set 값집합은 각 개체의 리터럴과 문자 그대로 대조
  (every-execution/task-continuous/conditional, durable/ephemeral). SHACL PASS면 이미 걸러지지만
  값집합-소스 의미 매핑은 눈으로 확인.
- **individual 수 산술로 recipe 전파 실증**: 중앙 +4(mem3+concept1). recipe closure 개체수가
  이전+4면(예 21: 141→145, 46: 146→150) core roles.ttl 경유 additive 전파가 union에 상속되되
  검증 안 깨짐이 증명됨. 카탈로그 변경 없는 additive(신규 core unit 금지) 배치 규율의 확증 신호.

## ★materialize "prose 미추가/byte-identical" 함정 (중요)
- **HEAD 원시 diff로 byte-identity 주장 금지**: working-tree엔 검증 대상과 무관한 다수
  uncommitted 변경이 섞여 있을 수 있어(git status로 확인) CLAUDE.md가 당연히 byte-differ함.
  → memory 델타 격리는 **구조적**으로: ① `grep -c "hasMemory\|HO.Memory" tools/materialize.py`=0
  (렌더러 분기 부재) ② 산출 CLAUDE.md에 대상 노드 참조 0 ③ HEAD-vs-working MANIFEST symdiff가
  정확히 대상 노드 엔트리뿐. 이 3개로 "prose 0바이트 변경" 확증. (clone에서 델타만 strip해
  재materialize하는 방법은 orphan 유발로 materialize REFUSE되기 쉬워 fragile — 구조적 증명이 낫다.)
- **INSTANCE_CLASSES whitelist(`tools/ontology_lib.py:65`)**: `most_specific_types`는 이 집합으로
  필터 → 신규 타입(HO.Memory)이 미등록이면 MANIFEST가 concrete subtype 대신 추론 상위
  `HarnessComponent`로 fallback(raise 아님, exit 0). 신규 component class 추가 시 MANIFEST 정밀
  typing 원하면 이 집합에 등록 필요 = tools 변경(developer ABox 범위 밖) → REC로 flag.

## coverage audit (source→representation)
3 소스 요소(firmware/cache/long-term)가 각 단일 mem 개체+구분속성으로 1:1, 표현 밖 요소 0.
"반영/consulted and reflected"는 activationCondition 텍스트로 담김. GAP 0.
