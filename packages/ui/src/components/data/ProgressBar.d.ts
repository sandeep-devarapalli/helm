import * as React from "react";

/** Determinate progress / distribution bar. */
export interface ProgressBarProps extends React.HTMLAttributes<HTMLDivElement> {
  current?: number;
  total?: number;
  /** Fill color. Default "accent" (green). */
  tone?: "accent" | "ink" | "danger" | "warning" | "info";
  /** Track thickness. Default "sm". */
  height?: "xs" | "sm" | "md";
  /** Show a trailing `current/total` mono label. */
  showCount?: boolean;
}

export function ProgressBar(props: ProgressBarProps): React.ReactElement;
