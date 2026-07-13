Entity or filter chip. `tone="entity"` is the blue inline ticker pill used when a symbol is mentioned in prose or a question.

```jsx
How does <Chip tone="entity" icon={<Landmark size={12} />}>NVDA</Chip>'s margin compare…
<Chip selected onClick={pick}>Momentum</Chip>
```

Default tone is the quiet bordered filter chip; `selected` fills it gray.
