# federation (owl:imports+catalog) 검증 재현 절차 + 함정

D1–D4 (catalog+owl:imports 로딩 / central-data 분리 / 도메인 IRI `id/<domain>/<slug>` /
2단계 validate 게이트) 아키텍처를 판정할 때의 표준 절차. 전부 `/usr/bin/python3`.

## 핵심 재현 (파일 절대 수정 금지 — env override + scratchpad script만)
- **구조 게이트**: `tools/validate.py` → PASS 4섹션 캡처.
- **로더 등가성 (D1)**: catalog+imports vs glob-fallback 유니온이 동일함을 증명.
  fallback 강제는 `HARNESS_CATALOG=/nonexistent` env로(파일 안 건드림). `ontology_lib`을
  `sys.modules`에서 지우고 reload해야 모듈-로드시 읽는 `CATALOG` 상수가 새 env를 반영한다.
  raw triple set diff(양방향)·`instance_nodes` 대칭차 모두 ∅ 확인. (여기선 둘 다 514 triples/62 개체.)
- **IRI 무결성 (D3)**: 유니온의 모든 subject/object에서 `.../id/` 접두 IRI를 도메인 세그먼트로
  분류. flat `id/<slug>`(도메인 없음)=0, dangling(instance-link 대상인데 typed individual 아님)=0
  이어야. `id/core/scheme`(skos:ConceptScheme)는 개체 아님 — 오탐 주의. 크로스도메인
  lpranging→core 엣지가 `instance_edges`로 실제 resolve 되는지 카운트.
- **발견성 (anti-rot)**: `retrieve.py "<원 request>" --format json`. 주의: JSON seeds 항목은
  `label`/`score`만 있고 **iri 없음** → 도메인 IRI 확인은 retrieve 출력 말고 그래프(§IRI)에서.
- **federation smoke (D4)**: `HARNESS_ROOT_ONTOLOGY=.../data/<domain>`로 유니온을 데이터
  유닛에 root → import closure가 schema+core+<domain>만 구성되는지·validate PASS인지.
  이게 data-repo CI 시나리오. `docs/ci/data-repo-validate.yml`이 실제로 central `validate.py`를
  composed union에 돌리는지(no-op 아님) 확인: catalog는 step env, ROOT_ONTOLOGY는 job env로
  상속됨. validate.py는 SHACL를 `lib.ONT_DIR/shapes`(central 체크아웃)에서 로드.
- **hygiene**: Write 툴 잔재(`</content>`,`</invoke>`,`<invoke`,`<parameter`,`</antml…`) 스캔.
  grep에 special char 넣으면 셸이 깨지니 python 스크립트로 needle 검사.
- **anti-drift**: abox에서 쓴 `ho:` 술어/타입 - tbox 선언 = ∅. 헤더는 owl:Ontology/owl:imports만.

## 판정 함정
- catalog가 존재하지만 없는 파일을 매핑할 수 있음(예: `data/authored`→authored.ttl 미존재).
  BFS는 missing을 조용히 skip → 유니온 개체수 불변이면 정상(의도된 optional). 결함 아님, note로.
- 63 vs 62 개체 불일치는 대개 `skos:ConceptScheme` 같은 non-INSTANCE_CLASS 노드.
- 물리 repo 분리·IRI publication·webui 도메인선택은 git/infra/webui 스코프 → inspection/user로
  라우팅되는 deferred. developer dispatch 판정에서 블로커로 잡지 말 것.

판정 리포트: `docs/verify/federation-architecture.md` (pass-with-notes: 8검증 전부 통과,
notes=authored.ttl 의도적 부재 + CI 템플릿 기본값 + deferred 3항목 올바르게 라우팅).
