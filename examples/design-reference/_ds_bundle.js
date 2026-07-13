/* @ds-bundle: {"format":4,"namespace":"EmberDesignSystem_fc1096","components":[{"name":"Avatar","sourcePath":"components/agent/Avatar.jsx"},{"name":"ChatBubble","sourcePath":"components/agent/ChatBubble.jsx"},{"name":"MandateCard","sourcePath":"components/agent/MandateCard.jsx"},{"name":"SwarmAgentRow","sourcePath":"components/agent/SwarmAgentRow.jsx"},{"name":"ToolCallRow","sourcePath":"components/agent/ToolCallRow.jsx"},{"name":"Button","sourcePath":"components/buttons/Button.jsx"},{"name":"IconButton","sourcePath":"components/buttons/IconButton.jsx"},{"name":"MetricTile","sourcePath":"components/data/MetricTile.jsx"},{"name":"ProgressBar","sourcePath":"components/data/ProgressBar.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Tab","sourcePath":"components/navigation/Tab.jsx"},{"name":"WatchlistRow","sourcePath":"components/navigation/WatchlistRow.jsx"},{"name":"Badge","sourcePath":"components/surfaces/Badge.jsx"},{"name":"Card","sourcePath":"components/surfaces/Card.jsx"},{"name":"Chip","sourcePath":"components/surfaces/Chip.jsx"}],"sourceHashes":{"components/agent/Avatar.jsx":"a57e56284927","components/agent/ChatBubble.jsx":"1f8b70ff4dba","components/agent/MandateCard.jsx":"54e8c6f58b48","components/agent/SwarmAgentRow.jsx":"063e43eaeef3","components/agent/ToolCallRow.jsx":"5a342a842331","components/buttons/Button.jsx":"3bdc327f202f","components/buttons/IconButton.jsx":"68bdeffe91ba","components/data/MetricTile.jsx":"2cf69a9119c1","components/data/ProgressBar.jsx":"848ee2610317","components/forms/Input.jsx":"a42330abccdd","components/navigation/Tab.jsx":"ecb6e8bf098e","components/navigation/WatchlistRow.jsx":"8d4abbaba38e","components/surfaces/Badge.jsx":"f26f372b41b9","components/surfaces/Card.jsx":"f88dbe84979f","components/surfaces/Chip.jsx":"22e675591c6d","ui_kits/console/Analyst.jsx":"20bd6590ff99","ui_kits/console/Workbench.jsx":"52a1c83fbab4","ui_kits/console/data.jsx":"3fe809c32fee","ui_kits/console/icons.jsx":"f423c5830a5a"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.EmberDesignSystem_fc1096 = window.EmberDesignSystem_fc1096 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/agent/Avatar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Avatar. `role="agent"` renders the helm mark (ink rounded square with a
 * mono glyph); `role="user"` renders the neutral gray circle with an
 * initial, as in the workbench's account row.
 */
function Avatar({
  role = "agent",
  size = 28,
  children,
  style,
  ...rest
}) {
  const isAgent = role === "agent";
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
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
      ...style
    }
  }, rest), children ?? (isAgent ? "h" : "U"));
}
Object.assign(__ds_scope, { Avatar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/agent/Avatar.jsx", error: String((e && e.message) || e) }); }

// components/agent/ChatBubble.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * One turn in the analyst thread. `role="user"` renders the question as a
 * quiet gray rounded block (full width); `role="agent"` renders plain rich
 * text — bold the lead sentence yourself, as the analyst does.
 */
function ChatBubble({
  role = "agent",
  timestamp,
  children,
  style,
  ...rest
}) {
  if (role === "user") {
    return /*#__PURE__*/React.createElement("div", _extends({
      style: {
        borderRadius: "var(--radius-xl)",
        border: "1px solid var(--color-border)",
        background: "var(--color-panel)",
        padding: "12px 16px",
        fontFamily: "var(--font-sans)",
        fontSize: "var(--text-base)",
        lineHeight: "var(--leading-relaxed)",
        color: "var(--color-text)",
        ...style
      }
    }, rest), children, timestamp && /*#__PURE__*/React.createElement("span", {
      style: {
        display: "block",
        fontFamily: "var(--font-mono)",
        fontSize: "var(--text-2xs)",
        color: "var(--color-text-faint)",
        marginTop: 6
      }
    }, timestamp));
  }
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-base)",
      lineHeight: "var(--leading-relaxed)",
      color: "var(--color-text)",
      ...style
    }
  }, rest), children, timestamp && /*#__PURE__*/React.createElement("span", {
    style: {
      display: "block",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-2xs)",
      color: "var(--color-text-faint)",
      marginTop: 8
    }
  }, timestamp));
}
Object.assign(__ds_scope, { ChatBubble });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/agent/ChatBubble.jsx", error: String((e && e.message) || e) }); }

// components/agent/ToolCallRow.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * A collapsed tool-call / reasoning row in the analyst thread — the gray
 * rounded rows labeled with a wrench ("Get Financials") or a chevron
 * ("Thought"). `kind="thought"` renders the quieter chevron variant.
 */
