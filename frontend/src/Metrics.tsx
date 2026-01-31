import { useMemo, useState } from "react";
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  FormControlLabel,
  Switch,
  Divider,
} from "@mui/material";

type Props = {
  matrix?: number[][];
  classNames?: string[];
  labels?: number[];
};

function clamp01(x: number) {
  return Math.max(0, Math.min(1, x));
}

function formatPct(x: number) {
  if (!Number.isFinite(x)) return "—";
  return `${(x * 100).toFixed(1)}%`;
}

function safeDiv(num: number, den: number) {
  return den === 0 ? NaN : num / den;
}

export default function Metrics({ matrix, classNames, labels }: Props) {
  const [normalized, setNormalized] = useState(false);

  const derived = useMemo(() => {

    const k = matrix?.length ?? 0;

    // Label ids used for headers + lookups.
    // If labels not provided, assume 0..k-1.
    const labelIds = labels ?? Array.from({ length: k }, (_, i) => i);

    // Ensure cm is always a k x k matrix (defensive)
    const cm: number[][] = Array.from({ length: k }, (_, i) =>
      Array.from({ length: k }, (_, j) => matrix?.[i]?.[j] ?? 0)
    );

    const rowTotals = cm.map((row) => row.reduce((a, b) => a + b, 0));
    const colTotals = Array.from({ length: k }, (_, j) =>
      cm.reduce((sum, row) => sum + row[j], 0)
    );

    const total = rowTotals.reduce((a, b) => a + b, 0);
    const correct = cm.reduce((sum, row, i) => sum + (row[i] ?? 0), 0);
    const accuracy = safeDiv(correct, total);

    // Per-class metrics (one-vs-rest)
    const perClass = labelIds.map((lab, i) => {
      const tp = cm[i]?.[i] ?? 0;
      const fp = (colTotals[i] ?? 0) - tp;
      const fn = (rowTotals[i] ?? 0) - tp;

      const precision = safeDiv(tp, tp + fp);
      const recall = safeDiv(tp, tp + fn);
      const f1 = safeDiv(2 * precision * recall, precision + recall);

      return {
        labelId: lab,
        name: classNames?.[lab] ?? classNames?.[i] ?? String(lab),
        tp,
        fp,
        fn,
        support: rowTotals[i] ?? 0,
        precision,
        recall,
        f1,
      };
    });

    const macroPrecision = safeDiv(
      perClass.reduce((s, c) => s + (Number.isFinite(c.precision) ? c.precision : 0), 0),
      perClass.reduce((s, c) => s + (Number.isFinite(c.precision) ? 1 : 0), 0)
    );
    const macroRecall = safeDiv(
      perClass.reduce((s, c) => s + (Number.isFinite(c.recall) ? c.recall : 0), 0),
      perClass.reduce((s, c) => s + (Number.isFinite(c.recall) ? 1 : 0), 0)
    );
    const macroF1 = safeDiv(
      perClass.reduce((s, c) => s + (Number.isFinite(c.f1) ? c.f1 : 0), 0),
      perClass.reduce((s, c) => s + (Number.isFinite(c.f1) ? 1 : 0), 0)
    );

    const weightedF1 = safeDiv(
      perClass.reduce(
        (s, c) => s + (Number.isFinite(c.f1) ? c.f1 * c.support : 0),
        0
      ),
      perClass.reduce((s, c) => s + c.support, 0)
    );

    // Normalized matrix: row-normalized (actual distribution)
    const cmNorm: number[][] = cm.map((row, i) => {
      const den = rowTotals[i] ?? 0;
      return row.map((v) => (den === 0 ? NaN : v / den));
    });

    // For heatmap scaling (counts)
    const maxCount = cm.reduce((m, row) => Math.max(m, ...row), 0);

    return {
      labelIds,
      cm,
      cmNorm,
      rowTotals,
      colTotals,
      total,
      correct,
      accuracy,
      perClass,
      macroPrecision,
      macroRecall,
      macroF1,
      weightedF1,
      maxCount,
    };
  }, [matrix, labels, classNames]);

  const { labelIds, cm, cmNorm, rowTotals, colTotals, total, accuracy, perClass, maxCount } =
    derived;

  const displayName = (labelId: number, i: number) =>
    classNames?.[labelId] ?? classNames?.[i] ?? String(labelId);

  const cellBg = (value: number, isNormalized: boolean) => {
    const intensity = isNormalized
      ? clamp01(Number.isFinite(value) ? value : 0)
      : maxCount === 0
        ? 0
        : clamp01(value / maxCount);

    const alpha = 0.06 + 0.42 * intensity;
    return `rgba(0,0,0,${alpha})`;
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
      <Box sx={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
        <Box>
          <Typography variant="body2" sx={{ opacity: 0.8 }}>
            Accuracy: <b>{formatPct(accuracy)}</b> · Samples: <b>{total}</b>
          </Typography>
        </Box>

        <FormControlLabel
          control={
            <Switch checked={normalized} onChange={(e) => setNormalized(e.target.checked)} />
          }
          label={normalized ? "Row-normalized" : "Counts"}
        />
      </Box>

      {/* Confusion Matrix */}
      <TableContainer component={Paper} variant="outlined">
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 700 }}>Actual \\ Pred</TableCell>
              {labelIds.map((lab, j) => (
                <TableCell key={lab} align="center" sx={{ fontWeight: 700 }}>
                  {displayName(lab, j)}
                </TableCell>
              ))}
              <TableCell align="center" sx={{ fontWeight: 700 }}>
                Total
              </TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {labelIds.map((labRow, i) => (
              <TableRow key={labRow}>
                <TableCell sx={{ fontWeight: 700 }}>{displayName(labRow, i)}</TableCell>

                {labelIds.map((labCol, j) => {
                  const value = normalized ? cmNorm[i]?.[j] : cm[i]?.[j];
                  const shown = normalized
                    ? Number.isFinite(value)
                      ? (value as number).toFixed(2)
                      : "—"
                    : String(cm[i]?.[j] ?? 0);

                  const isDiag = i === j;

                  return (
                    <TableCell
                      key={`${labRow}-${labCol}`}
                      align="center"
                      sx={{
                        fontVariantNumeric: "tabular-nums",
                        background: cellBg(
                          normalized ? (Number.isFinite(value) ? (value as number) : 0) : (cm[i]?.[j] ?? 0),
                          normalized
                        ),
                        border: isDiag ? "2px solid rgba(0,0,0,0.35)" : undefined,
                      }}
                      title={
                        normalized
                          ? `Actual ${displayName(labRow, i)} predicted ${displayName(
                              labCol,
                              j
                            )}: ${shown}`
                          : `Count: ${shown}`
                      }
                    >
                      {shown}
                    </TableCell>
                  );
                })}

                <TableCell align="center" sx={{ fontWeight: 700 }}>
                  {rowTotals[i] ?? 0}
                </TableCell>
              </TableRow>
            ))}

            <TableRow>
              <TableCell sx={{ fontWeight: 700 }}>Total</TableCell>
              {colTotals.map((t, j) => (
                <TableCell key={`coltotal-${j}`} align="center" sx={{ fontWeight: 700 }}>
                  {t}
                </TableCell>
              ))}
              <TableCell align="center" sx={{ fontWeight: 900 }}>
                {total}
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>

      <Divider />

      {/* Per-class metrics */}
      <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
        <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
          Per-class metrics
        </Typography>

        <TableContainer component={Paper} variant="outlined">
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 700 }}>Class</TableCell>
                <TableCell align="right" sx={{ fontWeight: 700 }}>
                  Support
                </TableCell>
                <TableCell align="right" sx={{ fontWeight: 700 }}>
                  Precision
                </TableCell>
                <TableCell align="right" sx={{ fontWeight: 700 }}>
                  Recall
                </TableCell>
                <TableCell align="right" sx={{ fontWeight: 700 }}>
                  F1
                </TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {perClass.map((c) => (
                <TableRow key={c.labelId}>
                  <TableCell sx={{ fontWeight: 700 }}>{c.name}</TableCell>
                  <TableCell align="right">{c.support}</TableCell>
                  <TableCell align="right">{formatPct(c.precision)}</TableCell>
                  <TableCell align="right">{formatPct(c.recall)}</TableCell>
                  <TableCell align="right">{formatPct(c.f1)}</TableCell>
                </TableRow>
              ))}

              <TableRow>
                <TableCell sx={{ fontWeight: 900 }}>Summary</TableCell>
                <TableCell align="right" sx={{ fontWeight: 900 }}>
                  {total}
                </TableCell>
                <TableCell align="right" sx={{ fontWeight: 900 }}>
                  {formatPct(derived.macroPrecision)}
                </TableCell>
                <TableCell align="right" sx={{ fontWeight: 900 }}>
                  {formatPct(derived.macroRecall)}
                </TableCell>
                <TableCell align="right" sx={{ fontWeight: 900 }}>
                  {formatPct(derived.macroF1)}
                </TableCell>
              </TableRow>

              <TableRow>
                <TableCell sx={{ fontWeight: 700 }}>Weighted F1</TableCell>
                <TableCell />
                <TableCell />
                <TableCell />
                <TableCell align="right" sx={{ fontWeight: 700 }}>
                  {formatPct(derived.weightedF1)}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Box>
  );
}
