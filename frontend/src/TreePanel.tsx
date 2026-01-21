// src/TreePanel.tsx
import { useMemo } from "react";
import ReactFlow, { Background, Controls, type Node, type Edge } from "reactflow";
import "reactflow/dist/style.css";

import type { TreeDTO } from "./api/types";
import { treeDtoToReactFlow } from "./api/mappers/treeToReactFlow";

type Props = {
  className?: string;
  tree: TreeDTO | null;
  error?: string;
};

export default function TreePanel({ className, tree, error }: Props) {
  const { nodes, edges } = useMemo((): { nodes: Node[]; edges: Edge[] } => {
    if (!tree) return { nodes: [], edges: [] };
    return treeDtoToReactFlow(tree);
  }, [tree]);

  if (error) {
    return (
      <div className={className} style={{ padding: 8 }}>
        {error}
      </div>
    );
  }

  if (!tree) {
    return (
      <div className={className} style={{ padding: 8 }}>
        Training…
      </div>
    );
  }

  return (
    <div className={className} style={{ height: "100%", width: "100%" }}>
      <ReactFlow nodes={nodes} edges={edges} fitView fitViewOptions={{ padding: 0.2 }}>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
