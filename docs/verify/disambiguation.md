# VERIFY — disambiguation audit (DA-1 관측 3분할 + DA-2 정의 명확화)

> 판정: **vnv** (2026-07-23). 대상 설계 `docs/plans/disambiguation-audit.md` §A(3분할)·§B~F(정의정리).
> 판정 전용 — ontology/tools 무편집. 도구 인터프리터 `/usr/bin/python3`(rdflib/pyshacl/owlrl).

## VERDICT: **PASS** (+ 3 non-blocking note)

독립 재실행으로 5개 축 전부 확증. GAP 없음.

---

## (1) validate + 잔재 0 — PASS

재현:
```
/usr/bin/python3 tools/validate.py
grep -rn ObservationArea ontology/ tools/ ONTOLOGYSTYLE.md
```
- `PASS`. **all 185 individuals reachable**(주장 185 일치), 4체크(SHACL/reachability/capabilities/assemblyOrder) 전부 ✓, duplicate label 0.
- `ObservationArea` grep = **0 매치**(ontology·tools·ONTOLOGYSTYLE 잔재 없음).
- 신규 3클래스 인스턴스(os- 5, aoi- 5, oa- 10)가 전부 reachable — validate가 orphan island 0을 보장(propertyChain 6/7/8 rollup). ObservationSpace/AreaOfInterest/AreaOfObservation orphan **0**.

## (2) DA-1 구조 정합 — PASS

TBox(`ontology/tbox/harness.ttl`):
- **3 클래스 ⊑ HarnessComponent**: `ho:ObservationSpace`(132), `ho:AreaOfInterest`(137), `ho:AreaOfObservation`(142) 모두 `rdfs:subClassOf ho:HarnessComponent` — subsumption으로 계수·reachable(INSTANCE_CLASSES 등록 불요, 비대칭 규율 준수).
- **agentObservation → ObservationSpace**: `rdfs:range ho:ObservationSpace`(336), NOT ⊑hasComponent(Agent를 Harness로 mistype 방지, 정의에 명시).
- **hasAreaOfInterest / hasAreaOfObservation = 중간노드 술어**: domain=ObservationSpace, range=각 area(340-350), **NOT ⊑hasComponent**(ObservationSpace를 Harness로 mistype 방지).
- **coversInterest AoO→AoI**: domain=AreaOfObservation, range=AreaOfInterest(352-356), NOT ⊑hasComponent(양 끝 Harness 아님) — reachability는 hasAreaOf*가 담당, coversInterest는 alignment만 추가.
- **propertyChain 6/7/8**(198-200): `(hasComponent agentObservation)` / `(… hasAreaOfInterest)` / `(… hasAreaOfObservation)`. 7/8은 **Deliverable 5번째 3-link 선례(`hasComponent hasStep stepProduces`)와 동형** — 각 chain이 hasComponent 접두로 시작해 inferred subject가 항상 Harness(중간노드 아님). TBox 정의문이 명시적으로 "mirroring the fifth chain".
- **shape 3 신규 + AgentShape**(`ontology/shapes/harness-shapes.ttl`): `ObservationSpaceShape`(prefLabel/projectsFrom≥1/hasAreaOfObservation≥1/maturity), `AreaOfInterestShape`(prefLabel/observationKind sh:in{internal,external} 1..1/maturity), `AreaOfObservationShape`(+tokenEstimate≥1), `AgentShape`(agentObservation≥1/cognitiveCapacity≥1). SHACL conforms → sh:in·min ↔ 개체값 **오타 0**.

ABox(`ontology/abox/core/roles.ttl`): 5 agent 각각 `Agent → agentObservation → os-<agent>(1) → {hasAreaOfInterest aoi-<agent>(1), hasAreaOfObservation oa-<agent>-{external,internal}(2)}`; os-가 `projectsFrom global-state`, cognitiveCapacity 150000. 외부 oa-가 `coversInterest` 해당 aoi-.
- **capacity fit Σ(oa tokenEstimate) ≤ 150000**(눈 합산): orchestrator 9000+2000=11000, developer 6000+1500=7500, vnv 5000+1500=6500, inspection 12000+1500=13500, synthesizer 8000+1500=9500 — **전부 여유 통과**.
- 계수: os- 5 + aoi- 5 + oa- 10 = 20 신규(agent 5는 기존). oa- 10 retype·agent 재배선(agentObservation→os-) 완료.

## (3) DA-2 정의 정합(B~F 비중복·비자기지칭) — PASS

