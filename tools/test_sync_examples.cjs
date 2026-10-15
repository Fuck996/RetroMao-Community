"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { test } = require("node:test");
const shared = path.join(__dirname, "../examples/activity-sync-shared");
const clone = value => JSON.parse(JSON.stringify(value));
const source = { id: "drive", name: "Drive", provider: "WEBDAV", scope: "account-root" };
const game = (id, extra = {}) => ({ id, platformId: "dc", title: "Shenmue II", romFileNames: ["Disc 1.chd", "Disc 2.chd"], favorite: false,
  recent: { lastPlayedAt: null, playCount: 0, importedPlayTimeSeconds: null }, ...extra });

function device(kind, games, cloud = new Map()) {
  const local = clone(games), data = { destination: source }, counts = { reads: 0, writes: 0, pages: 0, batches: 0 }, hooks = {};
  let document = null;
  const api = {
    ready: Promise.resolve({ locale: "en" }), data: { async get() { return clone(data); }, async patch(values) { Object.assign(data, clone(values)); } },
    tasks: { async progress() {} },
    library: {
      async records({ after, limit }) {
        counts.pages++;
        const start = after ? local.findIndex(item => item.id === after.gameId) + 1 : 0;
        const games = clone(local.slice(start, start + limit));
        return { games, next: start + limit < local.length ? { gameId: games.at(-1).id } : null };
      },
      async apply(edits, checkpoint) {
        if (hooks.beforeApply) hooks.beforeApply(edits);
        for (const edit of edits) {
          const item = local.find(game => game.id === edit.gameId);
          if (edit.recent) assert.ok(JSON.stringify(item.recent) === JSON.stringify(edit.recent.expected) || JSON.stringify(item.recent) === JSON.stringify(edit.recent.value));
        }
        for (const edit of edits) {
          const item = local.find(game => game.id === edit.gameId);
          if (edit.favorite !== undefined) item.favorite = edit.favorite;
          if (edit.recent) item.recent = clone(edit.recent.value);
        }
        if (checkpoint) Object.assign(data, clone(checkpoint));
        counts.batches++;
        if (hooks.afterApply) hooks.afterApply(edits);
      }
    },
    storage: {
      async sources() { return hooks.sources || [source]; },
      async read(target, key) {
        counts.reads++;
        if (hooks.beforeRead) hooks.beforeRead();
        document = kind + ":" + target.scope + ":" + key;
        return { token: "read-token", value: cloud.has(document) ? clone(cloud.get(document)) : null };
      },
      async write(token, value) { assert.equal(token, "read-token"); counts.writes++; cloud.set(document, clone(value)); }
    }
  };
  const context = vm.createContext({ retromao: api });
  for (const file of ["strings.js", "sync.js"]) vm.runInContext(fs.readFileSync(path.join(shared, file), "utf8"), context);
  return { local, data, cloud, counts, hooks, run: () => context.activitySync.run(kind) };
}

test("favorites merge once, propagate removal and stop writing unchanged documents", async () => {
  const a = device("favorites", [game("a", { favorite: true })]);
  const b = device("favorites", [game("b")], a.cloud);
  await a.run(); await b.run();
  assert.equal(b.local[0].favorite, true);
  b.local[0].favorite = false;
  await b.run(); await a.run();
  assert.equal(a.local[0].favorite, false);
  const written = a.counts.writes + b.counts.writes;
  await a.run(); await b.run();
  assert.equal(a.counts.writes + b.counts.writes, written);
  assert.equal(a.cloud.values().next().value.entries.length, 1);
});

test("a multi-ROM collection matches once regardless of filename order", async () => {
  const a = device("favorites", [game("a", { favorite: true })]); await a.run();
  const b = device("favorites", [game("b", { romFileNames: ["Disc 2.chd", "Disc 1.chd"] })], a.cloud);
  const result = await b.run();
  assert.equal(result.updated, 1); assert.equal(result.localCount, 1);
  assert.equal(b.local[0].favorite, true); assert.equal(b.counts.writes, 0);
});

test("different title, any changed ROM, missing disc and platform never match", async () => {
  const a = device("favorites", [game("a", { favorite: true })]); await a.run();
  for (const extra of [{ title: "SM2" }, { romFileNames: ["Disc 1.chd", "Disc 3.chd"] }, { romFileNames: ["Disc 1.chd"] }, { platformId: "ps2" }, { title: "shenmue II" }]) {
    const b = device("favorites", [game("b", extra)], a.cloud);
    await b.run(); assert.equal(b.local[0].favorite, false); assert.equal(b.counts.writes, 0);
  }
  assert.equal(a.cloud.values().next().value.entries.length, 1);
});

