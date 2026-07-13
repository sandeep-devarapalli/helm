# helm Workbench — UI kit

The core product surface: an Investi-style research + trading workbench operated by the Hermes agent.

**Entry:** `index.html` — fully interactive. Click watchlist rows to switch the workspace — US equities (AAPL / NVDA / TSLA), Indian equities (RELIANCE · NSE, ₹), and crypto (BTC / ETH — coins glyph, pair notation, 24h stats, crypto-specific subnav); switch chart ranges; then type in the analyst composer and send to watch Hermes assemble a desk, backtest, and propose mandates — commit one to see the live-run confirmation.

**Files**
- `index.html` — shell + all CSS (sidebar, tab strip, ticker page, analyst panel layout).
- `icons.jsx` — Lucide-path inline icon set (`window.Icons`).
- `data.jsx` — static ticker data + seeded chart series (`window.HelmData`).
- `Analyst.jsx` — right-hand analyst panel (default NVDA-vs-AMD thread + Hermes mandate flow).
- `Workbench.jsx` — sidebar, tabs, chart, stat grid, consensus card, facts column. Its self-mount is guarded (`window.HelmData` + `#root` + a once-flag) because the design-system compiler also bundles this file into `_ds_bundle.js` — keep the guard if you edit the mount.

**Composes:** Tab, WatchlistRow, ChatBubble, ToolCallRow, MandateCard, MetricTile, Badge, IconButton, Chip.

Surfaces recreated from the reference screenshots: explorer sidebar with watchlist, browser-style tab strip, ticker header with price, Overview subnav with Notes, chart card with range switcher, bordered stat grid, company facts column with description, analyst consensus card (distribution ticks, rating counts, price-target scale), and the analyst chat with visible tool calls.
