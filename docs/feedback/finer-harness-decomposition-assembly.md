---
status: approved            # 사용자만 approved로 바꾼다
targets: [id:h-lpranging, core:wf-multiagent, core:h-multiagent]
kind: proposal
---
# 하네스 더 잘게 분해 + 부품 조립(composition)을 그래프로 명시

## 요청 (사용자, 정정)
"설계내용(도메인 그래프)은 제외. **하네스를 더 잘게 분해**하고 **분해된 부품들이 어떻게
조립되는지에 집중**." → 온톨로지 범위는 harness 모델 그대로, SPEC granularity와 **조립 구조**만 세밀화.

## 현재 상태 (실측) — 이미 된 것 vs coarse
**이미 finer로 모델링됨(재제안 불필요)**:
- Role이 조립 scope를 선언: `ho:roleTool`(least-privilege tool 부분집합)·`ho:roleGuardrail`·
  `ho:rolePersona`·`ho:roleMemoryPolicy` (`role-developer` 등).
- Channel이 조립을 선언: `ho:channelParticipant`(참여 role)·`ho:involvesUser`·`ho:channelMedium`.

**아직 coarse / 조립이 암묵적(=이번 개선 대상)**:
1. **Workflow가 분해 안 됨**: `wf-multiagent`는 1노드 + 한 문장 정의. **step 구조 전무**
   (`WorkflowStep`/`hasStep` = 0). 실제 프로세스(6단계 생애주기 등)가 하나의 blob.
2. **SystemPrompt가 blob**: persona가 통짜. 실제 CLAUDE.md는 다중 섹션인데 섹션 분해 없음.
3. **조립 순서·구조가 그래프가 아니라 `materialize.py`에 하드코딩**: 섹션 순서가 코드 고정
   (`tools/materialize.py:51` "fixed order"). → "부품이 **어떻게** 조립되는가"가 SPEC이 아니라 EMIT
   코드에 들어있음(INV: SPEC이 조립을 규정해야 EMIT은 읽기만).
4. **부품 간 조립 edge 부재**: step↔tool/role/guardrail, guardrail↔workflow-step 같은
   **부품-대-부품** 관계가 없음(현재는 harness→부품 star + role-scoping뿐).

## 제안 (orchestrator 계획용) — 분해축 + 조립축

### 분해축 (coarse 부품을 sub-part로)
- **`ho:Workflow` → `ho:WorkflowStep`**(신규, ⊑HarnessComponent): 순서(`ho:stepOrder`/`ho:nextStep`)
  + step별 조립 edge `ho:stepUsesTool`·`ho:stepByRole`·`ho:stepGuardedBy`. 최우선(가장 큰 blob).
- **`ho:SystemPrompt` → 섹션/fragment**: prompt를 합성 가능한 조각으로(`ho:promptSection` +
  순서). 통짜 persona를 조립물로.

### 조립축 (부품이 어떻게 합쳐지는가를 그래프로)
- **조립 구조를 그래프 데이터로 승격**: 현재 materialize에 하드코딩된 섹션 순서·중첩을
  **온톨로지 property로**(`ho:assemblyOrder`/section 구조). → materialize는 그래프의 조립사양을
  **읽기만**(결정성은 총순서를 그래프가 규정해 유지). "조립 방식"이 inspectable·harness별 조정 가능해짐.
- **부품-대-부품 관계 명시**: step→tool/role/guardrail(위), guardrail→적용대상(role/step),
  tool→provides capability→소비 step. 암묵 조립을 typed edge로.

## 핵심 결정 (orchestrator/사용자)
1. **조립을 어디까지 그래프로 옮길까**: (a) Workflow step 분해만(최소·큰 효과) → (b) + SystemPrompt
   섹션 → (c) + 조립순서까지 그래프-구동(materialize 하드코딩 제거). 범위 선택.
   추천: **(a)부터 작게**(ODR §8), 검증 후 확장.
2. **결정성 보존**: 조립순서를 그래프로 옮기면 **총순서를 그래프가 규정**해야 byte-identical 유지
   (materialize N: 순서 미규정 시 fallback 아닌 error). anti-rot: sub-part 증가 → `tokenEstimate`·
   retrieve 예산 투영 재확인.
