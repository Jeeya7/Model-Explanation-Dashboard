import dagre from "dagre";
import type { Node, Edge } from "reactflow";

const NODE_W = 240;
const NODE_H = 70;

export function applyTreeLayout(nodes: Node[], edges: Edge[]) {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));

  g.setGraph({ rankdir: "TB", nodesep: 60, ranksep: 90 });

  nodes.forEach((n) => g.setNode(n.id, { width: NODE_W, height: NODE_H }));
  edges.forEach((e) => g.setEdge(e.source, e.target));

  dagre.layout(g);

  console.log("DAGRE layout running", nodes.length, edges.length);

  return nodes.map((n) => {
    const p = g.node(n.id);
    return {
      ...n,
      position: { x: p.x - NODE_W / 2, y: p.y - NODE_H / 2 },
    };
  });
}
