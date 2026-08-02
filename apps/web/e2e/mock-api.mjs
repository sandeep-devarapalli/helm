import http from "node:http";
import { URL } from "node:url";

export const WORKSPACES = {
  empty: "11111111-1111-4111-8111-111111111111",
  reconnect: "22222222-2222-4222-8222-222222222222",
  failure: "33333333-3333-4333-8333-333333333333",
  foreign: "44444444-4444-4444-8444-444444444444",
  responseLoss: "55555555-5555-4555-8555-555555555555",
  missing: "99999999-9999-4999-8999-999999999999",
};

const IDS = {
  emptyConversation: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
  reconnectConversation: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
  failureConversation: "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
  foreignConversation: "dddddddd-dddd-4ddd-8ddd-dddddddddddd",
  responseLossConversation: "abababab-abab-4bab-8bab-abababababab",
  emptyRun: "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
  reconnectRun: "ffffffff-ffff-4fff-8fff-ffffffffffff",
  failureRun: "12121212-1212-4212-8212-121212121212",
  responseLossRun: "56565656-5656-4656-8656-565656565656",
};

const createdAt = "2026-08-02T12:00:00Z";
let state;

function conversation(id, workspaceId, title, messages = []) {
  return { id, workspace_id: workspaceId, title, created_at: createdAt, messages };
}

function resetState() {
  state = {
    conversations: {
      [WORKSPACES.empty]: [],
      [WORKSPACES.reconnect]: [conversation(
        IDS.reconnectConversation,
        WORKSPACES.reconnect,
        "Reconnect evidence",
        [{
          id: "20202020-2020-4020-8020-202020202020",
          role: "assistant",
          content: "Reconnect workspace evidence only.",
          created_at: createdAt,
        }],
      )],
      [WORKSPACES.failure]: [conversation(
        IDS.failureConversation,
        WORKSPACES.failure,
        "Failure evidence",
      )],
      [WORKSPACES.foreign]: [conversation(
        IDS.foreignConversation,
        WORKSPACES.foreign,
        "Foreign evidence",
        [{
          id: "30303030-3030-4030-8030-303030303030",
          role: "assistant",
          content: "Foreign workspace private evidence.",
          created_at: createdAt,
        }],
      )],
      [WORKSPACES.responseLoss]: [conversation(
        IDS.responseLossConversation,
        WORKSPACES.responseLoss,
        "Response recovery",
      )],
    },
    runs: {},
    createRequests: [],
    runRequests: [],
    sseConnections: {},
    lastEventIds: {},
    apiRequests: [],
    restrictedRequests: [],
  };
}

resetState();

function sendJson(response, status, body) {
  response.writeHead(status, { "content-type": "application/json" });
  response.end(JSON.stringify(body));
}

async function readJson(request) {
  let body = "";
  for await (const chunk of request) body += chunk;
  return body ? JSON.parse(body) : {};
}

function workspaceConversations(workspaceId) {
  return state.conversations[workspaceId];
}

function scopedConversation(workspaceId, conversationId) {
  return workspaceConversations(workspaceId)?.find((item) => item.id === conversationId);
}

function publicConversation(item) {
  const { messages: _messages, ...value } = item;
  return value;
}

function publicRun(run) {
  if (!run) return null;
  return {
    id: run.id,
    status: run.status,
    event_stream_complete: run.event_stream_complete,
    projection_gap: run.projection_gap,
    approval_blocked: false,
    tool_provenance_status: run.tool_provenance_status,
  };
}

function runMode(workspaceId) {
  if (workspaceId === WORKSPACES.reconnect) return "reconnect";
  if (workspaceId === WORKSPACES.failure) return "failure";
  if (workspaceId === WORKSPACES.responseLoss) return "response-loss";
  return "success";
}

function runId(workspaceId) {
  if (workspaceId === WORKSPACES.reconnect) return IDS.reconnectRun;
  if (workspaceId === WORKSPACES.failure) return IDS.failureRun;
  if (workspaceId === WORKSPACES.responseLoss) return IDS.responseLossRun;
  return IDS.emptyRun;
}

