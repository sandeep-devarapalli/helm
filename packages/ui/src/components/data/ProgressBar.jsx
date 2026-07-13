import React from "react";

/**
 * Determinate progress / distribution bar. Default green fill on a panel
 * track; used for run progress, budget meters, and consensus distributions.
 */
export function ProgressBar({ current = 0, total = 100, tone = "accent", height = "sm", showCount = false, style, ...rest }) {
  const pct = total > 0 ? Math.min(100, Math.max(0, (current / total) * 100)) : 0;
  const h = { xs: 4, sm: 6, md: 10 }[height] || 6;
  const fills = {
    accent: "var(--color-accent)",
    ink: "var(--color-primary)",
    danger: "var(--color-danger)",
    warning: "var(--color-warning)",
    info: "var(--color-info)",
  };
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10, ...style }} {...rest}>
      <div
        style={{
          flex: 1,
          height: h,
          borderRadius: "var(--radius-full)",
          background: "var(--color-panel-hover)",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${pct}%`,
            height: "100%",
            borderRadius: "var(--radius-full)",
            background: fills[tone] || fills.accent,
            transition: "width var(--duration-slow) var(--ease-out)",
          }}
        />
      </div>
      {showCount && (
        <span
          style={{
            fontFamily: "var(--font-mono)",
            fontSize: "var(--text-2xs)",
            color: "var(--color-text-muted)",
            fontVariantNumeric: "tabular-nums",
            whiteSpace: "nowrap",
          }}
        >
          {current}/{total}
        </span>
      )}
    </div>
  );
}
