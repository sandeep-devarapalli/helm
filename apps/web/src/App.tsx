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
import { Badge, Button, Card, ChatBubble, MetricTile } from "@helm/ui";
import {
  loadConversationView,
  type ConversationView,
  type RunRefreshState,
} from "./workbench-data";

type HealthState = "checking" | "ready" | "unavailable";

const workspaceIdPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

const watchlist = [
  { symbol: "AAPL", venue: "NASDAQ", price: "$228.26", change: "+0.62%" },
  { symbol: "NVDA", venue: "NASDAQ", price: "$142.91", change: "+1.28%" },
  { symbol: "AMD", venue: "NASDAQ", price: "$156.74", change: "-0.31%" },
];

function useConversationView(workspaceId: string | null): ConversationView {
  const [loadedResult, setLoadedResult] = useState<{
    workspaceId: string;
    view: ConversationView;
  } | null>(null);
  const workspaceIsValid = workspaceId !== null && workspaceIdPattern.test(workspaceId);

  useEffect(() => {
    if (!workspaceIsValid || workspaceId === null) return;
    const controller = new AbortController();
    loadConversationView(workspaceId, fetch, controller.signal)
      .then((view) => setLoadedResult({ workspaceId, view }))
      .catch((error: unknown) => {
        if (!(error instanceof Error && error.name === "AbortError")) {
          setLoadedResult({ workspaceId, view: { status: "unavailable" } });
        }
      });
    return () => controller.abort();
  }, [workspaceId, workspaceIsValid]);

  if (workspaceId === null) return { status: "context-required" };
  if (!workspaceIsValid) return { status: "invalid-context" };
  if (loadedResult?.workspaceId !== workspaceId) return { status: "loading" };
  return loadedResult.view;
}

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

function timestamp(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function RunBadge({ run }: { run: RunRefreshState | null }) {
  if (run === null) return <Badge>No run</Badge>;
  if (run.approval_blocked) return <Badge tone="warning" dot>Approval blocked</Badge>;
  if (run.status === "failed") return <Badge tone="danger" dot>Failed</Badge>;
  if (run.status === "succeeded" && run.event_stream_complete && !run.projection_gap) {
    return <Badge tone="success" dot>Succeeded</Badge>;
  }
  if (["queued", "submitting", "running"].includes(run.status)) {
    return <Badge tone="ink" dot>{run.status}</Badge>;
  }
  return <Badge tone="warning" dot>{run.status}</Badge>;
}

function runSummaries(run: RunRefreshState): string[] {
  const summaries: string[] = [];
  if (run.approval_blocked) {
    summaries.push(
      "Hermes requested an unsupported approval. helm stopped the run; nothing was executed.",
    );
  }
  if (run.status === "failed") {
    summaries.push("The run failed. Persisted events remain available; no order path exists.");
  }
  if (run.projection_gap || !run.event_stream_complete) {
    summaries.push(
      "The persisted projection is incomplete. Do not treat this transcript as a complete result.",
    );
  }
  if (run.status === "cancelled" && !run.approval_blocked) {
    summaries.push("The run was cancelled. Nothing was executed.");
  }
  if (summaries.length === 0) {
    summaries.push(`Terminal run persisted. Tool provenance is ${run.tool_provenance_status}.`);
  }
  return summaries;
}

function ThreadState({ view }: { view: ConversationView }) {
  if (view.status === "loading") {
    return <div className="thread-state" role="status"><strong>Loading persisted conversation</strong><span>Reading canonical helm state.</span></div>;
  }
  if (view.status === "context-required") {
    return <div className="thread-state"><strong>Workspace context required</strong><span>Open helm with <code>?workspace=&lt;uuid&gt;</code>. Contexts are never guessed or shared.</span></div>;
  }
  if (view.status === "invalid-context") {
    return <div className="thread-state"><strong>Workspace context is invalid</strong><span>Provide one canonical workspace UUID.</span></div>;
  }
  if (view.status === "unavailable") {
    return <div className="thread-state danger" role="alert"><strong>Conversation unavailable</strong><span>The persisted state could not be loaded. Nothing was submitted or retried.</span></div>;
  }
  if (view.status === "empty") {
    return <div className="thread-state"><strong>No persisted conversation</strong><span>This workspace has no conversation to display. Sending remains disabled.</span></div>;
  }

  return (
    <>
      <div className="conversation-meta">
        <div><span className="section-label">Persisted conversation</span><strong>{view.conversation.title ?? "Untitled conversation"}</strong></div>
        <div className="conversation-badges"><Badge tone="info">Read only</Badge>{view.partialHistory ? <Badge tone="warning">Partial history</Badge> : null}</div>
      </div>
      {view.messages.length === 0 ? (
        <div className="thread-state"><strong>No persisted messages</strong><span>The conversation exists, but its public transcript is empty.</span></div>
      ) : view.messages.map((message) => (
        <ChatBubble key={message.id} role={message.role === "assistant" ? "agent" : "user"} timestamp={timestamp(message.created_at)}>
          <p className="message-content">{message.content}</p>
        </ChatBubble>
      ))}
      <Card tone="ghost" padding="md">
        <div className="run-summary">
          <div><span className="section-label">Latest Hermes run</span><RunBadge run={view.run} /></div>
          {view.run === null ? (
            <p>No Hermes run is persisted for this conversation.</p>
          ) : runSummaries(view.run).map((summary) => <p key={summary}>{summary}</p>)}
        </div>
      </Card>
      <Card tone="accent" padding="md">
        <div className="boundary-card">
          <ShieldCheck size={18} />
          <div><strong>Execution remains fail-closed</strong><span>No active mandate · no broker credentials · no order path</span></div>
        </div>
      </Card>
    </>
  );
}

export function HermesPanel({ health, view }: { health: HealthState; view: ConversationView }) {
  const hasConversation = view.status === "ready";
  return (
    <aside className="hermes-panel">
      <header className="panel-header">
        <div><Bot size={17} /><strong>Hermes</strong></div>
        <StatusBadge state={health} />
      </header>
      <div
        className="thread"
        aria-busy={view.status === "loading"}
        aria-live="polite"
      >
        <ThreadState view={view} />
      </div>
      <div className="composer">
        <div className="composer-box">
          <textarea aria-label="Message Hermes" disabled placeholder="Read-only transcript · sending activates in the next slice" rows={2} />
          <div>
            <span><Database size={13} />{hasConversation ? "Persisted conversation" : "No conversation session"}</span>
            <Button size="sm" disabled icon={<Activity size={14} />}>Send</Button>
          </div>
        </div>
      </div>
    </aside>
  );
}

export function App() {
  const health = useApiHealth();
  const workspaceId = typeof window === "undefined"
    ? null
    : new URLSearchParams(window.location.search).get("workspace");
  const conversationView = useConversationView(workspaceId);
  return (
    <div className="app-shell">
      <Sidebar />
      <MarketWorkspace />
      <HermesPanel health={health} view={conversationView} />
      <button className="search-shortcut" aria-label="Search"><Search size={15} /><span>Search</span><kbd>⌘K</kbd></button>
    </div>
  );
}
