import * as React from "react";

/** One Explorer watchlist row — icon + mono ticker, selected = gray fill. */
export interface WatchlistRowProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Ticker symbol, e.g. "AAPL". */
  symbol: string;
  /** Leading icon (defaults to the bank glyph). */
  icon?: React.ReactNode;
  selected?: boolean;
  /** Optional right-aligned change figure, e.g. "+3.69%". */
  change?: string;
  changeDirection?: "up" | "down";
  onClick?: React.MouseEventHandler<HTMLDivElement>;
}

export function WatchlistRow(props: WatchlistRowProps): React.ReactElement;
