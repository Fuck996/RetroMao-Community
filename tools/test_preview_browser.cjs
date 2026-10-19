"use strict";
const assert = require("node:assert/strict"), fs = require("node:fs"), path = require("node:path");
const { spawn } = require("node:child_process"), { once } = require("node:events");
const { chromium } = require("playwright");
const root = path.join(__dirname, "..");
async function start(source) {
  const child = spawn(process.env.RETROMAO_PYTHON || "python", ["-u", "tools/retromao.py", "preview", source, "--port", "0"], { cwd: root, windowsHide: true });
  let output = "";
  const url = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error("Preview did not start: " + output)), 30000);
    child.on("error", error => { clearTimeout(timer); reject(error); });
    child.on("exit", code => { clearTimeout(timer); reject(new Error("Preview exited: " + code + " " + output)); });
    child.stderr.on("data", data => { output += data; });
    child.stdout.on("data", data => { output += data; const match = output.match(/http:\/\/127\.0\.0\.1:\d+\//); if (match) { clearTimeout(timer); resolve(match[0]); } });
  }).catch(error => { child.kill(); throw error; });
  return { url, async stop() { const exited = once(child, "exit"); child.kill(); await exited; } };
}
(async () => {
  const browser = await chromium.launch({ ...(process.env.RETROMAO_BROWSER_CHANNEL ? { channel: process.env.RETROMAO_BROWSER_CHANNEL } : {}), headless: true });
  try {
    const server = await start("templates/plugin");
    try {
      const page = await browser.newPage({ viewport: { width: 1400, height: 1000 }, hasTouch: true });
      const errors = []; page.on("pageerror", error => errors.push(error.message));
      await page.goto(server.url);
      for (const locale of ["zh-Hans", "en", "ja"]) for (const size of ["1280,720", "960,720", "720,720"]) {
        await page.locator("#locale").selectOption(locale);
        await page.locator("#size").selectOption(size);
        const frame = page.frameLocator("#frame");
        await frame.locator("#games li").first().waitFor();
        assert.equal(await frame.locator("#games li").count(), 2);
        await frame.locator("#run").tap();
        try {
          await frame.locator("#status").filter({ hasText: /: 2$/ }).waitFor({ timeout: 10000 });
        } catch (error) {
          throw new Error(JSON.stringify({ locale, size, status: await frame.locator("#status").innerText(), failure: await frame.locator("#error").innerText(), pageErrors: errors }) + "\n" + error.message);
        }
        assert.equal(await frame.locator("#error").innerText(), "");
        const actual = page.frames().find(frame => frame.url().includes("/plugin/"));
        assert.equal(await actual.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
        await frame.locator("#run").focus();
        await page.keyboard.press("ArrowDown");
        if (locale === "zh-Hans" && size === "1280,720") {
          fs.mkdirSync(path.join(root, "reports"), { recursive: true });
          await page.screenshot({ path: path.join(root, "reports/preview-16x9.png") });
        }
      }
      assert.deepEqual(errors, []);
      await page.close();
    } finally { await server.stop(); }
    for (const [source, expected] of [["templates/platform", "bluemsx"], ["languages/en.json", "Example"]]) {
      const server = await start(source);
      try {
        const page = await browser.newPage();
        await page.goto(server.url);
        await page.locator("#rows tr").first().waitFor();
        assert.ok(await page.locator("#rows tr").count() > 0);
        if (source.includes("platform")) assert.ok((await page.locator("#rows").innerText()).includes(expected));
        await page.locator("#locale").selectOption("ja");
        await page.close();
      } finally { await server.stop(); }
    }
    process.stdout.write("Independent preview: three languages, three ratios, touch, focus, worker, platform and language views OK\n");
  } finally { await browser.close(); }
})().catch(error => { process.stderr.write(error.stack + "\n"); process.exitCode = 1; });
