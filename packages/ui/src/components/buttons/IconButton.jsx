import React from "react";

/**
 * Square, icon-only button for workbench chrome — tab closes, refresh,
 * sidebar controls. Pass a lucide icon node as children.
 */
export function IconButton({
  size = "md",
  variant = "ghost",
  active = false,
  disabled = false,
  title,
  children,
  style,
  ...rest
}) {
  const dims = { sm: 24, md: 30, lg: 36 }[size] || 30;
  const [hover, setHover] = React.useState(false);

  const base =
    variant === "solid"
      ? { background: "var(--color-primary)", color: "var(--color-primary-fg)" }
      : active
        ? { background: "var(--color-panel-hover)", color: "var(--color-text)" }
        : { background: "transparent", color: "var(--color-text-muted)" };

  const hoverStyle = !disabled && hover && variant !== "solid" && !active
    ? { background: "var(--color-panel)", color: "var(--color-text)" }
    : {};

  return (
    <button
      title={title}
      aria-label={title}
      disabled={disabled}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        width: dims,
        height: dims,
        borderRadius: "var(--radius-sm)",
        border: "1px solid transparent",
        cursor: disabled ? "not-allowed" : "pointer",
        opacity: disabled ? 0.45 : 1,
        transition: "background var(--duration-fast) var(--ease-standard), color var(--duration-fast) var(--ease-standard)",
        ...base,
        ...hoverStyle,
        ...style,
      }}
      {...rest}
    >
      {children}
    </button>
  );
}