function ToolCallRow({
  label,
  kind = "tool",
  detail,
  onClick,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const isThought = kind === "thought";
  if (isThought) {
    return /*#__PURE__*/React.createElement("div", _extends({
      onClick: onClick,
      onMouseEnter: () => setHover(true),
      onMouseLeave: () => setHover(false),
      style: {
        display: "flex",
        alignItems: "center",
        gap: 7,
        padding: "4px 2px",
        fontFamily: "var(--font-sans)",
        fontSize: "var(--text-base)",
        color: hover && onClick ? "var(--color-text)" : "var(--color-text-2)",
        cursor: onClick ? "pointer" : "default",
        ...style
      }
    }, rest), /*#__PURE__*/React.createElement("svg", {
      width: "14",
      height: "14",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: "currentColor",
      strokeWidth: "2",
      strokeLinecap: "round",
      strokeLinejoin: "round"
    }, /*#__PURE__*/React.createElement("polyline", {
      points: "9 18 15 12 9 6"
    })), /*#__PURE__*/React.createElement("span", null, label || "Thought"), detail && /*#__PURE__*/React.createElement("span", {
      style: {
        color: "var(--color-text-faint)",
        fontSize: "var(--text-sm)"
      }
    }, detail));
  }
  return /*#__PURE__*/React.createElement("div", _extends({
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
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
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("svg", {
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round",
    style: {
      color: "var(--color-text-muted)",
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("path", {
    d: "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"
  })), /*#__PURE__*/React.createElement("span", null, label), detail && /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-xs)",
      color: "var(--color-text-faint)",
      fontWeight: 400
    }
  }, detail));
}
Object.assign(__ds_scope, { ToolCallRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/agent/ToolCallRow.jsx", error: String((e && e.message) || e) }); }

// components/buttons/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Helm action button. Light workbench hierarchy: `primary` is ink-black,
 * `secondary` is a white bordered button, `ghost` is quiet text,
 * `danger` is the red destructive treatment.
 */
function Button({
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
    sm: {
      padding: "0 12px",
      height: 30,
      fontSize: "var(--text-sm)",
      gap: 6
    },
    md: {
      padding: "0 16px",
      height: 36,
      fontSize: "var(--text-base)",
      gap: 7
    },
    lg: {
      padding: "0 22px",
      height: 44,
      fontSize: "var(--text-md)",
      gap: 8
    }
  };
  const s = sizes[size] || sizes.md;
  const variants = {
    primary: {
      background: "var(--color-primary)",
      color: "var(--color-primary-fg)",
      border: "1px solid var(--color-primary)"
    },
    secondary: {
      background: "var(--color-surface)",
      color: "var(--color-text)",
      border: "1px solid var(--color-border-strong)"
    },
    ghost: {
      background: "transparent",
      color: "var(--color-text-muted)",
      border: "1px solid transparent"
    },
    danger: {
      background: "var(--color-danger-soft)",
      color: "var(--color-danger)",
      border: "1px solid hsl(3 50% 82%)"
    }
  };
  const v = variants[variant] || variants.primary;
  const [hover, setHover] = React.useState(false);
  const hoverStyle = !disabled && hover ? variant === "primary" ? {
    background: "var(--color-primary-hover)",
    borderColor: "var(--color-primary-hover)"
  } : variant === "ghost" ? {
    background: "var(--color-panel)",
    color: "var(--color-text)"
  } : variant === "danger" ? {
    background: "hsl(3 70% 93%)"
  } : {
    background: "var(--color-panel)"
  } : {};
  return /*#__PURE__*/React.createElement("button", _extends({
    disabled: disabled || loading,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
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
      ...style
    }
  }, rest), loading ? /*#__PURE__*/React.createElement(Spinner, null) : icon, children, iconRight);
}
function Spinner() {
  return /*#__PURE__*/React.createElement("span", {
    "aria-hidden": true,
    style: {
      width: 13,
      height: 13,
      borderRadius: "50%",
      border: "2px solid currentColor",
      borderTopColor: "transparent",
      display: "inline-block",
      animation: "helm-spin 0.7s linear infinite"
    }
  });
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/buttons/Button.jsx", error: String((e && e.message) || e) }); }

// components/agent/MandateCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * A trading-mandate tile — the consent surface Hermes proposes before any
 * live order. White card, hairline border (green when active), mono values.
 */
function MandateCard({
  ordinal = 1,
  label = "Balanced",
  universe = "US equities",
  maxOrder = "$5,000",
  dailyCap = "10 trades/day",
  leverage = "no leverage",
  notes,
  active = false,
  onCommit,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const row = (dt, dd, mono = true) => /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-xs)",
      color: "var(--color-text-muted)"
    }
  }, dt), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text)",
      fontFamily: mono ? "var(--font-mono)" : "var(--font-sans)",
      fontVariantNumeric: "tabular-nums"
    }
  }, dd));
  return /*#__PURE__*/React.createElement("div", _extends({
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      borderRadius: "var(--radius-lg)",
      padding: 14,
      border: `1px solid ${active ? "var(--color-accent-hairline)" : hover ? "var(--color-border-strong)" : "var(--color-border)"}`,
      background: active ? "var(--color-accent-soft)" : "var(--color-surface)",
      transition: "border-color var(--duration-base) var(--ease-standard)",
      fontFamily: "var(--font-sans)",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      marginBottom: 12
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 20,
      height: 20,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      borderRadius: "var(--radius-sm)",
      background: active ? "var(--color-accent)" : "var(--color-panel-hover)",
      color: active ? "#fff" : "var(--color-text-muted)",
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-xs)",
      fontWeight: "var(--weight-semibold)"
    }
  }, ordinal), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-base)",
      fontWeight: "var(--weight-semibold)",
      color: "var(--color-text)"
    }
  }, label)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: "10px 12px",
      marginBottom: notes ? 10 : 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      gridColumn: "1 / -1"
    }
  }, row("Universe", universe, false)), row("Max order", maxOrder), row("Daily cap", dailyCap), row("Leverage", leverage, false)), notes && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "0 0 14px",
      fontSize: "var(--text-sm)",
      lineHeight: "var(--leading-relaxed)",
      color: "var(--color-text-muted)"
    }
  }, notes), /*#__PURE__*/React.createElement(__ds_scope.Button, {
    size: "sm",
    fullWidth: true,
    variant: active ? "primary" : "secondary",
    onClick: onCommit
  }, "Commit \u201C", label, "\u201D"));
}
Object.assign(__ds_scope, { MandateCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/agent/MandateCard.jsx", error: String((e && e.message) || e) }); }

// components/buttons/IconButton.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Square, icon-only button for workbench chrome — tab closes, refresh,
 * sidebar controls. Pass a lucide icon node as children.
 */
function IconButton({
  size = "md",
  variant = "ghost",
  active = false,
  disabled = false,
  title,
  children,
  style,
  ...rest
}) {
  const dims = {
    sm: 24,
    md: 30,
    lg: 36
  }[size] || 30;
  const [hover, setHover] = React.useState(false);
  const base = variant === "solid" ? {
    background: "var(--color-primary)",
    color: "var(--color-primary-fg)"
  } : active ? {
    background: "var(--color-panel-hover)",
    color: "var(--color-text)"
  } : {
    background: "transparent",
    color: "var(--color-text-muted)"
  };
  const hoverStyle = !disabled && hover && variant !== "solid" && !active ? {
    background: "var(--color-panel)",
    color: "var(--color-text)"
  } : {};
  return /*#__PURE__*/React.createElement("button", _extends({
    title: title,
    "aria-label": title,
    disabled: disabled,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
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
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { IconButton });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/buttons/IconButton.jsx", error: String((e && e.message) || e) }); }

// components/data/MetricTile.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * A single stat cell — small gray label above a mono value, as in the
 * workbench's stat grids ("Prev Close / $294.38"). `sentiment` colors the
 * value green/red; default is ink.
 */
function MetricTile({
  label,
  value,
  sentiment = "neutral",
  sub,
  align = "center",
  style,
  ...rest
}) {
  const colors = {
    positive: "var(--color-up)",
    negative: "var(--color-down)",
    neutral: "var(--color-text)"
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      flexDirection: "column",
      alignItems: align === "center" ? "center" : "flex-start",
      gap: 4,
      padding: "10px 8px",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text-muted)"
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-md)",
      fontWeight: "var(--weight-medium)",
      fontVariantNumeric: "tabular-nums",
      color: colors[sentiment] || colors.neutral,
      textAlign: align === "center" ? "center" : "left",
      lineHeight: 1.35
    }
  }, value), sub && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-2xs)",
      color: "var(--color-text-faint)"
    }
  }, sub));
}
Object.assign(__ds_scope, { MetricTile });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/MetricTile.jsx", error: String((e && e.message) || e) }); }

// components/data/ProgressBar.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Determinate progress / distribution bar. Default green fill on a panel
 * track; used for run progress, budget meters, and consensus distributions.
 */
