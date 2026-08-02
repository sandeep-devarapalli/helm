# Architecture overview

helm starts as a modular monolith plus one durable worker.

- `apps/web` renders the conversational Workbench.
- `services/api` is the future canonical control plane for workspaces, conversations, research, mandates, policy, paper execution, and audit state.
- `services/worker` will claim durable research and backtest jobs.
- Postgres is canonical. SSE will project persisted ordered events to the browser.
- Upstream Hermes owns the agent loop, sessions, planning, memory, skills, and tool coordination.
- Pinned Vibe-Trading exposes a narrow finance MCP surface.

The current foundation includes persisted Hermes conversations, ordered event
projection, approval-gated preferences, and the M3A market-identity spine.
Research, backtesting, mandates, broker integration, and paper or live execution
remain later explicit stages.

helm is designed for isolated individual self-directed and institutional
proprietary operating contexts. Authentication does not imply trading
authority, and the two contexts never share credentials, accounts, mandates,
positions, or audit state. See [operating contexts](operating-contexts.md) and
the maintained [product roadmap](../roadmap.md).

## Operating loop

```text
Understand → Research → Validate → Decide → Propose mandate
→ Authorized principal commits → Execute inside mandate → Reconcile
→ Propose improvements → User approves or rejects
```

The model never becomes the policy or execution system.
