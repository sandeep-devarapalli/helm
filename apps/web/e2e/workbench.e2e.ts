import { expect, test, type Page } from "@playwright/test";

const webOrigin = `http://127.0.0.1:${process.env.HELM_E2E_WEB_PORT ?? "5173"}`;

const workspaces = {
  empty: "11111111-1111-4111-8111-111111111111",
  reconnect: "22222222-2222-4222-8222-222222222222",
  failure: "33333333-3333-4333-8333-333333333333",
  foreign: "44444444-4444-4444-8444-444444444444",
  responseLoss: "55555555-5555-4555-8555-555555555555",
};

const runIds = {
  empty: "eeeeeeee-eeee-4eee-8eee-eeeeeeeeeeee",
  reconnect: "ffffffff-ffff-4fff-8fff-ffffffffffff",
};

const conversationIds = {
  empty: "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
  reconnect: "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
  failure: "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
  responseLoss: "abababab-abab-4bab-8bab-abababababab",
};

type TestState = {
  createRequests: Array<{ workspaceId: string; conversationId: string }>;
  runRequests: Array<{ workspaceId: string; conversationId: string; content: string }>;
  sseConnections: Record<string, number>;
  lastEventIds: Record<string, Array<string | null>>;
  apiRequests: Array<{ method: string; path: string }>;
  restrictedRequests: Array<{ method: string; path: string }>;
  runs: Record<string, { status: string }>;
};

function url(workspaceId: string) {
  return `/app?workspace=${workspaceId}`;
}

function monitorBrowserBoundary(page: Page) {
  const problems: string[] = [];
  const unexpectedRequests: string[] = [];
  const mutations: string[] = [];
  page.on("console", (message) => {
    if (["warning", "error"].includes(message.type())) problems.push(message.text());
  });
  page.on("request", (request) => {
    if (!["eventsource", "fetch", "xhr"].includes(request.resourceType())) return;
    const requestUrl = new URL(request.url());
    if (requestUrl.origin !== webOrigin || !requestUrl.pathname.startsWith("/api/")) {
      unexpectedRequests.push(request.url());
      return;
    }
    if (request.method() !== "GET") mutations.push(`${request.method()} ${requestUrl.pathname}`);
  });
  return (
    expectedMutations: string[],
    allowedConsoleProblems: RegExp[] = [],
  ) => {
    expect(unexpectedRequests).toEqual([]);
    expect(mutations).toEqual(expectedMutations);
    expect(problems.filter((problem) => (
      !allowedConsoleProblems.some((pattern) => pattern.test(problem))
    ))).toEqual([]);
  };
}

test.beforeEach(async ({ request }) => {
  await request.post("/api/__test/reset");
});

test("public landing states the current boundary without touching the API", async ({ page }) => {
  const assertBoundary = monitorBrowserBoundary(page);
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "A governed conversational foundation for AI trading." })).toBeVisible();
  await expect(page.getByText("Market values are fixtures", { exact: true })).toBeVisible();
  await expect(page.getByText("A public foundation, not a trading release.", { exact: true })).toBeVisible();
  await expect(page.getByRole("rowheader", { name: "U.S. equities" })).toBeVisible();
  await expect(page.getByRole("rowheader", { name: "Indian equities" })).toBeVisible();
  await expect(page.getByRole("rowheader", { name: "Crypto spot" })).toBeVisible();
  await expect(page.getByRole("rowheader", { name: "Commodity ETF exposure" })).toBeVisible();
  await expect(page.getByText("Gold appears only as a structural ETF identity fixture; silver is not modeled or available.", { exact: false })).toBeVisible();
  await expect(page.getByText("Research · backtests · mandates · broker integration · orders · fills · learning · paper or live trading", { exact: true })).toBeVisible();
  await expect(page.getByRole("link", { name: "Open workbench" }).first()).toHaveAttribute("href", "/app");
  assertBoundary([]);
});

test("public landing fits a narrow mobile viewport", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");

  await expect(page.getByRole("heading", { name: "A governed conversational foundation for AI trading." })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Multi-market foundations, not market access." })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(390);
});

