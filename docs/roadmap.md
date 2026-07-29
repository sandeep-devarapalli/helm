# Product roadmap

helm is a conversational operating system for AI trading. Hermes coordinates
conversation, research, preference recall, and proposals. helm owns identity,
entitlements, mandates, deterministic risk, execution, reconciliation, and
audit state.

This roadmap turns the dated
[July 2026 research snapshot](research/2026-07-29-product-regulatory-architecture-roadmap.md)
into maintained delivery milestones. It is a product and engineering plan, not
legal, regulatory, tax, or investment advice.

## Product direction

helm is being designed for two distinct operating contexts:

1. **Individual self-directed.** An individual operates helm for accounts and
   capital they own, subject to the rules of their jurisdiction and broker.
2. **Institutional proprietary.** A proposed Dubai-based helm entity operates
   helm only for the entity's own capital across approved markets.

A third context—advising, managing, or executing for clients—is disabled and
out of scope until separately designed and authorized.

Authentication alone never grants trading authority. Every live capability is
bound to an explicit tuple:

```text
operating_context
legal_entity
account_owner
jurisdiction
market
asset_class
broker_or_venue
data_entitlements
approval_policy
capability_expiry
```

Approval for one tuple never authorizes another. Individual paper readiness
does not establish institutional live eligibility, and a Dubai entity does not
automatically have access to U.S., Indian, crypto, or commodity markets.

See [operating contexts](architecture/operating-contexts.md) for the authority
and isolation model.

## Non-negotiable boundaries

- Hermes is an untrusted proposal generator. It cannot access broker
  credentials, submit orders, change policy, approve itself, or operate the
  kill switch.
- Fixture, delayed, paper, and live behavior remain visibly distinct.
- No order exists without an active mandate and deterministic risk approval.
- Unknown broker state, stale or unentitled data, unresolved reconciliation,
  or missing authority fails closed.
- Monetary state uses decimal arithmetic with explicit units and currencies.
- Instrument identity is separate from venue and broker symbols.
- Market-data display, non-display, historical, derived, redistribution, and
  model-training rights are explicit data.
- Live enablement is a dated, revocable capability—not a configuration toggle
  selected by Hermes.
- `capital_owner = mandate_owner = broker_account_owner`; cross-owner execution
  fails closed.

## Delivery order

The preferred sequence is:

```text
shared foundation
→ real Hermes conversation
→ multi-market identity and entitlement model
→ auditable research and reproducible simulation
→ mandates, risk, governance, and reconciliation
→ U.S. equities paper
→ Dubai institutional paper operations
→ Indian equities research and sandbox
→ crypto spot and commodity-ETF paper
→ approved learning
→ one independently gated live pilot
→ direct commodity futures later
```

U.S. equities remain the first execution proof because they best match the
current foundation and available paper tooling. Multi-market concepts are
modeled before broker adapters so U.S.-specific assumptions do not become the
platform's permanent domain model.

## Milestones

### M0 — Public foundation closure

**Outcome:** a reproducible public foundation with upstream Hermes unchanged
and only curated read-only finance tools.

**Exit gates:**

- A clean clone starts web, API, worker, Postgres, pinned Hermes, and pinned
  Vibe through one documented flow.
- Hermes loads the helm profile and discovers only approved tools.
- Compatibility, forbidden-tool, secret, dependency, and runtime-lock checks
  pass in CI.
- Health signals do not imply that research or trading exists.

### M1 — Operating contexts and jurisdiction decisions

**Outcome:** the individual and proposed Dubai institutional contexts have
separate authority, entity, account, data, and deployment profiles.

**Exit gates:**

- Record entity, account-owner, revenue, custody, customer, and first-live-use
  decisions as architecture records.
- Compare DIFC/DFSA, a Dubai non-financial free zone or mainland structure,
  and other advised UAE alternatives before selecting a domicile.