function runEvents(run) {
  const terminal = run.mode === "failure"
    ? [3, "run.failed", { error: "Hermes projection failed safely." }]
    : [4, "run.completed", { output: "Canonical persisted evidence response." }];
  return [
    [0, "run.submitting", {}],
    [1, "run.started", {}],
    [2, "message.delta", { delta: "Recovered before reconnect; " }],
    ...(run.mode === "failure" ? [] : [[3, "message.delta", { delta: "continued after reconnect." }]]),
    terminal,
  ];
}

function sseFrame(sequence, eventType, payload) {
  return [
    `id: ${sequence}`,
    "event: run-event",
    `data: ${JSON.stringify({
      sequence_number: sequence,
      event_type: eventType,
      payload,
      created_at: createdAt,
      tool_provenance_complete: false,
    })}`,
    "",
    "",
  ].join("\n");
}

function finishRun(run, eventType) {
  run.status = eventType === "run.failed" ? "failed" : "succeeded";
  run.event_stream_complete = true;
  run.tool_provenance_status = "unavailable";
  if (eventType === "run.completed" && !run.assistantPersisted) {
    run.conversation.messages.push({
      id: `${run.id.slice(0, 8)}-9090-4090-8090-909090909090`,
      role: "assistant",
      content: "Canonical persisted evidence response.",
      created_at: createdAt,
    });
    run.assistantPersisted = true;
  }
}

function streamRun(request, response, run, url) {
  const headerCursor = request.headers["last-event-id"];
  const queryCursor = Number(url.searchParams.get("after") ?? -1);
  const cursor = Math.max(
    Number.isInteger(queryCursor) ? queryCursor : -1,
    headerCursor === undefined ? -1 : Number(headerCursor),
  );
  state.sseConnections[run.id] = (state.sseConnections[run.id] ?? 0) + 1;
  (state.lastEventIds[run.id] ??= []).push(headerCursor ?? null);
  response.writeHead(200, {
    "content-type": "text/event-stream",
    "cache-control": "no-cache",
    connection: "keep-alive",
  });
  response.write("retry: 50\n\n");

  const pending = runEvents(run).filter(([sequence]) => sequence > cursor);
  const firstReconnectBatch = run.mode === "reconnect" && !run.interrupted;
  const batch = firstReconnectBatch
    ? pending.filter(([sequence]) => sequence <= 2)
    : pending;
  let index = 0;
  const sendNext = () => {
    if (response.destroyed) return;
    const event = batch[index];
    if (!event) {
      if (firstReconnectBatch) run.interrupted = true;
      response.end();
      return;
    }
    const [sequence, eventType, payload] = event;
    if (
      run.mode === "success"
      && (eventType === "run.completed" || eventType === "run.failed")
      && !run.terminalReleased
    ) {
      setTimeout(sendNext, 20);
      return;
    }
    index += 1;
    if (eventType === "run.completed" || eventType === "run.failed") {
      finishRun(run, eventType);
    }
    response.write(sseFrame(sequence, eventType, payload));
    const delay = run.mode === "reconnect" && sequence === 3 ? 300 : 35;
    setTimeout(sendNext, delay);
  };
  setTimeout(sendNext, 20);
}

