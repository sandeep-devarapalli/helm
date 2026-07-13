import React from "react";

/**
 * Helm surface card. `default` is a quiet gray panel (the workbench's main
 * container, as in stat blocks and consensus cards); `white` is a white card
 * on gray ground; `accent` adds the green hairline for agent proposals;
 * `ghost` is border-only.
 */
export function Card({
  tone = "default",
  raised = false,
  padding = "md",
  interactive = false,
  children,
  style,
  ...rest
}) {
  const pad = { none: 0, sm: 12, md: 16, lg: 24 }[padding] ?? 16;
  const [hover, setHover] = React.useState(false);

  const tones = {
    default: { background: "var(--color-panel)", border: "1px solid var(--color-border)" },
    white: { background: "var(--color-surface)", border: "1px solid var(--color-border)" },
    accent: { background: "var(--color-surface)", border: "1px solid var(--color-accent-hairline)" },
    ghost: { background: "transparent", border: "1px solid var(--color-border)" },
  };

  return (
    <div
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        borderRadius: "var(--radius-lg)",
        padding: pad,
        boxShadow: raised ? "var(--shadow-sm)" : "none",
        transition: "border-color var(--duration-base) var(--ease-standard), background var(--duration-base) var(--ease-standard)",
        ...tones[tone],
        ...(interactive && hover ? { borderColor: "var(--color-border-strong)", background: "var(--color-panel-hover)" } : {}),
        ...style,
      }}
      {...rest}
    >
      {children}
    </div>
  );
}
