import { describe, expect, it } from "vitest";
import { parseRoadmap, roadmapSnapshot } from "./roadmap";

const milestoneCodes = [
  "M0", "M1", "M2", "M3", "M4", "M5", "M6",
  "M7", "M8", "M9", "M10", "M11A", "M11B", "M12",
];

describe("public roadmap snapshot", () => {
  it("covers every canonical milestone with the current public status", () => {
    expect(roadmapSnapshot.date).toMatch(/^[A-Z][a-z]+ \d{1,2}, \d{4}$/);
    expect(roadmapSnapshot.milestones.map(({ code }) => code)).toEqual(milestoneCodes);
    expect(roadmapSnapshot.milestones.every(({ status, tone }) => status && tone)).toBe(true);
  });

  it("fails closed when a milestone loses its public status", () => {
    const withoutM3Status = `## Progress snapshot — August 7, 2026

| Milestone | Status | Evidence and remaining gate |
| --- | --- | --- |

### M3 — Multi-market foundation

**Outcome:** Canonical identities work across target markets.
`;
    expect(() => parseRoadmap(withoutM3Status)).toThrow("Roadmap public status is missing for M3");
  });
});
