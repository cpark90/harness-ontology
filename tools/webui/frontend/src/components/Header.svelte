<script>
  import { postJSON } from "../lib/api.js";
  import { retrievePack, result, status, setStatus } from "../lib/stores.js";

  let q = "";
  let busy = false;

  async function runRetrieve() {
    if (!q.trim()) return;
    busy = true;
    setStatus("retrieve 중…");
    try {
      const pack = await postJSON("/api/retrieve", { request: q });
      retrievePack.set(pack);
      setStatus(`retrieve 완료 · ${pack.nodes.length} nodes`, "ok");
    } catch (e) {
      setStatus(e.message, "bad");
    } finally {
      busy = false;
    }
  }

  async function runValidate() {
    busy = true;
    setStatus("validate 중…");
    try {
      const v = await postJSON("/api/validate", {});
      result.set({ saved: null, validate: v });
      setStatus(v.pass ? "validate PASS" : "validate FAIL", v.pass ? "ok" : "bad");
    } catch (e) {
      setStatus(e.message, "bad");
    } finally {
      busy = false;
    }
  }
</script>

<header>
  <h1>Harness Ontology Manager</h1>
  <div class="tools">
    <input
      id="retrieve-q"
      type="text"
      placeholder="요청으로 검색 → context pack (retrieve)"
      bind:value={q}
      on:keydown={(e) => e.key === "Enter" && runRetrieve()}
    />
    <button on:click={runRetrieve} disabled={busy}>검색</button>
    <button on:click={runValidate} disabled={busy}>validate 전체</button>
    <span class="status {$status.cls}">{$status.msg}</span>
  </div>
</header>
