import * as React from "react";

/** One agent's live status row inside a swarm-run table. */
export interface SwarmAgentRowProps extends React.HTMLAttributes<HTMLDivElement> {
  name: string;
  role?: string;
  status?: "waiting" | "running" | "done" | "failed" | "blocked" | "retry" | "cancelled";
  /** Current tool name. */
  tool?: string;
  /** Elapsed time string, e.g. "1m 20s". */
  elapsed?: string;
  iterations?: number;
  /** Last output / error preview. */
  output?: string;
}

export function SwarmAgentRow(props: SwarmAgentRowProps): React.ReactElement;
