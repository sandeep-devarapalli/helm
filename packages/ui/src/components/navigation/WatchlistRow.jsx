import React from "react";

/**
 * One row in the Explorer watchlist — icon + mono ticker symbol. Selected
 * rows get the quiet gray fill. Optional right-aligned change figure.
 */
export function WatchlistRow({ symbol, icon, selected = false, change, changeDirection, onClick, style, ...rest }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        alignItems: "center",
        gap: 10,
        padding: "7px 12px 7px 14px",
        background: selected ? "var(--color-panel-hover)" : hover ? "var(--color-panel)" : "transparent",
        color: selected ? "var(--color-text)" : "var(--color-text-2)",
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-base)",
        fontWeight: "var(--weight-medium)",
        cursor: "pointer",
        transition: "background var(--duration-fast) var(--ease-standard)",
        userSelect: "none",
        ...style,
      }}
      {...rest}
    >
      <span style={{ display: "inline-flex", color: "var(--color-text-muted)", flexShrink: 0 }}>
        {icon ?? (
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 21h18M4 18h16M6 18V9M10 18V9M14 18V9M18 18V9M12 3 2 9h20L12 3z" /></svg>
        )}
      </span>
      <span>{symbol}</span>
      {change && (
        <span style={{ marginLeft: "auto", fontSize: "var(--text-xs)", color: changeDirection === "down" ? "var(--color-down)" : "var(--color-up)", fontVariantNumeric: "tabular-nums" }}>
          {change}
        </span>
      )}
    </div>
  );
}
