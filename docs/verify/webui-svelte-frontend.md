# vnv 판정 — web UI Svelte/Vite frontend 재작성

- 대상: developer가 재작성한 `tools/webui/frontend/` (Svelte5 + Vite6 + Cytoscape3, plain JS),
  Vite→`tools/webui/static/` 빌드, Dockerfile 멀티스테이지, compose `./tools` 마운트 제거.
- 신뢰원: `docs/webui-design.md` §4(API 계약)·§9(빌드/mount 아키텍처).
- 판정자: vnv (판정 전용, 온톨로지·코드 미편집). 실행 env: 셸 기본 `python3`엔 rdflib 없음 →
  **`/usr/bin/python3`** 사용(rdflib/pyshacl/owlrl/uvicorn/fastapi 보유 확인). node v22.22 / npm 10.9 /
  docker 29.6 / compose v5.3.
- 일시: 2026-07-21 (초판 needs-decision) → **2026-07-21 delta 재검증 후 pass 승격**.

## Verdict: **pass** (2차, 그대로 커밋 가능)

초판(아래 §초판)은 **모든 기능 게이트 PASS**였고 미결은 정책성 A/B 두 항목뿐이었다. developer가
A(마운트 가드)·B(dockerignore)를 코드로 해소했고, **그 delta를 독립 재검증한 결과 전부 PASS** →
verdict를 **needs-decision → pass**로 승격한다. 코드 재작업(developer 재분배) 불필요.

---

## Delta 재검증 (2026-07-21, A/B 해소분 한정)

### 바뀐 것 (승인된 변경, 직접 대조)
- `tools/webui/server.py` (해시 `74201bd…` → **`7cb1aff…`**, 예상된 변화): static mount에 가드.
  `from fastapi.responses import HTMLResponse` 추가(줄 33). 말미가 `if os.path.exists(_STATIC/
  index.html): app.mount(StaticFiles(html=True))` **else** `@app.get("/")`가
  `HTMLResponse(_UNBUILT_HTML, status_code=503)`(줄 247). `/api/*`·캐시·쓰기 로직은 무수정(코드 확인).
- `.dockerignore`: `node_modules/`·`tools/webui/frontend/node_modules/`·`tools/webui/frontend/dist/`
  제외 3줄 추가.
- **그 외 무변**: `docs/webui-design.md` mtime 14:18 < delta 편집(server.py/.dockerignore) 14:46 →
  문서 미수정. 백엔드 4도구·`ontology/**`도 불변(§D4).

### D1. 미빌드 경로 — PASS
- `static/`을 치운 뒤 `PYTHONPATH=tools /usr/bin/python3 -c "import tools.webui.server"` → **`IMPORT OK`**
  (초판의 `RuntimeError: Directory ... does not exist` 크래시 **해소**).
- uvicorn(port 8138) 기동 후 `GET /` → **503** `text/html` 934B, 본문에 **`npm install &amp;&amp;
  npm run build`** + `docker compose` 안내 포함. `GET /api/schema` → **200**, `GET /api/graph` →
  **200** (가드가 API 라우트를 막지 않음). 이후 `static/` 원복.

### D2. 정상 경로 회귀 — PASS
- `npm run build`(vite ✓ built) 후 uvicorn(port 8139): `GET /` → **200** `text/html` 406B, 본문에
  `id="app"` + `/assets/index-*.js|css` 참조(정상 SPA 복귀 — 가드가 빌드된 동작을 바꾸지 않음).
  `GET /assets/*.js` → 200, `GET /api/graph` → 200.

### D3. dockerignore(빌드 컨텍스트 축소) — PASS
- `docker compose build`: `#8 [internal] load build context … transferring context: **519.40kB**`
  (초판 실효 컨텍스트 **~36M**에서 급감 → host `node_modules` 35M **미전송** 확인). build exit 0.
- 정리: `docker image rm`으로 이미지 제거, 잔여 컨테이너 없음.

### D4. 무영향 — PASS
- `/usr/bin/python3 tools/validate.py` → **PASS** 유지.
- **server.py 외** 백엔드 4도구 해시 불변(`validate.py 7729b56…`, `retrieve.py 80523ad…`,
  `ontology_lib.py ae42c74…`, `ttl_writer.py 934b8d7…`), `ontology/**` 집계 **`bd14b132…`**(초판과 동일).
  server.py(`7cb1aff…`) 변경은 이번에 승인된 것이므로 예상된 유일한 백엔드 변화.

---

## §초판 판정 (needs-decision) — 이력 보존

> 아래는 2026-07-21 초판. 미결 A/B가 위 delta로 해소되어 **pass로 대체**됨(§A/§B는 이제 무효,
> 해소 증거는 §D1·§D3 참조). 기능 게이트 증거(§1~6·패리티)는 그대로 유효하다.