function ProgressBar({
  current = 0,
  total = 100,
  tone = "accent",
  height = "sm",
  showCount = false,
  style,
  ...rest
}) {
  const pct = total > 0 ? Math.min(100, Math.max(0, current / total * 100)) : 0;
  const h = {
    xs: 4,
    sm: 6,
    md: 10
  }[height] || 6;
  const fills = {
    accent: "var(--color-accent)",
    ink: "var(--color-primary)",
    danger: "var(--color-danger)",
    warning: "var(--color-warning)",
    info: "var(--color-info)"
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      height: h,
      borderRadius: "var(--radius-full)",
      background: "var(--color-panel-hover)",
      overflow: "hidden"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: `${pct}%`,
      height: "100%",
      borderRadius: "var(--radius-full)",
      background: fills[tone] || fills.accent,
      transition: "width var(--duration-slow) var(--ease-out)"
    }
  })), showCount && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--font-mono)",
      fontSize: "var(--text-2xs)",
      color: "var(--color-text-muted)",
      fontVariantNumeric: "tabular-nums",
      whiteSpace: "nowrap"
    }
  }, current, "/", total));
}
Object.assign(__ds_scope, { ProgressBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/ProgressBar.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Text input in the workbench's quiet style: white fill, hairline border,
 * subtle ink focus. Optional leading icon, label, hint / error.
 */
function Input({
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
  const h = {
    sm: 32,
    md: 38,
    lg: 44
  }[size] || 38;
  return /*#__PURE__*/React.createElement("label", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 6,
      fontFamily: "var(--font-sans)"
    }
  }, label && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text-2)"
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      height: h,
      padding: "0 12px",
      borderRadius: "var(--radius-md)",
      background: "var(--color-surface)",
      border: `1px solid ${error ? "var(--color-danger)" : focus ? "var(--color-border-strong)" : "var(--color-border)"}`,
      boxShadow: focus && !error ? "0 0 0 3px var(--color-panel-hover)" : "none",
      transition: "border-color var(--duration-fast) var(--ease-standard), box-shadow var(--duration-fast) var(--ease-standard)"
    }
  }, icon && /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--color-text-faint)",
      display: "inline-flex"
    }
  }, icon), /*#__PURE__*/React.createElement("input", _extends({
    onFocus: () => setFocus(true),
    onBlur: () => setFocus(false),
    style: {
      flex: 1,
      minWidth: 0,
      border: "none",
      outline: "none",
      background: "transparent",
      color: "var(--color-text)",
      fontFamily: mono ? "var(--font-mono)" : "var(--font-sans)",
      fontSize: "var(--text-base)",
      ...style
    }
  }, rest))), (hint || error) && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-xs)",
      color: error ? "var(--color-danger)" : "var(--color-text-faint)"
    }
  }, error || hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/navigation/Tab.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Browser-style workspace tab from the tab strip. Active tab: white fill
 * with an ink top bar; inactive: transparent with muted text. Includes an
 * optional close ×.
 */
function Tab({
  label,
  icon,
  active = false,
  onClose,
  onClick,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", _extends({
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
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
      ...style
    }
  }, rest), active && /*#__PURE__*/React.createElement("span", {
    style: {
      position: "absolute",
      top: 0,
      left: 0,
      right: 0,
      height: 2,
      background: "var(--color-primary)"
    }
  }), icon && /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      color: active ? "var(--color-text-2)" : "var(--color-text-faint)"
    }
  }, icon), /*#__PURE__*/React.createElement("span", null, label), onClose && /*#__PURE__*/React.createElement("span", {
    onClick: e => {
      e.stopPropagation();
      onClose();
    },
    style: {
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      width: 18,
      height: 18,
      borderRadius: 4,
      color: "var(--color-text-faint)"
    },
    onMouseEnter: e => {
      e.currentTarget.style.background = "var(--color-panel-hover)";
      e.currentTarget.style.color = "var(--color-text)";
    },
    onMouseLeave: e => {
      e.currentTarget.style.background = "transparent";
      e.currentTarget.style.color = "var(--color-text-faint)";
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "11",
    height: "11",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2.4",
    strokeLinecap: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M18 6 6 18M6 6l12 12"
  }))));
}
Object.assign(__ds_scope, { Tab });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/Tab.jsx", error: String((e && e.message) || e) }); }

// components/navigation/WatchlistRow.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * One row in the Explorer watchlist — icon + mono ticker symbol. Selected
 * rows get the quiet gray fill. Optional right-aligned change figure.
 */
function WatchlistRow({
  symbol,
  icon,
  selected = false,
  change,
  changeDirection,
  onClick,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", _extends({
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
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
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("span", {
    style: {
      display: "inline-flex",
      color: "var(--color-text-muted)",
      flexShrink: 0
    }
  }, icon ?? /*#__PURE__*/React.createElement("svg", {
    width: "15",
    height: "15",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M3 21h18M4 18h16M6 18V9M10 18V9M14 18V9M18 18V9M12 3 2 9h20L12 3z"
  }))), /*#__PURE__*/React.createElement("span", null, symbol), change && /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto",
      fontSize: "var(--text-xs)",
      color: changeDirection === "down" ? "var(--color-down)" : "var(--color-up)",
      fontVariantNumeric: "tabular-nums"
    }
  }, change));
}
Object.assign(__ds_scope, { WatchlistRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/WatchlistRow.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Small status badge. `tone` maps to the workbench's semantic palette —
 * "Buy" consensus is `success`, bearish counts are `danger`, entity pills
 * are `info`. Rounded-rectangle, soft tint fill.
 */
function Badge({
  tone = "neutral",
  dot = false,
  icon,
  mono = false,
  children,
  style,
  ...rest
}) {
  const tones = {
    neutral: {
      bg: "var(--color-panel-hover)",
      fg: "var(--color-text-2)"
    },
    success: {
      bg: "var(--color-success-soft)",
      fg: "var(--color-success)"
    },
    danger: {
      bg: "var(--color-danger-soft)",
      fg: "var(--color-danger)"
    },
    warning: {
      bg: "var(--color-warning-soft)",
      fg: "var(--color-warning)"
    },
    info: {
      bg: "var(--color-info-soft)",
      fg: "var(--color-info)"
    },
    ink: {
      bg: "var(--color-primary)",
      fg: "var(--color-primary-fg)"
    }
  };
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 5,
      padding: "3px 9px",
      borderRadius: "var(--radius-sm)",
      background: t.bg,
      color: t.fg,
      fontFamily: mono ? "var(--font-mono)" : "var(--font-sans)",
      fontSize: "var(--text-xs)",
      fontWeight: "var(--weight-semibold)",
      lineHeight: 1.5,
      whiteSpace: "nowrap",
      fontVariantNumeric: "tabular-nums",
      ...style
    }
  }, rest), dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: "50%",
      background: "currentColor"
    }
  }), icon, children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/Badge.jsx", error: String((e && e.message) || e) }); }

// components/agent/SwarmAgentRow.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Live status row for one agent in a Hermes desk run. Light-workbench
 * styling: sans name, mono tool/time, soft status badge.
 */
