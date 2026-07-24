# REORG-1: 중앙 ABox 파일 → DA-4 그룹 디렉토리 재조직 (순수 이동/split)

물리 레이아웃을 상위계층(DA-4)에 맞춘 재파일. **개체 내용·TBox·shapes 무변경** — 파일 이동 +
grab-bag split + federation(catalog/root imports/ONTOLOGYSTYLE) 갱신뿐.

## 왜 tool엔 투명한가 (핵심)
- 논리 IRI `.../data/core/<type>`는 **위치 독립** — 디렉토리 이동은 catalog의 `uri=` 경로만 갱신.
  `ontology_lib.py`엔 `abox/core/` 하드코딩 **없음**(catalog primary + glob fallback).
- glob fallback(`HARNESS_CATALOG=/nonexistent`)도 `ONT_DIR/**/*.ttl` **recursive `**`**라 서브디렉토리
  자동 픽업 → 두 로더 경로 다 PASS. (검증: 기본 + glob fallback + 명시 env 3경로 모두 185/PASS.)

## 레이아웃 (그룹 디렉토리 = DA-4 상위계층)
`ontology/abox/core/<group>/<type>.ttl`: behavioral(system-prompts·guardrails)·operational(tools)·
substrate(model-configs)·organization(roles·channels)·process(workflows)·vocab(concepts)·
spec(capabilities·patterns·constraints·domains-tasks)·observational(observation)·state(memory)·
information-space·assembly(assembly-sections)·wholes(harnesses). 개체 없는 그룹(verification 등)=파일 미생성.

## grab-bag split 방법 (byte-fidelity 라인 슬라이스)
retype 말고 **원본 라인 1-indexed 슬라이스 concat** 스크립트(`split-core-per-type-units.md` 패턴 재사용).
신규 유닛 = **prefix 블록(원본 L1-7 그대로) + 새 `owl:Ontology` 헤더(신규 IRI) + 이동 섹션(배너·주석 보존)**.
- roles.ttl → organization/roles.ttl(Role8+Agent5, IRI 유지) + observational/observation.ttl(OS5+AoI5+AoO10, 신규) + state/memory.ttl(Mem3, 신규).
- domains-tasks.ttl → spec/domains-tasks.ttl(Dom4+Task6) + information-space/information-space.ttl(EnvSpace+GlobalState, 신규).
- harnesses.ttl → wholes/harnesses.ttl(Harness7) + assembly/assembly-sections.ttl(AS8, 신규).
- cross-unit 참조(dom-design→env-space 등)는 잔류/신규 다른 파일에 걸쳐도 root union이 해석 → OK.

## federation 3점 동기화
- `catalog-v001.xml`(root): 13 uri 경로 갱신 + 신규 4 uri.
- `ontology/harness-ontology.ttl`: owl:imports +4 신규 IRI(observation/memory/information-space/assembly-sections).
- `ONTOLOGYSTYLE §4`: 그룹 디렉토리 [지킴] 규칙 추가(논리 IRI 유지·catalog가 IRI→경로).
- **REORG-2(recipe staging catalog)는 별건** — 여기선 중앙만.

## 게이트
validate 185 individuals 불변(이동/split은 count 무변경) + 4체크 green. 실패 시 catalog 경로/신규 IRI 헤더 점검.
