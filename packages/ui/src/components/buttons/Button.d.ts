import * as React from "react";

/**
 * Primary action button for the helm workbench.
 */
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual weight in the action hierarchy. Default "primary". */
  variant?: "primary" | "secondary" | "ghost" | "danger";
  /** Control height. Default "md". */
  size?: "sm" | "md" | "lg";
  /** Leading icon node (e.g. a lucide glyph). */
  icon?: React.ReactNode;
  /** Trailing icon node. */
  iconRight?: React.ReactNode;
  disabled?: boolean;
  /** Show a spinner and block interaction. */
  loading?: boolean;
  /** Stretch to fill the container width. */
  fullWidth?: boolean;
  children?: React.ReactNode;
}

export function Button(props: ButtonProps): React.ReactElement;
