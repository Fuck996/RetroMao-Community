"use strict";
const assert = require("node:assert/strict"), fs = require("node:fs"), path = require("node:path");
const { spawn, spawnSync } = require("node:child_process"), { once } = require("node:events");
const { chromium } = require("playwright");
const root = path.join(__dirname, "..");
(async () => {
  const server = spawn(process.env.RETROMAO_PYTHON || "python", ["-u", "tools/retromao.py", "preview", "extensions/azahar-plus", "--port", "0"], { cwd: root, windowsHide: true });
  let browser, output = "";
  try {
    const url = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error("Preview did not start: " + output)), 30000);
      server.once("error", error => { clearTimeout(timer); reject(error); });
      server.once("exit", code => { clearTimeout(timer); reject(new Error("Preview exited: " + code + output)); });
      server.stderr.on("data", data => { output += data; });
      server.stdout.on("data", data => { output += data; const match = output.match(/http:\/\/127\.0\.0\.1:\d+\//); if (match) { clearTimeout(timer); resolve(match[0]); } });
    });
    browser = await chromium.launch({ ...(process.env.RETROMAO_BROWSER_CHANNEL ? { channel: process.env.RETROMAO_BROWSER_CHANNEL } : {}), headless: true });
    const page = await browser.newPage({ viewport: { width: 1400, height: 1040 }, hasTouch: true });
    const errors = []; page.on("pageerror", error => errors.push(error.stack));
    await page.goto(url);
    for (const locale of ["zh-Hans", "zh-Hant", "en", "ja"]) for (const size of ["1280,720", "960,720", "720,720", "568,302"]) {
      await page.locator("#frame").evaluate((element, { locale, size }) => {
        const [width, height] = size.split(","); element.width = width; element.height = height;
        element.src = "/plugin/index.html?locale=" + locale + "&case=" + locale + size;
      }, { locale, size });
      const frame = page.frameLocator("#frame");
      await page.waitForFunction(({ locale, size }) => {
        const frame = document.querySelector("#frame"), doc = frame.contentDocument;
        return new URL(frame.contentWindow.location.href).searchParams.get("case") === locale + size &&
          doc?.documentElement?.lang === locale && doc.querySelectorAll(".entry").length === 2;
      }, { locale, size });
      await frame.locator(".entry").first().waitFor();
      await frame.locator("#add").tap();
      await frame.locator("#editor[open]").waitFor();
      assert.equal(await frame.locator("#platform").inputValue(), "3ds");
      assert.equal(await frame.locator("#package").inputValue(), "io.github.azaharplus.android");
      assert.equal(await frame.locator("#activity").inputValue(), "org.citra.citra_emu.activities.EmulationActivity");
      const actual = page.frames().find(item => item.url().includes("/plugin/"));
      assert.equal(await actual.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
      assert.equal(await frame.locator("#save").evaluate(element => { const r = element.getBoundingClientRect(); return r.bottom <= innerHeight && r.top >= 0; }), true);
      if (locale === "zh-Hans" && size === "1280,720") {
        fs.mkdirSync(path.join(root, "reports"), { recursive: true });
        await page.locator("#frame").screenshot({ path: path.join(root, "reports/custom-launchers-editor-16x9.png") });
      }
      await frame.locator("#platform").selectOption("nds");
      await frame.locator("#name").fill("Browser custom entry");
      await frame.locator("#package").focus(); await page.keyboard.press("ArrowDown");
      assert.notEqual(await actual.evaluate(() => document.activeElement.id), "package");
      await frame.locator("#save").tap();
      await frame.locator("#editor").waitFor({ state: "hidden" });
      const card = frame.locator(".entry").filter({ hasText: "Browser custom entry" });
      await card.waitFor();
      await card.locator("button").nth(1).tap();
      await card.locator("button").nth(1).waitFor({ state: "visible" });
      await page.waitForFunction(() => document.querySelector("#frame").contentDocument.querySelectorAll(".entry")[2].querySelectorAll("button")[1].disabled);
      await card.locator("button").first().tap();
      await frame.locator("#name").fill("Edited custom entry");
      if (!await frame.locator("#extras").isVisible()) await frame.locator("summary").tap();
      await frame.locator("#extras").fill('{"GamePath":"{romUri}","fullscreen":true,"index":2}');
      await frame.locator("#save").tap();
      await frame.locator("#editor").waitFor({ state: "hidden" });
      const edited = frame.locator(".entry").filter({ hasText: "Edited custom entry" });
      if (locale === "zh-Hans" && size === "1280,720") await page.locator("#frame").screenshot({ path: path.join(root, "reports/custom-launchers-list-16x9.png") });
      await edited.locator("button").last().tap();
      await frame.locator("#confirmation[open]").waitFor();
      await frame.locator("#delete-confirm").tap();
      await edited.waitFor({ state: "hidden" });
      assert.equal(await frame.locator(".entry").count(), 2);
      assert.equal(await frame.locator("#error").isVisible(), false);
    }
    assert.deepEqual(errors, []);
    process.stdout.write("Custom launch entries: four locales, 16:9/4:3/1:1, Azahar defaults, create/edit/delete/default, touch and directional focus passed. Preview fixtures only.\n");
  } finally {
    if (browser) await browser.close();
    if (server.exitCode === null) {
      const stopped = once(server, "exit");
      if (process.platform === "win32") {
        const result = spawnSync("taskkill", ["/PID", String(server.pid), "/T", "/F"], { windowsHide: true });
        if (result.status !== 0) throw new Error("Preview process cleanup failed: " + result.stderr);
      } else server.kill();
      await stopped;
    }
  }
})().catch(error => { process.stderr.write(error.stack + "\n"); process.exitCode = 1; });
