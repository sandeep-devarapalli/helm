# Trust boundaries

## Hermes boundary

Hermes receives conversation context, approved profile state, and curated tool schemas. It does not receive broker credentials, policy-administration tools, direct order-submission tools, or the kill switch. Memory and skill writes are approval-gated in `runtime/hermes-profile/config.yaml`.

## Finance-tool boundary

Stage 1 exposes six read-only Vibe tools: symbol search, market data, financial statements, stock profile, stock news, and SEC filings. Resources, prompts, sampling, filesystem tools, trading connectors, and shell tools are unavailable to Hermes.

## Future execution boundary

A future Hermes run may emit a typed `OrderIntent`. helm must persist it, validate an active mandate, apply deterministic risk rules, and produce an auditable `RiskDecision` before a paper adapter can submit it. Ambiguity, stale data, expired authority, duplicate idempotency keys, service failure, or an active kill switch fail closed.

## Operating-context boundary

Individual self-directed and institutional proprietary deployments have
separate legal entities or principals, workspaces, portfolios, accounts,
credentials, mandates, positions, approvals, reconciliation state, kill
switches, and audit records. No authority or data crosses that boundary.

Institutional policy defines roles and approval quorum outside Hermes.
Authentication alone is insufficient, and Hermes cannot hold an approving role.
See [operating contexts](operating-contexts.md).

## Runtime updates

Hermes runs from the immutable digest in `runtime/hermes.lock`. Stable releases are reviewed through an update issue and promoted only after compatibility tests. User data lives on a separate volume and must be snapshotted before any promoted update.
