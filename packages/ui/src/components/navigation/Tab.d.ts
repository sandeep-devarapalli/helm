import * as React from "react";

/** Browser-style workspace tab (tab strip of the workbench). */
export interface TabProps extends React.HTMLAttributes<HTMLDivElement> {
  /** Tab label — tickers and thread titles, rendered in mono. */
  label: string;
  /** Leading icon node. */
  icon?: React.ReactNode;
  /** Active tab: white fill + ink top bar. */
  active?: boolean;
  /** Show a close ×; called on click. */
  onClose?: () => void;
  onClick?: React.MouseEventHandler<HTMLDivElement>;
}

export function Tab(props: TabProps): React.ReactElement;
