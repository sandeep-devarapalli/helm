import React from "react";

/**
 * Entity / filter chip — the inline pill used for tickers inside prose
 * (blue tint + icon) and for selectable filters. Set `tone="entity"` for
 * the blue ticker-mention style; `selected` for an active filter.
 */
export function Chip({ selected = false, tone = "default", icon, children, onClick, style, ...rest }) {
  const [hover, setHover] = React.useState(false);
  const clickable = !!onClick;
  const isEntity = tone === "entity";
  return (
    <span
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 5,
        padding: isEntity ? "1px 7px" : "5px 12px",
        borderRadius: "var(--radius-sm)",
        border: isEntity
          ? "1px solid hsl(217 60% 86%)"
          : selected
            ? "1px solid var(--color-border-strong)"
            : "1px solid var(--color-border)",
        background: isEntity
          ? "var(--color-link-soft)"
          : selected
            ? "var(--color-panel-hover)"
            : clickable && hover
              ? "var(--color-panel)"
              : "var(--color-surface)",
        color: isEntity ? "var(--color-link)" : selected ? "var(--color-text)" : "var(--color-text-muted)",
        fontFamily: isEntity ? "var(--font-mono)" : "var(--font-sans)",
        fontSize: isEntity ? "var(--text-sm)" : "var(--text-sm)",
        fontWeight: "var(--weight-medium)",
        lineHeight: 1.4,
        cursor: clickable ? "pointer" : "default",
        transition: "background var(--duration-fast) var(--ease-standard), border-color var(--duration-fast) var(--ease-standard)",
        whiteSpace: "nowrap",
        verticalAlign: "baseline",
        ...style,
      }}
      {...rest}
    >
      {icon}
      {children}
    </span>
  );
}
