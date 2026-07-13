import React from "react";

/**
 * Avatar. `role="agent"` renders the helm mark (ink rounded square with a
 * mono glyph); `role="user"` renders the neutral gray circle with an
 * initial, as in the workbench's account row.
 */
export function Avatar({ role = "agent", size = 28, children, style, ...rest }) {
  const isAgent = role === "agent";
  return (
    <div
      style={{
        width: size,
        height: size,
        flexShrink: 0,
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: isAgent ? Math.round(size * 0.28) : "50%",
        background: isAgent ? "var(--color-primary)" : "var(--color-panel-hover)",
        color: isAgent ? "var(--color-primary-fg)" : "var(--color-text-muted)",
        fontFamily: "var(--font-mono)",
        fontWeight: "var(--weight-semibold)",
        fontSize: Math.round(size * 0.46),
        lineHeight: 1,
        ...style,
      }}
      {...rest}
    >
      {children ?? (isAgent ? "h" : "U")}
    </div>
  );
}
