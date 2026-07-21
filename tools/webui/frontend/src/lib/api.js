// 얇은 fetch 래퍼. 백엔드 API 계약(server.py)은 불변 — 여기서 소비만 한다.
// 에러는 body.detail(HTTPException)을 메시지로, status를 err.status로 실어 던진다
// (409 Conflict 등 상태 분기를 호출부가 하도록).

export async function api(path, opts) {
  const r = await fetch(path, opts);
  const body = await r.json().catch(() => ({}));
  if (!r.ok) {
    const err = new Error(body.detail || r.statusText || `HTTP ${r.status}`);
    err.status = r.status;
    err.body = body;
    throw err;
  }
  return body;
}

export const getJSON = (path) => api(path);

export const postJSON = (path, data) =>
  api(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data || {}),
  });

export const putJSON = (path, data) =>
  api(path, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
