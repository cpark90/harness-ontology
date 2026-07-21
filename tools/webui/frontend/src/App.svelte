<script>
  import { onMount } from "svelte";
  import { getJSON } from "./lib/api.js";
  import { schema, graph, setStatus } from "./lib/stores.js";
  import Header from "./components/Header.svelte";
  import NodeList from "./components/NodeList.svelte";
  import GraphView from "./components/GraphView.svelte";
  import Editor from "./components/Editor.svelte";

  let ready = false;

  onMount(async () => {
    try {
      schema.set(await getJSON("/api/schema"));
      graph.set(await getJSON("/api/graph"));
      ready = true;
      setStatus("준비됨", "ok");
    } catch (e) {
      setStatus("초기화 실패: " + e.message, "bad");
    }
  });
</script>

<Header />
<main>
  <section class="pane" id="left"><NodeList /></section>
  <section class="pane" id="center"><GraphView /></section>
  <section class="pane" id="right">
    {#if ready}
      <Editor />
    {:else}
      <div class="pane-head"><h2>편집기</h2></div>
      <p class="small">스키마 로딩 중…</p>
    {/if}
  </section>
</main>
