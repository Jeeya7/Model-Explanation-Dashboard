import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";
import type { TreeDTO } from "./api/types";

type ControlPanelProps = {
  tree: TreeDTO | null;
  values: number[];
  onChange: (values: number[]) => void;
};

export default function ControlPanel({
  tree,
  values,
  onChange,
}: ControlPanelProps) {
  if (!tree) {
    return (
      <div className="control-panel" style={{ padding: 8 }}>
        Loading controls...
      </div>
    );
  }

  const handleSliderChange =
    (index: number) => (_: Event, value: number | number[]) => {
      const next = [...values];
      next[index] = value as number;
      onChange(next);
    };

  return (
    <div className="control-panel" style={{ padding: 12 }}>
      {tree.feature_names.map((featureName, i) => (
        <Box key={featureName} sx={{ mb: 2 }}>
          <div style={{ fontSize: 13, marginBottom: 4 }}>
            {featureName}: <strong>{values[i]?.toFixed(2)}</strong>
          </div>
          <Slider
            value={values[i] ?? 0}
            min={0}
            max={10}
            step={0.1}
            onChange={handleSliderChange(i)}
          />
        </Box>
      ))}
    </div>
  );
}
