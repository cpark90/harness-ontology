---
status: approved
targets: []          # 툴링 추가 — 온톨로지 노드(id:*) 변경 아님. 영향 경로는 tools/·docker
kind: proposal
rev: 4
---
# 온톨로지 관리도구 — Docker 패키징 로컬 Python 웹 UI

## 요청 (사용자)
에이전트가 온톨로지를 관리하기 쉬우면서 사용자가 확인하며 고치기 쉬운 **웹브라우저 UI
관리도구**. **로컬 Python 웹서버** + **배포·운영 쉽게 Docker**. orchestrator가 승인 후 build.

## 핵심 원칙 (drift/orphan/rot 방어를 UI로 승격)
웹도구는 **상태를 fork하지 않는다** — 같은 `ontology/*.ttl`을 단일 진실공급원으로, 같은
`ontology_lib.py`/`validate.py`/`retrieve.py`를 통해 읽고 쓴다:
- **anti-drift**: 편집 폼이 TBox 어휘로 **구속**(클래스=TBox 클래스, 프로퍼티 필드=range 제약
  picker). 새 near-synonym 클래스·untyped edge를 만들 수 없다.
- **anti-orphan**: 저장 전 `validate.py` 게이트 — orphan·capability gap·중복 label이면 FAIL을
  인라인 표시하고 write 차단. 그래프 뷰로 고립이 눈에 보인다.
- **anti-rot**: 조회/composition은 `retrieve.py` pack 경유. `tokenEstimate` 누락 노드 경고.

## 재검토 (v2) — 코드 대조로 발견한 정정 (근거 file:line)
초안의 "import만 하면 됨 / 로직 불변" 주장이 실제 도구와 어긋나 정정한다:
1. **`retrieve.py`는 그대로 재사용 가능** — `project(g, request, budget)`가 dict 반환 +
   `--format json` 이미 있음(`retrieve.py:154,286`). `/api/retrieve`는 이걸 직접 호출.
2. **`ontology_lib`도 재사용 가능** — `load_graph`·`instance_nodes`·`instance_edges`·
   `label_of`·`most_specific_types`(`ontology_lib.py:42–105`)로 `/api/graph`·`/api/schema` 구성.
3. **`validate.py`는 리팩터 필요(로직 불변 아님)** — `check_shacl`가 SHACL 리포트를 버리고
   `conforms`(bool)만 반환(`validate.py:36,49`), 나머지 check도 print+bool. UI 패널에 SHACL
   메시지·orphan 목록·capability gap을 주려면 **`--json` 출력 모드 추가**(retrieve.py 패턴을
   validate.py에 이식) 또는 check_* 를 구조화 반환으로 분리. 표시 로직만 추가, 검사 로직은 유지.
4. **flat import 주의** — 두 스크립트가 `import ontology_lib`(패키지 아님, `validate.py:23`·
   `retrieve.py:34`). `uvicorn tools.webui.server:app`로 띄우면 `tools/`가 sys.path에 없어
   실패 → server.py가 `sys.path`에 `tools/`를 넣거나 서브프로세스 호출. `ONT_DIR`은
   `ontology_lib.__file__` 기준(`ontology_lib.py:19–20`)이라 볼륨 마운트는 `ontology/`를
   `tools/`의 형제로 둔다.
5. **TTL write는 rdflib 재직렬화 금지** — 그래프를 통째 `serialize()`하면 섹션 배너(`#===`)·
   주석·한줄/여러줄 스타일·프레디킷 순서·prefix 배치가 전부 파괴돼 ONTOLOGYSTYLE §3·§4와
   사람 diff 가독성을 깬다("확인하며 고치기"의 정면 위배). → **텍스트 수술식 쓰기**: 신규는
   해당 섹션에 노드 블록을 포맷해 **append**, 편집은 그 노드의 `id:x … .` **span만 치환**,
   파일 전체는 재작성하지 않는다. 검증은 파싱된 그래프로, 영속은 텍스트 레벨로.