test("legacy workspace links redirect to the canonical Workbench route", async ({ page }) => {
  await page.goto(`/?workspace=${workspaces.foreign}`);

  await expect(page).toHaveURL(`/app?workspace=${workspaces.foreign}`);
  await expect(page.getByText("Foreign workspace private evidence.", { exact: true })).toBeVisible();
});

test("first message creates one conversation and one bounded run", async ({ page, request }) => {
  const assertBoundary = monitorBrowserBoundary(page);
  await page.goto(url(workspaces.empty));

  await expect(page.getByText("Start a persisted conversation", { exact: true })).toBeVisible();
  await expect(page.getByText("Watchlist · fixture", { exact: true })).toBeVisible();
  await expect(page.getByText("Paper trading only", { exact: true })).toBeVisible();
  await expect(page.getByText("No live orders", { exact: true })).toBeVisible();

  const composer = page.getByRole("textbox", { name: "Message Hermes" });
  await expect(composer).toBeEnabled();
  await composer.fill("Create the first evidence review.");
  await page.locator("form.composer").evaluate((form) => {
    form.dispatchEvent(new SubmitEvent("submit", { bubbles: true, cancelable: true }));
    form.dispatchEvent(new SubmitEvent("submit", { bubbles: true, cancelable: true }));
  });

  await expect(page.getByText("Create the first evidence review.", { exact: true })).toHaveCount(1);
  await expect(composer).toBeDisabled();
  await page.locator("form.composer").evaluate((form) => {
    form.dispatchEvent(new SubmitEvent("submit", { bubbles: true, cancelable: true }));
  });

  const activeState = await (await request.get("/api/__test/state")).json() as TestState;
  expect(activeState.createRequests).toHaveLength(1);
  expect(activeState.runRequests).toHaveLength(1);
  await request.post(`/api/__test/runs/${runIds.empty}/release`);

  await expect(page.getByText("Canonical persisted evidence response.", { exact: true })).toHaveCount(1);
  await expect(page.getByText("Succeeded", { exact: true })).toBeVisible();
  await expect(page.getByText("Tool provenance is unavailable.", { exact: false })).toBeVisible();

  const state = await (await request.get("/api/__test/state")).json() as TestState;
  expect(state.createRequests).toEqual([expect.objectContaining({ workspaceId: workspaces.empty })]);
  expect(state.runRequests).toEqual([expect.objectContaining({
    workspaceId: workspaces.empty,
    content: "Create the first evidence review.",
  })]);
  expect(state.createRequests).toHaveLength(1);
  expect(state.runRequests).toHaveLength(1);
  expect(state.restrictedRequests).toEqual([]);
  assertBoundary([
    `POST /api/workspaces/${workspaces.empty}/conversations`,
    `POST /api/workspaces/${workspaces.empty}/conversations/${conversationIds.empty}/runs`,
  ]);
});

test("SSE reconnect resumes by Last-Event-ID without gaps or duplicates", async ({ page, request }) => {
  const assertBoundary = monitorBrowserBoundary(page);
  await page.goto(url(workspaces.reconnect));
  await page.getByRole("textbox", { name: "Message Hermes" }).fill("Recover this evidence stream.");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText("Recovered before reconnect; continued after reconnect.", { exact: true })).toHaveCount(1);
  await expect(page.getByText("Succeeded", { exact: true })).toBeVisible();
  await expect(page.getByText("Canonical persisted evidence response.", { exact: true })).toHaveCount(1);
  await page.reload();
  await expect(page.getByText("Recover this evidence stream.", { exact: true })).toHaveCount(1);
  await expect(page.getByText("Canonical persisted evidence response.", { exact: true })).toHaveCount(1);
  await expect(page.getByText("Live projection · provisional", { exact: true })).toHaveCount(0);

  const state = await (await request.get("/api/__test/state")).json() as TestState;
  expect(state.sseConnections[runIds.reconnect]).toBe(2);
  expect(state.lastEventIds[runIds.reconnect]).toEqual([null, "2"]);
  expect(state.restrictedRequests).toEqual([]);
  assertBoundary([
    `POST /api/workspaces/${workspaces.reconnect}/conversations/${conversationIds.reconnect}/runs`,
  ]);
});

