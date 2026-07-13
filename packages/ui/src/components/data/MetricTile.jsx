import React from "react";

/**
 * A single stat cell — small gray label above a mono value, as in the
 * workbench's stat grids ("Prev Close / $294.38"). `sentiment` colors the
 * value green/red; default is ink.
 */
export function MetricTile({ label, value, sentiment = "neutral", sub, align = "center", style, ...rest }) {
  const colors = {
    positive: "var(--color-up)",
    negative: "var(--color-down)",
    neutral: "var(--color-text)",
  };
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: align === "center" ? "center" : "flex-start",
        gap: 4,
        padding: "10px 8px",
        ...style,
      }}
      {...rest}
    >
      <span
        style={{
          fontFamily: "var(--font-sans)",
          fontSize: "var(--text-sm)",
          fontWeight: "var(--weight-medium)",
          color: "var(--color-text-muted)",
        }}
      >
        {label}
      </span>
      <span
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "var(--text-md)",
          fontWeight: "var(--weight-medium)",
          fontVariantNumeric: "tabular-nums",
          color: colors[sentiment] || colors.neutral,
          textAlign: align === "center" ? "center" : "left",
          lineHeight: 1.35,
        }}
      >
        {value}
      </span>
      {sub && (
        <span style={{ fontFamily: "var(--font-mono)", fontSize: "var(--text-2xs)", color: "var(--color-text-faint)" }}>
          {sub}
        </span>
      )}
    </div>
  );
}
