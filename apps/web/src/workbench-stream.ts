export type PublicRunEvent = {
  sequence_number: number;
  event_type: string;
  payload: Record<string, unknown>;
  created_at: string;
  tool_provenance_complete: boolean;
};

type EventSourcePort = {
  readonly readyState: number;
  addEventListener(type: string, listener: (event: Event) => void): void;
  close(): void;
};

export type EventSourceFactory = (url: string) => EventSourcePort;

type RunEventCallbacks = {
  onOpen(): void;
  onEvent(event: PublicRunEvent): void;
  onTerminal(event: PublicRunEvent): void;
  onReconnect(): void;
  onFailure(message: string): void;
};

const terminalEvents = new Set(["run.completed", "run.failed", "run.cancelled"]);
const activeStatuses = new Set(["queued", "submitting", "running"]);

export function isRunActive(status: string | undefined): boolean {
  return status !== undefined && activeStatuses.has(status);
}

export function runEventStreamUrl(
  workspaceId: string,
  conversationId: string,
  runId: string,
): string {
  return `/api/workspaces/${encodeURIComponent(workspaceId)}/conversations/${encodeURIComponent(conversationId)}/runs/${encodeURIComponent(runId)}/events/stream?after=-1`;
}

export function subscribeToRunEvents(
  workspaceId: string,
  conversationId: string,
  runId: string,
  callbacks: RunEventCallbacks,
  factory: EventSourceFactory = (url) => new EventSource(url),
): () => void {
  const source = factory(runEventStreamUrl(workspaceId, conversationId, runId));
  let lastSequence = -1;
  let closed = false;

  source.addEventListener("open", () => {
    if (!closed) callbacks.onOpen();
  });
  source.addEventListener("run-event", (rawEvent) => {
    if (closed) return;
    try {
      const event = JSON.parse((rawEvent as MessageEvent<string>).data) as PublicRunEvent;
      if (!Number.isSafeInteger(event.sequence_number) || event.sequence_number < 0) {
        throw new Error("invalid event sequence");
      }
      if (event.sequence_number <= lastSequence) return;
      if (event.sequence_number !== lastSequence + 1) {
        closed = true;
        source.close();
        callbacks.onFailure("Persisted event recovery contains a gap. The live projection was stopped.");
        return;
      }
      lastSequence = event.sequence_number;
      callbacks.onEvent(event);
      if (terminalEvents.has(event.event_type)) {
        closed = true;
        source.close();
        callbacks.onTerminal(event);
      }
    } catch {
      closed = true;
      source.close();
      callbacks.onFailure("helm returned an invalid persisted event. The live projection was stopped.");
    }
  });
  source.addEventListener("error", () => {
    if (closed) return;
    if (source.readyState === 2) {
      closed = true;
      source.close();
      callbacks.onFailure("The persisted event stream closed before a terminal event.");
      return;
    }
    callbacks.onReconnect();
  });

  return () => {
    closed = true;
    source.close();
  };
}
