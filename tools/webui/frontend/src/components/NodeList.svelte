<script>
  import { graph, editTarget, openNode, newNode } from "../lib/stores.js";
  import { typeColor } from "../lib/colors.js";

  // 타입별 그룹핑(첫 타입 기준). vanilla renderList()와 동형.
  $: groups = (() => {
    const g = {};
    for (const n of $graph.nodes) (g[(n.types && n.types[0]) || "Thing"] ||= []).push(n);
    return g;
  })();
  $: typeNames = Object.keys(groups).sort();
  $: activeId = $editTarget.id;
</script>

<div class="pane-head">
  <h2>노드</h2>
  <button on:click={newNode} title="새 노드">＋ 새 노드</button>
</div>

<div class="editor-scroll" style="flex:1">
  {#each typeNames as type}
    <div class="type-group">
      <div class="type-name">
        <span class="swatch" style="background:{typeColor(type)}"></span>{type}
      </div>
      {#each groups[type] as n (n.id)}
        <div
          class="node-item"
          class:active={n.id === activeId}
          on:click={() => openNode(n.id)}
          on:keydown={(e) => e.key === "Enter" && openNode(n.id)}
          role="button"
          tabindex="0"
        >
          <span>{n.label}</span>
          <span class="mat">{n.maturity || ""}</span>
        </div>
      {/each}
    </div>
  {/each}
</div>
