<script>
  import { onMount, onDestroy } from "svelte";
  import cytoscape from "cytoscape";
  import { graph, editTarget, openNode } from "../lib/stores.js";
  import { typeColor, typeShape } from "../lib/colors.js";
  import RetrievePanel from "./RetrievePanel.svelte";

  let container;
  let cy = null;
  let search = "";
  let lastGraph = null;

  function elements(g) {
    const ids = new Set(g.nodes.map((n) => n.id));
    const els = [];
    for (const n of g.nodes) {
      const t = (n.types && n.types[0]) || "Thing";
      els.push({ data: { id: n.id, label: n.label, type: t, maturity: n.maturity || "" } });
    }
    for (const e of g.edges) {
      if (!ids.has(e.s) || !ids.has(e.o)) continue; // asserted-only; skip dangling
      els.push({ data: { id: `${e.s}|${e.p}|${e.o}`, source: e.s, target: e.o, label: e.p } });
    }
    return els;
  }

  const STYLE = [
    { selector: "node", style: {
        "background-color": (ele) => typeColor(ele.data("type")),
        shape: (ele) => typeShape(ele.data("type")),
        label: "data(label)",
        "font-size": 8, color: "#1c2430",
        "text-valign": "bottom", "text-halign": "center", "text-margin-y": 2,
        width: 18, height: 18, "border-width": 1, "border-color": "#fff" } },
    { selector: "edge", style: {
        width: 1, "line-color": "#cbd2dc",
        "target-arrow-color": "#cbd2dc", "target-arrow-shape": "triangle",
        "curve-style": "bezier", "arrow-scale": 0.7,
        label: "data(label)", "font-size": 6, color: "#9aa3b2",
        "text-rotation": "autorotate" } },
    { selector: ".faded", style: { opacity: 0.12 } },
    { selector: "edge.faded", style: { opacity: 0.05 } },
    { selector: "node.hit", style: { "border-color": "#2f6fed", "border-width": 3 } },
    { selector: "node:selected", style: { "border-color": "#2f6fed", "border-width": 3 } },
  ];

  function build(g) {
    if (cy) cy.destroy();
    cy = cytoscape({
      container,
      elements: elements(g),
      style: STYLE,
      layout: { name: "cose", animate: false, padding: 24, nodeRepulsion: 7000, idealEdgeLength: 70 },
      wheelSensitivity: 0.25,
    });
    cy.on("tap", "node", (evt) => openNode(evt.target.id()));
    // 배경 탭 → 강조 해제
    cy.on("tap", (evt) => { if (evt.target === cy) clearHighlight(); });
  }

  function clearHighlight() {
    if (cy) cy.elements().removeClass("faded hit");
  }

  function focus(id) {
    if (!cy || !id) return;
    const node = cy.getElementById(id);
    if (node.empty()) return;
    const hood = node.closedNeighborhood();
    cy.elements().addClass("faded");
    hood.removeClass("faded");
    node.addClass("hit");
    cy.animate({ center: { eles: node }, zoom: Math.max(cy.zoom(), 1.2) }, { duration: 250 });
  }

  function runSearch() {
    if (!cy) return;
    const q = search.trim().toLowerCase();
    clearHighlight();
    if (!q) return;
    const hits = cy.nodes().filter((n) => (n.data("label") || "").toLowerCase().includes(q));
    if (hits.empty()) return;
    cy.elements().addClass("faded");
    hits.removeClass("faded").addClass("hit");
    hits.neighborhood().removeClass("faded");
    cy.animate({ fit: { eles: hits, padding: 50 }, duration: 250 });
  }

  // 이웃 확장: 현재 보이는(비-faded) 노드의 한 링 이웃을 추가로 드러낸다.
  function expandNeighbors() {
    if (!cy) return;
    const shown = cy.nodes().not(".faded");
    if (shown.empty() || shown.length === cy.nodes().length) return;
    const ring = shown.neighborhood();
    ring.removeClass("faded");
    shown.edgesWith(ring.nodes()).removeClass("faded");
  }

  function resetView() {
    if (!cy) return;
    clearHighlight();
    cy.animate({ fit: { padding: 24 }, duration: 250 });
  }

  function onResize() { if (cy) cy.resize(); }

  onMount(() => {
    // graph store 변화 시 재빌드(초기 boot + 저장 후 refreshGraph).
    const unsubG = graph.subscribe((g) => {
      if (!container || !g) return;
      if (g === lastGraph) return;
      lastGraph = g;
      build(g);
    });
    const unsubT = editTarget.subscribe((t) => focus(t && t.id));
    window.addEventListener("resize", onResize);
    return () => { unsubG(); unsubT(); window.removeEventListener("resize", onResize); };
  });

  onDestroy(() => { if (cy) cy.destroy(); });
</script>

<div class="pane-head">
  <h2>그래프</h2>
  <span class="hint">노드 클릭 → 편집 · 스크롤 줌 · 드래그 팬</span>
</div>

<div class="graph-toolbar">
  <input
    type="text"
    placeholder="라벨 검색 → 포커스"
    bind:value={search}
    on:keydown={(e) => e.key === "Enter" && runSearch()}
  />
  <button on:click={runSearch} title="검색·포커스">포커스</button>
  <button on:click={expandNeighbors} title="이웃 한 겹 확장">이웃+</button>
  <button on:click={resetView} title="전체 맞춤">맞춤</button>
</div>

<div class="cy-wrap"><div class="cy" bind:this={container}></div></div>

<RetrievePanel />