3. **coverage-audit gate**: WorkflowStep 등 신규 구조요소는 CLAUDE.md step-7 coverage 매핑 대상.
   신규 TBox 범주 → "Adding vocabulary" 규율(연결·orphan 방지).

## 권고 — 작게 반복 (ODR §8)
파일럿: `wf-multiagent`(또는 `wf-compose-harness`)를 **~3 WorkflowStep으로 분해** + step별
`stepUsesTool`/`stepByRole` 1~2개 + materialize가 그 step들을 Process 섹션에 순서대로 emit →
validate + retrieve(예산) + materialize(byte-identical) 확인. 통과 후 SystemPrompt 섹션·조립순서
그래프화로 확장.

## 범위 / 핸드오프
inspection은 조사·제안까지. TBox 신규 범주(`WorkflowStep`…)·조립 property·materialize 확장 저작은
orchestrator가 dispatch brief로 계획해 **developer** 수행(schema 변경은 coverage-audit gate 아래).
승인 = `status: open`→`approved` + 위 핵심결정 1(범위 a/b/c) 지정.

## 사용자 피드백
1. (c)
2. 승인
3. 승인

## inspection 검토 (2026-07-23 — 구현 계획 참고, orchestrator용)
승인 상태·미구현 확인 + 승인된 **범위 (c)**(WorkflowStep + SystemPrompt 섹션 + **조립순서 그래프-구동**)
기술 검토.

### 상태 (실측)
- 승인: 범위 **(c) 전체** + 결정2(결정성)·3(coverage-gate) 승인.
- **미구현**: `WorkflowStep`/`stepUsesTool`/`promptSection`/`assemblyOrder` 흔적 0 (ontology·tools·staging).
- 현재 in-flight batch4는 **reference-model**(레시피=참조저장)로 finer와 **무관**. finer 구현 브리프는 별도 필요.
- **프로세스 정정**: batch4 브리프가 stale 이름 `finer-domain-design-graph.md`를 참조 — 그 제안은
  폐기·교체됨(현재 = 이 파일 `finer-harness-decomposition-assembly.md`). orchestrator 참고.

### (c) 기술 검토 — 난이도·리스크 순
1. **조립순서 그래프-구동 = 최대 난점(리스크 高)**: 현재 materialize가 **고정 섹션 순서를 하드코딩**해
   byte-identical(원리5/INV-2)을 보장(`tools/materialize.py:51`). 이를 그래프로 옮기면 **결정성이
   "그래프가 총순서(total order)를 규정"에 의존**. → 필수: (i) 조립순서가 **total·well-defined인지
   validate/SHACL 체크**, (ii) 미규정 시 **error(승인된 결정2)**, (iii) materialize를 fixed→graph-driven
   리팩터하되 **byte-identical 회귀 테스트 유지**. 이 항목이 (c)의 핵심 위험.
2. **WorkflowStep reachability**: 신규 `ho:WorkflowStep`⊑HarnessComponent를 harness-reachable로 만들 때
   **`ho:Candidate`의 propertyChain 패턴 재사용**(harness→workflow→step) 권장 — 직접 sub-property는
   Workflow를 Harness로 mistype해 HarnessShape 트립(기존 Candidate 교훈과 동일 함정).
3. **SystemPrompt 섹션**: `promptSection`+순서. WorkflowStep과 같은 reachability·순서 규율.
4. **anti-rot**: workflow→여러 step, prompt→여러 section으로 **노드 수 증가** → 각 `tokenEstimate` 필수,
   `retrieve` 예산 투영 재확인(승인된 결정2).
5. **coverage-audit + Adding vocabulary**: 신규 구조요소는 CLAUDE.md step-7 매핑 + orphan 연결 규율.

### 권고 (구현 순서)
승인은 (c) 전체지만 **land는 (a)→(b)→(c) 순차**를 권함(ODR §8): ① WorkflowStep 파일럿(`wf-multiagent`
~3 step + step edge, materialize가 Process 섹션에 순서 emit, byte-identical 확인) → ② SystemPrompt 섹션
→ ③ 조립순서 그래프화(가장 위험 → 마지막, 회귀 테스트 강화). 각 단계 land마다 federate/materialize 검증.
inspection은 검토까지 — 구현 브리프·저작은 orchestrator/developer.
