import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { HermesPanel } from "./App";
import { loadConversationView, type ConversationView } from "./workbench-data";

const workspaceId = "11111111-1111-4111-8111-111111111111";
const conversationId = "22222222-2222-4222-8222-222222222222";

function jsonResponse(body: object, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function renderView(view: ConversationView): string {
  return renderToStaticMarkup(<HermesPanel health="ready" view={view} />);
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
    expect(markup).toContain("Read-only transcript");
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
});
