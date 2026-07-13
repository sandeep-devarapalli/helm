/* helm Workbench — main shell: sidebar, tab strip, ticker page. */
const { Tab, WatchlistRow, Badge, MetricTile, IconButton } = window.EmberDesignSystem_fc1096;
const I = window.Icons;
const DATA = window.HelmData;

const RANGES = ["1D", "1M", "6M", "1Y", "5Y"];

function PriceChart({ ticker, range }) {
  const t = DATA[ticker];
  const seedOffset = RANGES.indexOf(range) * 5;
  const pts = window.helmSeries(t.seed + seedOffset, t.dir === "down" && range !== "1D" ? -0.3 : t.drift);
  const w = 620, h = 210;
  const step = w / (pts.length - 1);
  const line = pts.map((v, i) => `${(i * step).toFixed(1)},${(h - (v / 100) * h).toFixed(1)}`).join(" ");
  const up = t.dir === "up";
  const stroke = up ? "var(--color-chart)" : "var(--color-down)";
  return (
    <svg viewBox={`0 0 ${w} ${h}`} preserveAspectRatio="none" style={{ width: "100%", height: 210, display: "block" }}>
      <defs>
        <linearGradient id={`fill-${ticker}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={up ? "hsl(152 50% 40% / .18)" : "hsl(3 62% 52% / .14)"} />
          <stop offset="100%" stopColor="hsl(0 0% 100% / 0)" />
        </linearGradient>
      </defs>
      <polygon points={`0,${h} ${line} ${w},${h}`} fill={`url(#fill-${ticker})`} />
      <polyline points={line} fill="none" stroke={stroke} strokeWidth="1.8" />
    </svg>
  );
}

function Consensus({ c }) {
  const total = c.bearish + c.neutral + c.bullish;
  const tickCount = 80;
  const bearTicks = Math.round((c.bearish / total) * tickCount);
  const neutTicks = Math.round((c.neutral / total) * tickCount);
  const labels = ["Str. Sell", "Sell", "Hold", "Buy", "Str. Buy"];
  const pos = (v) => v;
  return (
    <div className="panelcard">
      <div className="pchead">Analyst consensus</div>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
        <Badge tone={c.label === "Buy" ? "success" : "neutral"} style={{ fontSize: "var(--text-base)", padding: "5px 14px" }}>{c.label}</Badge>
        <span style={{ fontSize: "var(--text-sm)", color: "var(--color-text-muted)" }}><span className="font-mono">{c.analysts}</span> analysts</span>
      </div>
      <div className="dist">
        <span style={{ color: "var(--color-danger)" }}><span className="font-mono">{c.bearish}</span> Bearish</span>
        <span style={{ color: "var(--color-text-2)" }}><span className="font-mono">{c.neutral}</span> Neutral</span>
        <span style={{ color: "var(--color-success)" }}><span className="font-mono">{c.bullish}</span> Bullish</span>
      </div>
      <div className="ticks">
        {Array.from({ length: tickCount }).map((_, i) => (
          <span key={i} style={{
            flex: 1, height: i % 5 === 0 ? 14 : 10, borderRadius: 1,
            background: i < bearTicks ? "hsl(3 62% 52% / .65)" : i < bearTicks + neutTicks ? "var(--color-border-strong)" : "hsl(152 55% 32% / .6)",
          }} />
        ))}
      </div>
      <div className="ratings">
        {c.counts.map((n, i) => (
          <div className="rcell" key={i}>
            <div className="rnum" style={{ color: i < 2 ? (n > 0 ? "var(--color-danger)" : "var(--color-text-faint)") : i > 2 ? "var(--color-success)" : "var(--color-text)" }}>{n}</div>
            <div className="rlbl">{labels[i]}</div>
          </div>
        ))}
      </div>
      <div className="targetbar">
        <span className="knob" style={{ left: "30%" }} title="Current" />
        <span className="knob avg" style={{ left: "55%" }} title="Average" />
      </div>
      <div className="tlabels">
        <span>{c.low}</span><span>{c.current}</span><span style={{ color: "var(--color-accent)", fontWeight: 600 }}>{c.avg} {c.avgPct}</span><span>{c.high}</span>
      </div>
      <div className="tsubl">
        <span>● Low</span><span>○ Current</span><span>◉ Average</span><span>● High</span>
      </div>
    </div>
  );
}

function TickerPage({ ticker }) {
  const t = DATA[ticker];
  const [range, setRange] = React.useState("1Y");
  const [subtab, setSubtab] = React.useState("Overview");
  const dirColor = t.dir === "up" ? "var(--color-up)" : "var(--color-down)";
  return (
    <div className="page">
      <div className="thead">
        <div className="tlogo">{t.letter}</div>
        <div>
          <div className="tname">{t.name}</div>
          <div className="tsub">{t.symbol} &nbsp;·&nbsp; {t.exchange}</div>
        </div>
        <div className="tprice">
          <div className="p">{t.price}</div>
          <div className="c">Today <span style={{ color: dirColor }}>{t.today}</span></div>
        </div>
        <IconButton title="Refresh" style={{ marginTop: 4 }}>{I.refresh(15)}</IconButton>
      </div>

      <div className="subnav">
        {(t.kind === "crypto"
          ? ["Overview", "Markets", "On-chain", "Analysis", "Analytics"]
          : ["Overview", "Financials", "Earnings", "Holders", "Analysis", "Analytics"]
        ).map((s) => (
          <span key={s} className={"subtab" + (subtab === s ? " on" : "")} onClick={() => setSubtab(s)}>{s}</span>
        ))}
        <span className="notes">{I.file(14)} Notes</span>
      </div>

      <div className="cols">
        <div>
          <div className="chartcard">
            <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between" }}>
              <div>
                <div className="bigp">{t.price}</div>
                <div className="bigc" style={{ color: dirColor }}>{t.past}</div>
                <div className="plabel">{t.pastLabel}</div>
              </div>
              <div className="ranges">
                {RANGES.map((r) => (
                  <span key={r} className={"rbtn" + (range === r ? " on" : "")} onClick={() => setRange(r)}>{r}</span>
                ))}
              </div>
            </div>
            <PriceChart ticker={ticker} range={range} />
          </div>

          <div className="statgrid">
            {t.stats.map(([k, v]) => <MetricTile key={k} label={k} value={v} />)}
          </div>

          <div style={{ marginTop: 22 }}>
            <Consensus c={t.consensus} />
          </div>
        </div>

        <div>
          <div className="facts">
            {t.facts.map(([k, v]) => (
              <div className="frow" key={k}>
                <span className="fk">{k}</span>
                <span className="fv">{k === "Website" ? <a href="#" style={{ display: "inline-flex", alignItems: "center", gap: 5 }}>{v} {I.external(11)}</a> : v}</span>
              </div>
            ))}
          </div>
          <p className="about">{t.about}</p>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [ticker, setTicker] = React.useState("AAPL");
  const tickers = Object.keys(DATA);
  return (
    <div className="app">
      <aside className="side">
        <div className="brand">helm</div>
        <nav className="nav">
          <div className="navitem">{I.dollar(16)} Portfolio</div>
          <div className="navitem">{I.target(16)} Monitors</div>
          <div className="navitem">{I.zap(16)} Skills</div>
        </nav>
        <div className="sechead">Explorer</div>
        <div className="group">{I.chevDown(13)} Watchlist</div>
        <div className="watch">
          {tickers.concat(["MSFT", "GOOGL"]).map((s) => (
            <WatchlistRow
              key={s}
              symbol={s}
              icon={DATA[s] && DATA[s].kind === "crypto" ? I.coins(15) : undefined}
              selected={ticker === s}
              onClick={() => DATA[s] && setTicker(s)}
              style={!DATA[s] ? { opacity: 0.55 } : undefined}
            />
          ))}
        </div>
        <div className="sfoot">
          <span style={{ width: 22, height: 22, borderRadius: "50%", background: "var(--color-panel-hover)", display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 11, color: "var(--color-text-muted)" }}>D</span>
          hi@helm.trade
          <span style={{ marginLeft: "auto", color: "var(--color-text-faint)" }}>{I.chevUp(13)}</span>
        </div>
      </aside>

      <main className="center">
        <div className="tabstrip">
          <Tab label={ticker} icon={DATA[ticker].kind === "crypto" ? I.coins(13) : I.landmark(13)} active onClose={() => {}} />
        </div>
        <div className="content">
          <TickerPage ticker={ticker} key={ticker} />
        </div>
      </main>

      <window.AnalystPanel />
    </div>
  );
}

/* Mount only when running as the actual workbench page: the compiler also
   rides this file along inside _ds_bundle.js, where window.HelmData and the
   page scaffolding don't exist — stay inert there. */
if (window.HelmData && document.getElementById("root") && !window.__helmWorkbenchMounted) {
  window.__helmWorkbenchMounted = true;
  ReactDOM.createRoot(document.getElementById("root")).render(<App />);
}