function SwarmAgentRow({
  name,
  role,
  status = "waiting",
  tool,
  elapsed,
  iterations,
  output,
  style,
  ...rest
}) {
  const toneMap = {
    done: "success",
    failed: "danger",
    blocked: "warning",
    retry: "info",
    running: "ink",
    waiting: "neutral",
    cancelled: "neutral"
  };
  const cell = {
    fontFamily: "var(--font-mono)",
    fontSize: "var(--text-xs)",
    color: "var(--color-text-muted)",
    fontVariantNumeric: "tabular-nums"
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "grid",
      gridTemplateColumns: "9.5rem 6.5rem 9rem 4.5rem minmax(0,1fr)",
      gap: 10,
      alignItems: "center",
      padding: "9px 0",
      borderBottom: "1px solid var(--color-border)",
      ...style
    }
  }, rest), /*#__PURE__*/React.createElement("div", {
    style: {
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      color: "var(--color-text)",
      overflow: "hidden",
      textOverflow: "ellipsis",
      whiteSpace: "nowrap"
    }
  }, name), role && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: "var(--text-2xs)",
      color: "var(--color-text-faint)",
      overflow: "hidden",
      textOverflow: "ellipsis",
      whiteSpace: "nowrap"
    }
  }, role)), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(__ds_scope.Badge, {
    tone: toneMap[status] || "neutral",
    style: {
      textTransform: "capitalize"
    }
  }, status)), /*#__PURE__*/React.createElement("div", {
    style: {
      ...cell,
      overflow: "hidden",
      textOverflow: "ellipsis",
      whiteSpace: "nowrap"
    },
    title: tool
  }, tool || "—"), /*#__PURE__*/React.createElement("div", {
    style: {
      ...cell,
      textAlign: "right"
    }
  }, elapsed || "—"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: "var(--font-sans)",
      fontSize: "var(--text-sm)",
      color: "var(--color-text-muted)",
      overflow: "hidden",
      textOverflow: "ellipsis",
      whiteSpace: "nowrap"
    },
    title: output
  }, output || "—"));
}
Object.assign(__ds_scope, { SwarmAgentRow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/agent/SwarmAgentRow.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Helm surface card. `default` is a quiet gray panel (the workbench's main
 * container, as in stat blocks and consensus cards); `white` is a white card
 * on gray ground; `accent` adds the green hairline for agent proposals;
 * `ghost` is border-only.
 */
function Card({
  tone = "default",
  raised = false,
  padding = "md",
  interactive = false,
  children,
  style,
  ...rest
}) {
  const pad = {
    none: 0,
    sm: 12,
    md: 16,
    lg: 24
  }[padding] ?? 16;
  const [hover, setHover] = React.useState(false);
  const tones = {
    default: {
      background: "var(--color-panel)",
      border: "1px solid var(--color-border)"
    },
    white: {
      background: "var(--color-surface)",
      border: "1px solid var(--color-border)"
    },
    accent: {
      background: "var(--color-surface)",
      border: "1px solid var(--color-accent-hairline)"
    },
    ghost: {
      background: "transparent",
      border: "1px solid var(--color-border)"
    }
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      borderRadius: "var(--radius-lg)",
      padding: pad,
      boxShadow: raised ? "var(--shadow-sm)" : "none",
      transition: "border-color var(--duration-base) var(--ease-standard), background var(--duration-base) var(--ease-standard)",
      ...tones[tone],
      ...(interactive && hover ? {
        borderColor: "var(--color-border-strong)",
        background: "var(--color-panel-hover)"
      } : {}),
      ...style
    }
  }, rest), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/Card.jsx", error: String((e && e.message) || e) }); }

// components/surfaces/Chip.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Entity / filter chip — the inline pill used for tickers inside prose
 * (blue tint + icon) and for selectable filters. Set `tone="entity"` for
 * the blue ticker-mention style; `selected` for an active filter.
 */
function Chip({
  selected = false,
  tone = "default",
  icon,
  children,
  onClick,
  style,
  ...rest
}) {
  const [hover, setHover] = React.useState(false);
  const clickable = !!onClick;
  const isEntity = tone === "entity";
  return /*#__PURE__*/React.createElement("span", _extends({
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 5,
      padding: isEntity ? "1px 7px" : "5px 12px",
      borderRadius: "var(--radius-sm)",
      border: isEntity ? "1px solid hsl(217 60% 86%)" : selected ? "1px solid var(--color-border-strong)" : "1px solid var(--color-border)",
      background: isEntity ? "var(--color-link-soft)" : selected ? "var(--color-panel-hover)" : clickable && hover ? "var(--color-panel)" : "var(--color-surface)",
      color: isEntity ? "var(--color-link)" : selected ? "var(--color-text)" : "var(--color-text-muted)",
      fontFamily: isEntity ? "var(--font-mono)" : "var(--font-sans)",
      fontSize: isEntity ? "var(--text-sm)" : "var(--text-sm)",
      fontWeight: "var(--weight-medium)",
      lineHeight: 1.4,
      cursor: clickable ? "pointer" : "default",
      transition: "background var(--duration-fast) var(--ease-standard), border-color var(--duration-fast) var(--ease-standard)",
      whiteSpace: "nowrap",
      verticalAlign: "baseline",
      ...style
    }
  }, rest), icon, children);
}
Object.assign(__ds_scope, { Chip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/surfaces/Chip.jsx", error: String((e && e.message) || e) }); }

// ui_kits/console/Analyst.jsx
try { (() => {
/* Right-hand analyst panel: chat tabs, thread with tool calls, Hermes
   mandate flow on send. Exposes window.AnalystPanel. */
const {
  Tab,
  ChatBubble,
  ToolCallRow,
  Chip,
  Badge,
  MandateCard,
  MetricTile
} = window.EmberDesignSystem_fc1096;
const AIcons = window.Icons;
const BankSm = /*#__PURE__*/React.createElement("svg", {
  width: "12",
  height: "12",
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: "2",
  strokeLinecap: "round",
  strokeLinejoin: "round"
}, /*#__PURE__*/React.createElement("path", {
  d: "M3 21h18M4 18h16M6 18V9M10 18V9M14 18V9M18 18V9M12 3 2 9h20L12 3z"
}));
function DefaultThread() {
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(ChatBubble, {
    role: "user"
  }, "How does ", /*#__PURE__*/React.createElement(Chip, {
    tone: "entity",
    icon: BankSm
  }, "NVDA"), "\u2019s gross margin compare to AMD\u2019s over the last 4 quarters, and what\u2019s driving the gap?"), /*#__PURE__*/React.createElement(ToolCallRow, {
    kind: "thought",
    label: "Thought",
    onClick: () => {}
  }), /*#__PURE__*/React.createElement(ToolCallRow, {
    label: "Get Financials",
    onClick: () => {}
  }), /*#__PURE__*/React.createElement(ToolCallRow, {
    label: "Get Financials",
    onClick: () => {}
  }), /*#__PURE__*/React.createElement(ChatBubble, {
    role: "agent"
  }, /*#__PURE__*/React.createElement("div", {
    className: "prose"
  }, /*#__PURE__*/React.createElement("p", null, /*#__PURE__*/React.createElement("strong", null, "NVDA\u2019s gross margin has run 20\u201325 points above AMD\u2019s"), " over the trailing four quarters, averaging roughly 75% versus AMD\u2019s low-50s."), /*#__PURE__*/React.createElement("p", null, "The gap is mostly mix and pricing power:"), /*#__PURE__*/React.createElement("ul", null, /*#__PURE__*/React.createElement("li", null, "NVDA\u2019s data-center GPUs (Blackwell/Hopper) carry premium ASPs with limited near-term competition."), /*#__PURE__*/React.createElement("li", null, "AMD\u2019s Instinct MI-series is priced more aggressively to win share, and a larger share of AMD revenue still comes from lower-margin client and gaming.")))));
}
function HermesRun({
  step,
  onCommit,
  committed
}) {
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(ChatBubble, {
    role: "user"
  }, "Run a momentum strategy on my watchlist and keep risk under 8%."), step >= 1 && /*#__PURE__*/React.createElement(ToolCallRow, {
    kind: "thought",
    label: "Thought",
    onClick: () => {}
  }), step >= 2 && /*#__PURE__*/React.createElement(ToolCallRow, {
    label: "Assemble desk",
    detail: step > 2 ? "4 agents" : undefined,
    onClick: () => {}
  }), step >= 3 && /*#__PURE__*/React.createElement(ToolCallRow, {
    label: "Run Backtest",
    detail: step > 3 ? "5y · 2 markets" : undefined,
    onClick: () => {}
  }), step >= 4 && /*#__PURE__*/React.createElement(ChatBubble, {
    role: "agent"
  }, /*#__PURE__*/React.createElement("div", {
    className: "prose"
  }, /*#__PURE__*/React.createElement("p", null, /*#__PURE__*/React.createElement("strong", null, "The desk converged on a cross-sectional momentum tilt"), " with a volatility-target overlay \u2014 Sharpe 1.92 over five years, max drawdown 8.1%."), /*#__PURE__*/React.createElement("p", null, "Before anything trades live, commit a mandate. These are hard limits Hermes enforces on every order:")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gap: 10,
      marginTop: 12
    }
  }, /*#__PURE__*/React.createElement(MandateCard, {
    ordinal: 1,
    label: "Conservative",
    universe: "Watchlist (mega-cap)",
    maxOrder: "$2,500",
    dailyCap: "4 trades/day",
    leverage: "no leverage",
    onCommit: onCommit
  }), /*#__PURE__*/React.createElement(MandateCard, {
    ordinal: 2,
    label: "Balanced",
    universe: "Watchlist",
    maxOrder: "$5,000",
    dailyCap: "10 trades/day",
    leverage: "no leverage",
    active: true,
    notes: "Fits the stated 8% risk cap.",
    onCommit: onCommit
  }))), committed && /*#__PURE__*/React.createElement(ChatBubble, {
    role: "agent"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 10
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "success",
    dot: true
  }, "Mandate active \xB7 \u2264$5,000/order \xB7 10/day \xB7 expires 7d")), /*#__PURE__*/React.createElement("div", {
    className: "prose"
  }, /*#__PURE__*/React.createElement("p", null, "Committed. Hermes is running it \u2014 it re-backtests against live fills nightly and will draft any refinement as a diff for your approval. Nothing changes without your sign-off.")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "repeat(3,1fr)",
      border: "1px solid var(--color-border)",
      borderRadius: "var(--radius-lg)",
      background: "var(--color-panel)",
      overflow: "hidden",
      marginTop: 12
    }
  }, /*#__PURE__*/React.createElement(MetricTile, {
    label: "Return (5y)",
    value: "+18.4%",
    sentiment: "positive"
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "Sharpe",
    value: "1.92"
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "Max DD",
    value: "-8.1%",
    sentiment: "negative"
  }))), step > 0 && step < 4 && /*#__PURE__*/React.createElement("span", {
    className: "thinkdots",
    style: {
      padding: "2px 2px"
    }
  }, /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("span", null)));
}
function AnalystPanel() {
  const [mode, setMode] = React.useState("default"); // default | hermes
  const [step, setStep] = React.useState(0);
  const [committed, setCommitted] = React.useState(false);
  const [draft, setDraft] = React.useState("");
  const threadRef = React.useRef(null);
  const startRun = () => {
    if (!draft.trim()) return;
    setMode("hermes");
    setStep(0);
    setCommitted(false);
    setDraft("");
    [1, 2, 3, 4].forEach((s, i) => setTimeout(() => setStep(s), 700 * (i + 1)));
  };
  React.useEffect(() => {
    if (threadRef.current) threadRef.current.scrollTop = threadRef.current.scrollHeight;
  }, [step, committed, mode]);
  return /*#__PURE__*/React.createElement("aside", {
    className: "analyst"
  }, /*#__PURE__*/React.createElement("div", {
    className: "tabstrip",
    style: {
      borderBottom: "1px solid var(--color-border)"
    }
  }, /*#__PURE__*/React.createElement(Tab, {
    label: mode === "hermes" ? "Momentum run" : "NVDA vs AMD m…",
    icon: AIcons.msg(13),
    active: true,
    onClose: () => {}
  }), /*#__PURE__*/React.createElement(Tab, {
    label: "AAPL thesis",
    icon: AIcons.msg(13)
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      padding: "0 10px",
      marginLeft: "auto",
      color: "var(--color-text-muted)",
      cursor: "pointer"
    }
  }, AIcons.plus(15))), /*#__PURE__*/React.createElement("div", {
    className: "thread",
    ref: threadRef
  }, mode === "default" ? /*#__PURE__*/React.createElement(DefaultThread, null) : /*#__PURE__*/React.createElement(HermesRun, {
    step: step,
    committed: committed,
    onCommit: () => setCommitted(true)
  })), /*#__PURE__*/React.createElement("div", {
    className: "composer"
  }, /*#__PURE__*/React.createElement("div", {
    className: "cbox"
  }, /*#__PURE__*/React.createElement("textarea", {
    rows: "2",
    placeholder: "Ask your analyst\u2026 / for skills, @ for context",
    value: draft,
    onChange: e => setDraft(e.target.value),
    onKeyDown: e => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        startRun();
      }
    }
  }), /*#__PURE__*/React.createElement("div", {
    className: "crow"
  }, /*#__PURE__*/React.createElement("span", {
    className: "cmodel"
  }, "hermes"), /*#__PURE__*/React.createElement("button", {
    className: "send",
    disabled: !draft.trim(),
    onClick: startRun
  }, AIcons.arrowUp(15))))));
}
window.AnalystPanel = AnalystPanel;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/console/Analyst.jsx", error: String((e && e.message) || e) }); }

