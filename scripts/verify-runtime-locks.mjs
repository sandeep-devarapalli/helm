import { access, readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const runtime = join(root, "runtime");
const hermes = JSON.parse(await readFile(join(runtime, "hermes.lock"), "utf8"));
const hermesCompatibility = JSON.parse(
  await readFile(join(runtime, "hermes.compatibility.json"), "utf8"),
);
const vibe = JSON.parse(await readFile(join(runtime, "vibe.lock"), "utf8"));

if (!/^v\d{4}\.\d+\.\d+(?:\.\d+)?$/.test(hermes.release)) throw new Error("Invalid Hermes release pin");
if (!/^sha256:[a-f0-9]{64}$/.test(hermes.digest)) throw new Error("Hermes image must use an immutable digest");
if (!/^v\d+\.\d+\.\d+$/.test(vibe.release)) throw new Error("Invalid Vibe release pin");
if (!/^[a-f0-9]{40}$/.test(vibe.commit)) throw new Error("Vibe commit must be immutable");
if (
  hermesCompatibility.runtime_release !== hermes.release ||
  hermesCompatibility.runtime_commit !== hermes.commit
) {
  throw new Error("Hermes compatibility fixture does not match the runtime lock");
}
if (
  hermesCompatibility.result !== "m2-memory-approvals" ||
  hermes.compatibility !== hermesCompatibility.result
) {
  throw new Error("Hermes memory compatibility review is incomplete");
}
const instructions = hermesCompatibility.contracts?.run_instructions;
if (
  instructions?.request_field !== "instructions" ||
  instructions?.runtime_field !== "ephemeral_system_prompt" ||
  instructions?.lifetime !== "current-run-only"
) {
  throw new Error("Hermes ephemeral instructions contract changed unexpectedly");
}
for (const source of [
  instructions.request_mapping_source,
  instructions.prompt_assembly_source,
  instructions.persistent_prompt_exclusion_source,
  hermesCompatibility.contracts?.memory?.configuration_source,
]) {
  if (typeof source !== "string" || !source.includes(`/blob/${hermes.release}/`)) {
    throw new Error("Hermes compatibility source does not match the pinned release");
  }
}
const memoryContract = hermesCompatibility.contracts?.memory;
if (
  memoryContract?.memory_enabled !== false ||
  memoryContract?.user_profile_enabled !== false ||
  memoryContract?.provider !== ""
) {
  throw new Error("Hermes compatibility fixture enables memory");
}

const profile = join(runtime, "hermes-profile");
const required = ["distribution.yaml", "SOUL.md", "config.yaml", "mcp.json"];
for (const file of required) await access(join(profile, file));

const config = await readFile(join(profile, "config.yaml"), "utf8");
if (!/^skills:\n  write_approval: true$/m.test(config)) throw new Error("Hermes skill writes must require approval");
if (!/^memory:\n(?:  .+\n)*  write_approval: true$/m.test(config)) {
  throw new Error("Hermes memory writes must require approval");
}
if (!/^memory:\n  memory_enabled: false\n  user_profile_enabled: false$/m.test(config)) {
  throw new Error("Hermes built-in memory must remain disabled until workspace isolation exists");
}
if (!/^memory:\n(?:  .+\n)*  provider: ""$/m.test(config)) {
  throw new Error("Hermes external memory provider must remain disabled");
}
if (!/^model:\n  default: gpt-5\.4-mini-2026-03-17\n  provider: openai-api\n  base_url: ""\n  api_mode: codex_responses$/m.test(config)) {
  throw new Error("Hermes model pin changed unexpectedly");
}
if (!config.includes("transport: sse")) throw new Error("Vibe 0.1.11 requires Hermes legacy SSE transport");
const expectedDisabledToolsets = [
  "terminal",
  "file",
  "browser",
  "web",
  "search",
  "vision",
  "image_gen",
  "tts",
  "messaging",
  "homeassistant",
  "spotify",
  "discord_admin",
  "code_execution",
  "rl",
];
const disabledToolsets = config.match(/agent:\n  disabled_toolsets:\n((?:    - .+\n?)+)/)?.[1]
  ?.trim()
  .split("\n")
  .map((line) => line.replace(/^\s*-\s*/, ""));
if (JSON.stringify(disabledToolsets) !== JSON.stringify(expectedDisabledToolsets)) {
  throw new Error("Hermes disabled toolsets changed unexpectedly");
}
if (!/^platform_toolsets:\n  api_server:\n    - vibe_trading$/m.test(config)) {
  throw new Error("Hermes API server must expose only the curated Vibe toolset");
}

const expectedTools = [
  "search_symbol",
  "get_market_data",
  "get_financial_statements",
  "get_stock_profile",
  "get_stock_news",
  "get_sec_filings",
];
const mcp = JSON.parse(await readFile(join(profile, "mcp.json"), "utf8"));
const tools = mcp.mcpServers?.vibe_trading?.enabledTools;
if (!Array.isArray(tools) || JSON.stringify(tools) !== JSON.stringify(expectedTools)) {
  throw new Error("Unexpected Vibe tool allowlist");
}

const configTools = config.match(/    tools:\n      include:\n((?:        - .+\n?)+)/)?.[1]
  ?.trim()
  .split("\n")
  .map((line) => line.replace(/^\s*-\s*/, ""));
if (JSON.stringify(configTools) !== JSON.stringify(expectedTools)) {
  throw new Error("Hermes config and MCP tool allowlists differ");
}

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