- Obtain qualified advice on own-account dealing, crypto/VARA scope,
  commodities, cross-border market access, corporate tax, substance,
  AML/sanctions, beneficial ownership, and reporting.
- Obtain a regulator pre-application or perimeter response where counsel
  advises one; never infer an exemption from the phrase “own account.”
- Confirm broker and data-provider eligibility in writing for the selected
  entity and activity.
- Keep client advisory, managed accounts, pooled capital, and copy trading
  disabled.

M1 is an immediate parallel workstream, but it does not block paper engineering.
It blocks institutional live activation.

### M2 — Persistent Hermes conversation

**Outcome:** conversations and Hermes runs survive refresh and restart.

**Exit gates:**

- Persist workspaces, conversations, messages, agent runs, and ordered events.
- Project upstream Hermes events without duplicating its agent loop.
- Stream resumable events without gaps or duplicates.
- Stage every memory or learned-preference write for explicit approval.
- Preserve tool provenance, citations, failure state, and operating context.

### M3 — Multi-market foundation

**Outcome:** canonical market identity and accounting work for the target
markets before any broker-specific execution.

**Exit gates:**

- Model instruments separately from listings, venues, broker symbols, and
  derivative contracts.
- Support currencies and FX, decimal precision, calendars, sessions,
  settlement, corporate actions, tax lots, and data entitlements.
- Normalize representative fixtures for AAPL, RELIANCE, BTC/USD, a
  commodity ETF, and a later futures contract without symbol ambiguity.
- Isolate legal entity, workspace, portfolio, broker account, credentials,
  positions, and audit state.

### M4 — Auditable research and reproducible validation

**Outcome:** Hermes can produce evidence-backed research and deterministic
strategy evidence, not unsupported recommendations.

**Exit gates:**

- Persist goals, hypotheses, claims, evidence, falsifiers, and immutable
  strategy versions.
- Label source, observation time, market-data entitlement, staleness, and
  uncertainty.
- Reproduce an identical run-card hash from identical inputs.
- Model fees, slippage, FX, corporate actions, and weak validation honestly.
- Evaluate mature backtesting engines before building broad framework scope.

### M5 — Mandates, deterministic risk, and governance

**Outcome:** typed proposals become bounded mandates only through helm-owned
policy and authorized approval.

**Exit gates:**

- Compile strict proposals into versioned, signed, expiring mandates.
- Enforce exposure, concentration, loss, frequency, session, freshness, and
  entitlement limits outside Hermes.
- Add idempotency, replay protection, reconciliation holds, and kill switches.
- Support individual-owner approval and institutional role-based maker-checker
  approval without sharing authority.
- Produce an append-only audit trail with machine-readable rule decisions.

### M6 — U.S. equities paper

**Outcome:** one narrow U.S.-equities paper adapter proves execution and
reconciliation.

**Initial capability:** cash-only, long-only, whole-share, regular-session,
`DAY LIMIT` orders for allowlisted U.S.-listed equities and unleveraged ETFs.

**Exit gates:**

- One valid paper order executes and reconciles after restart.
- Duplicate requests, stale data, unknown order state, unsupported products,
  and every deliberate policy violation fail closed.
- Paper results are never presented as evidence of live performance.

### M7 — Dubai institutional paper operations

**Outcome:** the proposed institution can rehearse its own-capital operating
model without live authority.

**Exit gates:**

- Implement legal-entity, portfolio, account, role, approval, and segregation-
  of-duties boundaries.
- Add independent reconciliation, books-and-records retention, incident
  control, surveillance evidence, and administrator rearming.
- Confirm professional/nonprofessional data classification and non-display
  rights for each provider.
- Evaluate brokers for entity onboarding and multi-asset coverage; do not
  inherit an individual account's eligibility or terms.

### M8 — Indian equities research and sandbox

**Outcome:** NSE/BSE research, a deterministic local simulator, and a
broker-supported sandbox operate without claiming live eligibility.

