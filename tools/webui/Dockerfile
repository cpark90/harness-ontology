# Ontology management web UI — self-contained image (multi-stage).
#
# stage 1 (node): Svelte 프론트엔드를 tools/webui/static/으로 빌드한다. npm은 이
#   빌드 시점에만 네트워크를 쓴다(Cytoscape 등은 번들에 포함 → 런타임 오프라인).
# stage 2 (python): 런타임. node 불필요. tools/*.py + 빌드된 static을 담아 uvicorn 서빙.
#
# 온톨로지 TTL은 호스트에 남아 런타임에 bind-mount된다(docker-compose.yml 참고).
# 컨테이너는 무상태이고 단일 진실공급원(SSOT)은 이미지 안에 들어가지 않는다.

# --- stage 1: frontend build ---
FROM node:20-slim AS frontend
WORKDIR /app/tools/webui/frontend
# 의존성 먼저(레이어 캐시). vite outDir가 ../static이라 산출물은 /app/tools/webui/static에 난다.
COPY tools/webui/frontend/package.json tools/webui/frontend/package-lock.json ./
RUN npm ci
COPY tools/webui/frontend/ ./
RUN npm run build

# --- stage 2: python runtime ---
FROM python:3.12-slim

WORKDIR /app

# Deps: ontology stack + web server. Copied first for layer caching.
COPY requirements.txt /app/requirements.txt
COPY tools/webui/requirements.txt /app/tools/webui/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
 && pip install --no-cache-dir -r /app/tools/webui/requirements.txt

# App code. ontology/ is NOT copied — it is bind-mounted at runtime.
COPY tools /app/tools
# 프론트 소스·node_modules는 런타임에 불필요 → 제거하고 빌드 산출물만 받아 이미지를 가볍게.
RUN rm -rf /app/tools/webui/frontend
COPY --from=frontend /app/tools/webui/static /app/tools/webui/static

# import ontology_lib / validate / retrieve (flat imports) resolve from here.
ENV PYTHONPATH=/app/tools
EXPOSE 8000

CMD ["uvicorn", "tools.webui.server:app", "--host", "0.0.0.0", "--port", "8000"]