const server = http.createServer(async (request, response) => {
  const url = new URL(request.url ?? "/", "http://127.0.0.1:8000");
  const method = request.method ?? "GET";

  if (method === "GET" && url.pathname === "/health") {
    sendJson(response, 200, { status: "ok" });
    return;
  }
  if (method === "POST" && url.pathname === "/__test/reset") {
    resetState();
    sendJson(response, 200, { status: "reset" });
    return;
  }
  const release = url.pathname.match(/^\/__test\/runs\/([^/]+)\/release$/);
  if (method === "POST" && release) {
    const run = Object.values(state.runs).find((item) => item.id === release[1]);
    if (!run) {
      sendJson(response, 404, { detail: "run not found" });
      return;
    }
    run.terminalReleased = true;
    sendJson(response, 200, { status: "released" });
    return;
  }
  if (method === "GET" && url.pathname === "/__test/state") {
    sendJson(response, 200, {
      createRequests: state.createRequests,
      runRequests: state.runRequests,
      sseConnections: state.sseConnections,
      lastEventIds: state.lastEventIds,
      apiRequests: state.apiRequests,
      restrictedRequests: state.restrictedRequests,
      runs: Object.fromEntries(
        Object.entries(state.runs).map(([id, run]) => [id, publicRun(run)]),
      ),
    });
    return;
  }

  if (url.pathname.startsWith("/workspaces/")) {
    state.apiRequests.push({ method, path: url.pathname });
  }
  if (
    /\/(order-intents?|orders?|brokers?|credentials?|hermes|vibe|mandates?|policy|risk|execution|fills?|trades?|kill-switch)(\/|$)/.test(
      url.pathname,
    )
  ) {
    state.restrictedRequests.push({ method, path: url.pathname });
  }

  const collection = url.pathname.match(/^\/workspaces\/([^/]+)\/conversations$/);
  if (collection) {
    const workspaceId = collection[1];
    const conversations = workspaceConversations(workspaceId);
    if (!conversations) {
      sendJson(response, 404, { detail: "workspace not found" });
      return;
    }
    if (method === "GET") {
      sendJson(response, 200, {
        items: conversations.map(publicConversation),
        next_cursor: null,
      });
      return;
    }
    if (method === "POST") {
      await readJson(request);
      const item = conversation(
        IDS.emptyConversation,
        workspaceId,
        null,
      );
      conversations.unshift(item);
      state.createRequests.push({ workspaceId, conversationId: item.id });
      sendJson(response, 201, publicConversation(item));
      return;
    }
  }

  const messages = url.pathname.match(
    /^\/workspaces\/([^/]+)\/conversations\/([^/]+)\/messages$/,
  );
  if (method === "GET" && messages) {
    const item = scopedConversation(messages[1], messages[2]);
    if (!item) {
      sendJson(response, 404, { detail: "conversation not found" });
      return;
    }
    sendJson(response, 200, { items: item.messages, next_cursor: null });
    return;
  }

  const latest = url.pathname.match(
    /^\/workspaces\/([^/]+)\/conversations\/([^/]+)\/runs\/latest$/,
  );
  if (method === "GET" && latest) {
    const item = scopedConversation(latest[1], latest[2]);
    if (!item) {
      sendJson(response, 404, { detail: "conversation not found" });
      return;
    }
    sendJson(response, 200, { run: publicRun(state.runs[item.id]) });
    return;
  }

  const runs = url.pathname.match(
    /^\/workspaces\/([^/]+)\/conversations\/([^/]+)\/runs$/,
  );
  if (method === "POST" && runs) {
    const item = scopedConversation(runs[1], runs[2]);
    if (!item) {
      sendJson(response, 404, { detail: "conversation not found" });
      return;
    }
    const active = state.runs[item.id];
    if (active?.status === "running") {
      sendJson(response, 409, { detail: "conversation already has an active run" });
      return;
    }
    const body = await readJson(request);
    const id = runId(runs[1]);
    item.messages.push({
      id: `${id.slice(0, 8)}-8080-4080-8080-808080808080`,
      role: "user",
      content: body.content,
      created_at: createdAt,
    });
    const run = {
      id,
      workspaceId: runs[1],
      conversation: item,
      mode: runMode(runs[1]),
      status: "running",
      event_stream_complete: false,
      projection_gap: false,
      tool_provenance_status: "pending",
      interrupted: false,
      assistantPersisted: false,
      terminalReleased: runMode(runs[1]) !== "success",
    };
    state.runs[item.id] = run;
    state.runRequests.push({ workspaceId: runs[1], conversationId: item.id, content: body.content });
    if (run.mode === "response-loss") {
      sendJson(response, 503, { detail: "gateway response lost after acceptance" });
    } else {
      sendJson(response, 202, publicRun(run));
    }
    return;
  }

  const stream = url.pathname.match(
    /^\/workspaces\/([^/]+)\/conversations\/([^/]+)\/runs\/([^/]+)\/events\/stream$/,
  );
  if (method === "GET" && stream) {
    const item = scopedConversation(stream[1], stream[2]);
    const run = item && state.runs[item.id];
    if (!run || run.id !== stream[3]) {
      sendJson(response, 404, { detail: "run not found" });
      return;
    }
    streamRun(request, response, run, url);
    return;
  }

  sendJson(response, 404, { detail: "not found" });
});

server.listen(8000, "127.0.0.1");
for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => server.close(() => process.exit(0)));
}
