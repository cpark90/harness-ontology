# ABox 파일 레이아웃 → DA-4 taxonomy 재조직 (사용자 확정 2026-07-23)

> 상위: `disambiguation-audit.md §G`(taxonomy). 목적: 물리 파일 레이아웃을 상위 계층(DA-4)과 일치시킴.
> 원리: federation은 catalog가 **논리 IRI→파일경로**를 매핑 → 파일 이동은 catalog 경로만 갱신하면 tool(validate/materialize)엔 투명. grab-bag(roles/domains-tasks/harnesses)은 타입별 split 필요.

## 현 소재 → 목표 (그룹 디렉토리 + grab-bag split)
| 그룹 디렉토리 | 파일 | 담는 타입 | 논리 IRI |
|---|---|---|---|
| `behavioral/` | system-prompts.ttl | SystemPrompt, PromptSection | data/core/system-prompts (유지) |
| `behavioral/` | guardrails.ttl | Guardrail | data/core/guardrails (유지) |
| `observational/` | **observation.ttl** (roles.ttl에서 split) | ObservationSpace, AreaOfInterest, AreaOfObservation | **data/core/observation (신규)** |
| `operational/` | tools.ttl | Tool, Candidate | data/core/tools |
| `state/` | **memory.ttl** (roles.ttl split) | Memory | **data/core/memory (신규)** |
| `organization/` | roles.ttl | Role, Agent | data/core/roles (유지, 축소) |
| `organization/` | channels.ttl | Channel | data/core/channels |
| `process/` | workflows.ttl | Workflow, WorkflowStep, Deliverable | data/core/workflows |
| `substrate/` | model-configs.ttl | ModelConfig | data/core/model-configs |
| `spec/` | capabilities.ttl · patterns.ttl · constraints.ttl · domains-tasks.ttl | Capability · DesignPattern · Constraint · (Domain,Task) | 각 유지 |
| `information-space/` | **information-space.ttl** (domains-tasks split) | EnvironmentSpace, GlobalState | **data/core/information-space (신규)** |
| `assembly/` | **assembly-sections.ttl** (harnesses.ttl split) | AssemblySection | **data/core/assembly-sections (신규)** |
| `wholes/` | harnesses.ttl | Harness | data/core/harnesses (유지, 축소) |
| `vocab/` | concepts.ttl | Concept | data/core/concepts |

- **verification/**·**operational/candidate** 등 중앙 individual 없는 그룹은 파일 미생성(TBox 클래스만 존재).
- **신규 유닛 4**: observation · memory · information-space · assembly-sections (root imports +4, catalog +4).
- **grab-bag split 3**: roles→(roles + observation + memory) · domains-tasks→(domains-tasks + information-space) · harnesses→(harnesses + assembly-sections). 논리 IRI는 잔류분 유지 + split분 신규.

## Wave
- **REORG-1 (중앙)**: 파일 이동/split + `catalog-v001.xml`(경로 갱신 + 4 신규) + `ontology/harness-ontology.ttl`(owl:imports +4) + `ONTOLOGYSTYLE §4`(레이아웃 문서). validate PASS(경로 투명).
- **REORG-2 (recipe catalog)**: `staging/harness-recipes/catalog-v001.xml`(13 central경로 갱신 + 4 신규) + 전용 catalog-<name>.xml 4개. recipe federate PASS(per-recipe closure).
- **inspection**: 중앙 push(신규 레이아웃) + recipes repo catalog 갱신 push.

## 리스크
- **blast radius**: 중앙 unit 구조 변경 = 전 recipe federation catalog 동기화(D4). REORG-2에서 각 recipe federate 재검증 필수.
- 순수 이동/split — 개체 내용·TBox·shapes 무변경. 논리 IRI 잔류분 유지로 recipe TTL의 `owl:imports <root>`는 무영향(root가 신규 유닛 흡수).
