// 타입 문자열 → 결정적 색/모양. vanilla app.js의 hue 해시를 재사용해 리스트·그래프가
// 같은 타입에 같은 색을 쓰게 한다(오프라인, 외부 팔레트 의존 없음).

export function hue(s) {
  let h = 0;
  for (const c of s || "?") h = (h * 31 + c.charCodeAt(0)) % 360;
  return h;
}

export const typeColor = (t) => `hsl(${hue(t || "?")} 55% 55%)`;

// 알려진 상위 타입 → cytoscape 노드 모양(그 외는 ellipse). 하위클래스명이 와도
// 아래 키를 부분 포함하면 매칭되게 해 그래프에서 종류가 한눈에 구분되게 한다.
const SHAPES = [
  ["Harness", "round-rectangle"],
  ["SystemPrompt", "round-tag"],
  ["Prompt", "round-tag"],
  ["Workflow", "diamond"],
  ["Tool", "hexagon"],
  ["Guardrail", "octagon"],
  ["ModelConfig", "barrel"],
  ["Capability", "star"],
  ["Concept", "ellipse"],
];

export function typeShape(t) {
  const s = t || "";
  for (const [key, shape] of SHAPES) if (s.includes(key)) return shape;
  return "ellipse";
}
