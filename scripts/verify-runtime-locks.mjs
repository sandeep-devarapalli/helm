import { access, readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const runtime = join(root, "runtime");
const hermes = JSON.parse(await readFile(join(runtime, "hermes.lock"), "utf8"));
const vibe = JSON.parse(await readFile(join(runtime, "vibe.lock"), "utf8"));

if (!/^v\d{4}\.\d+\.\d+(?:\.\d+)?$/.test(hermes.release)) throw new Error("Invalid Hermes release pin");
if (!/^sha256:[a-f0-9]{64}$/.test(hermes.digest)) throw new Error("Hermes image must use an immutable digest");
if (!/^v\d+\.\d+\.\d+$/.test(vibe.release)) throw new Error("Invalid Vibe release pin");
if (!/^[a-f0-9]{40}$/.test(vibe.commit)) throw new Error("Vibe commit must be immutable");

const profile = join(runtime, "hermes-profile");
const required = ["distribution.yaml", "SOUL.md", "config.yaml", "mcp.json"];
for (const file of required) await access(join(profile, file));

const config = await readFile(join(profile, "config.yaml"), "utf8");
if (!config.includes("write_approval: true")) throw new Error("Hermes writes must require approval");
if (!config.includes("transport: sse")) throw new Error("Vibe 0.1.11 requires Hermes legacy SSE transport");
for (const blocked of ["terminal", "file", "browser", "code_execution"]) {
  if (!config.includes(`- ${blocked}`)) throw new Error(`Hermes toolset ${blocked} must remain disabled`);
}

const mcp = JSON.parse(await readFile(join(profile, "mcp.json"), "utf8"));
const tools = mcp.mcpServers?.vibe_trading?.enabledTools;
if (!Array.isArray(tools) || tools.length !== 6) throw new Error("Unexpected Vibe tool allowlist");

const compose = await readFile(join(root, "infra", "docker-compose.yml"), "utf8");
const expectedImage = `${hermes.image}@${hermes.digest}`;
if (!compose.includes(expectedImage)) throw new Error("Compose Hermes image does not match runtime/hermes.lock");
if (!compose.includes(`HELM_HERMES_VERSION: ${hermes.release}`)) {
  throw new Error("API Hermes version does not match runtime/hermes.lock");
}
if (!compose.includes(`VIBE_TRADING_VERSION: ${vibe.release.slice(1)}`)) {
  throw new Error("Compose Vibe version does not match runtime/vibe.lock");
}
if (!compose.includes(`HELM_VIBE_VERSION: ${vibe.release}`)) {
  throw new Error("API Vibe version does not match runtime/vibe.lock");
}

console.log(`Hermes ${hermes.release} and Vibe ${vibe.release} locks verified`);
