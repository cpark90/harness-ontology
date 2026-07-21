<script>
  // 저장(PUT /api/node) 및 validate(POST /api/validate) 결과 패널.
  // vanilla showResult()의 렌더링을 계승 — verdict / SHACL / orphan / capability
  // gap / duplicate + 컬러 diff 미리보기.
  import { result } from "../lib/stores.js";
  import DiffView from "./DiffView.svelte";

  $: r = $result;
  $: v = r && r.validate;
  // saved === null 이면 "validate 전체" 실행 결과(저장 아님)
  $: isValidateOnly = r && r.saved === null && !r.error;
</script>

{#if r}
  <div class="panel">
    {#if r.error}
      <div class="msg">{r.error}</div>
    {:else}
      {#if isValidateOnly}
        <h3>validate 결과</h3>
      {:else}
        <h3>{r.saved ? "저장됨" : "저장 실패 — 되돌림"}</h3>
      {/if}

      {#if v}
        <div class={v.pass ? "verdict-pass" : "verdict-fail"}>
          {v.pass ? "validate PASS" : "validate FAIL"}
          {#if v.triples}<span class="small"> · {v.triples} triples</span>{/if}
        </div>

        {#if v.shacl && !v.shacl.ok}
          <pre class="diff">{v.shacl.report}</pre>
        {/if}

        {#each (v.reachability && v.reachability.orphans) || [] as o}
          <div class="msg">orphan: {o.label}</div>
        {/each}

        {#each (v.capabilities && v.capabilities.gaps) || [] as g}
          <div class="msg">capability gap: {g.harness} → {g.missing.join(", ")}</div>
        {/each}

        {#each v.duplicates || [] as d}
          <div class="gap">중복 label: "{d.label}" [{d.types.join("/")}]</div>
        {/each}
      {/if}

      {#if r.diff}
        <DiffView diff={r.diff} />
      {/if}
    {/if}
  </div>
{/if}
