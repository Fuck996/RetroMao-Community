"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");

const root = path.join(__dirname, "..");
const inventory = JSON.parse(fs.readFileSync(path.join(root, "sdk/api.json"), "utf8"));
const sdk = fs.readFileSync(path.join(root, "sdk/runtime/retromao.js"), "utf8");

async function fixture() {
  const calls = [];
  const game = {
    id: "game-demo", platformId: "fc", favorite: false, hidden: false, localEntryRemoved: false,
    metadata: { title: "Demo", description: "", developer: "", publisher: "", genre: "", releaseDate: "", players: "", rating: null, sortTitle: "", extensions: {} },
    media: [], recent: { lastPlayedAt: null, playCount: 0, importedPlayTimeSeconds: null }, userEditedFields: [], userEditedMediaRoles: []
  };
  const task = { id: "task-demo", pluginId: "demo-plugin", version: "1.0.0", actionId: "run", state: "SUCCEEDED", message: "", completed: 1, total: 1, createdAt: 1, updatedAt: 2 };
  const source = { id: "source-demo", name: "Fixture", provider: "WEBDAV", scope: "scope-demo" };
  const responses = {
    "session.ready": () => ({ locale: "en", appLocale: "en", defaultLocale: "en", messages: {}, icons: ["star"] }),
    "library.game": () => game,
    "library.games": params => ({ games: params.after ? [] : [game], next: params.after ? null : { gameId: game.id } }),
    "library.records": params => ({ games: params.after ? [] : [{ id: game.id, platformId: game.platformId, title: game.metadata.title, romFileNames: ["demo.nes"], favorite: game.favorite, recent: game.recent }], next: params.after ? null : { gameId: game.id } }),
    "library.edit": params => params.returnGames === false ? null : [game],
    "media.folders": () => [{ id: "media-demo", platformId: "fc", role: "MEDIA", name: "Fixture media" }],
    "media.assets": params => params.afterPath ? [] : [{ folderId: "media-demo", path: "demo.png", revision: "r1", bytes: 100 }],
    "settings.get": () => ({}), "data.get": () => ({}), "data.patch": params => params,
    "storage.sources": () => [source], "storage.read": () => ({ token: "token-demo", value: null }), "storage.write": () => null,
    "http.request": () => ({ status: 200, headers: {}, body: "{}" }),
    "tasks.run": () => ({ ...task, state: "WAITING" }), "tasks.current": () => task, "tasks.get": () => task,
    "tasks.result": () => ({ dryRun: true }), "tasks.cancel": () => null, "tasks.progress": () => null
  };
  const port = { postMessage(raw) {
    const request = JSON.parse(raw);
    if (!request.method) return;
    calls.push(request);
    assert.ok(Object.hasOwn(responses, request.method), `Missing documented fixture: ${request.method}`);
    queueMicrotask(() => port.onmessage({ data: JSON.stringify({ id: request.id, result: responses[request.method](request.params) }) }));
  } };
  const context = vm.createContext({ android: { async getNamedPort() { return port; } }, console: { log() {} } });
  vm.runInContext(sdk, context);
  await new Promise(resolve => setImmediate(resolve));
  await context.retromao.ready;
  calls.length = 0;
  return { api: context.retromao, context, calls, port, task };
}

test("documented API surface exactly matches the shipped runtime", async () => {
  const { api } = await fixture();
  try {
    const paths = [];
    for (const [name, value] of Object.entries(api)) {
      if (name.startsWith("__")) continue;
      if (typeof value === "function" || typeof value !== "object" || typeof value.then === "function") paths.push(name);
      else for (const key of Object.keys(value)) paths.push(`${name}.${key}`);
    }
    assert.deepEqual(paths.sort(), inventory.members.map(entry => entry.path).sort());
    assert.equal(api.version, inventory.apiVersion);
  } finally { api.__dispose(); }
});

for (const entry of inventory.members) {
  test(`reference example executes through the real SDK: ${entry.path}`, { timeout: 5000 }, async () => {
    const { api, context, calls } = await fixture();
    try {
      await vm.runInContext(`(async () => { ${entry.example}\n })()`, context, { timeout: 1000 });
      if (entry.rpc && entry.path !== "ready") {
        assert.ok(calls.some(call => call.method === entry.rpc), `Example must call ${entry.path}`);
      }
      for (const call of calls) {
        assert.ok(inventory.members.some(member => member.rpc === call.method), `Undocumented RPC: ${call.method}`);
      }
    } finally { api.__dispose(); }
  });
}

test("reference task subscription receives pushes and unsubscribe releases it", async () => {
  const { api, port, task } = await fixture();
  try {
    const states = [];
    const stop = api.tasks.watch(task.id, current => states.push(current.state));
    port.onmessage({ data: JSON.stringify({ type: "task", task: { ...task, state: "RUNNING" } }) });
    stop();
    port.onmessage({ data: JSON.stringify({ type: "task", task }) });
    assert.deepEqual(states, ["RUNNING"]);
  } finally { api.__dispose(); }
});
