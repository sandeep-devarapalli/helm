import React from "react";

/**
 * Helm action button. Light workbench hierarchy: `primary` is ink-black,
 * `secondary` is a white bordered button, `ghost` is quiet text,
 * `danger` is the red destructive treatment.
 */
export function Button({
  variant = "primary",
  size = "md",
  icon,
  iconRight,
  disabled = false,
  loading = false,
  fullWidth = false,
  children,
  style,
  ...rest
}) {
  const sizes = {
    sm: { padding: "0 12px", height: 30, fontSize: "var(--text-sm)", gap: 6 },
    md: { padding: "0 16px", height: 36, fontSize: "var(--text-base)", gap: 7 },
    lg: { padding: "0 22px", height: 44, fontSize: "var(--text-md)", gap: 8 },
  };
  const s = sizes[size] || sizes.md;

  const variants = {
    primary: {
      background: "var(--color-primary)",
      color: "var(--color-primary-fg)",
      border: "1px solid var(--color-primary)",
    },
    secondary: {
      background: "var(--color-surface)",
      color: "var(--color-text)",
      border: "1px solid var(--color-border-strong)",
    },
    ghost: {
      background: "transparent",
      color: "var(--color-text-muted)",
      border: "1px solid transparent",
    },
    danger: {
      background: "var(--color-danger-soft)",
      color: "var(--color-danger)",
      border: "1px solid hsl(3 50% 82%)",
    },
  };
  const v = variants[variant] || variants.primary;

  const [hover, setHover] = React.useState(false);
  const hoverStyle = !disabled && hover
    ? variant === "primary"
      ? { background: "var(--color-primary-hover)", borderColor: "var(--color-primary-hover)" }
      : variant === "ghost"
        ? { background: "var(--color-panel)", color: "var(--color-text)" }
        : variant === "danger"
          ? { background: "hsl(3 70% 93%)" }
          : { background: "var(--color-panel)" }
    : {};

  return (
    <button
      disabled={disabled || loading}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: s.gap,
        height: s.height,
        padding: s.padding,
        width: fullWidth ? "100%" : undefined,
        fontFamily: "var(--font-sans)",
        fontSize: s.fontSize,
        fontWeight: "var(--weight-medium)",
        lineHeight: 1,
        borderRadius: "var(--radius-md)",
        cursor: disabled || loading ? "not-allowed" : "pointer",
        opacity: disabled ? 0.45 : 1,
        transition: "background var(--duration-fast) var(--ease-standard), color var(--duration-fast) var(--ease-standard), border-color var(--duration-fast) var(--ease-standard)",
        whiteSpace: "nowrap",
        ...v,
        ...hoverStyle,
        ...style,
      }}
      {...rest}
    >
      {loading ? <Spinner /> : icon}
      {children}
      {iconRight}
    </button>
  );
}

function Spinner() {
  return (
    <span
      aria-hidden
      style={{
        width: 13,
        height: 13,
        borderRadius: "50%",
        border: "2px solid currentColor",
        borderTopColor: "transparent",
        display: "inline-block",
        animation: "helm-spin 0.7s linear infinite",
      }}
    />
  );
}