각 쌍이 이제 **genus 자기지칭 제거 + 상호 구별절 존재 + 예시 비중복**:
- **B Workflow(60) vs DesignPattern(169)**: Workflow="concrete control flow … decomposed into ordered steps(hasStep)", 예시 single-pass/sense-act-observe/plan-dispatch-integrate/branch-merge. DesignPattern="abstract named pattern(appliesPattern tag, never instantiated into steps)", 예시 orchestrator-workers/peer-mesh/pipeline/fan-out-fan-in/reflection. **과거 겹치던 ReAct/plan-execute 예시 제거** → 경계 명확. 상호 "Distinguished from" 절 양방향.
- **C Guardrail(52) vs Constraint(173)**: Guardrail="behavioural policy an agent must follow(imperative)" — 정의문에서 **"constraint" 단어 genus 제거**(구별절에서만 등장). Constraint="declarative NFR". 양방향 구별.
- **D SystemPrompt(37) vs Instruction(42)**: SystemPrompt="standing persona framing, loaded on every inference" — **"instruction" genus 제거**. Instruction="on-demand named procedure/skill/slash-command, triggered". 양방향 구별.
- **E Tool(47) vs Capability(149)**: Tool="concrete invokable operation that PROVIDES capabilities(providesCapability)" — genus를 "operation"으로, "capability"는 구별절만. Capability="abstract ability". 양방향.
- **F Role(72) vs Agent(127)**: Role="mandate + policy π_i"(mandate로 좁힘, "관측/기능은 Agent가 부여" 명시). Agent="partially-observed distributed node(Role+ObservationSpace+functions), Role stays first-class". 양방향 구별절.

잔재 cleanup: `domains-tasks.ttl` 투영사슬 서술 `ObservationArea→ObservationSpace` 치환 완료; `ONTOLOGYSTYLE.md` 명명표에 os-/aoi-/oa- 3행 추가.

**DA-2 flag 판정(ho:notation 미존재 → integrationMode/triggerPhrase)**: `ho:notation` grep=0(미존재 확인). Instruction 정의가 참조하는 `ho:triggerPhrase`(759)·`ho:integrationMode`(734)는 datatype property로 **실재** — on-demand skill의 trigger/wiring을 이 둘로 표현하는 것이 정의 정합상 **문제없음**(notation 불요). 남은 conflation **없음**.

## (4) materialize byte-identity — PASS

재현: `grep -c <관측술어> tools/materialize.py` + h-multiagent build(임시 dir, git-free).
- materialize.py 관측술어(ObservationSpace/AreaOf*/agentObservation/coversInterest/projectsFrom/observationKind/hasAreaOf) 참조 = **0**(렌더러 분기 부재).
- `materialize.py h-multiagent --out <tmp>` → **exit 0**(78 components, 7 roles, 3 channels, lock 기록).
- 산출 트리 관측노드 참조 grep = **none**(CLAUDE.md 관측 모델 미emit).
- **class-level definition 미emit 확증**: DA-2로 바뀐 class skos:definition 특유 문구("imperative rule that disciplines"/"always-on persona framing"/"classification tag"/"concrete means") CLAUDE.md 매치 = **0** — materialize는 individual 텍스트만 emit, class 정의는 참조 안 함. → 관측 술어·class 정의 emitter 둘 다 미참조이므로 CLAUDE.md prose **byte 불변**(구조적 격리 증명; working-tree 무관 uncommitted 다수라 원시 HEAD diff 대신 이 방식).

## (5) recipe 무영향 — PASS

재현(central 심링크 기존 존재, per-recipe 전용 카탈로그·ROOT_ONTOLOGY):
- **21-code-reviewer**(catalog-v001.xml, ROOT_ONTOLOGY=…/21-code-reviewer): `validate.py` **PASS**, **200 reachable**(중앙 185 + 로컬 15), "1 harness assembly order"=per-recipe closure 확증(union 아님).
- **46-product-manager**(catalog-46-product-manager.xml, ROOT_ONTOLOGY=…/46-product-manager): **PASS**, **205 reachable**(185+20). 카탈로그 함정 회피(전용 catalog 사용).
- 관측 모델은 중앙·additive이므로 recipe가 상속·검증 통과 — 무영향 확인.

---

## Non-blocking notes (권고, 결함 아님)

- **N1 (내부 AoO에 대응 AoI 부재)**: 각 agent는 aoi-(external kind) 1개만 두고, oa-external이 이를 cover. oa-internal은 대응 internal AoI 없이 존재. 정의상 acceptable(AoI 무피복=unmet need 정의이지 AoO 무피복 제약은 없음; 모든 aoi는 피복됨). 향후 introspection을 정보요구로 모델링하려면 internal AoI 추가 여지 — 현재 결함 아님.
- **N2 (ONTOLOGYSTYLE 예시 오탈)**: 명명표 AreaOfInterest 예시가 `id:aoi-orchestrator-external`이나 실제 ABox는 `id:aoi-orchestrator`(suffix 없음, external 단일). 도구·검증엔 무영향인 문서 예시 불일치 — 스타일 doc 소폭 정정 권고(inspection/developer 범위).
- **N3 (capacity 대표값)**: 5 agent 모두 cognitiveCapacity 150000 단일값(mc-opus 파생). 대표 모델링 가정이며 SHACL이 sum-fit 미강제(의도적, tool/review 검사) — MAS-W 선례와 동일 수용.

라우팅: 전 항목 통과. N2만 경미한 doc 정정 후보(선택). 온톨로지 반영 불필요.
