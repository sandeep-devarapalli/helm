import * as React from "react";

/** Avatar — helm agent mark (ink square) or neutral user circle. */
export interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  /** "agent" (ink rounded square, mono glyph) or "user" (gray circle). Default "agent". */
  role?: "agent" | "user";
  /** Pixel size. Default 28. */
  size?: number;
  /** Override glyph / initial. */
  children?: React.ReactNode;
}

export function Avatar(props: AvatarProps): React.ReactElement;
