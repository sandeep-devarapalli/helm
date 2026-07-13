import * as React from "react";

/**
 * Surface container — quiet gray panel or white card.
 */
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /** "default" gray panel · "white" card · "accent" green hairline · "ghost" border-only. */
  tone?: "default" | "white" | "accent" | "ghost";
  /** Add a soft shadow. */
  raised?: boolean;
  /** Inner padding step. Default "md" (16px). */
  padding?: "none" | "sm" | "md" | "lg";
  /** Hover feedback (border + fill shift). */
  interactive?: boolean;
  children?: React.ReactNode;
}

export function Card(props: CardProps): React.ReactElement;
