The pre-trade consent tile the Hermes agent proposes before any live order — shows concrete guard rails and a commit action. Render 2–3 side by side as options.

```jsx
<MandateCard ordinal={2} label="Balanced" universe="US tech" maxOrder="$5,000" dailyCap="10 trades/day" leverage="no leverage" active onCommit={commit} />
```

Set `active` on the recommended option. `notes` adds an explanatory line. This is a safety surface — always surface the real limits, never hide them.