test("terminal failure stays explicit and cannot create an order", async ({ page, request }) => {
  const assertBoundary = monitorBrowserBoundary(page);
  await page.goto(url(workspaces.failure));
  await page.getByRole("textbox", { name: "Message Hermes" }).fill("Fail this research safely.");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText("Failed", { exact: true })).toBeVisible();
  await expect(page.getByText("The run failed. Persisted events remain available; no order path exists.", { exact: true })).toBeVisible();
  await expect(page.getByText("Execution remains fail-closed", { exact: true })).toBeVisible();
  await expect(page.getByText("Fail this research safely.", { exact: true })).toHaveCount(1);
  await expect(page.getByText("Canonical persisted evidence response.", { exact: true })).toHaveCount(0);

  const state = await (await request.get("/api/__test/state")).json() as TestState;
  expect(state.runs[conversationIds.failure].status).toBe("failed");
  expect(state.restrictedRequests).toEqual([]);
  assertBoundary([
    `POST /api/workspaces/${workspaces.failure}/conversations/${conversationIds.failure}/runs`,
  ]);
});

test("accepted run survives a lost response without leaving a duplicate-ready draft", async ({ page, request }) => {
  const assertBoundary = monitorBrowserBoundary(page);
  await page.goto(url(workspaces.responseLoss));
  const composer = page.getByRole("textbox", { name: "Message Hermes" });
  await composer.fill("Reconcile the accepted run once.");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText("Succeeded", { exact: true })).toBeVisible();
  await expect(page.getByText("Canonical persisted evidence response.", { exact: true })).toHaveCount(1);
  await expect(page.getByRole("alert")).toHaveCount(0);
  await expect(composer).toHaveValue("");

  const state = await (await request.get("/api/__test/state")).json() as TestState;
  expect(state.runRequests).toEqual([expect.objectContaining({
    workspaceId: workspaces.responseLoss,
    content: "Reconcile the accepted run once.",
  })]);
  expect(state.restrictedRequests).toEqual([]);
  assertBoundary([
    `POST /api/workspaces/${workspaces.responseLoss}/conversations/${conversationIds.responseLoss}/runs`,
  ], [/503/]);
});

test("workspace context never exposes or submits against another workspace", async ({ page, request }) => {
  const assertBoundary = monitorBrowserBoundary(page);
  await page.goto(url(workspaces.foreign));
  await expect(page.getByText("Foreign workspace private evidence.", { exact: true })).toBeVisible();

  await page.goto(url(workspaces.empty));
  await expect(page.getByText("Start a persisted conversation", { exact: true })).toBeVisible();
  await expect(page.getByText("Foreign workspace private evidence.", { exact: true })).toHaveCount(0);
  await page.getByRole("textbox", { name: "Message Hermes" }).fill("Scoped empty-workspace request.");
  await page.getByRole("button", { name: "Send" }).click();
  await expect(page.getByRole("textbox", { name: "Message Hermes" })).toBeDisabled();
  await request.post(`/api/__test/runs/${runIds.empty}/release`);
  await expect(page.getByText("Succeeded", { exact: true })).toBeVisible();

  await page.goto("/app?workspace=99999999-9999-4999-8999-999999999999");
  await expect(page.getByText("Conversation unavailable", { exact: true })).toBeVisible();
  await expect(page.getByText("Foreign workspace private evidence.", { exact: true })).toHaveCount(0);
  await expect(page.getByRole("textbox", { name: "Message Hermes" })).toBeDisabled();

  const state = await (await request.get("/api/__test/state")).json() as TestState;
  expect(state.createRequests).toEqual([expect.objectContaining({ workspaceId: workspaces.empty })]);
  expect(state.runRequests).toEqual([expect.objectContaining({ workspaceId: workspaces.empty })]);
  expect(state.restrictedRequests).toEqual([]);
  assertBoundary([
    `POST /api/workspaces/${workspaces.empty}/conversations`,
    `POST /api/workspaces/${workspaces.empty}/conversations/${conversationIds.empty}/runs`,
  ], [/404/]);
});
