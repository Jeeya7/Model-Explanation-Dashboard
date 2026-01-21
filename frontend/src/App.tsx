import { useEffect, useState } from "react";
import "./style/App.css";
import Header from "./HeaderBar";
import type { DatasetType } from "./HeaderBar";
import { Divider } from "@mui/material";
import LeftPanel from "./LeftPanel";

import { trainTree } from "./api/central";
import type { TreeDTO } from "./api/types";
import CenterPanel from "./CenterPanel";

function DashboardPage() {
  const [dataset, setDataset] = useState<DatasetType>("Iris");
  const [values, setValues] = useState<number[]>([]);

  const [tree, setTree] = useState<TreeDTO | null>(null);
  const [treeError, setTreeError] = useState<string>("");

  useEffect(() => {
    let cancelled = false;

    trainTree() // if you support dataset: trainTree(dataset)
      .then((t) => {
        if (cancelled) return;
        setTree(t);
        setTreeError("");

        // initialize slider values once tree arrives
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

  console.log("Rendered DashboardPage with tree:", tree);

  return (
    <div className="app">
      <Header dataset={dataset} onDatasetChange={setDataset} />

      <div className="dashboard">
        <div className="panel left-panel">
          <h2>Controls</h2>
          <Divider orientation="horizontal" />
          <p>Feature sliders</p>
          <LeftPanel tree={tree} values={values} onChange={setValues} />
        </div>

        <div className="panel center-panel">
          <h2>Decision Tree</h2>
          <Divider orientation="horizontal" />
          <CenterPanel tree={tree} error={treeError} />
        </div>

        <div className="panel right-panel">
          <h2>Metrics</h2>
          <Divider orientation="horizontal" />
          <p>Accuracy / confusion matrix</p>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
