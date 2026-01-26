// src/TreePanel.tsx
import { useMemo } from "react";
import ReactFlow, { Background, Controls, type Node, type Edge } from "reactflow";
import "reactflow/dist/style.css";
import "./style/TreePanel.css";

import type { TreeDTO, PredictionDTO } from "./api/types";
import { treeDtoToReactFlow } from "./api/mappers/treeToReactFlow";

type Props = {
  className?: string;
  tree: TreeDTO | null;
  error?: string;
  prediction?: PredictionDTO | null;
};

export default function TreePanel({ className, tree, error, prediction }: Props) {
  const { nodes: baseNodes, edges: baseEdges } = useMemo(() => {
  if (!tree) return { nodes: [], edges: [] };
  return treeDtoToReactFlow(tree);
  }, [tree]);
  
  const path = prediction?.path ?? null;

  const pathSet = useMemo(() => {
    return new Set((path ?? []).map(String));
  }, [path]);

  const pathEdgeSet = useMemo(() => {
    const p = (path ?? []).map(String);
    const s = new Set<string>();
    for (let i = 0; i < p.length - 1; i++) s.add(`${p[i]}->${p[i + 1]}`);
    return s;
  }, [path]);

  const nodes = useMemo(() => {
    if (!baseNodes.length) return baseNodes;
    if (!path) return baseNodes; // no highlight yet

    return baseNodes.map((n) => {
      const onPath = pathSet.has(String(n.id));
      return {
        ...n,
        className: onPath ? "node--onpath" : "node--offpath",
        data: { ...n.data, onPath }, // optional
      };
    });
  }, [baseNodes, path, pathSet]);

  const edges = useMemo(() => {
    if (!baseEdges.length) return baseEdges;
    if (!path) return baseEdges;

    return baseEdges.map((e) => {
      const key = `${String(e.source)}->${String(e.target)}`;
      const onPath = pathEdgeSet.has(key);
      return {
        ...e,
        className: onPath ? "edge--onpath" : "edge--offpath",
      };
    });
  }, [baseEdges, path, pathEdgeSet]);





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
