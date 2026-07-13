A single stat cell: small gray label above a mono value. Compose in bordered grids for stat strips ("Prev Close / Market Cap / Open").

```jsx
<MetricTile label="Market Cap" value="$4.48T" />
<MetricTile label="Today" value="+3.69%" sentiment="positive" />
```

`sentiment`: `positive` (green) | `negative` (red) | `neutral` (ink). Pre-format values; optional `sub` line; `align="start"` for left-aligned cells.