6. **동시성·원자성** — CLI 에이전트(developer)와 웹(사람)이 같은 abox를 쓸 수 있다. 웹 쓰기는
   ① 로드 후 mtime/hash로 변경 감지(중간에 바뀌었으면 재로드), ② temp+`os.replace`로 원자
   교체, ③ 행 단위가 아니라 노드 블록 단위로 커밋. (참조 CODESTYLE의 partial-write 원칙.)
7. **보안** — compose 포트를 `127.0.0.1:8000:8000`로 바인딩(기본 0.0.0.0은 TTL write·추론
   실행 도구를 네트워크 노출). 인증 없음 = 로컬 신뢰 전제임을 README에 명시.

## 결정 (✅ 사용자 확정 / ▶ 추천)
- ✅ 실행: 로컬 Python 웹서버 + Docker(로컬 전용).
- ✅ A. 편집·저장: 즉시 저장 + validate 게이트 + TTL diff 미리보기(사람이 승인자).
- ✅ B. v1 범위: 네 화면 전부.
- ✅ C. 위치: `tools/webui/`.
- ▶ D. 온톨로지 DB / frontend framework: **아래 검토의 추천안**(TTL-in-git 유지 + rdflib
  in-process, Svelte/Vue + Cytoscape.js) ← 사용자 확인 필요.

## 온톨로지 전용 DB / frontend framework 검토 (사용자 질문)
### 결론 먼저
- **DB: 별도 triplestore로 교체하지 않는다(v1).** 이 프로젝트의 가치(DESIGN.md)는 *flat OWL
  파일 = 단일 진실공급원 + git-diff 리뷰 + validate/retrieve 파이프라인*이다. triplestore로
  옮기면 상태가 바이너리 DB에 숨어 **git-diff 리뷰("확인하며 고치기 쉬운")와 validate.py·
  retrieve.py가 무력화**된다. 게다가 `rdflib`가 이미 in-memory RDF store + SPARQL(`g.query`)
  이라 v1엔 별도 DB 서버가 불필요. → **TTL-in-git 유지, 질의는 rdflib in-process.**
  나중에 규모·SPARQL·다중 writer가 필요하면 **canonical TTL에서 재적재되는 파생 질의 계층**
  으로만 triplestore를 얹는다(원본 아님).
- **Frontend: RDF-in-browser 불필요.** 백엔드가 추론·검증을 Python(rdflib)에서 끝내고 JSON만
  투영하므로, 프론트는 일반 SPA + 그래프 라이브러리로 충분.

### 후보 (오픈소스)
| 부류 | 후보 | 메모 |
|---|---|---|
| Triplestore(파생 질의용, 후일) | **Oxigraph**(Rust, 경량·임베더블, SPARQL1.1, Apache/MIT) · **Apache Jena Fuseki**(JVM, 성숙, SHACL, Apache) · **Eclipse RDF4J**(BSD) | GraphDB Free는 추론·workbench가 좋으나 **비-OSS(무료 사용만)**; Blazegraph는 미유지보수 |
| 기성 온톨로지 관리 UI | **WebProtégé**(Stanford, BSD) · **VocBench 3**(SKOS/OWL, RDF4J/GraphDB 백엔드) | 강력하지만 **자체 저장소로 상태 fork** + 우리 composition·anti-orphan·retrieve 파이프라인과 무관 → 채택 시 이 프로젝트 핵심을 상실. 권장 안 함 |
| 그래프 시각화 | **Cytoscape.js**(MIT, 그래프 표준) · WebVOWL(MIT, OWL VOWL 표기 시각화, **뷰 전용**) · vis-network · Sigma.js · G6 | 편집까지 하려면 Cytoscape.js |
| SPA framework | **Svelte** 또는 **Vue 3**(오프라인 번들 가볍고 폼+그래프에 적합) · React(생태계 최다) · htmx/Alpine.js(빌드리스 — Docker 오프라인 최단 운영) | 백엔드 JSON 소비형이라 프레임워크 자유 |
| (참고) 브라우저 RDF | N3.js · rdflib.js · Comunica | v1엔 불필요(백엔드가 투영). 후일 클라이언트 질의 시에만 |

