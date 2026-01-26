import Slider from "@mui/material/Slider";
import Box from "@mui/material/Box";
import type { TreeDTO } from "./api/types";
import Button from "@mui/material/Button";
import PlayCircleFilledIcon from "@mui/icons-material/PlayCircleFilled";

type ControlPanelProps = {
  tree: TreeDTO | null;
  values: number[];
  onChange: (values: number[]) => void;
  onPredict: () => void;
};

export default function ControlPanel({
  tree,
  values,
  onChange,
  onPredict,
}: ControlPanelProps) {
  if (!tree) {
    return (
      <div className="control-panel" style={{ padding: 8 }}>
        Loading controls...
      </div>
    );
  }

  const handleSliderChange =
    (index: number) => (_event: unknown, value: number | number[]) => {
      const v = Array.isArray(value) ? value[0] : value;
      const next = [...values];
      next[index] = v;
      onChange(next);
    };

  return (
    <div className="control-panel" style={{ padding: 12 }}>
      {tree.feature_names.map((featureName, i) => {
        const v = values[i] ?? 0;

        return (
          <Box key={`${featureName}-${i}`} sx={{ mb: 2 }}>
            <div style={{ fontSize: 13, marginBottom: 4 }}>
              {featureName}: <strong>{v.toFixed(2)}</strong>
            </div>
            <Slider
              value={v}
              min={0}
              max={10}
              step={0.1}
              onChange={handleSliderChange(i)}
            />
          </Box>
        );
      })}

      <Button
        startIcon={<PlayCircleFilledIcon />}
        variant="contained"
        onClick={onPredict}
        fullWidth
        sx={{ mt: 1 }}
      >
        Predict
      </Button>
    </div>
  );
}
