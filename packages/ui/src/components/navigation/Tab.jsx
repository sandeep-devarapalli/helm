import React from "react";

/**
 * Browser-style workspace tab from the tab strip. Active tab: white fill
 * with an ink top bar; inactive: transparent with muted text. Includes an
 * optional close ×.
 */
export function Tab({ label, icon, active = false, onClose, onClick, style, ...rest }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        position: "relative",
        display: "inline-flex",
        alignItems: "center",
        gap: 8,
        height: "var(--tabbar-height)",
        padding: "0 12px 0 16px",
        background: active ? "var(--color-surface)" : hover ? "hsl(0 0% 100% / 0.55)" : "transparent",
        borderRight: "1px solid var(--color-border)",
        color: active ? "var(--color-text)" : "var(--color-text-muted)",
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-sm)",
        fontWeight: "var(--weight-medium)",
        cursor: "pointer",
        whiteSpace: "nowrap",
        userSelect: "none",
        ...style,
      }}
      {...rest}
    >
      {active && (
        <span style={{ position: "absolute", top: 0, left: 0, right: 0, height: 2, background: "var(--color-primary)" }} />
      )}
      {icon && <span style={{ display: "inline-flex", color: active ? "var(--color-text-2)" : "var(--color-text-faint)" }}>{icon}</span>}
      <span>{label}</span>
      {onClose && (
        <span
          onClick={(e) => { e.stopPropagation(); onClose(); }}
          style={{
            display: "inline-flex", alignItems: "center", justifyContent: "center",
            width: 18, height: 18, borderRadius: 4, color: "var(--color-text-faint)",
          }}
          onMouseEnter={(e) => { e.currentTarget.style.background = "var(--color-panel-hover)"; e.currentTarget.style.color = "var(--color-text)"; }}
          onMouseLeave={(e) => { e.currentTarget.style.background = "transparent"; e.currentTarget.style.color = "var(--color-text-faint)"; }}
        >
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
        </span>
      )}
    </div>
  );
}
