import * as React from "react";

/** A single performance / backtest metric (label + monospaced value). */
export interface MetricTileProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Uppercase micro-label. */
  label: string;
  /** The value string (pre-formatted, e.g. "+18.4%", "1.92"). */
  value: React.ReactNode;
  /** Colors the value. Default "neutral". */
  sentiment?: "positive" | "negative" | "neutral";
  /** Optional secondary line under the value. */
  sub?: React.ReactNode;
  align?: "center" | "start";
}

export function MetricTile(props: MetricTileProps): React.ReactElement;
