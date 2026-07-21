import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

// 빌드 산출물은 server.py가 StaticFiles(html=True)로 서빙하는 tools/webui/static/에 낸다.
// base "/" 유지 — 자산은 /assets/*로 절대참조되고 StaticFiles가 그대로 서빙한다.
// emptyOutDir로 이전 vanilla 산출물(index.html/app.js/style.css)까지 깨끗이 대체한다.
export default defineConfig({
  plugins: [svelte()],
  base: "/",
  build: {
    outDir: "../static",
    emptyOutDir: true,
  },
});
