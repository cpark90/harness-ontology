# Coordination channels as `ho:Channel` individuals + new core unit

멀티에이전트의 **소통/조정 채널**을 중앙 중립 온톨로지에 반영. roles.ttl(role-taxonomy 노트)과
쌍둥이 패턴: 새 core unit + `ho:hasRole`-스타일 서브프로퍼티. detail-check 결과 채널 개념은
반영 전무였음(roles/guardrails/patterns만; "channel" 단어는 gr-report-over-prompt promptText에만).

## TBox 확장 (hasRole 패턴 그대로 모방)
- `ho:Channel` ⊑ HarnessComponent — conduit+participants+protocol를 잡는 컴포넌트(Role/Guardrail과 구별).
- `ho:hasChannel` ⊑ `ho:hasComponent`, range Channel, **domain 생략**(hasComponent서 상속=Harness).
  hasRole와 동일하게 서브프로퍼티라 새 shape 불요·reachable·orphan 아님.
- `ho:channelParticipant` domain Channel range Role — 엔드포인트 role(hasRole가 이미 묶은 것 지목).
- `ho:involvesUser` DatatypeProperty domain Channel range boolean(userFacing 옆에 배치, `true`/`false` 무따옴표).
- `ho:channelMedium` DatatypeProperty domain Channel range string(medium 서술; roleMemoryPolicy 스타일).
- 배치: Channel class는 Role 다음/Candidate 앞; obj prop은 hasRole 다음; datatype는 userFacing 다음.

## 함정/판단
- **tokenEstimate 불필요**: Channel은 skos:definition만 있고 promptText 없음 → Role 선례 따라 생략
  ([지킴]은 promptText-bearing류+Tool/Workflow에만 요구). channelMedium은 짧은 지시문(prose 아님).
- 참조는 같은 파일 = 같은 core namespace라 `id:role-*`(cross-ns `core:` 아님). roles.ttl 컨벤션 일치.
- 배선 3점 동시(role 노트와 동일): channels.ttl 자체 owl:Ontology(schema만 import) + catalog-v001.xml
  (repo root) `core-channels` 엔트리 + root harness-ontology.ttl owl:imports. → 두 로더 parity.

## 실제 채널 3개(소스=repo CLAUDE.md + docs/feedback/*)
- chan-agent-user: orchestrator+inspection, involvesUser true, "durable file channel (inbox/report)";
  report-over-prompt, 사용자만 open→approved 승인 게이트.
- chan-orchestrator-inspection: 동 participants, false, "persistent file channel + status markers
  (wip->rename, frontmatter status)"; verify lane(inbox→verified)+inquiry lane(open→answered→closed),
  verify-then-proceed(시간가정 금지).
- chan-dispatch: orchestrator+worker roles(developer/research/inspection-worker/vnv/design), false,
  "dispatch (subagent spawn)".
- 전부 maturity "reviewed", tagged c-multiagent, h-multiagent에 hasChannel로 배선.

## 게이트
validate 73→76 typed(id/ subject 77=+scheme) PASS; 두 로더 778 triples·individual set 동일;
retrieve "orchestrator inspection user ... channel coordination"에 chan-* 3개 표면.
