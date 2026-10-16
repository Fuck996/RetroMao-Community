"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { chromium } = require("playwright");
const root = path.join(__dirname, "..");
const shared = path.join(root, "examples/activity-sync-shared");
const output = path.join(root, "../app/build/reports/ui-screenshots");
const sdk = fs.readFileSync(path.join(root, "sdk/runtime/retromao.js"), "utf8");

function bridge() {
  const source = { id: "drive", name: "演示网盘", provider: "WEBDAV", scope: "example" };
  const result = { scope: source.scope, localCount: 42, updated: 8, uploaded: 2, unmatched: 1, skipped: 0, finishedAt: 1780000000000,
    unmatchedGames: [{ platformId: "dc", title: "Shenmue II" }] };
  let task = null;
  window.retromaoNative = { postMessage(raw) {
    const request = JSON.parse(raw);
    let response;
    switch (request.method) {
      case "session.ready": response = { locale: window.testLocale, colors: { text: "#ece5da", background: "#171614", surface: "#24211c", outline: "#514b42", primary: "#e4bd83", muted: "#bdb4a7" } }; break;
      case "storage.sources": response = [source]; break;
      case "data.get": response = { destination: source, lastSync: { scope: source.scope, ...result } }; break;
      case "data.patch": response = request.params; break;
      case "tasks.current": response = task; break;
      case "tasks.run": response = task = { id: "task", state: "RUNNING", completed: 1, total: 3, message: "DC" }; break;
      case "tasks.cancel": task = { ...task, state: "CANCELLED" }; response = null; break;
      case "tasks.result": response = result; break;
      default: throw new Error("Unexpected page request: " + request.method);
    }
    queueMicrotask(() => {
      window.retromaoNative.onmessage({ data: JSON.stringify({ id: request.id, result: response }) });
      if (task) window.retromaoNative.onmessage({ data: JSON.stringify({ type: "task", task }) });
    });
  } };
}

(async () => {
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ channel: "msedge", headless: true });
  try {
    for (const kind of ["favorites", "recent"]) for (const [width, height] of [[1280, 720], [960, 720], [720, 720]]) {
      const context = await browser.newContext({ viewport: { width, height }, isMobile: false, hasTouch: true });
      try {
        const page = await context.newPage();
        const errors = []; page.on("pageerror", error => errors.push(error.message));
        await page.route("https://plugin-test.local/**", async route => {
          const file = new URL(route.request().url()).pathname.slice(1) || "index.html";
          const target = file.startsWith("__retromao/") ? path.join(root, "sdk/runtime", file.slice(11)) :
            ["mode.js", "icon.png"].includes(file) ? path.join(root, "examples", kind === "favorites" ? "favorites-sync" : "recent-sync", file) : path.join(shared, file);
          await route.fulfill({ path: target });
        });
        await page.addInitScript("window.testLocale='zh-Hans';(" + bridge.toString() + ")();\n" + sdk);
        await page.goto("https://plugin-test.local/");
        await page.waitForFunction(() => document.querySelector("#localCount").textContent === "42");
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
        await page.locator("#sync").scrollIntoViewIfNeeded();
        assert.equal(await page.locator("#sync").isEnabled(), true);
        await page.locator("#source").focus(); await page.keyboard.press("ArrowDown");
        assert.equal(await page.locator("#sync").evaluate(element => element === document.activeElement), true);
        await page.locator("#sync").tap(); await page.waitForFunction(() => !document.querySelector("#cancel").hidden);
        assert.equal(await page.locator("#source").isDisabled(), true);
        await page.locator("#cancel").tap(); await page.waitForFunction(() => document.querySelector("#cancel").hidden);
        assert.equal(await page.locator("#sync").isEnabled(), true);
        await page.screenshot({ path: path.join(output, "sync-" + kind + "-" + width + "x" + height + ".png"), fullPage: true });
        assert.deepEqual(errors, []);
        process.stdout.write(kind + " " + width + "x" + height + ": touch, focus, progress, cancel OK\n");
      } finally { await context.close(); }
    }
  } finally { await browser.close(); }
})().catch(error => { process.stderr.write(error.stack + "\n"); process.exitCode = 1; });
