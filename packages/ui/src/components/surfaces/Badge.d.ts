import * as React from "react";

/** Small semantic status badge (soft tint, rounded rectangle). */
export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  /** Semantic color. "ink" is the filled black badge. Default "neutral". */
  tone?: "neutral" | "success" | "danger" | "warning" | "info" | "ink";
  /** Show a leading status dot. */
  dot?: boolean;
  /** Leading icon node. */
  icon?: React.ReactNode;
  /** Set the label in mono (for numeric badges). */
  mono?: boolean;
  children?: React.ReactNode;
}

export function Badge(props: BadgeProps): React.ReactElement;
