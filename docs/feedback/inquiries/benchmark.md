---
status: closed        # open(user) → answered(inspection) → closed(orchestrator)
targets: []           # 노드 변경 아님 — 아키텍처/거버넌스 사안
---

> **반영 완료 (orchestrator, 2026-07-21)**: 사용자 확정 D1=owl:imports+catalog · D2=repo 분리 ·
> D3=`.../id/<domain>/<slug>` 서브네임스페이스 · D4=기여자 로컬+data-repo CI. developer dispatch로
> 구현, vnv 독립검증 **pass-with-notes**(차단 없음). 산출: `docs/federation-design.md`(설계·마이그
> 레이션·후속), loader(`catalog-v001.xml`+`ontology/harness-ontology.ttl`+`ontology_lib.load_graph`),
> ONTOLOGYSTYLE §2a/§4, `docs/CONTRIBUTING-ONTOLOGY.md`, `docs/ci/data-repo-validate.yml`. 검증 리포트:
> `docs/verify/federation-architecture.md`. **후속(이 lane 밖)**: 물리 GitHub repo 분할·생성 →
> inspection 세션 + 사용자 계정(대상 repo 지정 시 진행).
# 질문(사용자): auto처럼 GitHub 연합·순수데이터 온톨로지 + 기여 가이드라인

https://github.com/lu-w/auto
이 자율주행 관련 온톨로지와 같이 온톨로지들을 github을 저장소로 서로 연결성을 가지게 개별
확장해가고 싶어. 온톨로지 구축에 참여하는 다른 유저도 각자의 github에 온톨로지를 업로드할 때
참고하는 가이드라인을 만들어서 제공하려고해. 또한 이 온톨로지의 포맷도 참고하고 싶고, 온톨로지
저장용 github에는 최대한 도구들은 없고 순수 데이터만 저장해놓고 싶어. 예를 들어 작업할 때는
해당 git을 clone해서 작업하고 push하는 식으로.

## 답 (inspection 조사 — 2026-07-21)

### 1. auto가 실제로 무엇인가 (참조 대상 확인)
- **순수 데이터 OWL repo, 도구 없음.** main `automotive_urban_traffic_ontology.owl`이
  하위 온톨로지(`criticality_phenomena.owl` 등)를 `owl:imports`로 단일 그래프로 통합, IRI→로컬
  파일 매핑은 **`catalog-v001.xml`**(Protégé 카탈로그). 버전은 **GitHub releases**(v2.0.0,
  2023-08). 라이선스 MIT. 근거: WebFetch(repo 루트 + raw README) 2회.
- README엔 **IRI 패턴·import 구문·기여 가이드가 명시돼 있지 않음** → 정확한 네임스페이스/카탈로그
  매핑은 `.owl`·`catalog-v001.xml` 원문을 봐야 확정(현 조사 한계, 아래 §한계).
- **시사점**: auto의 "서로 연결성" = **IRI 기반 `owl:imports` + catalog**. 연합의 표준 메커니즘.

### 2. 우리 현재 구조 대조 (핵심 gap 3축)
- **로딩이 owl:imports가 아니라 디렉토리 glob**: `load_graph`가 `ontology/**/*.ttl`을 전부
  parse해 한 그래프로 병합(`tools/ontology_lib.py:50-54`). abox는 `owl:imports` 없이 `ho:`/`id:`
  네임스페이스 공유 + **같은 폴더에 있다는 사실**만으로 병합됨(`ontology/abox/seed.ttl:1-7`).
  → **타 repo의 온톨로지를 현 로더는 읽지 못한다.**
- **data와 tools가 한 repo**: TBox(`tbox/harness.ttl`)·SHACL(`shapes/`)·validate/retrieve/webui가
  abox와 동거. 사용자의 "저장 repo = 순수 데이터"와 정면으로 다름.
- **가치(anti-orphan/drift/rot)는 병합된 전체 그래프 검증에서 나옴**(DESIGN.md) — 연합에선
  "union을 어떻게 구성하느냐"가 검증 성립의 전제가 된다.

