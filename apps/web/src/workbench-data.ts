type FetchLike = (input: string, init?: RequestInit) => Promise<Response>;

type ConversationSummary = {
  id: string;
  title: string | null;
  created_at: string;
};

type PublicMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
};

export type RunRefreshState = {
  id: string;
  status: string;
  event_stream_complete: boolean;
  projection_gap: boolean;
  approval_blocked: boolean;
  tool_provenance_status: string;
};

export type ConversationView =
  | { status: "loading" }
  | { status: "context-required" }
  | { status: "invalid-context" }
  | { status: "unavailable" }
  | { status: "empty" }
  | {
      status: "ready";
      conversation: ConversationSummary;
      messages: PublicMessage[];
      run: RunRefreshState | null;
      partialHistory: boolean;
    };

async function responseJson<T>(response: Response): Promise<T> {
  if (!response.ok) throw new Error(`helm API request failed with ${response.status}`);
  return response.json() as Promise<T>;
}

export async function loadConversationView(
  workspaceId: string,
  fetcher: FetchLike = fetch,
  signal?: AbortSignal,
): Promise<ConversationView> {
  const workspacePath = encodeURIComponent(workspaceId);
  const conversations = await responseJson<{ items: ConversationSummary[] }>(
    await fetcher(`/api/workspaces/${workspacePath}/conversations?limit=1`, { signal }),
  );
  const conversation = conversations.items[0];
  if (!conversation) return { status: "empty" };

  const conversationPath = encodeURIComponent(conversation.id);
  const [messagePage, latestRun] = await Promise.all([
    fetcher(
      `/api/workspaces/${workspacePath}/conversations/${conversationPath}/messages?limit=100`,
      { signal },
    ).then((response) => responseJson<{ items: PublicMessage[]; next_cursor: string | null }>(response)),
    fetcher(
      `/api/workspaces/${workspacePath}/conversations/${conversationPath}/runs/latest`,
      { signal },
    ).then((response) => responseJson<{ run: RunRefreshState | null }>(response)),
  ]);

  return {
    status: "ready",
    conversation,
    messages: messagePage.items,
    run: latestRun.run,
    partialHistory: messagePage.next_cursor !== null,
  };
}
