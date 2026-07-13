import React from "react";
import { Button } from "../buttons/Button.jsx";

/**
 * A trading-mandate tile — the consent surface Hermes proposes before any
 * live order. White card, hairline border (green when active), mono values.
 */
export function MandateCard({
  ordinal = 1,
  label = "Balanced",
  universe = "US equities",
  maxOrder = "$5,000",
  dailyCap = "10 trades/day",
  leverage = "no leverage",
  notes,
  active = false,
  onCommit,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const row = (dt, dd, mono = true) => (
    <div>
      <div style={{ fontSize: "var(--text-xs)", color: "var(--color-text-muted)" }}>{dt}</div>
      <div style={{ fontSize: "var(--text-sm)", fontWeight: "var(--weight-medium)", color: "var(--color-text)", fontFamily: mono ? "var(--font-mono)" : "var(--font-sans)", fontVariantNumeric: "tabular-nums" }}>{dd}</div>
    </div>
  );

  return (
    <div
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        borderRadius: "var(--radius-lg)",
        padding: 14,
        border: `1px solid ${active ? "var(--color-accent-hairline)" : hover ? "var(--color-border-strong)" : "var(--color-border)"}`,
        background: active ? "var(--color-accent-soft)" : "var(--color-surface)",
        transition: "border-color var(--duration-base) var(--ease-standard)",
        fontFamily: "var(--font-sans)",
        ...style,
      }}
      {...rest}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 12 }}>
        <span
          style={{
            width: 20, height: 20, display: "inline-flex", alignItems: "center", justifyContent: "center",
            borderRadius: "var(--radius-sm)", background: active ? "var(--color-accent)" : "var(--color-panel-hover)",
            color: active ? "#fff" : "var(--color-text-muted)",
            fontFamily: "var(--font-mono)", fontSize: "var(--text-xs)", fontWeight: "var(--weight-semibold)",
          }}
        >
          {ordinal}
        </span>
        <span style={{ fontSize: "var(--text-base)", fontWeight: "var(--weight-semibold)", color: "var(--color-text)" }}>{label}</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px 12px", marginBottom: notes ? 10 : 14 }}>
        <div style={{ gridColumn: "1 / -1" }}>{row("Universe", universe, false)}</div>
        {row("Max order", maxOrder)}
        {row("Daily cap", dailyCap)}
        {row("Leverage", leverage, false)}
      </div>

      {notes && (
        <p style={{ margin: "0 0 14px", fontSize: "var(--text-sm)", lineHeight: "var(--leading-relaxed)", color: "var(--color-text-muted)" }}>{notes}</p>
      )}

      <Button size="sm" fullWidth variant={active ? "primary" : "secondary"} onClick={onCommit}>Commit &ldquo;{label}&rdquo;</Button>
    </div>
  );
}
