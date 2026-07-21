<script>
  // context pack(POST /api/retrieve) 결과: base-harness 후보 / capability gaps /
  // 예산 사용량 + 스코프 노드. 노드 클릭 → 그래프 포커스 + 편집기 로드.
  import { retrievePack, openNode } from "../lib/stores.js";

  const ID_NS = "https://harness-ontology.dev/id/core/";
  const toQname = (uri) => (uri && uri.startsWith(ID_NS) ? "id:" + uri.slice(ID_NS.length) : uri);

  $: pack = $retrievePack;
</script>

{#if pack}
  <div class="panel">
    <h3>context pack · {pack.budget_used}/{pack.budget} tokens · {pack.nodes.length} nodes</h3>

    {#if pack.candidates && pack.candidates.length}
      <div class="small">base-harness 후보</div>
      {#each pack.candidates as c}
        <div class="cand"><span>{c.label}</span><span class="small">rel {c.relevance}</span></div>
      {/each}
    {/if}

    <div class="small" style="margin-top:6px">capability gaps</div>
    {#if pack.gaps && pack.gaps.length}
      {#each pack.gaps as g}
        <div class="gap">⚠ {g}</div>
      {/each}
    {:else}
      <div class="small">none</div>
    {/if}

    {#if pack.nodes && pack.nodes.length}
      <div class="small" style="margin-top:6px">스코프 노드 (클릭 → 편집)</div>
      {#each pack.nodes as n (n.id)}
        <div
          class="pack-node"
          on:click={() => openNode(toQname(n.id))}
          on:keydown={(e) => e.key === "Enter" && openNode(toQname(n.id))}
          role="button"
          tabindex="0"
        >
          {n.label}
          <span class="small"> · {(n.types || []).join("/")} · rel {n.relevance}</span>
        </div>
      {/each}
    {/if}
  </div>
{/if}
