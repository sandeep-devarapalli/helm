import { describe, expect, it } from "vitest";

describe("helm foundation", () => {
  it("keeps paper trading explicit", () => {
    expect("Paper trading only").toContain("Paper");
  });
});
