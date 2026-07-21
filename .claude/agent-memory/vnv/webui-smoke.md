# webui (tools/webui) 검증 재현 절차

Svelte/Vite frontend + FastAPI backend web UI 스모크·판정 노하우.

## 실행 env
- 셸 기본 `python3`엔 rdflib **없음** → **`/usr/bin/python3`** 사용(rdflib/pyshacl/owlrl/uvicorn/fastapi 보유).
- node/npm/docker 존재. docker daemon 도달 가능(`docker info`).

## 재현 명령
- 프론트 빌드(재현성 증명 위해 `static/` 먼저 rm): `cd tools/webui/frontend && npm install && npm run build`
  → `../static/{index.html,assets/*}` 생성. 해시 파일명 동일 = 재현 가능. 경고 `chunk >500kB`는
  Cytoscape 번들 때문(정상, 오프라인 요건의 결과).
- 비-Docker 서버: `PYTHONPATH=tools /usr/bin/python3 -m uvicorn tools.webui.server:app --host 127.0.0.1 --port <p>`.
  엔드포인트: `/`(html), `/assets/*`, `/api/schema`, `/api/graph`, `/api/node/{id}`, `POST /api/validate`,
  `POST /api/retrieve`. graph는 41 nodes/62 edges(현 abox 기준).
- Docker: `docker compose build && docker compose up -d`(127.0.0.1:8000) → 스모크 → `docker compose down`
  + `docker image rm harness_ontology-webui:latest`로 원복. 최종 이미지 320MB, 컨테이너 내 `frontend/`
  는 `rm -rf`로 제거됨(static만).

## 판정 함정 / 요령
- **repo에 커밋 없음(전부 `??`)** → `git diff --stat` 무의미. 백엔드 무영향은 **sha256 스냅샷 전/후 대조**로.
  대상: `tools/{validate,retrieve,ontology_lib}.py`, `tools/webui/{server,ttl_writer}.py`, `ontology/**` 집계.
  기준 해시(변하면 조사): validate `7729b56`, retrieve `80523ad`, ontology_lib `ae42c74`,
  ttl_writer `934b8d7`, ontology/** 집계 `bd14b132`. server.py는 가드 추가 후 `74201bd`→`7cb1aff`.
- **docs 집계해시 비교 시** 내가 쓴 `docs/verify/*.md`가 포함돼 값이 바뀐다 — `-not -path '*/verify/*'`로
  제외하거나 mtime으로 실제 변경 파일 식별. ontology 집계(`bd14b132`)가 진짜 무영향 지표.
- **ttl_writer 비파괴 라운드트립**: `plan_upsert`만 dry 호출(`atomic_write` 금지). `render_block`은
  입력 키 순서 무관하게 `ORDER`(ttl_writer.py:25) 단조 비감소. abox 집계해시 전후 동일 확인으로 미변경 입증.
- **오프라인 판정**: `static/`에 http(s) 문자열 있어도 대부분 라이선스/`svelte.dev/e/*` 에러문서/온톨로지 IRI
  상수 = 런타임 fetch 아님. index.html이 로컬 `/assets/*`만 참조하고 CDN `<script>` 없으면 self-contained.
- **delta만 재검증**할 땐 바뀐 파일 해시 대조 + 미빌드/정상 두 경로 스모크 + build context 크기만 보면 됨.

## 이력: static-missing 가드 + dockerignore (해소 완료)
- A: 초판엔 `static/` 부재 시 `import tools.webui.server`가 `RuntimeError: Directory '.../static' does
  not exist`(server.py StaticFiles 생성)로 크래시 → 비-Docker uvicorn 안 뜸. → developer가 가드 추가:
  `if exists(static/index.html): mount(StaticFiles)` else `@app.get("/")` → `HTMLResponse(503, npm run
  build 안내)`. 재검증: 미빌드 시 import OK / `GET /`=503(안내 포함) / `/api/*`=200, 빌드 시 `GET /`=200 복귀.
- B: `.dockerignore`에 `node_modules/`·`frontend/node_modules/`·`frontend/dist/` 추가 → 빌드 컨텍스트
  ~36M → **519kB**로 급감(`transferring context:` 라인으로 측정). 미빌드/정상 경로 모두 회귀 없음.

판정 리포트: `docs/verify/webui-svelte-frontend.md` (초판 needs-decision → delta 재검증 후 **pass**).
