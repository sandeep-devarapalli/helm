One turn in the analyst thread.

```jsx
<ChatBubble role="user">How does NVDA's gross margin compare to AMD's?</ChatBubble>
<ChatBubble role="agent"><strong>NVDA's gross margin has run 20–25 points above AMD's</strong> over the trailing four quarters…</ChatBubble>
```

`role="user"` renders the question as a quiet gray rounded block; `role="agent"` renders plain rich text — bold the lead sentence. Put ToolCallRows between question and answer.
