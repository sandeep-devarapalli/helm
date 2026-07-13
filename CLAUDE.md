# CLAUDE.md — helm

helm is the full conversational operating system for AI trading. Hermes is the required upstream operating core and must remain unmodified. helm-owned code supplies the Workbench, profile distribution, curated finance tools, persistence, mandates, deterministic policy, execution boundaries, and audit state.

Read `README.md`, `docs/architecture/overview.md`, `docs/architecture/trust-boundaries.md`, and `AGENTS.md` before working. For UI changes, also read `docs/brand/design.md` and the relevant component prompt under `packages/ui`.

Never imply that a fixture is live, that a configured runtime is connected, or that a proposed trade executed. Never give Hermes broker credentials or the ability to alter policy or the kill switch. Do not fork or privately patch Hermes; contribute missing capabilities upstream or use its public profile, skill, MCP, plugin, and gateway surfaces.
