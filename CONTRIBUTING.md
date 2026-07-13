# Contributing to helm

helm welcomes focused contributions to its Workbench, control-plane foundation, Hermes profile, finance-tool boundary, and design system.

## Before starting

- Read `AGENTS.md` and the architecture documents.
- Open an issue before changing trust boundaries, runtime pins, domain contracts, or product direction.
- Never bundle upstream source, screenshots, credentials, broker data, or Hermes user state.
- Do not patch or fork Hermes inside helm.

## Development

```zsh
pnpm install
uv sync --all-groups
pnpm lint && pnpm typecheck && pnpm test && pnpm build
uv run ruff check . && uv run mypy services && uv run pytest
node scripts/verify-runtime-locks.mjs
docker compose -f infra/docker-compose.yml config
```

UI changes must use existing tokens and primitives, include real browser verification, and label every fixture/delayed/paper/live state. Runtime updates must change the relevant lock, upstream notice, compatibility evidence, and release notes together.

Keep pull requests small, explain why the change is necessary, and include verification evidence. Contributions are licensed under the repository MIT License.
