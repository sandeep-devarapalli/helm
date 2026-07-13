import * as React from "react";

/** Text input — white fill, hairline border, quiet focus. */
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  /** Leading icon node. */
  icon?: React.ReactNode;
  /** Helper text under the field. */
  hint?: string;
  /** Error text; switches the field to the danger style. */
  error?: string;
  size?: "sm" | "md" | "lg";
  /** Set the input text in mono (symbols, amounts). */
  mono?: boolean;
}

export function Input(props: InputProps): React.ReactElement;
