One agent's live row inside a swarm-run status table. Render a header row yourself and stack these beneath it.

```jsx
<SwarmAgentRow name="Risk officer" role="review" status="running" tool="run_bench_strict" elapsed="1m 08s" iterations={5} output="Screening 460 factors…" />
```

`status`: `waiting | running | done | failed | blocked | retry | cancelled` (drives the status pill color). All other fields are optional and fall back to an em dash.
