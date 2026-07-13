import * as React from "react";

/** Collapsed tool-call / thought row in the analyst thread. */
export interface ToolCallRowProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Row label, e.g. "Get Financials" or "Thought". */
  label: string;
  /** "tool" = gray rounded row with wrench; "thought" = quiet chevron row. */
  kind?: "tool" | "thought";
  /** Optional right-aligned mono detail (e.g. "1.2s"). */
  detail?: string;
  /** Makes the row clickable (expand/collapse affordance). */
  onClick?: React.MouseEventHandler<HTMLDivElement>;
}

export function ToolCallRow(props: ToolCallRowProps): React.ReactElement;