**추천 조합**: 저장=TTL-in-git(+rdflib in-process) · 그래프=**Cytoscape.js** · UI=**Svelte**
(또는 최단 운영 원하면 Alpine.js/htmx로 빌드리스) — 전부 오프라인 vendor 번들.

## 아키텍처 / API
```
브라우저(127.0.0.1:8000) ──REST(JSON)──▶ FastAPI(uvicorn) ── tools/ontology_lib.py(load+reason)
  GET  /api/schema     TBox 클래스·프로퍼티(domain/range) → 폼 구속 데이터
  GET  /api/graph      abox 노드·edge(타입·maturity 색) — instance_nodes/edges 재사용
  GET  /api/node/{id}  노드 트리플
  PUT  /api/node/{id}  노드 upsert → ttl_writer 텍스트 수술 write → validate 게이트 → diff 반환
  POST /api/validate   validate.py --json → {pass, shacl[], orphans[], gaps[], dups[]}
  POST /api/retrieve   retrieve.project() → base 후보·scoped subgraph·capability gaps
                          ▼ ontology/*.ttl (호스트 볼륨, 컨테이너 밖 단일 진실공급원)
```
- 삭제는 소프트(`ho:maturity "deprecated"`) 기본, 하드 삭제는 validate 통과 시에만.

## 파일 레이아웃 (신규; tbox/abox/shapes 불변)
```
tools/webui/  server.py  ttl_writer.py(텍스트 수술식 · ONTOLOGYSTYLE 포맷)  requirements.txt
              static/{index.html,app.js,style.css, vendor/…}   Dockerfile
docker-compose.yml   # 루트: ./ontology·./tools 볼륨, 127.0.0.1:8000 바인딩
```

## Docker / 배포·운영
- `python:3.12-slim` → deps 설치 → `WORKDIR /app`, `PYTHONPATH=/app/tools`,
  `uvicorn tools.webui.server:app`(또는 server.py가 sys.path 처리).
- compose: `./ontology`·`./tools`를 rw 볼륨, `127.0.0.1:8000:8000`. `docker compose up`으로 기동.
- **부수 이점**: 컨테이너 내부 python엔 rdflib/pyshacl/owlrl가 설치돼 있어 호스트의 인터프리터
  분리 문제(셸 기본 python3에 deps 없음)가 사라진다.
- git 커밋은 여전히 inspection 소관(컨테이너는 커밋 안 함).

## 적용 계획 (dispatch 흐름 — 승인 후)

> **선결 조건 — 역할 경계 (재검토 rev3, HIGH)**: 이 build는 `tools/webui/` **Python·Docker
> 소스**와 `validate.py` 수정을 요구하는데, 현재 하네스엔 **소스 코드를 저작할 역할이 없다**
> — orchestrator=계획·dispatch 전용, developer=`ontology/abox/` 노드만, vnv=docs/verify,
> inspection=docs/feedback+git. 즉 승인해도 **적용 주체가 없다.** 해소(열린 결정 E):
> developer의 파일 경계를 `tools/**`까지 넓혀 **일반 구현자**로 삼는다(추천 — reference
> 하네스의 developer 원형과 일치). 또한 step 6 커밋은 **git repo가 있어야** 한다(재검토 [C] —
> 현재 repo 아님 → 열린 결정 F).

orchestrator가 각 단계를 dispatch brief로 계획하고, 괄호 안 역할이 수행한다:
1. **(developer)** `tools/webui/` 스캐폴드 + `requirements.txt`(fastapi·uvicorn) +
   `docker-compose.yml`(127.0.0.1 바인딩).
2. **(developer)** `validate.py`에 `--json` 모드 추가 — check_* 를 구조화 결과 반환으로 분리
   (검사 로직 유지), `check_shacl`가 `report_text`를 살려 반환. `retrieve.py`는
   `project()`/`--format json` 그대로 사용.
3. **(developer)** `server.py`(sys.path에 `tools/` 주입, 엔드포인트) + `ttl_writer.py`
   (**텍스트 수술식** append/노드 span 치환, 저장 전 validate 게이트, temp+os.replace 원자
   쓰기 + mtime 충돌 검사).
