import "./style/LeftPanel.css";
import ControlPanel from "./ControlPanel";
import PredictionPanel from "./PredictionPanel";
import type { TreeDTO } from "./api/types";
import { useState } from "react";

type LeftPanelProps = {
  tree: TreeDTO | null;
  values: number[];
  onChange: (values: number[]) => void;
};

export default function LeftPanel({ tree, values, onChange }: LeftPanelProps) {
  const [runId, setRunId] = useState(0);

  const handlePredict = () => {
    setRunId((x) => x + 1);
  };

  return (
    <div className="left-panel">
      <div className="left-panel-header"></div>

      <div className="left-panel-controls">
        <ControlPanel
          tree={tree}
          values={values}
          onChange={onChange}
          onPredict={handlePredict}
        />
      </div>

      <PredictionPanel
        tree={tree}
        featureValues={values}
        runId={runId}
      />
    </div>
  );
}
