# AGENTS.md — helm

Instructions for coding agents working in this repository.

## What this repository is

helm is the full conversational operating system for AI trading. It is not merely a design system or a generic research chat. Users talk to Hermes; Hermes operates research, strategy work, and proposals across helm. Deterministic helm services own mandates, risk, execution, reconciliation, and audit state.

The upstream `NousResearch/hermes-agent` runtime is required and used unchanged. Do not vendor, fork, patch, or reimplement Hermes. Product behavior belongs in the versioned profile under `runtime/hermes-profile/`, helm-owned services, and curated MCP tools. Adopt upstream stable releases only through the compatibility-tested lock update workflow.

## Required reading

1. `README.md`
2. `docs/architecture/overview.md`
3. `docs/architecture/trust-boundaries.md`
4. `docs/brand/design.md` before UI work
5. The relevant `packages/ui/src/components/<group>/<Name>.prompt.md` before changing a primitive

## Product invariants

- Fixture, delayed, paper, and live states are always explicit and never conflated.
- Hermes may produce proposals and typed order intents; it cannot call brokers, read broker credentials, change policy, or operate the kill switch.
- No order exists without an active committed mandate and deterministic helm risk approval.
- Memory, preference, strategy, skill, risk, and mandate changes require explicit approval.
- Weak, partial, stale, or failed evidence stays visibly weak.
- Stage 1 health must not imply that research, execution, or learning exists.

## Code and repository rules

- Keep changes small and focused. Do not add later-stage behavior to foundation work.
- Prefer existing files and direct code over new abstractions.
- Use `packages/ui` tokens and primitives; numbers remain mono and Lucide is the only icon set.
- Never hand-edit generated files in `examples/design-reference/`.
- Never commit credentials, source screenshots, copied upstream assets, broker data, or user-owned Hermes state.
- Remove macOS-generated duplicate files such as `* 2.md` and `* 2.yml` before handoff; preserve the canonical file.
- Update this file after a user correction so the mistake is not repeated.

## Git and verification

- Use `main`; never force-push it without approval.
- Squash-merge pull requests.
- Run the affected pnpm and uv checks, runtime-lock verification, and Docker Compose validation.
- When tooling stalls in an iCloud-hosted workspace, check for File Provider placeholders and materialize or cleanly reinstall locked dependencies before retrying.
- Investigate failures at their root rather than retrying or skipping them.
