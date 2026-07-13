import { useEffect, useState } from "react";
import {
  Activity,
  Bot,
  ChartNoAxesCombined,
  CircleDollarSign,
  Database,
  FlaskConical,
  MessageSquare,
  PanelLeftClose,
  Search,
  ShieldCheck,
  Target,
} from "lucide-react";
import { Badge, Button, Card, ChatBubble, Chip, MetricTile, ToolCallRow } from "@helm/ui";

type HealthState = "checking" | "ready" | "unavailable";

const watchlist = [
  { symbol: "AAPL", venue: "NASDAQ", price: "$228.26", change: "+0.62%" },
  { symbol: "NVDA", venue: "NASDAQ", price: "$142.91", change: "+1.28%" },
  { symbol: "AMD", venue: "NASDAQ", price: "$156.74", change: "-0.31%" },
];

function useApiHealth() {
  const [state, setState] = useState<HealthState>("checking");

  useEffect(() => {
    const controller = new AbortController();
    fetch("/api/health", { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error("health check failed");
        setState("ready");
      })
      .catch((error: unknown) => {
        if (!(error instanceof DOMException && error.name === "AbortError")) setState("unavailable");
      });
    return () => controller.abort();
  }, []);

  return state;
}

function StatusBadge({ state }: { state: HealthState }) {
  if (state === "ready") return <Badge tone="success" dot>API ready</Badge>;
  if (state === "unavailable") return <Badge tone="warning" dot>API unavailable</Badge>;
  return <Badge dot>Checking API</Badge>;
}

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="wordmark">helm</div>
      <nav className="primary-nav" aria-label="Primary">
        <button className="nav-row active"><MessageSquare size={16} />Hermes</button>
        <button className="nav-row"><ChartNoAxesCombined size={16} />Research</button>
        <button className="nav-row"><FlaskConical size={16} />Strategies</button>
        <button className="nav-row"><ShieldCheck size={16} />Mandates</button>
        <button className="nav-row"><CircleDollarSign size={16} />Paper portfolio</button>
      </nav>

      <div className="section-label">Watchlist · fixture</div>
      <div className="watchlist">
        {watchlist.map((item, index) => (
          <button className={`watch-row ${index === 0 ? "selected" : ""}`} key={item.symbol}>
            <span>
              <strong>{item.symbol}</strong>
              <small>{item.venue}</small>
            </span>
            <span className="quote">
              <strong>{item.price}</strong>
              <small className={item.change.startsWith("+") ? "up" : "down"}>{item.change}</small>
            </span>
          </button>
        ))}
      </div>

      <div className="sidebar-foot">
        <Badge tone="warning">Paper trading only</Badge>
        <span>Foundation build</span>
      </div>
    </aside>
  );
}

function MarketWorkspace() {
  return (
    <main className="workspace">
      <header className="workspace-header">
        <button className="quiet-icon" aria-label="Collapse sidebar"><PanelLeftClose size={17} /></button>
        <div className="workspace-title">
          <strong>AAPL</strong>
          <span>Apple Inc. · NASDAQ</span>
        </div>
        <div className="market-price">
          <strong>$228.26</strong>
          <span>+$1.41 (+0.62%)</span>
        </div>
      </header>

      <div className="subnav" aria-label="Entity views">
        <button className="active">Overview</button>
        <button>Research</button>
        <button>Hypotheses</button>
        <button>Runs</button>
        <button>Audit</button>
      </div>

      <section className="workspace-body">
        <div className="foundation-note">
          <div>
            <span className="section-label">Stage 1 foundation</span>
            <h1>One operating surface for Hermes.</h1>
            <p>The shell, control-plane boundary, and upstream runtime configuration are in place. Research, market values, mandates, and execution remain explicitly inactive until their verified stages ship.</p>
          </div>
          <Badge tone="info">No live orders</Badge>
        </div>

        <div className="metrics" aria-label="Illustrative market fixture">
          <MetricTile label="Price fixture" value="$228.26" sub="Illustrative" />
          <MetricTile label="Day fixture" value="+0.62%" sentiment="positive" sub="Not live data" />
          <MetricTile label="Mandate" value="None" sub="Execution blocked" />
          <MetricTile label="Position" value="0 shares" sub="Paper account" />
        </div>

        <div className="operating-loop">
          <div className="section-heading">
            <div>
              <span className="section-label">Operating contract</span>
              <h2>Hermes reasons. helm enforces.</h2>
            </div>
            <Target size={20} />
          </div>
          <ol>
            <li className="complete"><span>01</span><div><strong>Understand</strong><small>Conversation and approved preferences</small></div></li>
            <li><span>02</span><div><strong>Research</strong><small>Curated finance tools and evidence</small></div></li>
            <li><span>03</span><div><strong>Validate</strong><small>Reproducible backtests and risk checks</small></div></li>
            <li><span>04</span><div><strong>Operate</strong><small>Only inside a committed mandate</small></div></li>
            <li><span>05</span><div><strong>Learn</strong><small>Every change waits for approval</small></div></li>
          </ol>
        </div>
      </section>
    </main>
  );
}

function HermesPanel({ health }: { health: HealthState }) {
  return (
    <aside className="hermes-panel">
      <header className="panel-header">
        <div><Bot size={17} /><strong>Hermes</strong></div>
        <StatusBadge state={health} />
      </header>
      <div className="thread">
        <ChatBubble role="user">
          Help me build a steady US-equity strategy with a maximum drawdown of 8%.
        </ChatBubble>
        <ToolCallRow kind="thought" label="Foundation preview" detail="inactive" />
        <ToolCallRow label="Vibe finance tools" detail="configured · not connected" />
        <ToolCallRow label="helm policy engine" detail="server-owned" />
        <ChatBubble role="agent">
          <div className="agent-answer">
            <p><strong>The operating boundary is ready, but no strategy has been researched or executed.</strong></p>
            <p>When the next stages are connected, I will gather evidence and propose a reproducible strategy. Nothing can trade until you commit a mandate, and policy enforcement remains outside my runtime.</p>
            <div className="answer-chips">
              <Chip>US equities</Chip>
              <Chip>Max drawdown 8%</Chip>
              <Chip>Approval required</Chip>
            </div>
          </div>
        </ChatBubble>
        <Card tone="accent" padding="md">
          <div className="boundary-card">
            <ShieldCheck size={18} />
            <div><strong>Execution is fail-closed</strong><span>No active mandate · no broker credentials · no order path</span></div>
          </div>
        </Card>
      </div>
      <div className="composer">
        <div className="composer-box">
          <textarea aria-label="Message Hermes" disabled placeholder="Hermes conversation activates in Stage 2" rows={2} />
          <div>
            <span><Database size={13} />No runtime session</span>
            <Button size="sm" disabled icon={<Activity size={14} />}>Send</Button>
          </div>
        </div>
      </div>
    </aside>
  );
}

export function App() {
  const health = useApiHealth();
  return (
    <div className="app-shell">
      <Sidebar />
      <MarketWorkspace />
      <HermesPanel health={health} />
      <button className="search-shortcut" aria-label="Search"><Search size={15} /><span>Search</span><kbd>⌘K</kbd></button>
    </div>
  );
}
