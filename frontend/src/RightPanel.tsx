import Metrics from "./Metrics";
import type { TreeDTO } from "./api/types";

type RightPanelProps = {
  tree: TreeDTO | null;
};

export default function RightPanel({ tree }: RightPanelProps) {

  if (!tree) return <div>Loading tree data...</div>;
  if (!tree.confusion_matrix || tree.confusion_matrix.length === 0) {
    return <div>No confusion matrix data available.</div>;
  }

  return (
    <div>
        <Metrics
          matrix={tree.confusion_matrix}
          classNames={tree.label_names}
          labels={tree.label_names.map((_, i) => i)}
        />
    </div>
  );
}
