import React from "react";

/**
 * One turn in the analyst thread. `role="user"` renders the question as a
 * quiet gray rounded block (full width); `role="agent"` renders plain rich
 * text — bold the lead sentence yourself, as the analyst does.
 */
export function ChatBubble({ role = "agent", timestamp, children, style, ...rest }) {
  if (role === "user") {
    return (
      <div
        style={{
          borderRadius: "var(--radius-xl)",
          border: "1px solid var(--color-border)",
          background: "var(--color-panel)",
          padding: "12px 16px",
          fontFamily: "var(--font-sans)",
          fontSize: "var(--text-base)",
          lineHeight: "var(--leading-relaxed)",
          color: "var(--color-text)",
          ...style,
        }}
        {...rest}
      >
        {children}
        {timestamp && (
          <span style={{ display: "block", fontFamily: "var(--font-mono)", fontSize: "var(--text-2xs)", color: "var(--color-text-faint)", marginTop: 6 }}>
            {timestamp}
          </span>
        )}
      </div>
    );
  }

  return (
    <div
      style={{
        fontFamily: "var(--font-sans)",
        fontSize: "var(--text-base)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-text)",
        ...style,
      }}
      {...rest}
    >
      {children}
      {timestamp && (
        <span style={{ display: "block", fontFamily: "var(--font-mono)", fontSize: "var(--text-2xs)", color: "var(--color-text-faint)", marginTop: 8 }}>
          {timestamp}
        </span>
      )}
    </div>
  );
}
