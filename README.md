# helm

helm is an open-source conversational operating system for AI trading. Users talk to Hermes; Hermes coordinates research, strategy validation, and proposals while helm owns deterministic mandates, policy, execution, reconciliation, and audit state.

This repository uses the upstream [Hermes Agent](https://github.com/NousResearch/hermes-agent) runtime unchanged and connects a pinned [Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) MCP runtime for curated finance tools. helm is not affiliated with Nous Research or HKUDS.

## Current status

Stage 1 is a public foundation, not a trading release.

- The Workbench shell and reusable helm UI package are present.
- The API and worker expose honest health/version surfaces.
- Hermes and Vibe versions are pinned, and the helm Hermes profile requires approval for memory and skill writes.
- The Hermes profile pins `gpt-5.4-mini-2026-03-17` through the upstream `openai-api` provider.
- Research, backtests, mandates, broker credentials, orders, fills, learning, and live trading are not implemented.
- Values visible in the Workbench are labeled fixtures. The product is paper-trading-first; live capital remains blocked.

## Architecture

```text
apps/web                React and TypeScript Workbench
services/api            FastAPI control plane foundation
services/worker         Durable-job worker foundation
packages/ui             helm tokens and React primitives
runtime/hermes-profile  helm-owned profile for upstream Hermes
runtime/*.lock          Verified upstream runtime pins
examples/design-reference
docs/architecture
docs/brand
infra/docker-compose.yml
```

The hard boundary is intentional:

1. Hermes may reason and propose.
2. Vibe tools may retrieve and analyze finance data.
3. Only helm-owned deterministic policy code may authorize an order.
4. No active mandate means no execution.

See [architecture overview](docs/architecture/overview.md) and [trust boundaries](docs/architecture/trust-boundaries.md).

## Direction and roadmap

helm is designed for two separate operating contexts: self-directed individuals
using their own accounts, and a proposed Dubai-based institutional entity using
only its own capital. Client advisory and managed-account activity remain
disabled and out of scope. No proposed entity location or paper capability
implies live-trading authorization.

See the maintained [product roadmap](docs/roadmap.md), the
[operating-context model](docs/architecture/operating-contexts.md), and the
dated [July 2026 research snapshot](docs/research/2026-07-29-product-regulatory-architecture-roadmap.md).

## Local development

Requirements: macOS, Docker Desktop, Node.js, pnpm through Corepack, Python 3.12, and uv.

```zsh
pnpm install
uv sync --all-groups

pnpm dev
uv run uvicorn helm.main:app --app-dir services/api --reload
```

Open the Workbench:

```zsh
open http://localhost:5173
```

Run the complete Stage 1 foundation:

```zsh
./scripts/configure-openai-key.sh
docker compose --env-file .env -f infra/docker-compose.yml up --build
open http://localhost:5173
```

The setup command prompts without echo and saves the provider credential in the ignored local `.env` file. The pinned Hermes container needs a configured model before conversation works. Stage 1 validates configuration and health only; it does not ship placeholder model credentials.

## Verification

```zsh
pnpm lint
pnpm typecheck
pnpm test
pnpm build

uv run ruff check .
uv run mypy services
uv run pytest
uv lock --check

node scripts/verify-runtime-locks.mjs
docker compose -f infra/docker-compose.yml config
```

## Upstream policy

- Hermes is required and used as published; private patches and forks are prohibited.
- `runtime/hermes.lock` pins the accepted stable release and immutable container digest.
- New stable releases produce an update-review issue. The lock changes only after compatibility and safety checks pass.
- `runtime/vibe.lock` pins the finance runtime. Hermes sees only the allowlisted read-only tools in the helm profile during Stage 1.
- Credentials and user-owned Hermes state remain outside the profile distribution and Git history.

## License

helm-owned code is MIT licensed. Upstream runtime and icon/font notices are recorded in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
