Collapsed tool-call or thought row in the analyst thread — how the agent "shows its work".

```jsx
<ToolCallRow kind="thought" label="Thought" />
<ToolCallRow label="Get Financials" detail="1.2s" onClick={expand} />
```

`kind="tool"` (default) renders the gray rounded row with a wrench; `kind="thought"` renders the quiet chevron row. Stack them between the user question and the answer text.
