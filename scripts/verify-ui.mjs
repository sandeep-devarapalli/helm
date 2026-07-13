import { access, readdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "packages", "ui");
const groups = await readdir(join(root, "src", "components"), { withFileTypes: true });

for (const group of groups.filter((entry) => entry.isDirectory())) {
  const directory = join(root, "src", "components", group.name);
  const files = await readdir(directory);
  for (const file of files.filter((name) => name.endsWith(".jsx"))) {
    const base = join(directory, file.slice(0, -4));
    await access(`${base}.d.ts`);
    await access(`${base}.prompt.md`);
  }
}

await access(join(root, "styles.css"));
console.log("helm UI contracts verified");