### 3. 목표별 파급효과 + 결정지점
**(a) GitHub 연합 다중 repo (auto처럼)** — 현 glob 로더로는 불가. 3안:
- **owl:imports + catalog**(auto 방식): IRI로 참조, catalog가 IRI→로컬클론 매핑. loader를
  imports 해석형으로 교체 필요. auto와 최정합.
- **git submodule**: 외부 data repo를 `ontology/abox/<repo>/`로 vendor → **glob 그대로 동작
  (최소 변경)**. 버전 핀 = submodule commit.
- **manifest(repos.txt)**: 연합 repo 목록을 clone+merge하는 스텝을 도구에 추가.
→ 어느 안이든 loader는 tools 변경 = **developer 소관**.

**(b) data/tools 분리 (순수 데이터 repo)** — repo 2계층 분리 권장:
- **schema/tooling repo**(중앙·권위): TBox + shapes + validate/retrieve/webui + guideline + CI.
- **data repo(s)**(순수 TTL abox, 기여자별 github): 작업 = clone→편집→validate(중앙 도구로)→push/PR.
- anti-drift와 **양립**: TBox(어휘)가 중앙에서 권위 유지, data repo는 거기에 conform.
- **단, "도구 없음"이면 검증 게이트가 통합 시점으로 밀린다**(기여 시점 fail 약화). 해소: 기여자가
  중앙 도구를 로컬로 실행(guideline 명시)하거나, data repo CI가 중앙 `validate.py`를 pull해 게이트.

**(c) IRI 전략 (연합의 필수 선결)** — 현 단일 base `https://harness-ontology.dev/id/`는 독립 repo
간 **slug 충돌·orphan 위험**. 기여자/도메인별 서브네임스페이스(`.../id/<domain>/<slug>`) 강제 필요.
cross-repo edge(A의 개체가 B의 개체를 `hasComponent`)는 **union 위에서만** reachability/SHACL 성립.

**(d) 포맷 참조** — auto=OWL(RDF/XML), 우리=Turtle. 포맷 자체보다 **연결 규약**(공유 TBox IRI +
imports/catalog + IRI 네이밍 + `tokenEstimate` + `Concept` 태깅)을 guideline으로 고정하는 게 핵심.
`ONTOLOGYSTYLE.md §1a–1d`가 이미 그 원형이라 기여자용으로 발췌·확장하면 됨.

### 4. 권고 (요약)
- 아키텍처: **중앙 schema+tooling repo + 순수-data abox repo(들)**, 공유 TBox IRI로 연결. 연합
  로딩은 **submodule(최소 변경) 또는 owl:imports+catalog(auto 정합)** 중 택1 — 초기엔 submodule 권장.
- 선결 결정: **[D1]** 연합 메커니즘(submodule / imports+catalog / manifest), **[D2]** repo 분리
  여부·경계, **[D3]** IRI 네임스페이스 규약, **[D4]** 검증 게이트 위치(기여자 로컬 vs 통합 CI).
- guideline 내용(권고): 공유 TBox 임포트법 · id 네이밍 규약 · 필수 술어(prefLabel/maturity/
  tokenEstimate/Concept 태깅) · validate 통과 후 PR · Turtle 포맷 규약. **저작은 developer/
  orchestrator 소관**(inspection은 내용 권고까지).

### 한계 (verify-then-proceed)
- auto 내부(`catalog-v001.xml`·`.owl`의 IRI/import 원문)는 README만으론 미확정 — 정밀 대조엔
  원문 fetch가 추가로 필요(필요 시 다음 사이클에 조사).
- 이 요청은 **그래프 노드 변경이 아니라 아키텍처/거버넌스** 사안 → `retrieve.py` projection 대상
  아님. 현 `validate.py` = **PASS**(변경 없음). 실제 반영(loader 교체·repo 분리·guideline·TBox
  IRI 규약)은 tools/TBox/문서 저작이므로 **inspection 범위 밖 → orchestrator(developer dispatch)**
  로 넘겨 D1–D4 확정 후 진행해야 함.
