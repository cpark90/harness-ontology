# Role characteristics organization + optional ho:userFacing

roles.ttl 리팩터: 7 role을 bare classification stub → 특성 명시 노드로. `ho:userFacing`을
required 분류 프로퍼티에서 **optional 특성**으로 재정의.

## userFacing = OPTIONAL (present-only 시맨틱)
- 이전: 모든 role에 `ho:userFacing true|false`. 변경: **true인 것에만** 붙임(orchestrator,
  inspection). worker 5개(developer/research/inspection-worker/vnv/design)에선 false를 **삭제** →
  부재=not-user-facing. TBox definition도 "OPTIONAL, not defining; absence carries the meaning,
  false normally omitted"로 갱신.
- materialize `build_role_md`: userFacing은 원래 emit 안 됨. `g.value(role, HO.userFacing)`가
  present일 때만 "**User-facing role**"/"**Not user-facing**" 라인 emit(부재면 무출력). manifest
  record도 `if uf is not None: rec['userFacing']=bool(uf)`. → present-only 대칭.

## role 특성 배선 = 기존 core 파트 IRI REUSE (도메인 발명 금지)
- `ho:roleGuardrail`(→Guardrail), `ho:roleTool`(→Tool), `ho:roleMemoryPolicy`(string 1줄).
  rolePersona는 **스킵**(새 SystemPrompt 저작=heavy persona 금지, YAGNI; definition으로 충분).
- **함정**: roleTool/roleGuardrail 대상은 SHACL상 아무 Tool/Guardrail이나 range OK(no shape가
  "harness usesTool ⊇ roleTool" 강제 안 함). 하지만 TBox definition 컨벤션이 "Points at Tools the
  harness already binds via usesTool"라 **충실하려면** roleTool로 새 tool 쓰면 harness usesTool에도
  추가해야 함. 예: research에 tool-websearch/tool-retriever 주려고 h-multiagent usesTool에 둘 추가
  (이미 h-research가 써서 globally reachable→orphan은 아니지만 컨벤션 준수차 harness scope에 포함).
  usesTool에 provider 추가는 requiresCapability 짝맞춤 위반 아님(extra provider 허용).
- 새 노드 0개(persona 안 만듦)→ individual count 불변(99). triple만 증가.

## 예측 배선(이번 세션)
orchestrator: tools none(gr-delegated=no tool exec) / gr-{delegated-orchestration,report-over-prompt,
bounded-context,reuse-first}. inspection(user-facing,git): tool-shell,editor / gr-{traceability,
report-over-prompt,least-privilege,verify-proceed}. developer: editor,shell / gr-{dispatch-execution,
least-privilege,reuse-first,controlled-vocabulary}. research: websearch,retriever / gr-{dispatch,
least-privilege,grounding,bounded-context}. inspection-worker: retriever,shell / gr-{dispatch,
least-privilege,report-over-prompt,verify-proceed}. vnv: shell,retriever / gr-{dispatch,least-privilege,
verify-proceed,no-arbitrary-decision}. design: tools none / gr-{dispatch,least-privilege,simplicity,
root-cause,grounding}.

## channel redefinability (Task 4)
스키마 무변경으로 이미 지원 — harness가 `ho:hasChannel`로 어떤 채널 개체를 선언할지 고르므로
inter-agent 관계는 harness-scoped. 중앙 chan-* 는 reusable DEFAULT; harness가 자기 Channel 개체
(자기 channelParticipant/medium)로 redefine 가능. ho:Channel/ho:hasChannel definition + docs
(composition-methodology.md)에 명시만 추가. 즉 "관계는 global 고정 아님"은 문서/정의 레벨 사항.
