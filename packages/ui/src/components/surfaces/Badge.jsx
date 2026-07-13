import React from "react";

/**
 * Small status badge. `tone` maps to the workbench's semantic palette —
 * "Buy" consensus is `success`, bearish counts are `danger`, entity pills
 * are `info`. Rounded-rectangle, soft tint fill.
 */
export function Badge({ tone = "neutral", dot = false, icon, mono = false, children, style, ...rest }) {
  const tones = {
    neutral: { bg: "var(--color-panel-hover)", fg: "var(--color-text-2)" },
    success: { bg: "var(--color-success-soft)", fg: "var(--color-success)" },
    danger: { bg: "var(--color-danger-soft)", fg: "var(--color-danger)" },
    warning: { bg: "var(--color-warning-soft)", fg: "var(--color-warning)" },
    info: { bg: "var(--color-info-soft)", fg: "var(--color-info)" },
    ink: { bg: "var(--color-primary)", fg: "var(--color-primary-fg)" },
  };
  const t = tones[tone] || tones.neutral;

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 5,
        padding: "3px 9px",
        borderRadius: "var(--radius-sm)",
        background: t.bg,
        color: t.fg,
        fontFamily: mono ? "var(--font-mono)" : "var(--font-sans)",
        fontSize: "var(--text-xs)",
        fontWeight: "var(--weight-semibold)",
        lineHeight: 1.5,
        whiteSpace: "nowrap",
        fontVariantNumeric: "tabular-nums",
        ...style,
      }}
      {...rest}
    >
      {dot && (
        <span style={{ width: 6, height: 6, borderRadius: "50%", background: "currentColor" }} />
      )}
      {icon}
      {children}
    </span>
  );
}