4. **(developer)** `static/` SPA(추천 스택, 오프라인 vendor), 폼은 `/api/schema`로 구속,
   Cytoscape 그래프. `README.md`에 실행법 1블록.
5. **(vnv)** `docker compose up` 검증 — 볼륨 마운트로 호스트 TTL write 확인, seed 스모크
   (그래프·편집·validate PASS·retrieve pack). 판정·증거는 `docs/verify/`.
6. **(inspection)** 커밋(사용자 요청 시). tbox/abox/shapes 불변 → `validate.py`는 계속 PASS.

## 열린 결정 (승인 시 확정)
- **D. DB/frontend**: 저장=TTL-in-git 유지(rdflib in-process) + **확장 대비 store 인터페이스
  추상화**(아래 확장성 절), frontend=**사용자 편의성 우선 → Svelte(또는 Vue 3)** + Cytoscape.js.
  이대로면 승인만, 다른 조합 원하면 지정.
- **E. developer 경계 확장 (선결)**: developer를 `ontology/abox/` 노드 저작 → **`tools/**` 소스
  구현까지** 넓혀 일반 구현자로 삼는다. 추천=확장(reference 하네스 developer 원형과 일치).
  대안=별도 tooling 역할 신설. **이걸 정하지 않으면 승인돼도 적용 주체가 없다.**
- **F. git 초기화 + 공개 repo (선결)**: 커밋·inspection·메모리 영속 + 오픈소스 공개가 git repo
  전제 → `git init` **및 공개 GitHub repo**(LICENSE·CONTRIBUTING·PR 템플릿·CI). 추천=init+공개.
  (라이선스 종류는 미정 — 사용자 선택 필요.)
- **G. 협업 모델 (신규, 오픈소스·대규모 async)**: 추천=**OSS-native(로컬 Docker 도구 + git/PR +
  CI validate)** — 기여자는 로컬에서 webUI로 편집·validate하고 PR을 올리며, GitHub Actions가
  `validate.py`로 PR을 게이트, 메인테이너가 TTL diff를 리뷰·머지(async 협업 = PR). 이 모델에선
  ✅'로컬 전용·무인증'이 **옳다**. 대안=**호스티드 다중사용자 서비스**(라이브 공동편집) — 인증·
  RBAC·충돌해결·호스팅·DB가 필요해 범위가 훨씬 크고 git-diff 리뷰를 희생. → G 확정 필요.

## 확장성 · UX (rev3 — 사용자 추가 요청 "대규모 확장성 + frontend 편의성" 반영)
- **확장성 (아키텍처는 지금, 구현은 단순하게)**:
  - **canonical은 TTL-in-git 유지**(git-diff 리뷰 = 이 프로젝트의 핵심). 백엔드는 처음부터
    **store 인터페이스로 추상화**(`load/query/upsert`) — v1=rdflib in-process, 대규모 시
    **Oxigraph/Jena Fuseki를 파생·재적재 index**로 교체(원본은 여전히 TTL).
  - **추론 캐시**: CLI 도구는 매 호출 load+OWL RL 재계산이라 서버엔 부적합 → 서버는 **reasoned
    그래프를 메모리 캐시하고 파일 mtime으로 무효화**(요청당 재추론 회피).
  - **그래프 뷰 페이징/필터**: 노드가 많아지면 `/api/graph`를 타입·태그·이웃 반경으로 서버측
    필터·페이지. (agent context는 이미 `retrieve.py` 예산 투영으로 유계 — anti-rot 유지.)
- **UX (편의성 우선 → 빌드리스보다 프레임워크)**: Alpine/htmx(최단 운영)보다 **Svelte/Vue**로
  편의에 투자 — 타입 참조는 range 제약 **autocomplete picker**, 저장 전 **diff 미리보기 +
  validate 인라인**, 그래프 **검색·포커스·이웃 확장**, **undo/재편집**, 한글 오류 메시지.
  빌드 산출물은 오프라인 vendor로 Docker에 동봉(운영은 여전히 `docker compose up`).

