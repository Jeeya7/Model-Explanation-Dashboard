import "./style/LeftPanel.css";
import ControlPanel from "./ControlPanel";
import type { TreeDTO } from "./api/types";

export default function LeftPanel({ tree, values, onChange }: { tree: TreeDTO | null; values: number[]; onChange: (values: number[]) => void }) {
    return (
        <div className="left-panel">
            <div className="left-panel-header"></div>
            <div className="left-panel-controls">
                <ControlPanel tree={tree} values={values} onChange={onChange} />
            </div>
        </div>
    );
}