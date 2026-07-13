/* Right-hand analyst panel: chat tabs, thread with tool calls, Hermes
   mandate flow on send. Exposes window.AnalystPanel. */
const { Tab, ChatBubble, ToolCallRow, Chip, Badge, MandateCard, MetricTile } = window.EmberDesignSystem_fc1096;
const AIcons = window.Icons;

const BankSm = <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 21h18M4 18h16M6 18V9M10 18V9M14 18V9M18 18V9M12 3 2 9h20L12 3z"/></svg>;

function DefaultThread() {
  return (
    <>
      <ChatBubble role="user">
        How does <Chip tone="entity" icon={BankSm}>NVDA</Chip>&rsquo;s gross margin compare to AMD&rsquo;s over the last 4 quarters, and what&rsquo;s driving the gap?
      </ChatBubble>
      <ToolCallRow kind="thought" label="Thought" onClick={() => {}} />
      <ToolCallRow label="Get Financials" onClick={() => {}} />
      <ToolCallRow label="Get Financials" onClick={() => {}} />
      <ChatBubble role="agent">
        <div className="prose">
          <p><strong>NVDA&rsquo;s gross margin has run 20&ndash;25 points above AMD&rsquo;s</strong> over the trailing four quarters, averaging roughly 75% versus AMD&rsquo;s low-50s.</p>
          <p>The gap is mostly mix and pricing power:</p>
          <ul>
            <li>NVDA&rsquo;s data-center GPUs (Blackwell/Hopper) carry premium ASPs with limited near-term competition.</li>
            <li>AMD&rsquo;s Instinct MI-series is priced more aggressively to win share, and a larger share of AMD revenue still comes from lower-margin client and gaming.</li>
          </ul>
        </div>
      </ChatBubble>
    </>
  );
}

function HermesRun({ step, onCommit, committed }) {
  return (
    <>
      <ChatBubble role="user">
        Run a momentum strategy on my watchlist and keep risk under 8%.
      </ChatBubble>
      {step >= 1 && <ToolCallRow kind="thought" label="Thought" onClick={() => {}} />}
      {step >= 2 && <ToolCallRow label="Assemble desk" detail={step > 2 ? "4 agents" : undefined} onClick={() => {}} />}
      {step >= 3 && <ToolCallRow label="Run Backtest" detail={step > 3 ? "5y · 2 markets" : undefined} onClick={() => {}} />}
      {step >= 4 && (
        <ChatBubble role="agent">
          <div className="prose">
            <p><strong>The desk converged on a cross-sectional momentum tilt</strong> with a volatility-target overlay &mdash; Sharpe 1.92 over five years, max drawdown 8.1%.</p>
            <p>Before anything trades live, commit a mandate. These are hard limits Hermes enforces on every order:</p>
          </div>
          <div style={{ display: "grid", gap: 10, marginTop: 12 }}>
            <MandateCard ordinal={1} label="Conservative" universe="Watchlist (mega-cap)" maxOrder="$2,500" dailyCap="4 trades/day" leverage="no leverage" onCommit={onCommit} />
            <MandateCard ordinal={2} label="Balanced" universe="Watchlist" maxOrder="$5,000" dailyCap="10 trades/day" leverage="no leverage" active notes="Fits the stated 8% risk cap." onCommit={onCommit} />
          </div>
        </ChatBubble>
      )}
      {committed && (
        <ChatBubble role="agent">
          <div style={{ marginBottom: 10 }}>
            <Badge tone="success" dot>Mandate active · ≤$5,000/order · 10/day · expires 7d</Badge>
          </div>
          <div className="prose">
            <p>Committed. Hermes is running it &mdash; it re-backtests against live fills nightly and will draft any refinement as a diff for your approval. Nothing changes without your sign-off.</p>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", border: "1px solid var(--color-border)", borderRadius: "var(--radius-lg)", background: "var(--color-panel)", overflow: "hidden", marginTop: 12 }}>
            <MetricTile label="Return (5y)" value="+18.4%" sentiment="positive" />
            <MetricTile label="Sharpe" value="1.92" />
            <MetricTile label="Max DD" value="-8.1%" sentiment="negative" />
          </div>
        </ChatBubble>
      )}
      {step > 0 && step < 4 && (
        <span className="thinkdots" style={{ padding: "2px 2px" }}><span></span><span></span><span></span></span>
      )}
    </>
  );
}

function AnalystPanel() {
  const [mode, setMode] = React.useState("default"); // default | hermes
  const [step, setStep] = React.useState(0);
  const [committed, setCommitted] = React.useState(false);
  const [draft, setDraft] = React.useState("");
  const threadRef = React.useRef(null);

  const startRun = () => {
    if (!draft.trim()) return;
    setMode("hermes"); setStep(0); setCommitted(false); setDraft("");
    [1, 2, 3, 4].forEach((s, i) => setTimeout(() => setStep(s), 700 * (i + 1)));
  };

  React.useEffect(() => {
    if (threadRef.current) threadRef.current.scrollTop = threadRef.current.scrollHeight;
  }, [step, committed, mode]);

  return (
    <aside className="analyst">
      <div className="tabstrip" style={{ borderBottom: "1px solid var(--color-border)" }}>
        <Tab label={mode === "hermes" ? "Momentum run" : "NVDA vs AMD m…"} icon={AIcons.msg(13)} active onClose={() => {}} />
        <Tab label="AAPL thesis" icon={AIcons.msg(13)} />
        <div style={{ display: "flex", alignItems: "center", padding: "0 10px", marginLeft: "auto", color: "var(--color-text-muted)", cursor: "pointer" }}>{AIcons.plus(15)}</div>
      </div>

      <div className="thread" ref={threadRef}>
        {mode === "default"
          ? <DefaultThread />
          : <HermesRun step={step} committed={committed} onCommit={() => setCommitted(true)} />}
      </div>

      <div className="composer">
        <div className="cbox">
          <textarea
            rows="2"
            placeholder="Ask your analyst… / for skills, @ for context"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); startRun(); } }}
          />
          <div className="crow">
            <span className="cmodel">hermes</span>
            <button className="send" disabled={!draft.trim()} onClick={startRun}>{AIcons.arrowUp(15)}</button>
          </div>
        </div>
      </div>
    </aside>
  );
}

window.AnalystPanel = AnalystPanel;
