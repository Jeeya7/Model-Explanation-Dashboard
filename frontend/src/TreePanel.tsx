// src/TreePanel.tsx
import { useEffect, useMemo, useState } from "react";
import ReactFlow, { Background, Controls, type Node, type Edge } from "reactflow";
import "reactflow/dist/style.css";

import { trainTree } from "./api/central";
import type { TreeDTO } from "./api/types";
import { treeDtoToReactFlow } from "./api/mappers/treeToReactFlow";

type Props = {
  className?: string;
};

export default function TreePanel({ className }: Props) {
  const [tree, setTree] = useState<TreeDTO | null>(null);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    let cancelled = false;

    trainTree()
      .then((data) => {
        if (!cancelled) setTree(data);
      })
      .catch((e) => {
        if (!cancelled) setError(String(e));
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const { nodes, edges } = useMemo((): { nodes: Node[]; edges: Edge[] } => {
    if (!tree) return { nodes: [], edges: [] };
    return treeDtoToReactFlow(tree);
  }, [tree]);

  if (error) return <div className={className} style={{ padding: 8 }}>{error}</div>;
  if (!tree) return <div className={className} style={{ padding: 8 }}>Training…</div>;

  return (
    <div className={className} style={{ height: "100%", width: "100%" }}>
      <ReactFlow nodes={nodes} edges={edges} fitView fitViewOptions={{ padding: 0.2 }}>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
