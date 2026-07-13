Browser-style workspace tab for the workbench tab strip. Compose a row of them above the content area.

```jsx
<Tab label="AAPL" icon={<Landmark size={13} />} active onClose={close} />
<Tab label="NVDA vs AMD m…" icon={<MessageSquare size={13} />} onClose={close} />
```

Active tabs get a white fill + 2px ink top bar. Labels are mono (tickers, thread titles). `onClose` adds the ×.
