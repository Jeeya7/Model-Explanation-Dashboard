import type { TreeDTO, PredictionDTO } from "./api/types";
import { getPrediction } from "./api/predict";
import { useState, useRef, useEffect } from "react";

type PredictionPanelProps = {
  tree: TreeDTO | null;
  featureValues: number[];
  runId: number;
};
 
export default function PredictionPanel({ tree, featureValues, runId }: PredictionPanelProps) {
  const [prediction, setPrediction] = useState<PredictionDTO | null>(null);
  
  const featureRef = useRef<number[]>(featureValues);

  const classIndex = prediction?.predicted_class ?? null;
  const classLabel =
  classIndex == null
    ? null
    : tree?.label_names?.[classIndex] ?? `Class ${classIndex}`;

  useEffect(() => {
    featureRef.current = featureValues;
  }, [featureValues]);

  useEffect(() => {
    if (!tree) return;
    if (runId === 0) return;

    getPrediction(featureRef.current, tree)
      .then(setPrediction)
      .catch(console.error);
  }, [tree, runId]);

  if (!tree) {
    return (
      <div className="prediction-panel" style={{ padding: 8 }}>
        Loading prediction...
      </div>
    );
  }

  return (
    <div className="prediction-panel" style={{ padding: 12 }}>
      {prediction ? (
        <div style={{ fontSize: 13 }}>
          Predicted class: <strong>{classLabel ?? "None"}</strong>
        </div>
      ) : (
        <div style={{ fontSize: 13 }}>Click Predict</div>
      )}
    </div>
  );
}
