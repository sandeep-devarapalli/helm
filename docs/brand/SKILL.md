---
name: helm-design
description: Use this skill to generate well-branded interfaces and assets for helm, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

helm is an agent-operated trading studio: users describe strategies in plain language and the Hermes agent researches, backtests, and runs them inside user-committed mandates — across US equities, Indian equities (NSE/BSE, ₹), and crypto (24/7). The look is a calm, light "paper workbench" — warm off-white surfaces, ink text, hairline borders, IBM Plex Sans for UI, IBM Plex Mono for the lowercase `helm` wordmark and every number, green `hsl(152 55% 32%)` as the market/brand accent, ink-black primary buttons, Lucide icons, no emoji.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. Link `styles.css` and build with the token CSS custom properties. If working on production code, copy assets and read the rules here to become an expert in designing with this brand.

Key files:
- `styles.css` — the single stylesheet to link (imports all tokens/fonts).
- `design.md` — condensed design spec (color, type, markets & number formatting, icons, voice).
- `tokens/` — colors, typography, spacing, effects, fonts, base.
- `components/` — React primitives (Button, IconButton, Card, Badge, Chip, Input, MetricTile, ProgressBar, Tab, WatchlistRow, Avatar, ChatBubble, ToolCallRow, SwarmAgentRow, MandateCard) with `.d.ts` + `.prompt.md`.
- `examples/design-reference/ui_kits/console/` — the original interactive Workbench reference (ticker workspace + Hermes analyst panel).
- `ui_kits/landing/` — the marketing landing page.
- `foundations/` — specimen cards for colors, type, spacing, brand voice, iconography, wordmark.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.
