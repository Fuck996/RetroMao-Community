"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs"), path = require("node:path"), vm = require("node:vm");
const root = path.join(__dirname, "..");
async function bridge(capabilities = ["LIBRARY_READ", "LIBRARY_WRITE"], search = "") {
  const data = { manifest: { id: "example.test", defaultLocale: "zh-Hans", capabilities }, fixtures: JSON.parse(fs.readFileSync(path.join(root, "tools/preview/fixtures.json"), "utf8")) };
  const context = vm.createContext({ URL, URLSearchParams, TextEncoder, location: { search }, addEventListener() {}, fetch: async () => ({ ok: true, json: async () => data }) });
  vm.runInContext(fs.readFileSync(path.join(root, "tools/preview/mock-host.js"), "utf8"), context);
  let id = 0;
  return async (method, params = {}) => new Promise((resolve, reject) => {
    context.retromaoNative.onmessage = event => { const message = JSON.parse(event.data); if (message.error) reject(new Error(message.error)); else resolve(message.result); };
    context.retromaoNative.postMessage(JSON.stringify({ id: String(++id), method, params }));
  });
}
test("preview preserves capability checks and rejects unsupported methods", async () => {
  const call = await bridge([]);
  await assert.rejects(call("library.records", { limit: 10 }), /LIBRARY_READ/);
  await assert.rejects(call("invented.api"), /Unsupported preview method/);
});
test("preview paginates fixture records and applies explicit favorite values", async () => {
  const call = await bridge();
  const first = await call("library.records", { limit: 1 });
  assert.equal(first.games.length, 1);
  const second = await call("library.records", { limit: 1, after: first.next });
  assert.notEqual(first.games[0].id, second.games[0].id);
  await call("library.edit", { changes: [{ gameId: "demo-1", favorite: false }], checkpoint: { done: true } });
  await call("library.edit", { changes: [{ gameId: "demo-1", favorite: false }] });
  assert.equal((await call("library.games", { limit: 10, collection: "FAVORITES" })).games.length, 0);
  assert.deepEqual(await call("data.get"), { done: true });
});
test("configuration pages cannot run business actions or access the library", async () => {
  const call = await bridge(["LIBRARY_READ"], "?config=1");
  await assert.rejects(call("tasks.run", { action: "count" }), /configuration/);
  await assert.rejects(call("library.records", { limit: 10 }), /configuration/);
});
test("preview applies each edit batch atomically and exposes conflicts", async () => {
  const call = await bridge();
  await assert.rejects(call("library.edit", { changes: [{ gameId: "demo-1", favorite: false }, { gameId: "absent", favorite: true }] }), /Unknown game/);
  assert.equal((await call("library.game", { id: "demo-1" })).favorite, true);
  await assert.rejects(call("library.edit", { changes: [{ gameId: "demo-1", recent: { expected: {}, value: {} } }] }), /conflict/);
});
