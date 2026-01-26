import "./style/LeftPanel.css";
import ControlPanel from "./ControlPanel";
import PredictionPanel from "./PredictionPanel";
import type { TreeDTO, PredictionDTO } from "./api/types";


type LeftPanelProps = {
  tree: TreeDTO | null;
  values: number[];
  onChange: (values: number[]) => void;
  runId: number;
  onPrediction: (prediction: PredictionDTO) => void;
  onPredict: () => void;
};
export default function LeftPanel({ tree, values, onChange, runId, onPrediction, onPredict }: LeftPanelProps) {

  return (
    <div className="left-panel">
      <div className="left-panel-header"></div>

      <div className="left-panel-controls">
        <ControlPanel
          tree={tree}
          values={values}
          onChange={onChange}
          onPredict={onPredict}
        />
      </div>

      <PredictionPanel
        tree={tree}
        featureValues={values}
        runId={runId}
        onPrediction={onPrediction}
      />
    </div>
  );
}
