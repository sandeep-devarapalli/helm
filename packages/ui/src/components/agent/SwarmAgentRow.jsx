import React from "react";
import { Badge } from "../surfaces/Badge.jsx";

/**
 * Live status row for one agent in a Hermes desk run. Light-workbench
 * styling: sans name, mono tool/time, soft status badge.
 */
export function SwarmAgentRow({ name, role, status = "waiting", tool, elapsed, iterations, output, style, ...rest }) {
  const toneMap = {
    done: "success",
    failed: "danger",
    blocked: "warning",
    retry: "info",
    running: "ink",
    waiting: "neutral",
    cancelled: "neutral",
  };
  const cell = { fontFamily: "var(--font-mono)", fontSize: "var(--text-xs)", color: "var(--color-text-muted)", fontVariantNumeric: "tabular-nums" };

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "9.5rem 6.5rem 9rem 4.5rem minmax(0,1fr)",
        gap: 10,
        alignItems: "center",
        padding: "9px 0",
        borderBottom: "1px solid var(--color-border)",
        ...style,
      }}
      {...rest}
    >
      <div style={{ minWidth: 0 }}>
        <div style={{ fontFamily: "var(--font-sans)", fontSize: "var(--text-sm)", fontWeight: "var(--weight-medium)", color: "var(--color-text)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {name}
        </div>
        {role && <div style={{ fontSize: "var(--text-2xs)", color: "var(--color-text-faint)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{role}</div>}
      </div>
      <div>
        <Badge tone={toneMap[status] || "neutral"} style={{ textTransform: "capitalize" }}>{status}</Badge>
      </div>
      <div style={{ ...cell, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }} title={tool}>{tool || "—"}</div>
      <div style={{ ...cell, textAlign: "right" }}>{elapsed || "—"}</div>
      <div style={{ fontFamily: "var(--font-sans)", fontSize: "var(--text-sm)", color: "var(--color-text-muted)", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }} title={output}>
        {output || "—"}
      </div>
    </div>
  );
}