// ui_kits/console/Workbench.jsx
try { (() => {
/* helm Workbench — main shell: sidebar, tab strip, ticker page. */
const {
  Tab,
  WatchlistRow,
  Badge,
  MetricTile,
  IconButton
} = window.EmberDesignSystem_fc1096;
const I = window.Icons;
const DATA = window.HelmData;
const RANGES = ["1D", "1M", "6M", "1Y", "5Y"];
function PriceChart({
  ticker,
  range
}) {
  const t = DATA[ticker];
  const seedOffset = RANGES.indexOf(range) * 5;
  const pts = window.helmSeries(t.seed + seedOffset, t.dir === "down" && range !== "1D" ? -0.3 : t.drift);
  const w = 620,
    h = 210;
  const step = w / (pts.length - 1);
  const line = pts.map((v, i) => `${(i * step).toFixed(1)},${(h - v / 100 * h).toFixed(1)}`).join(" ");
  const up = t.dir === "up";
  const stroke = up ? "var(--color-chart)" : "var(--color-down)";
  return /*#__PURE__*/React.createElement("svg", {
    viewBox: `0 0 ${w} ${h}`,
    preserveAspectRatio: "none",
    style: {
      width: "100%",
      height: 210,
      display: "block"
    }
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: `fill-${ticker}`,
    x1: "0",
    y1: "0",
    x2: "0",
    y2: "1"
  }, /*#__PURE__*/React.createElement("stop", {
    offset: "0%",
    stopColor: up ? "hsl(152 50% 40% / .18)" : "hsl(3 62% 52% / .14)"
  }), /*#__PURE__*/React.createElement("stop", {
    offset: "100%",
    stopColor: "hsl(0 0% 100% / 0)"
  }))), /*#__PURE__*/React.createElement("polygon", {
    points: `0,${h} ${line} ${w},${h}`,
    fill: `url(#fill-${ticker})`
  }), /*#__PURE__*/React.createElement("polyline", {
    points: line,
    fill: "none",
    stroke: stroke,
    strokeWidth: "1.8"
  }));
}
function Consensus({
  c
}) {
  const total = c.bearish + c.neutral + c.bullish;
  const tickCount = 80;
  const bearTicks = Math.round(c.bearish / total * tickCount);
  const neutTicks = Math.round(c.neutral / total * tickCount);
  const labels = ["Str. Sell", "Sell", "Hold", "Buy", "Str. Buy"];
  const pos = v => v;
  return /*#__PURE__*/React.createElement("div", {
    className: "panelcard"
  }, /*#__PURE__*/React.createElement("div", {
    className: "pchead"
  }, "Analyst consensus"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: c.label === "Buy" ? "success" : "neutral",
    style: {
      fontSize: "var(--text-base)",
      padding: "5px 14px"
    }
  }, c.label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: "var(--text-sm)",
      color: "var(--color-text-muted)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-mono"
  }, c.analysts), " analysts")), /*#__PURE__*/React.createElement("div", {
    className: "dist"
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--color-danger)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-mono"
  }, c.bearish), " Bearish"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--color-text-2)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-mono"
  }, c.neutral), " Neutral"), /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--color-success)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    className: "font-mono"
  }, c.bullish), " Bullish")), /*#__PURE__*/React.createElement("div", {
    className: "ticks"
  }, Array.from({
    length: tickCount
  }).map((_, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      flex: 1,
      height: i % 5 === 0 ? 14 : 10,
      borderRadius: 1,
      background: i < bearTicks ? "hsl(3 62% 52% / .65)" : i < bearTicks + neutTicks ? "var(--color-border-strong)" : "hsl(152 55% 32% / .6)"
    }
  }))), /*#__PURE__*/React.createElement("div", {
    className: "ratings"
  }, c.counts.map((n, i) => /*#__PURE__*/React.createElement("div", {
    className: "rcell",
    key: i
  }, /*#__PURE__*/React.createElement("div", {
    className: "rnum",
    style: {
      color: i < 2 ? n > 0 ? "var(--color-danger)" : "var(--color-text-faint)" : i > 2 ? "var(--color-success)" : "var(--color-text)"
    }
  }, n), /*#__PURE__*/React.createElement("div", {
    className: "rlbl"
  }, labels[i])))), /*#__PURE__*/React.createElement("div", {
    className: "targetbar"
  }, /*#__PURE__*/React.createElement("span", {
    className: "knob",
    style: {
      left: "30%"
    },
    title: "Current"
  }), /*#__PURE__*/React.createElement("span", {
    className: "knob avg",
    style: {
      left: "55%"
    },
    title: "Average"
  })), /*#__PURE__*/React.createElement("div", {
    className: "tlabels"
  }, /*#__PURE__*/React.createElement("span", null, c.low), /*#__PURE__*/React.createElement("span", null, c.current), /*#__PURE__*/React.createElement("span", {
    style: {
      color: "var(--color-accent)",
      fontWeight: 600
    }
  }, c.avg, " ", c.avgPct), /*#__PURE__*/React.createElement("span", null, c.high)), /*#__PURE__*/React.createElement("div", {
    className: "tsubl"
  }, /*#__PURE__*/React.createElement("span", null, "\u25CF Low"), /*#__PURE__*/React.createElement("span", null, "\u25CB Current"), /*#__PURE__*/React.createElement("span", null, "\u25C9 Average"), /*#__PURE__*/React.createElement("span", null, "\u25CF High")));
}
function TickerPage({
  ticker
}) {
  const t = DATA[ticker];
  const [range, setRange] = React.useState("1Y");
  const [subtab, setSubtab] = React.useState("Overview");
  const dirColor = t.dir === "up" ? "var(--color-up)" : "var(--color-down)";
  return /*#__PURE__*/React.createElement("div", {
    className: "page"
  }, /*#__PURE__*/React.createElement("div", {
    className: "thead"
  }, /*#__PURE__*/React.createElement("div", {
    className: "tlogo"
  }, t.letter), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "tname"
  }, t.name), /*#__PURE__*/React.createElement("div", {
    className: "tsub"
  }, t.symbol, " \xA0\xB7\xA0 ", t.exchange)), /*#__PURE__*/React.createElement("div", {
    className: "tprice"
  }, /*#__PURE__*/React.createElement("div", {
    className: "p"
  }, t.price), /*#__PURE__*/React.createElement("div", {
    className: "c"
  }, "Today ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: dirColor
    }
  }, t.today))), /*#__PURE__*/React.createElement(IconButton, {
    title: "Refresh",
    style: {
      marginTop: 4
    }
  }, I.refresh(15))), /*#__PURE__*/React.createElement("div", {
    className: "subnav"
  }, (t.kind === "crypto" ? ["Overview", "Markets", "On-chain", "Analysis", "Analytics"] : ["Overview", "Financials", "Earnings", "Holders", "Analysis", "Analytics"]).map(s => /*#__PURE__*/React.createElement("span", {
    key: s,
    className: "subtab" + (subtab === s ? " on" : ""),
    onClick: () => setSubtab(s)
  }, s)), /*#__PURE__*/React.createElement("span", {
    className: "notes"
  }, I.file(14), " Notes")), /*#__PURE__*/React.createElement("div", {
    className: "cols"
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "chartcard"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "space-between"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "bigp"
  }, t.price), /*#__PURE__*/React.createElement("div", {
    className: "bigc",
    style: {
      color: dirColor
    }
  }, t.past), /*#__PURE__*/React.createElement("div", {
    className: "plabel"
  }, t.pastLabel)), /*#__PURE__*/React.createElement("div", {
    className: "ranges"
  }, RANGES.map(r => /*#__PURE__*/React.createElement("span", {
    key: r,
    className: "rbtn" + (range === r ? " on" : ""),
    onClick: () => setRange(r)
  }, r)))), /*#__PURE__*/React.createElement(PriceChart, {
    ticker: ticker,
    range: range
  })), /*#__PURE__*/React.createElement("div", {
    className: "statgrid"
  }, t.stats.map(([k, v]) => /*#__PURE__*/React.createElement(MetricTile, {
    key: k,
    label: k,
    value: v
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 22
    }
  }, /*#__PURE__*/React.createElement(Consensus, {
    c: t.consensus
  }))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    className: "facts"
  }, t.facts.map(([k, v]) => /*#__PURE__*/React.createElement("div", {
    className: "frow",
    key: k
  }, /*#__PURE__*/React.createElement("span", {
    className: "fk"
  }, k), /*#__PURE__*/React.createElement("span", {
    className: "fv"
  }, k === "Website" ? /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 5
    }
  }, v, " ", I.external(11)) : v)))), /*#__PURE__*/React.createElement("p", {
    className: "about"
  }, t.about))));
}
function App() {
  const [ticker, setTicker] = React.useState("AAPL");
  const tickers = Object.keys(DATA);
  return /*#__PURE__*/React.createElement("div", {
    className: "app"
  }, /*#__PURE__*/React.createElement("aside", {
    className: "side"
  }, /*#__PURE__*/React.createElement("div", {
    className: "brand"
  }, "helm"), /*#__PURE__*/React.createElement("nav", {
    className: "nav"
  }, /*#__PURE__*/React.createElement("div", {
    className: "navitem"
  }, I.dollar(16), " Portfolio"), /*#__PURE__*/React.createElement("div", {
    className: "navitem"
  }, I.target(16), " Monitors"), /*#__PURE__*/React.createElement("div", {
    className: "navitem"
  }, I.zap(16), " Skills")), /*#__PURE__*/React.createElement("div", {
    className: "sechead"
  }, "Explorer"), /*#__PURE__*/React.createElement("div", {
    className: "group"
  }, I.chevDown(13), " Watchlist"), /*#__PURE__*/React.createElement("div", {
    className: "watch"
  }, tickers.concat(["MSFT", "GOOGL"]).map(s => /*#__PURE__*/React.createElement(WatchlistRow, {
    key: s,
    symbol: s,
    icon: DATA[s] && DATA[s].kind === "crypto" ? I.coins(15) : undefined,
    selected: ticker === s,
    onClick: () => DATA[s] && setTicker(s),
    style: !DATA[s] ? {
      opacity: 0.55
    } : undefined
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sfoot"
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 22,
      height: 22,
      borderRadius: "50%",
      background: "var(--color-panel-hover)",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 11,
      color: "var(--color-text-muted)"
    }
  }, "D"), "hi@helm.trade", /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: "auto",
      color: "var(--color-text-faint)"
    }
  }, I.chevUp(13)))), /*#__PURE__*/React.createElement("main", {
    className: "center"
  }, /*#__PURE__*/React.createElement("div", {
    className: "tabstrip"
  }, /*#__PURE__*/React.createElement(Tab, {
    label: ticker,
    icon: DATA[ticker].kind === "crypto" ? I.coins(13) : I.landmark(13),
    active: true,
    onClose: () => {}
  })), /*#__PURE__*/React.createElement("div", {
    className: "content"
  }, /*#__PURE__*/React.createElement(TickerPage, {
    ticker: ticker,
    key: ticker
  }))), /*#__PURE__*/React.createElement(window.AnalystPanel, null));
}

