# GAP-3: `core/verification/` data unit 신설 (순수 relocation) + 전용 catalog 재동기화

co-locate된 leaf(scn-/fp-)를 자기 DA-4 그룹 유닛으로 옮기는 **순수 relocation** 레시피.
개체 IRI는 위치독립이므로 그래프는 무변경 — 파일·federation 배선만 바뀐다.

## 절차 (relocation = 4점 동기화)
1. 신규 `ontology/abox/core/<group>/<type>.ttl` = 원본 prefix 블록(L1-7 그대로) + 자기
   `owl:Ontology` 헤더(`.../data/core/<type>`, `owl:imports` 중앙 schema만) + 배너 + **라인 슬라이스로
   옮긴 개체 블록**(retype·재작성 금지 — `/usr/bin/python3`로 `src[a:b]` concat이 byte-fidelity).
2. 원본 파일: 옮긴 블록 + 그 전용 배너만 삭제(잔여 섹션 무접촉).
3. `ontology/harness-ontology.ttl` root `owl:imports` +1 IRI, 4. `catalog-v001.xml` +1 uri,
   5. `staging/harness-recipes/catalog-v001.xml`(+dedicated catalog) +1 uri(`central/` prefix).
- 게이트: validate **개체 수 불변**(증감 0이면 유실/중복 없음) + glob fallback(`HARNESS_CATALOG=/nonexistent`,
  `**` recursive라 신규 서브디렉토리 자동) + per-recipe closure.

## ★함정: 전용 catalog-<recipe>.xml은 조용히 썩는다
- REORG-1/2 때 공유 catalog만 그룹경로로 갱신 → 4개 dedicated catalog는 **평면경로 잔존 + 신규유닛 누락**.
- 증상이 "에러"가 아니라 **부분 closure**: 미해결 import를 로더가 건너뛰어 `41 individuals`만 로드되고
  capability/assemblyOrder가 FAIL(원인 파일이 catalog라고 안 알려줌). 개체 수가 기대치보다 작으면 catalog 의심.
- 대응: dedicated catalog의 central 블록을 **공유 catalog의 central 블록으로 통째 치환**(root~data-auth 라인 범위
  스크립트 치환, recipe 엔트리는 파일별로 보존). 4개 전부 PASS로 복구(216~218).

## 배너(§1d) 재작성
옮기고 나면 "이 유닛이 없어서 여기 둔다"는 원래 배너 사유가 소멸 → 새 유닛 배너는 **역할 요약 + 무엇이
이 부품을 연결하는가**(hasTestScenario/hasFailurePolicy = 직접 ⊑hasComponent)로 다시 쓴다.

## 파급: "individual 없는 그룹은 파일 미생성" 서술이 stale
`ONTOLOGYSTYLE §4`와 `docs/plans/abox-taxonomy-reorg.md`가 `verification/`을 **파일 없는 그룹 예시**로
인용 → 유닛 신설 시 두 곳 예시 교체 필요(developer 소유 밖이면 FLAG로 보고).
