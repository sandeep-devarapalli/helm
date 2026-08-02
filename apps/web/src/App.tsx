import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";
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
  createConversation,
  loadConversationView,
  submitConversationMessage,
  type ConversationView,
  type RunRefreshState,
} from "./workbench-data";
import {
  isRunActive,
  subscribeToRunEvents,
  type PublicRunEvent,
} from "./workbench-stream";

type HealthState = "checking" | "ready" | "unavailable";

export type RunStreamState = {
  runId: string | null;
  phase: "idle" | "connecting" | "live" | "reconnecting" | "failed";
  delta: string;
  error: string | null;
};

const idleRunStream: RunStreamState = {
  runId: null,
  phase: "idle",
  delta: "",
  error: null,
};

export function openedRunStream(state: RunStreamState, runId: string): RunStreamState {
  return state.runId === runId
    ? { ...state, phase: "live", error: null }
    : { runId, phase: "live", delta: "", error: null };
}

const workspaceIdPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

const watchlist = [
  { symbol: "AAPL", venue: "NASDAQ", price: "$228.26", change: "+0.62%" },
  { symbol: "NVDA", venue: "NASDAQ", price: "$142.91", change: "+1.28%" },
  { symbol: "AMD", venue: "NASDAQ", price: "$156.74", change: "-0.31%" },
];