구현 자체는 **모든 기능 게이트 PASS**(빌드·비-Docker 스모크·Docker 스모크·백엔드 무영향·
ttl_writer 라운드트립·오프라인 자기완결 전부 green). 다만 orchestrator가 넘긴 **A(정책 리스크)**
가 **실제 재현**되어 결정이 필요하고, **B(빌드 위생)** 는 한 줄 수정거리다. A/B만 정리하면
곧바로 `pass`(그대로 커밋 가능)로 승격 가능 — 코드 재작업(developer 재분배)은 불필요.

---

## 항목별 증거

### 1. 프론트 빌드 — PASS
- 명령: `cd tools/webui/frontend && npm install && npm run build` (사전에 `static/` 삭제해 재생성 증명).
- `npm install`: `added 1 package, audited 42 packages`, `0 vulnerabilities`.
- `npm run build` (vite v6.4.3): `✓ 122 modules transformed`, `✓ built in ~1.9s`, exit 0.
- 산출: `tools/webui/static/index.html`(406B) + `assets/index-CAwsU6ec.css`(4.68kB) +
  `assets/index-TiWH0uSp.js`(511.74kB, gzip 168kB). **해시 파일명이 삭제 전과 동일 → 재현 가능**.
- 경고 1건(비-에러): `Some chunks are larger than 500 kB`(Cytoscape 번들 포함 때문 — 오프라인
  요건의 필연적 결과). 코드 스플릿 미적용은 로컬 authoring 도구엔 무해.

### 2. 서버 기동 스모크 (비-Docker) — PASS
- 명령: `PYTHONPATH=tools /usr/bin/python3 -m uvicorn tools.webui.server:app --host 127.0.0.1 --port 8137`.
- `GET /` → **200** `text/html` 406B (빌드된 SPA, `/assets/*` 절대참조).
- `GET /assets/index-TiWH0uSp.js` → **200** `text/javascript` 511739B.
- `GET /assets/index-CAwsU6ec.css` → **200** `text/css` 4681B.
- `GET /api/schema` → **200** (classes 15, objectProperties 24, datatypeProperties 4).
- `GET /api/graph` → **200** (nodes 41, edges 62).
- 추가 라우트: `GET /api/node/id:cap-codeexec`=200, `POST /api/validate`=200(**pass=true**),
  `POST /api/retrieve`=200(pack keys: request/terms/seeds/nodes/edges/candidates/gaps/budget),
  `GET /nonexistent-page`=404. uvicorn 로그에 error/warn/traceback **없음**.

### 3. Docker 스모크 — PASS
- `docker compose build`: 멀티스테이지 성공(stage1 node 빌드 → `✓ built`, stage2 python), exit 0.
- `docker compose up -d` 후 (`127.0.0.1:8000`): `GET /`=**200**, `GET /assets/*.js`=**200**(511739B),
  `GET /api/graph`=**200**(nodes 41/edges 62 — **bind-mount된 `./ontology`에서 로드**, 호스트와 동일),
  `POST /api/validate`=**200 pass=true**.
- 최종 이미지 **320MB**, 컨테이너 내 `/app/tools/webui/frontend` **부재**(`rm -rf frontend` 적용됨),
  `static/`만 존재 → 이미지 자기완결 확인.
- `docker compose down`으로 컨테이너·네트워크 정리, 빌드 이미지도 `docker image rm`로 제거(환경 원복).
- 참고: **ontology write bind-mount(호스트 TTL 영속)** 는 SSOT 변경을 피하려 실측하지 않음.
  read 방향 마운트(그래프 로드)는 위에서 확인. 쓰기 경로는 §5·ttl_writer 코드리뷰로 갈음(항목 5).

### 4. 백엔드 무영향 — PASS
- `git diff --stat`은 무의미(repo에 커밋 없음, 전부 `??` untracked) → **sha256 스냅샷 전/후 대조**로 판정.
- 백엔드 5도구 해시 **불변**(테스트 전=후 동일):
  `tools/validate.py 7729b56…`, `tools/retrieve.py 80523ad…`, `tools/ontology_lib.py ae42c74…`,
  `tools/webui/server.py 74201bd…`, `tools/webui/ttl_writer.py 934b8d7…`.
  (주: 초판 시점 값. server.py는 이후 delta에서 승인 하에 `7cb1aff…`로 바뀜 — §Delta 참조.)
- `ontology/**` 집계해시 `bd14b13…`, `docs/**` 집계해시 `f7c53af…` — 둘 다 **전/후 불변**.
- `/usr/bin/python3 tools/validate.py` → `✓ SHACL / ✓ reachability / ✓ capabilities` → **PASS**.
  `--json` → `pass=true` (keys: pass/triples/shacl/reachability/capabilities/duplicates).

### 5. ttl_writer 라운드트립 (비파괴) — PASS
- `plan_upsert`를 **dry 호출만**(`atomic_write` 미호출), `ontology/abox`는 미변경.
- `render_block`: 입력 dict 키 순서가 뒤섞여도 출력이 `ORDER` 기준 **단조 비감소**(monotonic 확인).
  문자열 프레디킷은 quote, `id:` 참조는 unquote, `ho:tokenEstimate`는 int. `a ho:Harness` 선두.
