import type { TreeDTO } from "./api/types";
import "./style/CenterPanel.css";
import TreePanel from "./TreePanel";

export default function CenterPanel({ tree, error }: { tree: TreeDTO | null; error?: string }) {
  return (
    <div className="center-panel">
      <div className="center-panel-header"></div>
      <div className="center-panel-canvas">
        <TreePanel tree={tree} error={error} />
      </div>
    </div>
  );
}