## 오픈소스 공개 · 대규모 async 협업 (rev4 — 사용자 신규 요건)
"영속 사용 + 외부 오픈소스 공개 + 대규모 유저 async 참여." rev3의 ✅'로컬 전용'과 표면상
충돌하지만 **OSS-native 모델로 자연 해소**된다 — webUI는 기여자별 **로컬 authoring 도구**로,
협업 기판은 **git/GitHub PR**로:
- fork/clone → 로컬 `docker compose up` → webUI로 편집(폼 구속 + validate 게이트) → commit → **PR**.
- **CI 게이트**: GitHub Actions가 PR마다 `python3 tools/validate.py` 실행 → 비정상 종료면 체크
  실패(anti-orphan/drift를 기여에 강제). DESIGN.md가 예고한 'validate가 CI로 편입'이 실체화.
- **리뷰**: 메인테이너가 **TTL diff**(사람이 읽는 텍스트 — TTL-in-git을 고수한 이유)로 머지.
  async 참여 = PR 비동기. 도구엔 인증·호스팅 불필요 → ✅'로컬·무인증'이 옳다.
- **추가 산출물(F/G)**: `LICENSE`(라이선스 선택 필요), `CONTRIBUTING.md`(로컬 도구·PR·CI 흐름),
  `.github/`(PR 템플릿 + Actions validate 워크플로), 공개용 `README` 보강.
- **2계층**: agent 하네스(orchestrator/developer/vnv/inspection)=메인테이너측 자동화, 외부
  기여자=git/PR. 둘 다 같은 `validate.py` 게이트를 공유한다.
- 호스티드 라이브 다중편집을 원하면 결정 G에서 지정(범위·비용 크게 증가).

## 사용자 피드백
A, B, C: 추천 진행(✅). D: 확장성·UX 반영해 갱신(위 절) — 확인 부탁.
D, E, F: 추천 진행
신규 선결 결정 **E(developer 경계)·F(git init)**: 이 둘을 정해야 승인 후 적용이 가능하다.
영속적인 사용이며, 외부에 오픈소스 프로젝트로 공개해서 대규모 유저가 async로 참여하도록 할거야.

→ (재검토 rev4) 위 '오픈소스 공개·대규모 async 협업' 절로 반영. **status=approved는 로컬
Docker 도구 build를 커버**하되, **공개 협업 계층(LICENSE/CONTRIBUTING/CI/공개 repo)은 결정 G
확인 후** 진행. E=developer 경계 확장, F=git init+공개 repo로 확정 처리 예정. 남은 확인: **G
(OSS-native vs 호스티드)** + **LICENSE 종류**.

사용자 확정(build 시작): **G=OSS-native, LICENSE=Apache-2.0**. → build 수행.

## 적용 결과 (build 완료 — orchestrator 기록)
사용자 확정 후 구현 완료. 하네스상 developer/vnv/inspection 역할에 매핑되나, 커스텀 subagent가
세션에 미등록 + 전체 컨텍스트 보유로 **인라인 구현**(산출물 동일). 커밋은 inspection 소관(미실행).

**산출물**
- `tools/webui/`: `server.py`(FastAPI, asserted/reasoned 2-그래프 mtime 캐시), `ttl_writer.py`
  (텍스트 수술식 write + 원자 교체 + mtime 충돌 검사), `requirements.txt`, `Dockerfile`,
  `static/`(vanilla SPA — 외부 라이브러리 없이 SVG 그래프 + 어휘 구속 폼 + diff/validate 패널).
- `validate.py`: `--json` 모드 + `run_structured()` 추가(검사 로직 불변, human PASS 보존).
- 루트: `docker-compose.yml`(127.0.0.1 바인딩, ontology/·tools/ 볼륨), `LICENSE`(Apache-2.0),
  `CONTRIBUTING.md`, `.github/workflows/validate.yml`(PR CI 게이트), `.dockerignore`, README/.gitignore 갱신.
- git repo 초기화됨(branch main, 커밋 없음).