**Exit gates:**

- Model INR accounting, venue calendars, tick sizes, price bands, freeze
  quantities, settlement, and corporate actions.
- Pass a supported broker sandbox workflow plus local deterministic paper tests.
- Treat Indian-resident self-directed access and Dubai-entity access as
  separate legal, broker, tax, custody, and market-access questions.
- Obtain a Designated Depository Participant or custodian feasibility opinion
  on the proposed entity's FPI eligibility, ownership/control, PAN, KYC, bank,
  demat, and custody path before institutional execution-adapter work.
- Keep Indian live execution blocked pending current broker and qualified
  regulatory confirmation.

### M9 — Crypto spot and commodity-ETF paper

**Outcome:** two bounded paper profiles extend the shared control plane.

**Exit gates:**

- Crypto is spot-only, unleveraged, allowlisted, continuously reconciled, and
  uses keys with withdrawals and transfers disabled at the venue.
- Crypto models 24/7 risk days, precision, fees, venue outages, and asset and
  venue concentration.
- The proposed Dubai institution documents the applicable VARA NOC,
  registration, licensing, venue, custody, AML/sanctions, and Travel Rule path
  before funded virtual-asset trading.
- Commodity exposure is initially through explicitly allowlisted unleveraged
  listed ETFs and remains labeled as securities exposure.
- Crypto and commodity eligibility are evaluated separately for the individual
  and proposed Dubai institutional contexts.

### M10 — Approved learning

**Outcome:** Hermes improves from outcomes without silently changing trading
authority.

**Exit gates:**

- Separate hard constraints, soft preferences, and reusable skills.
- Group evidence-backed learning proposals for approval.
- Apply only approved changes to future runs.
- Rejected learning leaves behavior unchanged.
- Learning cannot modify limits, mandates, roles, live capabilities, or policy.

### M11A — Individual live-pilot gate

**Outcome:** one counsel- and broker-approved individual, account, market, and
capability may be considered for a tightly bounded pilot.

**Gate:** qualified legal review, broker approval, market-data rights, security
review, separate live deployment, incident recovery, reconciliation, and dated
capability approvals are complete. No roadmap milestone guarantees activation.

### M11B — Dubai institutional live-pilot gate

**Outcome:** the proposed Dubai entity may be considered for one own-capital
market pilot.

**Gate:** entity formation and substance, written regulatory-perimeter advice
or applicable approval/NOC/registration, broker/entity onboarding, beneficial
ownership and AML/sanctions, tax and reporting, professional data rights,
governance, independent security, and market-specific access are documented
and approved. This gate is independent from M11A.

### M12 — Direct commodity futures and derivatives

**Outcome:** deferred until direct futures are demonstrably necessary.

**Gate:** applicable regulatory classification, broker and exchange approval,
professional data rights, margin, position limits, expiry, rolling,
first-notice, delivery, overnight risk, and incident controls are proven.
Commodity ETFs do not satisfy this gate for futures.

## Current implementation slice

The next engineering PR after foundation closure should implement only the
Stage 2A persistence spine:

- `Workspace`
- `Conversation`
- `Message`
- `AgentRun`
- ordered `RunEvent`
- the first Alembic migration
- create/list/get conversation endpoints
- persistence and isolation tests

Hermes invocation, SSE projection, and Workbench activation should follow in
separate focused PRs. In parallel, M1 should produce the Dubai counsel and
broker decision packet; it should not add live code.

## Planning rules

- GitHub milestones mirror these headings; issues carry market and operating-
  context labels.
- A milestone is complete only when its exit gates have evidence.
- Legal or broker review tasks record decisions and sources but never claim
  authorization beyond written scope.
- Dates are assigned only after dependencies, entity choices, and external
  onboarding are known.
- The roadmap is updated when assumptions change; the dated research snapshot
  remains immutable apart from provenance corrections.
