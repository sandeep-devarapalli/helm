import * as React from "react";

/** Square, icon-only button for console chrome and row controls. */
export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: "sm" | "md" | "lg";
  /** "ghost" (quiet), "solid" (filled accent). Default "ghost". */
  variant?: "ghost" | "solid";
  /** Active/selected state (accent tint). */
  active?: boolean;
  disabled?: boolean;
  /** Accessible label + tooltip. */
  title?: string;
  /** Icon glyph. */
  children?: React.ReactNode;
}

export function IconButton(props: IconButtonProps): React.ReactElement;
