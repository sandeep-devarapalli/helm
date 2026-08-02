import { describe, expect, it, vi } from "vitest";
import {
  runEventStreamUrl,
  subscribeToRunEvents,
  type PublicRunEvent,
} from "./workbench-stream";

class FakeEventSource {
  readyState = 0;
  closed = false;
  private listeners = new Map<string, Array<(event: Event) => void>>();

  addEventListener(type: string, listener: (event: Event) => void) {
    this.listeners.set(type, [...(this.listeners.get(type) ?? []), listener]);
  }

  close() {
    this.closed = true;
  }

  emit(type: string, data?: object) {
    const event = data === undefined
      ? new Event(type)
      : ({ data: JSON.stringify(data) } as unknown as Event);
    for (const listener of this.listeners.get(type) ?? []) listener(event);
  }
}

const workspaceId = "11111111-1111-4111-8111-111111111111";
const conversationId = "22222222-2222-4222-8222-222222222222";
const runId = "33333333-3333-4333-8333-333333333333";

function event(sequence: number, eventType: string): PublicRunEvent {
  return {
    sequence_number: sequence,
    event_type: eventType,
    payload: {},
    created_at: "2026-08-02T04:00:00Z",
    tool_provenance_complete: false,
  };
}

describe("helm persisted run stream", () => {
  it("connects only to the workspace-scoped helm SSE endpoint and deduplicates replay", () => {
    const source = new FakeEventSource();
    const received: number[] = [];
    const terminal = vi.fn();
    let requestedUrl = "";

    subscribeToRunEvents(workspaceId, conversationId, runId, {
      onOpen: vi.fn(),
      onEvent: (item) => received.push(item.sequence_number),
      onTerminal: terminal,
      onReconnect: vi.fn(),
      onFailure: vi.fn(),
    }, (url) => {
      requestedUrl = url;
      return source;
    });

    source.emit("run-event", event(0, "run.submitting"));
    source.emit("run-event", event(0, "run.submitting"));
    source.emit("run-event", event(1, "run.started"));
    source.emit("run-event", event(2, "run.completed"));

    expect(requestedUrl).toBe(runEventStreamUrl(workspaceId, conversationId, runId));
    expect(received).toEqual([0, 1, 2]);
    expect(terminal).toHaveBeenCalledOnce();
    expect(source.closed).toBe(true);
  });

  it("fails closed on an event gap and reports reconnecting for a recoverable transport error", () => {
    const source = new FakeEventSource();
    const reconnect = vi.fn();
    const failure = vi.fn();

    subscribeToRunEvents(workspaceId, conversationId, runId, {
      onOpen: vi.fn(),
      onEvent: vi.fn(),
      onTerminal: vi.fn(),
      onReconnect: reconnect,
      onFailure: failure,
    }, () => source);

    source.emit("error");
    source.emit("run-event", event(0, "run.submitting"));
    source.emit("run-event", event(2, "message.delta"));

    expect(reconnect).toHaveBeenCalledOnce();
    expect(failure).toHaveBeenCalledWith(expect.stringContaining("contains a gap"));
    expect(source.closed).toBe(true);
  });
});
