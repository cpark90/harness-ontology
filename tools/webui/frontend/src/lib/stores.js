import { writable } from "svelte/store";
import { getJSON } from "./api.js";

// --- 공유 상태 (vanilla app.js의 state 객체를 store로 승격) --------------------
export const schema = writable(null); // {classes, objectProperties, datatypeProperties}
export const graph = writable({ nodes: [], edges: [] }); // /api/graph
export const mtimes = writable(null); // 동시성: 마지막 저장 응답의 mtimes
export const status = writable({ msg: "로딩 중…", cls: "" });
export const result = writable(null); // 저장/validate 결과 패널
export const retrievePack = writable(null); // context pack 패널

// 편집 대상 신호. nonce로 같은 id(또는 null) 재선택도 항상 트리거되게 한다.
export const editTarget = writable({ id: null, nonce: 0 });
let _nonce = 0;
export function openNode(id) {
  editTarget.set({ id, nonce: ++_nonce });
}
export function newNode() {
  editTarget.set({ id: null, nonce: ++_nonce });
}

export function setStatus(msg, cls = "") {
  status.set({ msg, cls });
}

export async function refreshGraph() {
  graph.set(await getJSON("/api/graph"));
}
