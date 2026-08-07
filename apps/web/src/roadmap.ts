import roadmapMarkdown from "../../../docs/roadmap.md?raw";

export type RoadmapStatusTone = "complete" | "active" | "pending" | "planned" | "gated";

export type RoadmapMilestone = {
  code: string;
  title: string;
  outcome: string;
  status: string;
  tone: RoadmapStatusTone;
};

export type RoadmapSnapshot = {
  date: string;
  milestones: RoadmapMilestone[];
};

const toneByStatus: Record<string, RoadmapStatusTone> = {
  "Closure verification": "pending",
  "External evidence pending": "pending",
  Completed: "complete",
  "In progress": "active",
  Planned: "planned",
  "Gated or deferred": "gated",
};

function plainText(markdown: string) {
  return markdown
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function statusCodes(label: string, milestoneCodes: string[]) {
  const [start, end] = label.split(/[–-]/).map((code) => code.trim());
  if (!end) return [start];

  const startIndex = milestoneCodes.indexOf(start);
  const endIndex = milestoneCodes.indexOf(end);
  if (startIndex < 0 || endIndex < startIndex) {
    throw new Error(`Invalid roadmap status range: ${label}`);
  }
  return milestoneCodes.slice(startIndex, endIndex + 1);
}

export function parseRoadmap(markdown: string): RoadmapSnapshot {
  const date = markdown.match(/^## Progress snapshot — (.+)$/m)?.[1]?.trim();
  if (!date) throw new Error("Roadmap progress snapshot date is missing");

  const headings = [...markdown.matchAll(/^### (M\d+[A-Z]?) — (.+)$/gm)];
  if (!headings.length) throw new Error("Roadmap milestone headings are missing");

  const milestoneCodes = headings.map((match) => match[1]);
  const statuses = new Map<string, string>();
  for (const match of markdown.matchAll(/^\| (M\d+[A-Z]?(?:–M\d+[A-Z]?)?) \| ([^|]+) \|/gm)) {
    for (const code of statusCodes(match[1], milestoneCodes)) {
      if (statuses.has(code)) throw new Error(`Duplicate roadmap status for ${code}`);
      statuses.set(code, match[2].trim());
    }
  }

  const milestones = headings.map((heading, index) => {
    const code = heading[1];
    const sectionStart = heading.index ?? 0;
    const sectionEnd = headings[index + 1]?.index ?? markdown.length;
    const section = markdown.slice(sectionStart, sectionEnd);
    const outcome = section.match(/\*\*Outcome:\*\*\s*([\s\S]*?)(?=\n\n|$)/)?.[1];
    if (!outcome) throw new Error(`Roadmap outcome is missing for ${code}`);

    const status = statuses.get(code);
    if (!status) throw new Error(`Roadmap public status is missing for ${code}`);
    const tone = toneByStatus[status];
    if (!tone) throw new Error(`Roadmap public status is unsupported for ${code}: ${status}`);

    return {
      code,
      title: plainText(heading[2]),
      outcome: plainText(outcome),
      status,
      tone,
    };
  });

  return { date, milestones };
}

export const roadmapSnapshot = parseRoadmap(roadmapMarkdown);
