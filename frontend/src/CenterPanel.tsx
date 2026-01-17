import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";

const nodes = [
  {
    id: "1",
    position: { x: 250, y: 0 },
    data: { label: "Petal Width < 0.8\nIG: 0.91" },
  },
  {
    id: "2",
    position: { x: 100, y: 100 },
    data: { label: "Setosa" },
  },
  {
    id: "3",
    position: { x: 400, y: 100 },
    data: { label: "Petal Width ≥ 0.8" },
  },
];

const edges = [
  { id: "e1-2", source: "1", target: "2" },
  { id: "e1-3", source: "1", target: "3" },
];

export default function TreePanel() {
  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  );
}
