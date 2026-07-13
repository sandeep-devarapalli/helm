import * as React from "react";

/**
 * A trading-mandate profile tile — the agent's pre-trade consent surface.
 */
export interface MandateCardProps extends React.HTMLAttributes<HTMLDivElement> {
  ordinal?: number;
  label?: string;
  universe?: string;
  /** Max order notional, pre-formatted (e.g. "$5,000"). */
  maxOrder?: string;
  /** Daily trade cap label. */
  dailyCap?: string;
  leverage?: string;
  notes?: string;
  /** Highlight as the selected option. */
  active?: boolean;
  onCommit?: () => void;
}

export function MandateCard(props: MandateCardProps): React.ReactElement;