function useConversationView(workspaceId: string | null) {
  const [loadedResult, setLoadedResult] = useState<{
    workspaceId: string;
    view: ConversationView;
  } | null>(null);
  const requestGeneration = useRef(0);
  const latestRefresh = useRef<Promise<ConversationView> | null>(null);
  const workspaceIsValid = workspaceId !== null && workspaceIdPattern.test(workspaceId);

  const refresh = useCallback((): Promise<ConversationView> => {
    if (!workspaceIsValid || workspaceId === null) {
      return Promise.resolve({ status: "invalid-context" });
    }
    const generation = ++requestGeneration.current;
    const request = loadConversationView(workspaceId)
      .catch(() => ({ status: "unavailable" } as const))
      .then((view): ConversationView | Promise<ConversationView> => {
        if (generation !== requestGeneration.current) {
          const newerRequest = latestRefresh.current;
          return newerRequest && newerRequest !== request ? newerRequest : view;
        }
        setLoadedResult({ workspaceId, view });
        return view;
      });
    latestRefresh.current = request;
    return request;
  }, [workspaceId, workspaceIsValid]);
  useEffect(() => {
    if (!workspaceIsValid || workspaceId === null) return;
    const controller = new AbortController();
    const generation = ++requestGeneration.current;
    loadConversationView(workspaceId, fetch, controller.signal)
      .then((view) => {
        if (generation === requestGeneration.current) setLoadedResult({ workspaceId, view });
      })
      .catch((error: unknown) => {
        if (
          generation === requestGeneration.current
          && !(error instanceof Error && error.name === "AbortError")
        ) {
          setLoadedResult({ workspaceId, view: { status: "unavailable" } });
        }
      });
    return () => controller.abort();
  }, [workspaceId, workspaceIsValid]);

  let view: ConversationView;
  if (workspaceId === null) view = { status: "context-required" };
  else if (!workspaceIsValid) view = { status: "invalid-context" };
  else if (loadedResult?.workspaceId !== workspaceId) view = { status: "loading" };
  else view = loadedResult.view;
  return { view, refresh };
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
  if (run.status === "indeterminate") return <Badge tone="warning" dot>Outcome uncertain</Badge>;
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
  if (isRunActive(run.status)) {
    summaries.push("Hermes is active. Streamed text is provisional until helm persists the terminal transcript.");
  }
  if (run.status === "indeterminate") {
    summaries.push(
      "The submission outcome is uncertain. Replacement runs remain blocked until the state is resolved.",
    );
  }
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

function ThreadState({ view, stream }: { view: ConversationView; stream: RunStreamState }) {
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
    return <div className="thread-state"><strong>Start a persisted conversation</strong><span>Your first message creates one workspace-scoped conversation, then submits one Hermes run through helm.</span></div>;
  }
  const streamIsActive = stream.runId === view.run?.id && isRunActive(view.run?.status);

  return (
    <>
      <div className="conversation-meta">
        <div><span className="section-label">Persisted conversation</span><strong>{view.conversation.title ?? "Untitled conversation"}</strong></div>
        <div className="conversation-badges"><Badge tone="info">Persisted</Badge>{view.partialHistory ? <Badge tone="warning">Partial history</Badge> : null}</div>
      </div>
      {view.messages.length === 0 ? (
        <div className="thread-state"><strong>No persisted messages</strong><span>The conversation exists, but its public transcript is empty.</span></div>
      ) : view.messages.map((message) => (
        <ChatBubble key={message.id} role={message.role === "assistant" ? "agent" : "user"} timestamp={timestamp(message.created_at)}>
          <p className="message-content">{message.content}</p>
        </ChatBubble>
      ))}
      {streamIsActive && stream.delta ? (
        <div className="live-projection" aria-live="polite">
          <span className="section-label">Live projection · provisional</span>
          <ChatBubble role="agent"><p className="message-content">{stream.delta}</p></ChatBubble>
        </div>
      ) : null}
      {streamIsActive && stream.error ? (
        <div className="thread-state danger" role="alert">
          <strong>Live projection stopped</strong>
          <span>{stream.error} The canonical persisted transcript remains authoritative.</span>
        </div>
      ) : null}
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

export function HermesPanel({
  health,
  view,
  stream = idleRunStream,
  submitting = false,
  submissionError = null,
  onSubmit,
}: {
  health: HealthState;
  view: ConversationView;
  stream?: RunStreamState;
  submitting?: boolean;
  submissionError?: string | null;
  onSubmit?: (content: string) => Promise<void>;
}) {
  const [draft, setDraft] = useState("");
  const hasConversation = view.status === "ready";
  const conversationId = hasConversation ? view.conversation.id : null;
  const [draftConversationId, setDraftConversationId] = useState(conversationId);
  if (conversationId && conversationId !== draftConversationId) {
    if (draftConversationId) setDraft("");
    setDraftConversationId(conversationId);
  }
  const canStartConversation = view.status === "empty";
  const runBlocksSubmission = hasConversation && (
    isRunActive(view.run?.status)
    || view.run?.status === "indeterminate"
    || view.run?.approval_blocked === true
    || view.run?.projection_gap === true
  );
  const canCompose = Boolean(onSubmit)
    && health === "ready"
    && (hasConversation || canStartConversation)
    && !runBlocksSubmission
    && !submitting;
  const activityLabel = submitting
    ? "Submitting to helm"
    : stream.phase === "reconnecting"
      ? "Recovering persisted events"
      : stream.phase === "connecting" || stream.phase === "live"
        ? "Hermes run active"
        : hasConversation
          ? "Persisted conversation"
          : canStartConversation
            ? "New persisted conversation"
            : "No conversation session";

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const content = draft.trim();
    if (!canCompose || !content || !onSubmit) return;
    try {
      await onSubmit(content);
      setDraft("");
    } catch {
      // The parent exposes the bounded helm API failure without clearing the draft.
    }
  }

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
        <ThreadState view={view} stream={stream} />
      </div>
      <form className="composer" onSubmit={handleSubmit}>
        {submissionError ? <div className="composer-error" role="alert">{submissionError}</div> : null}
        <div className="composer-box">
          <textarea
            aria-label="Message Hermes"
            disabled={!canCompose}
            maxLength={20_000}
            onChange={(event) => setDraft(event.target.value)}
            placeholder={canCompose ? "Ask Hermes to research or explain…" : "Message submission is unavailable"}
            rows={2}
            value={draft}
          />
          <div>
            <span><Database size={13} />{activityLabel}</span>
            <Button
              size="sm"
              disabled={!canCompose || draft.trim().length === 0}
              loading={submitting}
              icon={<Activity size={14} />}
            >Send</Button>
          </div>
        </div>
      </form>
    </aside>
  );
}