- `plan_upsert` NEW → `authored.ttl` `created=True`(헤더+블록 계획). REPLACE(`id:dom-coding`, seed.ttl)
  → 해당 subject **span만** 치환(diff +3/-1), 다른 블록 불변.
- 검증: dry 호출 전후 `ontology/abox/*.ttl` 집계해시 **동일 → ABOX UNCHANGED**. 실파일 변경 없음.

### 6. 오프라인 / 자기완결 — PASS
- 빌드된 `static/`의 http(s) 문자열 24건은 전부 **런타임 fetch 아님**: MIT/jQuery 라이선스 텍스트,
  `svelte.dev/e/*`(에러 발생 시에만 안내되는 문서 URL), `harness-ontology.dev/id/`(온톨로지 IRI 상수).
  외부 CDN `<script>`/CSS `@import`/remote asset **없음**. `index.html`은 로컬 `/assets/*`만 참조.
- Cytoscape **번들 포함**(js 내 매칭 + 511kB 번들 크기). `docker compose up` 운영은 오프라인 성립.

### 기능 패리티 (코드리뷰 범위 — 런타임 클릭 미수행)
브라우저 상호작용은 미실행, **코드 수준**으로만 §4 계약 소비를 확인:
- `App.svelte`→`/api/schema`로 폼 구속. `Header.svelte`→`/api/retrieve`·`/api/validate`.
- `Editor.svelte`→`PUT /api/node`, 클래스는 `$schema.classes` **드롭다운**(free-text 클래스 불가 =
  drift 가드 유지), objectProperties는 schema 기반 picker, 저장 실패 시 `"저장 안 됨 · validate FAIL
  (되돌림)"` 상태 표기(롤백 UX). `ResultPanel`/`DiffView`(색상 unified diff)/`RetrievePanel`(base
  후보·capability gaps)/`GraphView`+`colors.js`(cytoscape). v1 4화면 + API 6엔드포인트 커버 확인.
- UI 산문은 한글·용어는 영어 — 언어정책(`gr-lang`, ONTOLOGYSTYLE §1d) 부합. 프론트 코드는 온톨로지
  TTL이 아니므로 ONTOLOGYSTYLE [지킴]은 대체로 무관, 위반 없음.

---

## orchestrator 결정 필요 (developer가 넘긴 A/B) — ✅ delta에서 해소됨

> 초판의 미결. 아래 A/B는 §Delta(D1·D3)에서 코드로 해소·재검증 완료 → 더는 결정 대기 항목 아님.
> 이력·재현 절차 참고용으로 보존.

### A. `static/` gitignore → fresh clone에서 uvicorn 기동 불가 — **재현됨 (실제 리스크)** → ✅ 해소(D1)
- 재현: `static/`을 치우고 `PYTHONPATH=tools /usr/bin/python3 -c "import tools.webui.server"` →
  **`RuntimeError: Directory '.../tools/webui/static' does not exist`** (server.py:222
  `StaticFiles(directory=...)` 생성 시점). 즉 **모듈 import 단계에서 크래시 → uvicorn이 아예 안 뜬다.**
- 영향: fresh clone 후 **비-Docker** 로컬 실행 시 `npm run build`(또는 Docker 빌드)를 **먼저** 하지
  않으면 원인 불명확한 raw RuntimeError로 실패. Docker 경로는 이미지가 static을 굽기 때문에 무관.
- **해소**: developer가 옵션 (b)를 택함 — static 부재 시 `@app.get("/")`가 503 친절 안내 반환,
  import 크래시 제거. §D1에서 재검증 PASS.

### B. `.dockerignore`에 `node_modules` 미포함 → 빌드 컨텍스트/레이어 부풀림 — **관측됨 (경미)** → ✅ 해소(D3)
- 사실: `.dockerignore`가 `node_modules/`·`tools/webui/frontend/node_modules/`를 제외하지 않아
  `tools/webui/frontend/node_modules`(**35M**)가 실효 빌드 컨텍스트(~36M)에 실렸었다.
- **해소**: `.dockerignore`에 해당 3줄 추가 → 컨텍스트 전송 **519.40kB**로 급감(§D3 재검증 PASS).

---

## 재현에 쓴 인터프리터/명령 요약
- deps 있는 인터프리터: `/usr/bin/python3` (셸 기본 `python3`은 `ModuleNotFoundError: rdflib`).
- 빌드: `cd tools/webui/frontend && npm install && npm run build`.
- 서버: `PYTHONPATH=tools /usr/bin/python3 -m uvicorn tools.webui.server:app --host 127.0.0.1 --port <p>`.
- 미빌드 재현: `mv static …; import tools.webui.server; GET /`(503) · `GET /api/schema`(200); static 원복.
- validate: `/usr/bin/python3 tools/validate.py [--json]` → PASS.
- docker: `docker compose build`(context 519kB) / `up -d` / `down` / `image rm`.
- 무결성: `sha256sum`으로 백엔드 도구·`ontology/**`·`docs/**` 전/후 대조(server.py만 승인된 변화).