test("unmatched remote records stay available after another device publishes changes", async () => {
  const a = device("favorites", [game("a", { favorite: true })]); await a.run();
  const b = device("favorites", [game("b", { title: "Other", favorite: true })], a.cloud);
  const result = await b.run();
  assert.equal(result.unmatched, 1); assert.equal(a.cloud.values().next().value.entries.length, 2);
});

test("recent sync keeps maxima without inflating counts and treats multiple ROMs as one", async () => {
  const a = device("recent", [game("a", { recent: { lastPlayedAt: 100, playCount: 5, importedPlayTimeSeconds: 20 } })]); await a.run();
  const b = device("recent", [game("b", { recent: { lastPlayedAt: 200, playCount: 3, importedPlayTimeSeconds: 30 } })], a.cloud);
  await b.run(); await a.run();
  const value = { lastPlayedAt: 200, playCount: 5, importedPlayTimeSeconds: 30 };
  assert.deepEqual(a.local[0].recent, value); assert.deepEqual(b.local[0].recent, value);
  const writes = a.counts.writes + b.counts.writes;
  await a.run(); await b.run(); assert.equal(a.counts.writes + b.counts.writes, writes);
  assert.equal(a.cloud.values().next().value.entries.length, 1);
});

test("two plugins and different configured channels keep independent records", async () => {
  const sharedCloud = new Map();
  const favorites = device("favorites", [game("a", { favorite: true })], sharedCloud);
  const recent = device("recent", [game("b", { recent: { lastPlayedAt: 1, playCount: 1, importedPlayTimeSeconds: null } })], sharedCloud);
  await favorites.run(); await recent.run(); assert.equal(sharedCloud.size, 2);
  favorites.data.destination = { ...source, id: "other", provider: "BAIDU", scope: "other-account" };
  favorites.hooks.sources = [favorites.data.destination]; favorites.local[0].favorite = false;
  await favorites.run();
  assert.equal(sharedCloud.size, 2); assert.equal([...sharedCloud.values()].find(value => value.kind === "favorites").entries[0].favorite, true);
});

test("cancellation after a committed batch preserves its baseline and manual edits", async () => {
  const a = device("favorites", Array.from({ length: 250 }, (_, index) => game("a" + index, { title: "Game " + index, favorite: true })));
  await a.run();
  const b = device("favorites", a.local.map(item => ({ ...item, id: "b" + item.id, favorite: false })), a.cloud);
  b.hooks.afterApply = () => { throw new Error("cancelled"); };
  await assert.rejects(b.run(), /cancelled/);
  assert.equal(b.local.filter(item => item.favorite).length, 200);
  b.local[0].favorite = false; delete b.hooks.afterApply;
  await b.run(); await a.run();
  assert.equal(b.local[0].favorite, false); assert.equal(a.local[0].favorite, false);
  assert.equal(b.local.filter(item => item.favorite).length, 249);
  assert.equal(b.counts.batches, 2); assert.equal(b.counts.pages, 4);
});

test("malformed remote data fails without writes or local changes", async () => {
  const b = device("favorites", [game("b")]);
  b.cloud.set("favorites:account-root:dc.json", { schemaVersion: 1, kind: "recent", platformId: "dc", entries: [] });
  await assert.rejects(b.run(), /Invalid remote/); assert.equal(b.counts.writes, 0); assert.equal(b.counts.batches, 0);
});

test("missing configuration and cancelled reads never upload or edit games", async () => {
  const b = device("favorites", [game("b", { favorite: true })]);
  delete b.data.destination;
  await assert.rejects(b.run(), /Select a valid/); assert.equal(b.counts.reads, 0);
  b.data.destination = source; b.hooks.beforeRead = () => { throw new Error("cancelled"); };
  await assert.rejects(b.run(), /cancelled/); assert.equal(b.counts.writes, 0); assert.equal(b.counts.batches, 0);
});

test("launching a game during recent sync preserves the newer local play record", async () => {
  const a = device("recent", [game("a", { recent: { lastPlayedAt: 100, playCount: 1, importedPlayTimeSeconds: null } })]); await a.run();
  const b = device("recent", [game("b")], a.cloud);
  b.hooks.beforeApply = () => { b.local[0].recent = { lastPlayedAt: 200, playCount: 1, importedPlayTimeSeconds: null }; };
  await assert.rejects(b.run());
  assert.equal(b.local[0].recent.lastPlayedAt, 200);
  delete b.hooks.beforeApply; await b.run(); await a.run();
  assert.equal(a.local[0].recent.lastPlayedAt, 200);
});
