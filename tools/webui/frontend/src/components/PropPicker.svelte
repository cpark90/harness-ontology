<script>
  // 한 object property의 값(id 참조 배열)을 range 타입으로 구속되는 autocomplete로 편집.
  // vanilla의 datalist를 대체 — chip 표시 + 필터 드롭다운 + 키보드 탐색.
  import { graph } from "../lib/stores.js";

  export let prop; // {id, label, range, domain}
  export let value = []; // 현재 선택된 id 참조(qname "id:...") 배열
  export let onChange = () => {};

  let query = "";
  let open = false;
  let hi = 0; // 하이라이트된 옵션 인덱스

  $: rangeShort = (prop.range || "").split(":").pop();

  // range 타입에 맞는 후보만(범위 없으면 전체). 이미 선택된 것·질의어로 추가 필터.
  $: candidates = $graph.nodes
    .filter((n) => !rangeShort || (n.types || []).includes(rangeShort))
    .filter((n) => !value.includes(n.id))
    .filter((n) => {
      const q = query.trim().toLowerCase();
      if (!q) return true;
      return n.label.toLowerCase().includes(q) || n.id.toLowerCase().includes(q);
    })
    .slice(0, 40);

  function labelFor(id) {
    const n = $graph.nodes.find((x) => x.id === id);
    return n ? n.label : id;
  }

  function add(id) {
    if (!id || value.includes(id)) return;
    value = [...value, id];
    onChange(value);
    query = "";
    hi = 0;
    open = false;
  }

  function remove(id) {
    value = value.filter((x) => x !== id);
    onChange(value);
  }

  function onKey(e) {
    if (e.key === "ArrowDown") { open = true; hi = Math.min(hi + 1, candidates.length - 1); e.preventDefault(); }
    else if (e.key === "ArrowUp") { hi = Math.max(hi - 1, 0); e.preventDefault(); }
    else if (e.key === "Enter") {
      e.preventDefault();
      if (candidates[hi]) add(candidates[hi].id);
    } else if (e.key === "Escape") { open = false; }
  }
</script>

<div class="prop-row">
  <div class="plabel">
    {prop.label} — {prop.id}{#if prop.range}<span class="rng"> → {prop.range}</span>{/if}
  </div>

  {#if value.length}
    <div class="chips">
      {#each value as id (id)}
        <span class="chip">{labelFor(id)}<button type="button" title="제거" on:click={() => remove(id)}>×</button></span>
      {/each}
    </div>
  {/if}

  <div class="picker">
    <input
      type="text"
      placeholder={rangeShort ? `${rangeShort} 검색·선택…` : "노드 검색·선택…"}
      bind:value={query}
      on:focus={() => (open = true)}
      on:input={() => { open = true; hi = 0; }}
      on:blur={() => setTimeout(() => (open = false), 150)}
      on:keydown={onKey}
    />
    {#if open}
      <div class="dropdown" role="listbox">
        {#if candidates.length}
          {#each candidates as c, i (c.id)}
            <div
              class="opt"
              class:hi={i === hi}
              role="option"
              aria-selected={i === hi}
              tabindex="-1"
              on:mousedown|preventDefault={() => add(c.id)}
            >
              <span>{c.label}</span><span class="oid">{c.id}</span>
            </div>
          {/each}
        {:else}
          <div class="empty">후보 없음{rangeShort ? ` (range: ${rangeShort})` : ""}</div>
        {/if}
      </div>
    {/if}
  </div>
</div>
