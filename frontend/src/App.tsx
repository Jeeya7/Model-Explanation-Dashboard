import { useState } from "react";
import "./style/App.css";
import Header from "./HeaderBar";
import type { DatasetType } from "./HeaderBar";
import { Divider } from "@mui/material";
import TreePanel from "./CenterPanel";


function DashboardPage() {
  const [dataset, setDataset] = useState<DatasetType>("Iris");

  return (
    <div className="app">
      {/* Header */}
      <Header dataset={dataset} onDatasetChange={setDataset} />

      {/* Main dashboard */}
      <div className="dashboard">
        {/* Left column */}
        <div className="panel left-panel">
          <h2>Controls</h2>
          <Divider orientation="horizontal"/>
          <p>Feature sliders go here</p>
        </div>
        
        {/* Center column */}
        <div className="panel center-panel">
          <h2>Decision Tree</h2>
          <Divider orientation="horizontal"/>
          <TreePanel />
        </div>
        
        {/* Right column */}
        <div className="panel right-panel">
          <h2>Metrics</h2>
          <Divider orientation="horizontal"/>
          <p>Accuracy / confusion matrix</p>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
