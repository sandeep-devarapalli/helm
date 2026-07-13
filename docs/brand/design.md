# helm — Design Specification

The single-source design spec for **helm**, the agent-operated trading studio ("vibe trading" operated by the Hermes agent). Read this before writing any UI. The deeper design guide with sources and rationale is `readme.md`; this file is the condensed spec.

## Identity

- **Name:** helm — always lowercase, always IBM Plex Mono semibold. The wordmark IS the logo today; no mark has been adopted yet.
- **Logo (exploration, not yet adopted):** four candidate marks live in `explorations/Logo Exploration.html` — **1a The wheel** (literal ship's helm, ring + eight handles in the 2px icon grammar), **1b The turn** (same wheel with the NE handle green and extended — steered up-and-to-the-right), **1c The tick ring** (wheel abstracted to twelve radial ticks, echoing the product's consensus tick-strips), **1d The prompt** (no pictogram; wordmark + green block cursor, `helm▊`). Until one is chosen, keep using the type-only wordmark and do not invent other marks.
- **Vibe:** a calm paper workbench — an IDE for investing. Native-macOS-app feel: quiet, dense-but-breathing, zero gloss, no hype.
- **Pitch framing:** users describe strategies in plain language; the **Hermes agent** researches, backtests, and runs them live — inside mandates the user commits. Safety (visible tool calls, approval diffs, hard limits) is a first-class feature.

## Color

Use CSS custom properties from `styles.css` (definitions in `tokens/colors.css`). Never hardcode hex values.

| Role | Token | Value |
|---|---|---|
| Page | `--color-bg` | hsl(60 20% 99%) warm paper |
| Content surface | `--color-surface` | white |
| Quiet panel fill | `--color-panel` / `--color-panel-hover` | 96% / 92% |
| Hairline border | `--color-border` / `--color-border-strong` | 90% / 84% |
| Text | `--color-text` (ink 11%), `--color-text-2`, `--color-text-muted`, `--color-text-faint` | |
| Primary action | `--color-primary` | **ink-black**, not green |
| Brand/market accent | `--color-accent` | green hsl(152 55% 32%) — up, Buy, charts, commits |
| Down/bearish | `--color-down` | red hsl(3 62% 52%) |
| Links & entity pills | `--color-link` | blue hsl(217 72% 50%) — nothing else |

Semantic colors always render as **soft tint fill + solid colored text** (`--color-*-soft` backgrounds). Dark mode does not exist.

## Typography

- **UI / display:** IBM Plex Sans 400–700. Display weight 600, tracking −1.5%.
- **Mono (IBM Plex Mono):** the wordmark, every price, ticker, timestamp, percentage, tab label, account email — every figure, always `tabular-nums`. Numbers are NEVER set in the sans face.
- Scale (from `tokens/typography.css`): body 14px, sidebar nav 15px, card titles 18px, entity titles 28px, marketing headings 40px, hero 56px. Micro-labels 11px uppercase with 0.08em tracking.
- Analyst answers **bold the lead sentence carrying the headline number**.

## Layout & spacing

- 4px grid; card padding 16–24px. Explorer sidebar 240px, analyst panel 380px, tab strip 44px (`tokens/spacing.css`).
- Hairline 1px borders carry all structure. Stat grids are bordered cell grids (internal hairlines), not floating tiles.
- Radii: 6 controls · 8 buttons/inputs/tabs · 10 cards · 14 chat blocks · 20 window mock · full pills.
- Shadows near-zero: xs (logo tiles, composer), sm (raised cards), `--shadow-window` only under the marketing macOS mock.

## Interaction

- Hover: fills shift one panel step (transparent → panel → panel-2); text muted → ink. No scale/bounce.
- Active tab: white fill + 2px ink top bar. Active subnav: 2px ink underline.
- Motion: 120/200/320ms color/opacity transitions only. Thinking dots for agent latency. No decorative animation.

## Charts

Thin 1.8px green line + soft gradient fill fading to transparent; red when the period is down. No gridlines in small charts. Consensus = tick-mark strips (red → gray → green).

## Iconography

**Lucide only.** Outline, 2px stroke, `currentColor`. Vocabulary: `landmark` = ticker/company, `wrench` = tool call, chevron = thought/expand, `dollar-sign` Portfolio, `target` Monitors, `zap` Skills, `message-square` threads, `shield` mandates, `arrow-up` send. **No emoji, no filled icons, no mixed sets, no hand-drawn SVGs.**

## Voice

- Calm, evidential, work-shown. Number first, then reasoning. Sentence case everywhere.
- Tickers mono caps (`AAPL · NASDAQ`); signed directional figures (`+$10.86 (+3.69%)`).
- Never: hype, guarantees, exclamation marks, emoji, synergy-speak.
- Safety stated plainly: "Nothing trades until you commit a mandate." / "Nothing is written until you approve it."

## Markets & number formatting

helm covers **US equities, Indian equities (NSE/BSE), and crypto**. All figures IBM Plex Mono + `tabular-nums`; direction colors identical across markets (green up / red down).

- **US equities:** `AAPL · NASDAQ` · `$305.24` · `+$10.86 (+3.69%)` · caps in `$T`/`$B`.
- **Indian equities:** `RELIANCE · NSE` · `₹2,904.15` · `+₹31.20 (+1.09%)` · market caps in lakh crore: `₹19.65L Cr`.
- **Crypto:** pair notation `BTC/USD · 24/7` · no "close" language — use 24h low/high/volume · coins glyph (Lucide `coins`) instead of `landmark` in watchlists/tabs.
- Specimen: `foundations/type-markets.card.html`. Live data shapes: `ui_kits/console/data.jsx` (AAPL/NVDA/TSLA/RELIANCE/BTC/ETH).

## Component inventory

React primitives in `components/` (each has `.jsx` + `.d.ts` + `.prompt.md` + a card HTML):

Button, IconButton · Card, Badge, Chip · Input · MetricTile, ProgressBar · Tab, WatchlistRow · Avatar, ChatBubble, ToolCallRow, SwarmAgentRow, MandateCard.

Compose these; do not re-implement them inside screens. Reference implementations of full screens: `ui_kits/console/` (workbench) and `ui_kits/landing/` (marketing).