/* Mount only when running as the actual workbench page: the compiler also
   rides this file along inside _ds_bundle.js, where window.HelmData and the
   page scaffolding don't exist — stay inert there. */
if (window.HelmData && document.getElementById("root") && !window.__helmWorkbenchMounted) {
  window.__helmWorkbenchMounted = true;
  ReactDOM.createRoot(document.getElementById("root")).render(/*#__PURE__*/React.createElement(App, null));
}
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/console/Workbench.jsx", error: String((e && e.message) || e) }); }

// ui_kits/console/data.jsx
try { (() => {
/* Static demo data for the helm workbench kit. */
window.HelmData = {
  AAPL: {
    name: "Apple Inc.",
    symbol: "AAPL",
    exchange: "NASDAQ",
    letter: "A",
    price: "$305.24",
    today: "+$10.86 (+3.69%)",
    dir: "up",
    past: "+$92.69 (+43.63%)",
    pastLabel: "Past year",
    seed: 7,
    drift: 0.55,
    stats: [["Prev Close", "$294.38"], ["Market Cap", "$4.48T"], ["Open", "$294.09"], ["P/E Ratio", "35.51"], ["Day Range", "$293.68 – $306.64"], ["Dividend Yield", "0.4%"]],
    facts: [["Symbol", "AAPL"], ["IPO Date", "Dec 12, 1980"], ["CEO", "Timothy D. Cook"], ["Full-time Employees", "166000"], ["Sector", "Technology"], ["Industry", "Consumer Electronics"], ["Country", "US"], ["Exchange", "NASDAQ"], ["Website", "www.apple.com"]],
    about: "Apple Inc. is a global technology corporation that specializes in the conceptualization, production, and sale of a diverse suite of electronic devices. Its comprehensive hardware lineup features the well-known iPhone smartphones, Mac personal computers, and versatile iPad tablets.",
    consensus: {
      label: "Buy",
      analysts: 111,
      bearish: 7,
      neutral: 34,
      bullish: 70,
      counts: [0, 7, 34, 69, 1],
      low: "$253.00",
      current: "$305.24",
      avg: "$327.00",
      avgPct: "+7.13%",
      high: "$400.00"
    }
  },
  NVDA: {
    name: "NVIDIA Corp.",
    symbol: "NVDA",
    exchange: "NASDAQ",
    letter: "N",
    price: "$1,204.55",
    today: "+$28.40 (+2.41%)",
    dir: "up",
    past: "+$512.10 (+73.95%)",
    pastLabel: "Past year",
    seed: 3,
    drift: 0.75,
    stats: [["Prev Close", "$1,176.15"], ["Market Cap", "$2.96T"], ["Open", "$1,180.00"], ["P/E Ratio", "72.40"], ["Day Range", "$1,171.30 – $1,208.88"], ["Dividend Yield", "0.02%"]],
    facts: [["Symbol", "NVDA"], ["IPO Date", "Jan 22, 1999"], ["CEO", "Jensen Huang"], ["Full-time Employees", "29600"], ["Sector", "Technology"], ["Industry", "Semiconductors"], ["Country", "US"], ["Exchange", "NASDAQ"], ["Website", "www.nvidia.com"]],
    about: "NVIDIA Corporation designs and supplies graphics processing units, systems-on-chip, and full-stack accelerated computing platforms. Its data-center GPUs power the large-scale training and inference behind modern AI systems.",
    consensus: {
      label: "Buy",
      analysts: 64,
      bearish: 2,
      neutral: 8,
      bullish: 54,
      counts: [0, 2, 8, 46, 8],
      low: "$900.00",
      current: "$1,204.55",
      avg: "$1,310.00",
      avgPct: "+8.75%",
      high: "$1,500.00"
    }
  },
  TSLA: {
    name: "Tesla, Inc.",
    symbol: "TSLA",
    exchange: "NASDAQ",
    letter: "T",
    price: "$188.02",
    today: "-$4.11 (-2.14%)",
    dir: "down",
    past: "-$52.60 (-21.86%)",
    pastLabel: "Past year",
    seed: 11,
    drift: -0.3,
    stats: [["Prev Close", "$192.13"], ["Market Cap", "$599B"], ["Open", "$191.80"], ["P/E Ratio", "47.20"], ["Day Range", "$186.40 – $193.10"], ["Dividend Yield", "—"]],
    facts: [["Symbol", "TSLA"], ["IPO Date", "Jun 29, 2010"], ["CEO", "Elon Musk"], ["Full-time Employees", "140473"], ["Sector", "Consumer Cyclical"], ["Industry", "Auto Manufacturers"], ["Country", "US"], ["Exchange", "NASDAQ"], ["Website", "www.tesla.com"]],
    about: "Tesla, Inc. designs, manufactures and sells fully electric vehicles, energy generation and storage systems, and related services, alongside its autonomous-driving software programs.",
    consensus: {
      label: "Hold",
      analysts: 52,
      bearish: 14,
      neutral: 24,
      bullish: 14,
      counts: [4, 10, 24, 12, 2],
      low: "$120.00",
      current: "$188.02",
      avg: "$196.00",
      avgPct: "+4.24%",
      high: "$310.00"
    }
  },
  RELIANCE: {
    name: "Reliance Industries",
    symbol: "RELIANCE",
    exchange: "NSE",
    letter: "R",
    price: "₹2,904.15",
    today: "+₹31.20 (+1.09%)",
    dir: "up",
    past: "+₹412.80 (+16.57%)",
    pastLabel: "Past year",
    seed: 5,
    drift: 0.4,
    stats: [["Prev Close", "₹2,872.95"], ["Market Cap", "₹19.65L Cr"], ["Open", "₹2,880.00"], ["P/E Ratio", "28.40"], ["Day Range", "₹2,868.10 – ₹2,912.40"], ["Dividend Yield", "0.34%"]],
    facts: [["Symbol", "RELIANCE"], ["Listed", "Nov 29, 1977"], ["Chairman", "Mukesh D. Ambani"], ["Full-time Employees", "347362"], ["Sector", "Energy / Conglomerate"], ["Industry", "Oil & Gas Refining"], ["Country", "IN"], ["Exchange", "NSE · BSE"], ["Website", "www.ril.com"]],
    about: "Reliance Industries is India's largest private-sector conglomerate, spanning oil-to-chemicals, retail, and digital services. Jio Platforms and Reliance Retail drive its consumer businesses alongside the legacy energy franchise.",
    consensus: {
      label: "Buy",
      analysts: 38,
      bearish: 3,
      neutral: 12,
      bullish: 23,
      counts: [1, 2, 12, 20, 3],
      low: "₹2,400.00",
      current: "₹2,904.15",
      avg: "₹3,150.00",
      avgPct: "+8.47%",
      high: "₹3,500.00"
    }
  },
  BTC: {
    kind: "crypto",
    name: "Bitcoin",
    symbol: "BTC/USD",
    exchange: "Crypto · 24/7",
    letter: "B",
    price: "$118,240",
    today: "+$2,110 (+1.82%)",
    dir: "up",
    past: "+$46,380 (+64.55%)",
    pastLabel: "Past year",
    seed: 13,
    drift: 0.6,
    stats: [["24h Low", "$114,890"], ["Market Cap", "$2.33T"], ["24h High", "$119,760"], ["24h Volume", "$48.2B"], ["Circulating", "19.71M BTC"], ["Dominance", "54.1%"]],
    facts: [["Pair", "BTC/USD"], ["Launched", "Jan 3, 2009"], ["Creator", "Satoshi Nakamoto"], ["Max Supply", "21M BTC"], ["Asset Class", "Cryptocurrency"], ["Consensus", "Proof of Work"], ["Market", "24/7"], ["Halving", "Apr 2028 (est.)"], ["Website", "bitcoin.org"]],
    about: "Bitcoin is the largest cryptocurrency by market capitalization — a decentralized, proof-of-work network whose fixed 21M supply underpins its store-of-value thesis. It trades continuously, 24/7, across global venues.",
    consensus: {
      label: "Buy",
      analysts: 24,
      bearish: 4,
      neutral: 8,
      bullish: 12,
      counts: [1, 3, 8, 10, 2],
      low: "$80,000",
      current: "$118,240",
      avg: "$135,000",
      avgPct: "+14.17%",
      high: "$180,000"
    }
  },
  ETH: {
    kind: "crypto",
    name: "Ethereum",
    symbol: "ETH/USD",
    exchange: "Crypto · 24/7",
    letter: "E",
    price: "$4,312.77",
    today: "-$66.20 (-1.51%)",
    dir: "down",
    past: "+$1,890.40 (+78.04%)",
    pastLabel: "Past year",
    seed: 17,
    drift: 0.5,
    stats: [["24h Low", "$4,268.10"], ["Market Cap", "$518.6B"], ["24h High", "$4,402.35"], ["24h Volume", "$21.7B"], ["Circulating", "120.3M ETH"], ["Staked", "28.9%"]],
    facts: [["Pair", "ETH/USD"], ["Launched", "Jul 30, 2015"], ["Creator", "Vitalik Buterin et al."], ["Max Supply", "— (burn-offset)"], ["Asset Class", "Cryptocurrency"], ["Consensus", "Proof of Stake"], ["Market", "24/7"], ["Gas (avg)", "4.2 gwei"], ["Website", "ethereum.org"]],
    about: "Ethereum is the leading smart-contract platform — the settlement layer for stablecoins, DeFi, and tokenized assets. Its proof-of-stake design pays staking yield while transaction fees burn supply.",
    consensus: {
      label: "Hold",
      analysts: 30,
      bearish: 6,
      neutral: 12,
      bullish: 12,
      counts: [2, 4, 12, 10, 2],
      low: "$3,000",
      current: "$4,312",
      avg: "$4,800",
      avgPct: "+11.30%",
      high: "$6,000"
    }
  }
};

/* Seeded random-walk series so charts are stable per ticker/range. */
window.helmSeries = function (seed, drift, n = 60) {
  let s = seed;
  const rnd = () => {
    s = (s * 16807 + 11) % 2147483647;
    return s % 1000 / 1000;
  };
  const pts = [50];
  for (let i = 1; i < n; i++) {
    pts.push(Math.max(6, Math.min(94, pts[i - 1] + (rnd() - 0.5 + drift * 0.09) * 7)));
  }
  return pts;
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/console/data.jsx", error: String((e && e.message) || e) }); }

// ui_kits/console/icons.jsx
try { (() => {
/* Lucide-style inline icon set for the helm workbench kit. 2px stroke. */
const svg = (children, size = 16) => /*#__PURE__*/React.createElement("svg", {
  width: size,
  height: size,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: "2",
  strokeLinecap: "round",
  strokeLinejoin: "round"
}, children);
window.Icons = {
  dollar: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("line", {
    x1: "12",
    y1: "2",
    x2: "12",
    y2: "22"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"
  })), s),
  target: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "10"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "6"
  }), /*#__PURE__*/React.createElement("circle", {
    cx: "12",
    cy: "12",
    r: "2"
  })), s),
  zap: s => svg(/*#__PURE__*/React.createElement("path", {
    d: "M13 2 3 14h9l-1 8 10-12h-9l1-8z"
  }), s),
  landmark: s => svg(/*#__PURE__*/React.createElement("path", {
    d: "M3 21h18M4 18h16M6 18V9M10 18V9M14 18V9M18 18V9M12 3 2 9h20L12 3z"
  }), s),
  chevDown: s => svg(/*#__PURE__*/React.createElement("polyline", {
    points: "6 9 12 15 18 9"
  }), s),
  chevRight: s => svg(/*#__PURE__*/React.createElement("polyline", {
    points: "9 18 15 12 9 6"
  }), s),
  chevUp: s => svg(/*#__PURE__*/React.createElement("polyline", {
    points: "18 15 12 9 6 15"
  }), s),
  msg: s => svg(/*#__PURE__*/React.createElement("path", {
    d: "M7.9 20A9 9 0 1 0 4 16.1L2 22Z"
  }), s),
  plus: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("line", {
    x1: "12",
    y1: "5",
    x2: "12",
    y2: "19"
  }), /*#__PURE__*/React.createElement("line", {
    x1: "5",
    y1: "12",
    x2: "19",
    y2: "12"
  })), s),
  x: s => svg(/*#__PURE__*/React.createElement("path", {
    d: "M18 6 6 18M6 6l12 12"
  }), s),
  refresh: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
    d: "M3 12a9 9 0 0 1 15-6.7L21 8"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M21 3v5h-5"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M21 12a9 9 0 0 1-15 6.7L3 16"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M3 21v-5h5"
  })), s),
  file: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
    d: "M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M14 2v5h5"
  })), s),
  wrench: s => svg(/*#__PURE__*/React.createElement("path", {
    d: "M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"
  }), s),
  arrowUp: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("line", {
    x1: "12",
    y1: "19",
    x2: "12",
    y2: "5"
  }), /*#__PURE__*/React.createElement("polyline", {
    points: "5 12 12 5 19 12"
  })), s),
  external: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
    d: "M15 3h6v6"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M10 14 21 3"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"
  })), s),
  shield: s => svg(/*#__PURE__*/React.createElement("path", {
    d: "M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"
  }), s),
  coins: s => svg(/*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
    cx: "8",
    cy: "8",
    r: "6"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M18.09 10.37A6 6 0 1 1 10.34 18"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M7 6h1v4"
  }), /*#__PURE__*/React.createElement("path", {
    d: "m16.71 13.88.7.71-2.82 2.82"
  })), s)
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/console/icons.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Avatar = __ds_scope.Avatar;

__ds_ns.ChatBubble = __ds_scope.ChatBubble;

__ds_ns.MandateCard = __ds_scope.MandateCard;

__ds_ns.SwarmAgentRow = __ds_scope.SwarmAgentRow;

__ds_ns.ToolCallRow = __ds_scope.ToolCallRow;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.IconButton = __ds_scope.IconButton;

__ds_ns.MetricTile = __ds_scope.MetricTile;

__ds_ns.ProgressBar = __ds_scope.ProgressBar;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Tab = __ds_scope.Tab;

__ds_ns.WatchlistRow = __ds_scope.WatchlistRow;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Chip = __ds_scope.Chip;

})();
