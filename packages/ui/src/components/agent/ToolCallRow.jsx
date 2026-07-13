import React from "react";

/**
 * A collapsed tool-call / reasoning row in the analyst thread — the gray
 * rounded rows labeled with a wrench ("Get Financials") or a chevron
 * ("Thought"). `kind="thought"` renders the quieter chevron variant.
 */
export function ToolCallRow({ label, kind = "tool", detail, onClick, style, ...rest }) {
  const [hover, setHover] = React.useState(false);
  const isThought = kind === "thought";

  if (isThought) {
    return (
      <div
        onClick={onClick}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        style={{
          display: "flex",
          alignItems: "center",
          gap: 7,
          padding: "4px 2px",
          fontFamily: "var(--font-sans)",
          fontSize: "var(--text-base)",
          color: hover && onClick ? "var(--color-text)" : "var(--color-text-2)",
          cursor: onClick ? "pointer" : "default",
          ...style,
        }}
        {...rest}
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 18 15 12 9 6" /></svg>
        <span>{label || "Thought"}</span>
        {detail && <span style={{ color: "var(--color-text-faint)", fontSize: "var(--text-sm)" }}>{detail}</span>}
      </div>
    );
  }

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "flex",
        alignItems: "center",
        gap: 9,
        padding: "9px 13px",
        borderRadius: "var(--radius-md)",
        border: "1px solid var(--color-border)",
        background: hover && onClick ? "var(--color-panel-hover)" : "var(--color-panel)",
        fontFamily: "var(--font-sans)",
        fontSize: "var(--text-base)",
        fontWeight: "var(--weight-medium)",
        color: "var(--color-text-2)",
        cursor: onClick ? "pointer" : "default",
        transition: "background var(--duration-fast) var(--ease-standard)",
        ...style,
      }}
      {...rest}
    >
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "var(--color-text-muted)", flexShrink: 0 }}>
        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" />
      </svg>
      <span>{label}</span>
      {detail && <span style={{ marginLeft: "auto", fontFamily: "var(--font-mono)", fontSize: "var(--text-xs)", color: "var(--color-text-faint)", fontWeight: 400 }}>{detail}</span>}
    </div>
  );
}
