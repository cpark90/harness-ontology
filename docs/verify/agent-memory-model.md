# Verify — agent memory 3-tier schema 확장

- **판정자**: vnv (independent re-run; developer self-check 미신뢰)
- **일자**: 2026-07-23
- **스펙**: `docs/plans/dispatch-agent-memory-model.md`
- **대상 델타**: TBox(`ontology/tbox/harness.ttl`) `ho:Memory`+`ho:hasMemory`+4 datatype props;
  shape(`ontology/shapes/harness-shapes.ttl`) `ho:MemoryShape`; ABox `id:c-memory`(concepts.ttl),
  `id:mem-firmware/-cache/-longterm`(roles.ttl), `id:h-multiagent ho:hasMemory ×3`(harnesses.ttl).

## VERDICT: PASS (with 2 non-blocking recommendations)

전 항목 독립 재실행으로 green. 소스 3요소가 각각 한 표현으로 완전 매핑됨. 발견된 2건은
tools 계층(developer의 ABox 범위 밖)·후속 렌더링으로, 이번 스키마 확장의 결함이 아님.

---

## (1) 중앙 validate — PASS

실행: `/usr/bin/python3 tools/validate.py`
- `PASS`, 4 체크 전부 green: **SHACL / reachability / capabilities / assemblyOrder**.
- **individual 수 = 130** (주장과 일치; 이전 126 → +4 = mem×3 + concept×1).
- reachability: **all 130 individuals reachable from a Harness** (orphan island 0). mem 3개는
  `ho:hasMemory ⊑ ho:hasComponent`(OWL RL 추론) 경유로 `id:h-multiagent`에서 도달 →
  reachable 집합에 포함됨이 곧 subPropertyOf 전파의 실증.
- SHACL conforms → `ho:ComponentConnectivityShape`(targetClass `ho:HarnessComponent`, mem은
  추론상 그 하위) + 신설 `ho:MemoryShape` 모두 통과, under-specified 노드 없음.

## (2) TBox 패턴 정합 — PASS

- `ho:Memory rdfs:subClassOf ho:HarnessComponent` (harness.ttl:82-85) — `ho:Channel`/`ho:Role`와
  동일 계층 관례. `ho:hasMemory rdfs:subPropertyOf ho:hasComponent` (harness.ttl:223-228),
  `rdfs:domain ho:Harness` / `rdfs:range ho:Memory` — 주어가 Harness인 직접 sub-property로
  `ho:hasRole`/`ho:hasChannel`와 정확히 일치(propertyChain 아님, 올바름).
- discriminator datatype props(harness.ttl:467-489) domain `ho:Memory`·range `xsd:string` 정합.
- **shape `sh:in` ↔ 개체 값 대조 (오타 위반 0)**:
  - `ho:memoryReadTiming sh:in ("every-execution" "task-continuous" "conditional")` ↔
    개체값 `every-execution`(firmware)/`task-continuous`(cache)/`conditional`(longterm) — 정확 일치.
  - `ho:memoryPersistence sh:in ("durable" "ephemeral")` ↔ `durable`/`ephemeral`/`durable` — 일치.
  - min/max 1 강제, `skos:prefLabel`·`skos:definition`·`ho:maturity` min1 — 3개체 모두 충족
    (maturity `draft`, tokenEstimate 55/55/80, tagged `id:c-memory`+`id:c-multiagent`).
- concept `id:c-memory`: `skos:topConceptOf id:scheme` + `skos:related id:c-autonomy` → 연결됨,
  orphan 아님. (developer는 broader 대신 topConcept+related 선택 — orphan-free이므로 수용가능.)

## (3) recipe 무영향 (blast-radius, roadmap §5 D4) — PASS (2 recipe)

per-recipe closure(union 아님) 재검증, central 심링크 = working-tree:
- **21-code-reviewer** (`catalog-v001.xml`, root `.../21-code-reviewer`): **PASS**, 4체크 green,
  **145 individuals** (= 중앙 130 + 로컬 15; 이전 141 = 126+15 → +4 확인).
- **46-product-manager** (`catalog-46-product-manager.xml`): **PASS**, 4체크 green,
  **150 individuals** (+4 대비 이전 146).
- 두 recipe 모두 "1 harness assembly order" 확증. **mem 3개가 recipe union에 core roles.ttl
  경유로 상속되어 나타나되(개체수 +4로 실증) 검증을 깨지 않음** — 카탈로그 변경 없는 additive
  전파(스펙 §1 배치 규율)가 의도대로 동작.

## (4) materialize 무크래시 (regression guard) — PASS + FLAG 실증

- `/usr/bin/python3 tools/materialize.py h-multiagent --out <tmp>` → **exit 0**, 정상 산출
  (CLAUDE.md + MANIFEST + 7 role .md + 3 channel + lock).
