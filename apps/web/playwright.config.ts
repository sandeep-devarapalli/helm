import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  testMatch: "**/*.e2e.ts",
  fullyParallel: false,
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: "list",
  outputDir: "../../output/playwright",
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    viewport: { width: 1440, height: 1000 },
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: [
    {
      command: "node e2e/mock-api.mjs",
      url: "http://127.0.0.1:8000/health",
      name: "mock helm API",
      reuseExistingServer: false,
    },
    {
      command: "pnpm exec vite --host 127.0.0.1 --port 5173 --strictPort",
      url: "http://127.0.0.1:5173",
      name: "Workbench",
      reuseExistingServer: false,
    },
  ],
});
