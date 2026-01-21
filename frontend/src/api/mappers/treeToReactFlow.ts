import type { Node, Edge } from "reactflow";
import type { TreeDTO, TreeNodeDTO, TreeEdgeDTO } from "../types";
import { applyTreeLayout } from "./treeLayout";

function formatNodeLabel(n: TreeNodeDTO, featureNames: string[], labelNames: string[]) {
  if (n.is_leaf) {
    const cls = n.predicted_class ?? n.value;
    return cls != null ? labelNames[cls] : "Leaf";
  }

  const feature = n.feature != null ? featureNames[n.feature] : "feature?";
  const thr = n.threshold != null ? n.threshold : "?";
  const ig = n.information_gain != null ? `\nIG: ${n.information_gain.toFixed(3)}` : "";

  return `${feature} < ${thr}${ig}`;
}

function edgeLabel(e: TreeEdgeDTO, featureNames: string[]) {
  const f = e.feature != null ? featureNames[e.feature] : "feature?";
  return `${f} ${e.operator} ${e.threshold}`;
}

export function treeDtoToReactFlow(tree: TreeDTO): { nodes: Node[]; edges: Edge[] } {
  const nodeList = Object.values(tree.nodes);
  const edgeList = Object.values(tree.edges);

  const nodes: Node[] = nodeList.map((n) => {
    const isLeaf = n.is_leaf || n.value != null;
    const isRoot =
      tree.root_id != null && String(tree.root_id) === String(n.id);

    return {
      id: String(n.id),
      position: { x: 0, y: 0 }, // placeholder; layout will set real positions
      data: {
        label: formatNodeLabel(n, tree.feature_names, tree.label_names),
      },
      className: isRoot
        ? "root-node"
        : isLeaf
        ? "leaf-node"
        : "decision-node",
    };
  });

  const edges: Edge[] = edgeList.map((e, i) => ({
    id: `e-${e.source}-${e.target}-${i}`,
    source: String(e.source),
    target: String(e.target),
    label: edgeLabel(e, tree.feature_names),
    type: "smoothstep",
  }));

  const laidOutNodes = applyTreeLayout(nodes, edges);
  return { nodes: laidOutNodes, edges };
}

