# Splitting the central `core` ABox into per-component-type units

중앙 `core` data unit(구 `ontology/abox/seed.ttl`)을 컴포넌트 타입별 여러 문서
`ontology/abox/core/<type>.ttl`로 쪼개는 재파일(restructure) 작업 노트. 개체 IRI는
`.../id/core/<slug>` 그대로 두고 **파일 위치만** 바꾸는 순수 re-file.

## 파일 분할 (11 units, 64 individuals)
concepts(10 Concept + `id:scheme` ConceptScheme는 개체 count에 안 들어감) · capabilities(7) ·
constraints(1) · model-configs(2) · tools(4) · guardrails(14) · patterns(4) · workflows(4) ·
system-prompts(4) · domains-tasks(Domain 4 + Task 6 = 10) · harnesses(4). 합 64.
- **함정**: seed엔 `ho:Constraint`(`id:con-lowlatency`)가 있는데 타입별 파일 목록에서 빠지기 쉽다.
  "타입별 분할" 원칙대로 `constraints.ttl`을 따로 만든다(누락/오분류 금지). brief 목록에 없으면 보고.
- `id:scheme`(skos:ConceptScheme)은 `INSTANCE_CLASSES`에 없어 validate의 64 count에 안 잡힌다 →
  concepts.ttl에 두되 count 기대치는 그대로 64.

## Byte-identical move 방법 (권장)
retyping 말고 **원본 라인 슬라이스 스크립트**로 이동: `lines=open(seed).readlines()` 후
1-indexed 범위를 concat. prefix 블록(seed L1-7)·`#=====` 배너·노드 본문 전부 슬라이스로 재사용 →
바이트 동일 보장. 검증: 원본 seed vs 새 파일 union을 rdflib로 파싱해 owl:Ontology 트리플만 제외하고
triple set diff가 0인지 확인(여기선 364=364, diff 0, ontology decl 1→11).

## Wiring 선택 = root union (siblings 서로 import 안 함)
각 per-type 파일은 자기 `owl:Ontology`(문서 IRI `.../data/core/<type>`)로 **schema만** import.
cross-unit 참조(harness→tool/guardrail 등)는 root(`harness-ontology.ttl`)의 `owl:imports`가 11개
unit을 전부 나열 → **root union에서 해석**. sibling 상호 import는 안 씀(단순·일관, gr-simplicity).
catalog-v001.xml은 각 `.../data/core/<type>` IRI→`ontology/abox/core/<type>.ttl` 매핑.

## 게이트 / gotcha
- 두 로더 경로 동치 증명: 기본(imports+catalog) vs `HARNESS_CATALOG=/nonexistent`(glob fallback).
  reload로 `ontology_lib` 다시 import해 env 반영. 둘 다 triples·individuals 동일해야(여기 1429/64).
  split 후 triple 총수는 owl:Ontology decl이 1→11로 늘어 baseline보다 커짐(1389→1429) — 정상,
  개체 64·비-ontology 데이터 트리플 364는 불변.
- retrieve 랭킹: `candidates`·`gaps`는 완전 동일. 단 **동점 score(예 2.7) seeds의 tie-order**는
  triple 삽입 순서가 바뀌면 재배열될 수 있다(비의미적). IRI·score·candidate 결과는 불변이므로
  "same rankings, IRIs unchanged" 충족. tie를 결정화하려 retrieve.py sort 손대지 말 것(scope 밖·전역 동작 변경).
- seed.ttl 이름 참조: `tools/`엔 사실상 없음(retrieve.py의 "seed"는 검색 시드로 무관). live 구조
  문서만 갱신(README layout·federation-design catalog표·ONTOLOGYSTYLE 배너 ref·CI 템플릿).
  `docs/verify/**`·`docs/feedback/**`·`docs/plans/**`는 시점 기록(immutable)이라 건드리지 않음.
- ONTOLOGYSTYLE §4에 "한 도메인 data를 per-type 다중 문서로 분할 가능(`.../data/<domain>/<type>`)"
  [지킴] 규칙 추가함.
