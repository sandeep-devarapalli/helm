import React from "react";

/**
 * Text input in the workbench's quiet style: white fill, hairline border,
 * subtle ink focus. Optional leading icon, label, hint / error.
 */
export function Input({
  label,
  icon,
  hint,
  error,
  size = "md",
  mono = false,
  style,
  ...rest
}) {
  const [focus, setFocus] = React.useState(false);
  const h = { sm: 32, md: 38, lg: 44 }[size] || 38;

  return (
    <label style={{ display: "flex", flexDirection: "column", gap: 6, fontFamily: "var(--font-sans)" }}>
      {label && (
        <span style={{ fontSize: "var(--text-sm)", fontWeight: "var(--weight-medium)", color: "var(--color-text-2)" }}>
          {label}
        </span>
      )}
      <span
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          height: h,
          padding: "0 12px",
          borderRadius: "var(--radius-md)",
          background: "var(--color-surface)",
          border: `1px solid ${error ? "var(--color-danger)" : focus ? "var(--color-border-strong)" : "var(--color-border)"}`,
          boxShadow: focus && !error ? "0 0 0 3px var(--color-panel-hover)" : "none",
          transition: "border-color var(--duration-fast) var(--ease-standard), box-shadow var(--duration-fast) var(--ease-standard)",
        }}
      >
        {icon && <span style={{ color: "var(--color-text-faint)", display: "inline-flex" }}>{icon}</span>}
        <input
          onFocus={() => setFocus(true)}
          onBlur={() => setFocus(false)}
          style={{
            flex: 1,
            minWidth: 0,
            border: "none",
            outline: "none",
            background: "transparent",
            color: "var(--color-text)",
            fontFamily: mono ? "var(--font-mono)" : "var(--font-sans)",
            fontSize: "var(--text-base)",
            ...style,
          }}
          {...rest}
        />
      </span>
      {(hint || error) && (
        <span style={{ fontSize: "var(--text-xs)", color: error ? "var(--color-danger)" : "var(--color-text-faint)" }}>
          {error || hint}
        </span>
      )}
    </label>
  );
}
