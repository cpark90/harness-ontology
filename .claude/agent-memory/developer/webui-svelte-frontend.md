# webui frontend: Svelte+Vite → static/ 빌드·서빙 아키텍처

`tools/webui/` web UI의 프론트를 vanilla JS→Svelte로 재작성할 때의 재사용 지식.
백엔드 API 계약(server.py)은 불변 — 소비만 한다.

## 핵심 제약: 볼륨 shadowing
- `server.py`는 `tools/webui/static/`를 `StaticFiles(html=True)`로 서빙(불변).
- 따라서 **vite `build.outDir = "../static"`** (frontend/ 기준), `base "/"` 유지
  → 자산이 `/assets/*`로 절대참조되고 StaticFiles가 서빙. `emptyOutDir: true`로
  이전 vanilla 3파일(index.html/app.js/style.css)까지 깨끗이 대체.
- **compose에서 `./tools:/app/tools` 마운트 제거**해야 함. 마운트하면 호스트의 (빌드 안 된)
  static이 이미지에 구운 산출물을 가려 빈 페이지가 됨. `./ontology`만 마운트(SSOT).
  ttl_writer/ontology_lib 경로는 ontology/ 기준이라 영속·검증 무영향.
- **Dockerfile 멀티스테이지**: stage1 `node:20-slim`에서 `npm ci && npm run build`(outDir가
  `/app/tools/webui/static`에 나오게 WORKDIR=`/app/tools/webui/frontend`), stage2 `python`이
  `COPY tools` 후 `rm -rf tools/webui/frontend`(node_modules·소스 제거) 하고
  `COPY --from=frontend .../static`로 산출물만 받음. 최종 이미지에 node 불필요.
- `.gitignore`: `node_modules/`, `tools/webui/static/`(빌드 산출물). lock파일은 커밋(npm ci용).

## Svelte 5 주의
- mount API: `import { mount } from "svelte"; mount(App, {target})` (구 `new App()` 아님).
- 클래식 문법(`export let`, `$:`, `on:click`, stores `$store`) 전부 동작.
- a11y 경고: 캡션용 `<label>`(control 미연결)은 `A form label must be associated…` 경고.
  캡션은 `<div class="cap">`로 바꾸고 CSS `form label, form .cap`로 스타일 공유하면 깔끔.
  클릭 div는 `role="button" tabindex="0"` + keydown, picker 옵션은 `role=listbox/option`.

## API 응답 형태 (소비 기준, server.py 신뢰원)
- `/api/schema` → `{classes[{id,label,super[]}], objectProperties[{id,label,range,domain}],
  datatypeProperties[]}`. objectProperties에 SKOS broader/narrower/related/topConceptOf 포함.
- `/api/graph` → `{nodes[{id,label,types[],maturity}], edges[{s,p,o}]}` (asserted only).
- `/api/node/{id}` → `{id,type,objectProps{pq:[qname]},dataProps{pq:[str]}}`.
- `PUT /api/node` body: id,type + `skos:prefLabel`(str),`skos:altLabel`([]),`skos:definition`,
  objprop:[id..], `ho:promptText`,`ho:tokenEstimate`(num),`ho:salience`(num),`ho:maturity`, `_mtimes`.
  응답 `{saved,validate,diff,file[,mtimes]}`. 저장 실패(FAIL)면 서버가 롤백+`saved:false`.
  409 Conflict = 파일이 read 이후 변경 → 재로드 유도.
- `POST /api/validate` → run_structured: `{pass,triples,shacl{ok,report},reachability{ok,
  orphans[{label,uri}]},capabilities{ok,gaps[{harness,missing[]}]},duplicates[{label,types[],members[]}]}`.
- `POST /api/retrieve {request,budget?}` → `{candidates[{label,relevance}],gaps[str],
  budget,budget_used,nodes[{id(fullURI),label,types[],relevance,...}],edges[]}`.
  retrieve의 node.id는 full URI(str) — `id:` qname으로 변환하려면 `https://harness-ontology.dev/id/` 접두 치환.

## 스모크 (Docker 없이도)
- `cd tools/webui/frontend && npm install && npm run build` → static/ 생성.
- `PYTHONPATH=tools uvicorn tools.webui.server:app` 후 `/`,`/assets/*`,`/api/*` 200 확인.
- Docker: `docker compose build` (멀티스테이지) → `up -d` → curl 스모크.
## 후속 결정 반영 (server 가드 + dockerignore)
- **static 부재 가드(server.py 마지막 mount)**: static/은 gitignore라 fresh clone에서 빈 채로
  `import server` 시 `StaticFiles(directory=...)`가 `RuntimeError` → import 크래시. 해소:
  `os.path.exists(static/index.html)`면 기존대로 `app.mount("/", StaticFiles(...,html=True))`,
  없으면 `@app.get("/")`로 `HTMLResponse(status_code=503)` 친절 안내(빌드 명령 포함) 반환.
  `/api/*`는 더 구체적 경로라 shadow 안 됨. `from fastapi.responses import HTMLResponse` 추가.
  정상(빌드됨) 경로 동작은 바이트 동일. 테스트: static 잠시 mv → import OK·GET/=503·/api=200.
- **`.dockerignore`에 node_modules 추가**: 이미 `.dockerignore` 존재(.git/__pycache__/ontology/
  docs/.github 등). `node_modules/`·`tools/webui/frontend/node_modules/`·`.../dist/` 추가하면
  빌드 컨텍스트 35M→~30kB. 멀티스테이지가 `npm ci`로 이미지 내부 설치하므로 host 전송 불필요.
