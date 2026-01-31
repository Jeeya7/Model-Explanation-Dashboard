import { useEffect, useState } from "react";
import "./style/App.css";
import Header from "./HeaderBar";
import type { DatasetType } from "./HeaderBar";
import { Divider } from "@mui/material";
import LeftPanel from "./LeftPanel";
import RightPanel from "./RightPanel";

import { trainTree } from "./api/central";
import type { PredictionDTO, TreeDTO } from "./api/types";
import CenterPanel from "./CenterPanel";

function DashboardPage() {
  const [dataset, setDataset] = useState<DatasetType>("Iris");
  const [values, setValues] = useState<number[]>([]);
  const [runId, setRunId] = useState(0);
  const [tree, setTree] = useState<TreeDTO | null>(null);
  const [treeError, setTreeError] = useState<string>("");
  const [prediction, setPrediction] = useState<PredictionDTO | null>(null);

  // 🔹 NEW: metrics panel collapse state
  const [metricsCollapsed, setMetricsCollapsed] = useState(false);

  const handlePredict = () => {
    setPrediction(null);
    setRunId((x) => x + 1);
  };

  useEffect(() => {
    let cancelled = false;

    trainTree()
      .then((t) => {
        if (cancelled) return;
        setTree(t);
        setTreeError("");

        setValues((prev) =>
          prev.length === t.feature_names.length
            ? prev
            : new Array(t.feature_names.length).fill(0)
        );
      })
      .catch((e) => {
        if (cancelled) return;
        setTreeError(String(e));
      });

    return () => {
      cancelled = true;
    };
  }, [dataset]);

  return (
    <div className="app">
      <Header dataset={dataset} onDatasetChange={setDataset} />

      <div className="dashboard">
        {/* LEFT PANEL */}
        <div className="panel left-panel">
          <h2>Controls</h2>
          <Divider orientation="horizontal" />
          <LeftPanel
            tree={tree}
            values={values}
            runId={runId}
            onPredict={handlePredict}
            onPrediction={setPrediction}
            onChange={setValues}
          />
        </div>

        {/* CENTER PANEL */}
        <div className="panel center-panel">
          <h2>Decision Tree</h2>
          <Divider orientation="horizontal" />
          <CenterPanel
            tree={tree}
            error={treeError}
            prediction={prediction}
          />
        </div>

        {/* RIGHT PANEL (RESIZABLE / COLLAPSIBLE) */}
        <div
          className="panel right-panel"
          style={{
            width: metricsCollapsed ? 56 : 360,
            transition: "width 180ms ease",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: 8,
            }}
          >
            {!metricsCollapsed && <h2 style={{ margin: 0 }}>Metrics</h2>}

            <button
              onClick={() => setMetricsCollapsed((v) => !v)}
              style={{
                cursor: "pointer",
                border: "none",
                background: "transparent",
                fontSize: 16,
              }}
              title={metricsCollapsed ? "Show metrics" : "Hide metrics"}
            >
              {metricsCollapsed ? "⟨" : "⟩"}
            </button>
          </div>

          {!metricsCollapsed && (
            <>
              <Divider orientation="horizontal" />
              <RightPanel tree={tree} />
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