- **developer FLAG 실증**: `INSTANCE_CLASSES`(`tools/ontology_lib.py:65-71`)에 `HO.Memory` **미등록** →
  `most_specific_types`가 whitelist 필터로 추론 상위 `HarnessComponent`로 fallback →
  MANIFEST에서 mem 3개가 `"type": "HarnessComponent"`로 기록(Role/Channel/Tool처럼 concrete
  subtype 아님). **raise 아닌 graceful fallback**임을 확인(exit 0).
- **memory가 CLAUDE.md prose에 미추가**임을 **구조적으로 증명**:
  - `tools/materialize.py`에 `hasMemory`/`HO.Memory` 참조 **0건** → CLAUDE.md 렌더러에 memory
    분기 없음(`grep -c` = 0). 유일한 "Memory" 언급은 `ho:roleMemoryPolicy`(line 561, role .md로
    렌더되는 기존 속성, `ho:Memory` 클래스와 무관).
  - 산출 CLAUDE.md에 memory 노드(mem-firmware/cache/longterm) 참조 **0건**(grep).
  - HEAD vs working-tree MANIFEST symdiff에서 memory 관련 델타는 **정확히 mem×3 HarnessComponent
    엔트리뿐** — 즉 memory 변경은 MANIFEST에만 3줄 추가, prose에는 영향 0.
  - **주의(방법론)**: 원 브리프의 "CLAUDE.md byte-identical" 대조를 HEAD로 직접 하면
    현재 working-tree에 **memory와 무관한 다수 uncommitted 변경**(workflow-step 분해, persona
    다행화, role prose 확장, h-multiagent definition 편집)이 섞여 CLAUDE.md가 byte-differ함.
    따라서 byte-identity는 **HEAD 원시 diff가 아니라 위 구조적 격리**(렌더러 분기 부재 + MANIFEST
    단독 델타)로 확증했다. memory 변경 자체는 CLAUDE.md prose를 **0바이트** 바꾼다.
- 임시 out dir·HEAD worktree·클론 모두 정리 완료(`git worktree list` = main 단독).

## (5) coverage audit (source → representation) — PASS (누락 0)

| 소스 요소(사용자) | 표현(개체 + 구분 속성) | 의미 대응 |
|---|---|---|
| ① firmware: 매 실행/spawn 전량 필수 확인 | `id:mem-firmware`: readTiming `every-execution` + readScope `full` + persistence `durable` | "매 실행"=every-execution, "전량"=full, definition "MUST read in full on every execution/spawn" — 완전 |
| ② cache: task 내부 소멸까지 누적 | `id:mem-cache`: readTiming `task-continuous` + persistence `ephemeral` + readScope `full` | "task 내부 누적"=task-continuous, "소멸"=ephemeral(discarded when task ends) — 완전 |
| ③ long-term: 조건 달성 시 해당부분 확인·반영 | `id:mem-longterm`: readTiming `conditional` + readScope `selective` + persistence `durable` + `memoryActivationCondition` | "조건 달성"=conditional+activationCondition, "해당부분"=selective, "안 읽지만 유지"=durable, "반영"=activationCondition 텍스트 "consulted and reflected" — 완전 |

- 3 소스 요소 → 각각 **단일 표현**으로 1:1 매핑, 표현 밖으로 둔 요소 **없음**.
- read-timing / persistence / 조건-반영 3축 의미 **누락 0**. `GAP 없음`.

---

## GAP / 권고 (전부 non-blocking, 이번 스키마 델타의 결함 아님)

- **REC-1 (materialize 정밀 typing, low)**: `tools/ontology_lib.py` `INSTANCE_CLASSES`에
  `HO.Memory` 추가 시 MANIFEST가 concrete `"Memory"` subtype 기록(Role/Channel/Tool과 parity).
  현재는 `HarnessComponent` fallback(무해). developer ABox 범위 밖(tools 변경) → orchestrator가
  후속 dispatch로 판단. **비차단**.
- **REC-2 (memory 렌더링 후속, low)**: memory 아키텍처가 emitted harness(CLAUDE.md 또는 role .md)
  에 노출되려면 assembly-section/renderer 확장 필요. 스펙 §6이 이번 범위 밖으로 명시했고 온톨로지
  표현이 요청 핵심이므로 **의도된 경계**. 향후 "agent가 자기 memory 티어를 인지"해야 하면 별도
  후속으로 트리거. **비차단**.

## 재현 명령 (실행한 그대로)

```
/usr/bin/python3 tools/validate.py
cd staging/harness-recipes
HARNESS_CATALOG=catalog-v001.xml            HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/21-code-reviewer   /usr/bin/python3 central/tools/validate.py
HARNESS_CATALOG=catalog-46-product-manager.xml HARNESS_ROOT_ONTOLOGY=https://harness-ontology.dev/recipes/46-product-manager /usr/bin/python3 central/tools/validate.py
/usr/bin/python3 tools/materialize.py h-multiagent --out <tmp>   # exit 0; MANIFEST mem×3=HarnessComponent; CLAUDE.md prose 0 memory refs
grep -c "hasMemory\|HO.Memory" tools/materialize.py               # 0 (렌더러 분기 부재)
```
