import * as React from "react";

/**
 * One turn in the analyst thread.
 */
export interface ChatBubbleProps extends React.HTMLAttributes<HTMLDivElement> {
  /** "user" = gray rounded question block; "agent" = plain rich text. */
  role?: "user" | "agent";
  /** Quiet mono time label. */
  timestamp?: string;
  children?: React.ReactNode;
}

export function ChatBubble(props: ChatBubbleProps): React.ReactElement;
