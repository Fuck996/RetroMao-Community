"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");
const sdk = fs.readFileSync(path.join(__dirname, "../sdk/runtime/retromao.js"), "utf8");

async function host(environment = { locale: "en", icons: ["star", "history"] }) {
  const messages = [];
  const port = { postMessage(raw) { messages.push(JSON.parse(raw)); } };
  const context = vm.createContext({ android: { async getNamedPort(name) { assert.equal(name, "retromao"); return port; } } });
  vm.runInContext(sdk, context);
  await new Promise(resolve => setImmediate(resolve));
  const receive = value => port.onmessage({ data: JSON.stringify(value) });
  const request = messages.find(item => item.method === "session.ready");
  receive({ id: request.id, result: environment });
  await context.retromao.ready;
  messages.length = 0;
  return { api: context.retromao, context, messages, receive };
}

test("ready exposes the plugin-selected language and author messages without additional RPC", async () => {
  const environment = { locale: "en", appLocale: "ja", defaultLocale: "en", locales: ["en", "zh-Hans"], messages: { hint: "Choose" } };
  const { api, messages } = await host(environment);
  const selected = await api.ready;
  assert.equal(selected.locale, "en"); assert.equal(selected.appLocale, "ja");
  assert.equal(selected.messages.hint, "Choose"); assert.equal(selected.defaultLocale, "en");
  assert.equal(messages.length, 0);
  api.__dispose();
});

test("SDK throttles concurrent RPC and does not change favorite into toggle", async () => {
  const { api, messages, receive } = await host();
  const pending = Array.from({ length: 9 }, () => api.favorites.set("game", true));
  assert.equal(messages.length, 4);
  for (let index = 0; index < 9; index++) {
    const request = messages[index];
    assert.equal(request.method, "library.edit");
    assert.deepEqual(request.params.changes, [{ gameId: "game", favorite: true }]);
    receive({ id: request.id, result: [] });
  }
  await Promise.all(pending);
  api.__dispose();
  await assert.rejects(api.data.get(), /session closed/);
});

test("missing extension properties remain different from explicit JSON null", async () => {
  const { api, messages, receive } = await host();
  const storing = api.index.patch("game", { note: { value: null } });
  assert.deepEqual(messages[0].params.changes[0].extensions, { note: { value: null } });
  receive({ id: messages[0].id, result: [] }); await storing;
  const removing = api.index.patch("game", { note: { expected: null } });
  assert.deepEqual(messages[1].params.changes[0].extensions, { note: { expected: null } });
  receive({ id: messages[1].id, result: [] }); await removing;
  api.__dispose();
});

test("task watchers share pushed status and dispose rejects outstanding calls", async () => {
  const { api, messages, receive } = await host();
  const seen = [];
  receive({ type: "task", task: { id: "task", state: "RUNNING" } });
  const stop = api.tasks.watch("task", task => seen.push(task.state));
  receive({ type: "task", task: { id: "task", state: "SUCCEEDED" } });
  stop(); receive({ type: "task", task: { id: "task", state: "FAILED" } });
  assert.deepEqual(seen, ["RUNNING", "SUCCEEDED"]);
  const request = api.library.game("game");
  receive({ id: messages[0].id, error: "Capability denied" });
  await assert.rejects(request, /Capability denied/);
  const waiting = api.data.get();
  api.__dispose();
  await assert.rejects(waiting, /page closed/);
});

test("background actions use registered entry and surface real errors", async () => {
  const { api, messages, context } = await host();
  vm.runInContext("retromao.define({actions:{run: async args => ({note:args.note}), fail: () => {throw new Error('action failed')}}});", context);
  await api.__run("run", { note: "example" });
  assert.deepEqual(messages.pop(), { type: "complete", result: { note: "example" } });
  await api.__run("fail", {});
  const failed = messages.pop(); assert.equal(failed.type, "failure"); assert.match(failed.error, /action failed/);
  await api.__run("missing", {});
  assert.match(messages.pop().error, /not registered/);
  api.__dispose();
});

test("lightweight records, atomic checkpoints and scoped storage use the common bridge", async () => {
  const { api, messages, receive } = await host();
  const records = api.library.records();
  assert.equal(messages[0].method, "library.records"); assert.equal(messages[0].params.limit, 200);
  receive({ id: messages[0].id, result: { games: [], next: null } }); await records;
  const applied = api.library.apply([{ gameId: "game", favorite: true }], { baseline: { game: true } });
  assert.equal(messages[1].params.returnGames, false); assert.deepEqual(messages[1].params.checkpoint, { baseline: { game: true } });
  receive({ id: messages[1].id, result: null }); await applied;
  const source = { id: "drive", scope: "scope", name: "Drive", provider: "BAIDU" };
  const read = api.storage.read(source, "dc.json");
  assert.equal(messages[2].method, "storage.read"); assert.deepEqual(messages[2].params, { sourceId: "drive", scope: "scope", key: "dc.json" });
  receive({ id: messages[2].id, result: { token: "snapshot", value: null } }); await read;
  const write = api.storage.write("snapshot", { entries: [] });
  assert.deepEqual(messages[3].params, { token: "snapshot", value: { entries: [] } });
  receive({ id: messages[3].id, result: null }); await write; api.__dispose();
});

test("public icon names come from the host and need no per-icon RPC", async () => {
  const { api, messages } = await host();
  assert.deepEqual(Array.from(await api.icons.list()), ["star", "history"]);
  assert.equal(api.icons.url("star"), "/__retromao/icons/star.svg");
  assert.throws(() => api.icons.url("../private"), /Unknown public icon/);
  assert.equal(messages.length, 0); api.__dispose();
});