export function App() {
  const health = useApiHealth();
  const workspaceId = typeof window === "undefined"
    ? null
    : new URLSearchParams(window.location.search).get("workspace");
  const { view: conversationView, refresh } = useConversationView(workspaceId);
  const [stream, setStream] = useState<RunStreamState>(idleRunStream);
  const [submitting, setSubmitting] = useState(false);
  const [submissionError, setSubmissionError] = useState<string | null>(null);
  const submitInFlight = useRef(false);
  const conversationId = conversationView.status === "ready" ? conversationView.conversation.id : null;
  const runId = conversationView.status === "ready" ? conversationView.run?.id ?? null : null;
  const runStatus = conversationView.status === "ready" ? conversationView.run?.status : undefined;

  useEffect(() => {
    if (!workspaceId || !conversationId || !runId || !isRunActive(runStatus)) return;
    return subscribeToRunEvents(workspaceId, conversationId, runId, {
      onOpen: () => setStream((state) => openedRunStream(state, runId)),
      onEvent: (event: PublicRunEvent) => setStream((state) => {
        const currentDelta = state.runId === runId ? state.delta : "";
        return {
          ...state,
          runId,
          phase: "live",
          delta: event.event_type === "message.delta" && typeof event.payload.delta === "string"
            ? currentDelta + event.payload.delta
            : currentDelta,
        };
      }),
      onTerminal: () => { void refresh(); },
      onReconnect: () => {
        setStream((state) => ({ ...state, phase: "reconnecting" }));
        void refresh();
      },
      onFailure: (error) => {
        setStream((state) => ({ ...state, phase: "failed", error }));
        void refresh();
      },
    });
  }, [conversationId, refresh, runId, runStatus, workspaceId]);

  const submit = useCallback(async (content: string) => {
    if (!workspaceId) throw new Error("workspace context unavailable");
    if (submitInFlight.current) throw new Error("message submission already in progress");
    submitInFlight.current = true;
    setSubmitting(true);
    setSubmissionError(null);
    let targetConversationId = conversationId;
    try {
      targetConversationId ??= (await createConversation(workspaceId)).id;
      await submitConversationMessage(workspaceId, targetConversationId, content);
      await refresh();
    } catch (error) {
      const refreshedView = await refresh();
      if (submissionIsPersisted(
        refreshedView,
        targetConversationId,
        content,
        runId,
      )) return;
      setSubmissionError(
        error instanceof Error
          ? "helm could not persist this request. The draft was preserved; nothing was retried."
          : "Message submission failed before a run could be confirmed.",
      );
      throw error;
    } finally {
      submitInFlight.current = false;
      setSubmitting(false);
    }
  }, [conversationId, refresh, runId, workspaceId]);

  const visibleStream = runId && isRunActive(runStatus)
    ? stream.runId === runId
      ? stream
      : { ...idleRunStream, runId, phase: "connecting" as const }
    : idleRunStream;
  return (
    <div className="app-shell">
      <Sidebar />
      <MarketWorkspace />
      <HermesPanel
        key={workspaceId ?? "no-workspace"}
        health={health}
        view={conversationView}
        stream={visibleStream}
        submitting={submitting}
        submissionError={submissionError}
        onSubmit={submit}
      />
      <button className="search-shortcut" aria-label="Search"><Search size={15} /><span>Search</span><kbd>⌘K</kbd></button>
    </div>
  );
}

function submissionIsPersisted(
  view: ConversationView,
  conversationId: string | null,
  content: string,
  previousRunId: string | null,
) {
  if (
    !conversationId
    || view.status !== "ready"
    || view.conversation.id !== conversationId
    || !view.run
    || view.run.id === previousRunId
  ) return false;
  const lastUserMessage = [...view.messages].reverse().find((message) => message.role === "user");
  return lastUserMessage?.content === content;
}
