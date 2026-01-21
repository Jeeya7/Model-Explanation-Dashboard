import "./style/CenterPanel.css";
import TreePanel from "./TreePanel";

export default function CenterPanel() {
  return (
    <div className="center-panel">
      <div className="center-panel-header"></div>
      <div className="center-panel-canvas">
        <TreePanel />
      </div>
    </div>
  );
}