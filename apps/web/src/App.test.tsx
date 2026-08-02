import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { HermesPanel, openedRunStream, type RunStreamState } from "./App";
import {
  loadConversationView,
  submitConversationMessage,
  type ConversationView,
} from "./workbench-data";

const workspaceId = "11111111-1111-4111-8111-111111111111";
const conversationId = "22222222-2222-4222-8222-222222222222";

function jsonResponse(body: object, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function renderView(
  view: ConversationView,
  interactive = false,
  stream?: RunStreamState,
): string {
  return renderToStaticMarkup(
    <HermesPanel
      health="ready"
      view={view}
      stream={stream}
      onSubmit={interactive ? async () => undefined : undefined}
    />,
  );
}

describe("helm persisted Workbench", () => {
  it("loads only the explicit workspace and fetches transcript state in parallel", async () => {
    const requested: string[] = [];
    const fetcher = vi.fn(async (input: string) => {
      requested.push(input);
      if (input.endsWith("conversations?limit=1")) {
        return jsonResponse({
          items: [{ id: conversationId, title: "Evidence review", created_at: "2026-08-02T04:00:00Z" }],
        });
      }
      if (input.endsWith("messages?limit=100")) {
        return jsonResponse({
          items: [{
            id: "33333333-3333-4333-8333-333333333333",
            role: "user",
            content: "Review NVDA evidence.",
            created_at: "2026-08-02T04:01:00Z",
          }],
          next_cursor: null,
        });
      }
      return jsonResponse({ run: null });
    });

    const view = await loadConversationView(workspaceId, fetcher);

    expect(view.status).toBe("ready");
    expect(requested).toEqual([
      `/api/workspaces/${workspaceId}/conversations?limit=1`,
      `/api/workspaces/${workspaceId}/conversations/${conversationId}/messages?limit=100`,
      `/api/workspaces/${workspaceId}/conversations/${conversationId}/runs/latest`,
    ]);
  });

  it("submits one trimmed message only to the workspace-scoped helm run endpoint", async () => {
    const fetcher = vi.fn(async () => jsonResponse({
      id: "44444444-4444-4444-8444-444444444444",
      status: "running",
      event_stream_complete: false,
    }, 202));

    await submitConversationMessage(workspaceId, conversationId, "  Review AAPL evidence.  ", fetcher);

    expect(fetcher).toHaveBeenCalledOnce();
    expect(fetcher).toHaveBeenCalledWith(
      `/api/workspaces/${workspaceId}/conversations/${conversationId}/runs`,
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ content: "Review AAPL evidence." }),
      }),
    );
  });

  it.each([
    [{ status: "loading" } as const, "Loading persisted conversation"],
    [{ status: "empty" } as const, "No persisted conversation"],
    [{ status: "unavailable" } as const, "Conversation unavailable"],
    [{ status: "context-required" } as const, "Workspace context required"],
  ])("renders the %s state explicitly", (view, expected) => {
    expect(renderView(view)).toContain(expected);
  });

  it("renders approval-blocked persisted state without enabling submission", () => {
    const markup = renderView({
      status: "ready",
      conversation: {
        id: conversationId,
        title: "Approval boundary",
        created_at: "2026-08-02T04:00:00Z",
      },
      messages: [{
        id: "33333333-3333-4333-8333-333333333333",
        role: "assistant",
        content: "No action was taken.",
        created_at: "2026-08-02T04:01:00Z",
      }],
      run: {
        id: "44444444-4444-4444-8444-444444444444",
        status: "cancelled",
        event_stream_complete: false,
        projection_gap: true,
        approval_blocked: true,
        tool_provenance_status: "unavailable",
      },
      partialHistory: false,
    });

    expect(markup).toContain("Approval blocked");
    expect(markup).toContain("nothing was executed");
    expect(markup).toContain("persisted projection is incomplete");
    expect(markup).toContain("Message submission is unavailable");
    expect(markup).toContain("disabled");
  });

  it("keeps partial transcript and incomplete run evidence visibly weak", () => {
    const markup = renderView({
      status: "ready",
      conversation: {
        id: conversationId,
        title: null,
        created_at: "2026-08-02T04:00:00Z",
      },
      messages: [],
      run: {
        id: "44444444-4444-4444-8444-444444444444",
        status: "failed",
        event_stream_complete: false,
        projection_gap: true,
        approval_blocked: false,
        tool_provenance_status: "partial",
      },
      partialHistory: true,
    });

    expect(markup).toContain("Partial history");
    expect(markup).toContain("No persisted messages");
    expect(markup).toContain("The run failed");
    expect(markup).toContain("persisted projection is incomplete");
  });

  it("announces asynchronous and failed transcript states", () => {
    expect(renderView({ status: "loading" })).toContain("aria-live=\"polite\"");
    expect(renderView({ status: "unavailable" })).toContain("role=\"alert\"");
  });

  it("preserves the same run's provisional delta when EventSource reconnects", () => {
    expect(openedRunStream({
      runId: "44444444-4444-4444-8444-444444444444",
      phase: "reconnecting",
      delta: "Evidence before reconnect. ",
      error: null,
    }, "44444444-4444-4444-8444-444444444444")).toEqual({
      runId: "44444444-4444-4444-8444-444444444444",
      phase: "live",
      delta: "Evidence before reconnect. ",
      error: null,
    });
  });

  it("enables drafting only for a healthy persisted conversation without a blocking run", () => {
    const markup = renderView({
      status: "ready",
      conversation: {
        id: conversationId,
        title: "Evidence review",
        created_at: "2026-08-02T04:00:00Z",
      },
      messages: [],
      run: null,
      partialHistory: false,
    }, true);

    expect(markup).toContain("Ask Hermes to research or explain");
    expect(markup).toContain("Persisted conversation");
  });

  it("labels streamed text as provisional and blocks another active submission", () => {
    const runId = "44444444-4444-4444-8444-444444444444";
    const markup = renderView({
      status: "ready",
      conversation: {
        id: conversationId,
        title: "Evidence review",
        created_at: "2026-08-02T04:00:00Z",
      },
      messages: [],
      run: {
        id: runId,
        status: "running",
        event_stream_complete: false,
        projection_gap: false,
        approval_blocked: false,
        tool_provenance_status: "pending",
      },
      partialHistory: false,
    }, true, {
      runId,
      phase: "live",
      delta: "Research is still in progress.",
      error: null,
    });

    expect(markup).toContain("Live projection · provisional");
    expect(markup).toContain("Research is still in progress.");
    expect(markup).toContain("Streamed text is provisional");
    expect(markup).toContain("Message submission is unavailable");
  });

  it("removes provisional text after the canonical run becomes terminal", () => {
    const runId = "44444444-4444-4444-8444-444444444444";
    const markup = renderView({
      status: "ready",
      conversation: {
        id: conversationId,
        title: "Evidence review",
        created_at: "2026-08-02T04:00:00Z",
      },
      messages: [{
        id: "55555555-5555-4555-8555-555555555555",
        role: "assistant",
        content: "Canonical result.",
        created_at: "2026-08-02T04:02:00Z",
      }],
      run: {
        id: runId,
        status: "succeeded",
        event_stream_complete: true,
        projection_gap: false,
        approval_blocked: false,
        tool_provenance_status: "unavailable",
      },
      partialHistory: false,
    }, true, {
      runId,
      phase: "live",
      delta: "Stale provisional result.",
      error: null,
    });

    expect(markup).toContain("Canonical result.");
    expect(markup).not.toContain("Stale provisional result.");
    expect(markup).not.toContain("Live projection · provisional");
  });
});
