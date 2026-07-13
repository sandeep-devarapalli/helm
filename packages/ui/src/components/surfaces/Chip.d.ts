import * as React from "react";

/** Entity / filter chip. `tone="entity"` is the blue inline ticker pill. */
export interface ChipProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** "default" filter chip or "entity" blue ticker-mention pill. */
  tone?: "default" | "entity";
  /** Selected/active state (filter chips). */
  selected?: boolean;
  /** Leading icon node. */
  icon?: React.ReactNode;
  /** When provided, the chip becomes clickable with hover feedback. */
  onClick?: React.MouseEventHandler<HTMLSpanElement>;
  children?: React.ReactNode;
}

export function Chip(props: ChipProps): React.ReactElement;
