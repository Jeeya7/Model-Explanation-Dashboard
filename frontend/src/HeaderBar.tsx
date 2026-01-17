import "./style/HeaderBar.css";
import { Divider } from "@mui/material";
import Box from "@mui/material/Box";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import type { SelectChangeEvent } from "@mui/material/Select";

type DatasetType = "Iris" | "Wine" | "Custom";

interface HeaderProps {
  dataset: DatasetType;
  onDatasetChange: (value: DatasetType) => void;
}

function Header({ dataset, onDatasetChange }: HeaderProps) {
  const handleChange = (e: SelectChangeEvent) => {
    onDatasetChange(e.target.value as DatasetType);
  };

  return (
    <div className="header">
      <h1>Model Explanation Dashboard</h1>

          <Divider orientation="horizontal"
              sx={{
                    borderColor: "rgba(255, 255, 255, 0.25)", // soft white
                    my: 2, // vertical margin
                }} />

      <div className="subheader">
        <h3>Understand and Interpret Your Machine Learning Models</h3>

        <Box sx={{ minWidth: 200 }}>
          <FormControl fullWidth size="small">
            <InputLabel
              id="datasetlabel"
              sx={{ color: "white" }}
            >
              Dataset
            </InputLabel>

            <Select
              labelId="datasetlabel"
              value={dataset}
              label="Dataset"
              onChange={handleChange}
              sx={{
                backgroundColor: "#071934",
                color: "white",
                borderRadius: "8px",

                "& .MuiOutlinedInput-notchedOutline": {
                  borderColor: "#d1d5db",
                },
                "&:hover .MuiOutlinedInput-notchedOutline": {
                  borderColor: "#2563eb",
                },
                "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
                  borderColor: "#2563eb",
                },
              }}
              MenuProps={{
                PaperProps: {
                  sx: {
                    backgroundColor: "#ffffff",
                  },
                },
              }}
            >
              <MenuItem value="Iris">Iris</MenuItem>
              <MenuItem value="Wine">Wine</MenuItem>
              <MenuItem value="Custom">Custom</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </div>
    </div>
  );
}

export default Header;
export type { DatasetType };