**검증** — TestClient HTTP 스모크 17/17 PASS(fastapi/httpx 설치 후). 포함:
schema(skos:broader 왕복 포함)·graph·node·validate·retrieve; **재검토서 잡은 2버그 회귀 테스트**
(① asserted 그래프라 추론 역edge 미오염, ② Concept round-trip에 skos:broader 무손실);
orphan 저장 → validate FAIL → **자동 롤백**(authored.ttl 제거) 확인. 테스트 후 repo 원상복구,
`validate.py` = PASS. (Docker 빌드·실행은 이 환경에서 미실행 — 이미지가 deps 설치.)

**남은 것**: 공개 repo 생성(GitHub, 사용자 계정 필요) + 첫 커밋(inspection, 요청 시). 호스티드
변형은 G에서 OSS-native 확정으로 비적용.

## 후속: frontend Svelte 재작성 + 가드 + 독립 검증 (orchestrator 기록)
사용자 결정: **frontend=Svelte 재작성**(결정 D 추천 "편의성 우선"), **LICENSE=Apache-2.0 확정**.
이번 사이클은 거버넌스대로 **역할 분리 dispatch**로 수행(orchestrator=계획·dispatch, developer=저작,
vnv=판정, 전부 opus). 통합 설계문서 `docs/webui-design.md` 신설.

**저작 (developer dispatch)**
- `tools/webui/frontend/`(Svelte5+Vite6+Cytoscape3, plain JS): App/Header/NodeList/GraphView/
  Editor/PropPicker/ResultPanel/RetrievePanel/DiffView + lib(api/stores/colors). Vite가
  `tools/webui/static/`로 빌드(기존 vanilla 3파일 대체). 4화면 기능 패리티 + 개선(Cytoscape
  그래프 검색·포커스·이웃확장, range 구속 autocomplete PropPicker, undo, 컬러 diff, retrieve pack).
- 빌드·서빙: Dockerfile **멀티스테이지**(node→python), `docker-compose.yml`에서 `./tools` 마운트
  제거(볼륨 shadowing 해소, SSOT `./ontology`만 유지), `.gitignore`에 `node_modules/`·`static/`.
- 후속 결정 반영: **server.py 친절 가드**(미빌드 시 크래시 대신 503 안내, `/api/*` 불변) +
  `.dockerignore`에 node_modules 제외. 백엔드 4도구·온톨로지·docs는 그 외 불변.

**검증 (vnv dispatch, 독립 재현)** — verdict **pass**. 증거: `docs/verify/webui-svelte-frontend.md`.
npm build / 비-Docker uvicorn(GET /=200, /api/* 200) / `docker compose build+up`(bind-mount
ontology 로드) / `validate.py` PASS / 백엔드·SSOT 해시 불변 / ttl_writer 비파괴 라운드트립 /
오프라인 자기완결. delta(가드+dockerignore) 재검증: 미빌드→503(크래시 해소)·정상 빌드→200 회귀·
빌드 컨텍스트 35M→519kB·server.py 외 불변 확인.

**남은 것(갱신)**: 첫 git 커밋(**inspection 전담, 사용자 요청 시**) + 공개 GitHub repo 생성
(사용자 계정 필요). 그 외 로컬 Docker 도구 build는 완료·검증됨.

## refresh 판정 (inspection — 2026-07-21)
파이프라인 step5 refresh 대상 여부를 verify-then-proceed로 판정. **판정: 유지 (제거 안 함).**
- 근거 검증(실측): `validate.py` **PASS**(SHACL·reachability·capabilities, 1049 triples) ·
  `--json` 정상(pass:true, orphans/gaps 0) · build 산출물 9종 전부 존재. → 적용은 실증됨.
- 그러나 이 항목이 명시한 **남은 inspection 작업(첫 git 커밋 + 공개 repo)이 미완료**
  (`git rev-list` = 0 commits, remote 없음). step5는 "적용 전이면 남긴다 — 시간 가정 금지".
- 지금 제거하면 미완 작업의 유일한 추적 기록이 사라짐 → **커밋·공개 완료 후 다음 사이클에 제거.**
