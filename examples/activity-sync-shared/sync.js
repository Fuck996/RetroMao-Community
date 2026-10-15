(function (global) {
  "use strict";
  const sameRecent = (a, b) => a.lastPlayedAt === b.lastPlayedAt && a.playCount === b.playCount && a.importedPlayTimeSeconds === b.importedPlayTimeSeconds;
  const maxNullable = (a, b) => a == null ? b : b == null ? a : Math.max(a, b);
  const mergeRecent = (a, b) => ({ lastPlayedAt: maxNullable(a.lastPlayedAt, b.lastPlayedAt), playCount: Math.max(a.playCount, b.playCount),
    importedPlayTimeSeconds: maxNullable(a.importedPlayTimeSeconds, b.importedPlayTimeSeconds) });
  const identity = entry => JSON.stringify([entry.title, [...entry.romFileNames].sort()]);
  const validIdentity = entry => typeof entry.title === "string" && entry.title.length > 0 && Array.isArray(entry.romFileNames) &&
    entry.romFileNames.length > 0 && entry.romFileNames.every(name => typeof name === "string" && name.length > 0);

  function readDocument(value, kind, platformId, t) {
    if (value === null) return new Map();
    if (value.schemaVersion !== 1 || value.kind !== kind || value.platformId !== platformId || !Array.isArray(value.entries)) throw new Error(t("invalidCloud"));
    const entries = new Map();
    for (const entry of value.entries) {
      if (!validIdentity(entry)) throw new Error(t("invalidCloud"));
      if (kind === "favorites") {
        if (typeof entry.favorite !== "boolean") throw new Error(t("invalidCloud"));
      } else {
        const recent = entry.recent;
        if (!recent || !Number.isSafeInteger(recent.lastPlayedAt) || recent.lastPlayedAt < 0 ||
            !Number.isSafeInteger(recent.playCount) || recent.playCount < 0 || recent.playCount > 2147483647 ||
            recent.importedPlayTimeSeconds !== null && (!Number.isSafeInteger(recent.importedPlayTimeSeconds) || recent.importedPlayTimeSeconds < 0)) throw new Error(t("invalidCloud"));
      }
      const key = identity(entry);
      if (entries.has(key)) throw new Error(t("invalidCloud"));
      entries.set(key, entry);
    }
    return entries;
  }

  async function run(kind) {
    const { locale } = await retromao.ready;
    const t = key => global.activitySyncText(locale, kind, key);
    const data = await retromao.data.get();
    const destination = data.destination;
    const sources = await retromao.storage.sources();
    const source = destination && sources.find(item => item.id === destination.id && item.scope === destination.scope);
    if (!source) throw new Error(t("chooseSource"));
    await retromao.tasks.progress(0, null, t("readingLibrary"));
    const platforms = new Map();
    let after = null, skipped = 0;
    do {
      const page = await retromao.library.records({ after, limit: 200 });
      for (const game of page.games) {
        if (!validIdentity(game)) { skipped++; continue; }
        if (!platforms.has(game.platformId)) platforms.set(game.platformId, new Map());
        const groups = platforms.get(game.platformId), key = identity(game);
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push(game);
      }
      after = page.next;
    } while (after);
    const summary = { scope: source.scope, localCount: 0, updated: 0, uploaded: 0, unmatched: 0, skipped, platforms: platforms.size, finishedAt: 0, unmatchedGames: [] };
    let completed = 0;
    for (const [platformId, groups] of platforms) {
      await retromao.tasks.progress(completed, platforms.size, t("syncing") + " · " + platformId);
      const document = await retromao.storage.read(source, platformId + ".json");
      const remote = readDocument(document.value, kind, platformId, t);
      const entries = new Map(remote), changes = [], baselineKey = "baseline:" + source.scope + ":" + platformId;
      const baseline = { ...(data[baselineKey] || {}) }, nextBaseline = { ...baseline };
      let remoteChanged = false;
      for (const [key, games] of groups) {
        const first = games[0], previous = remote.get(key);
        let value;
        if (kind === "favorites") {
          const local = games.some(game => game.favorite), known = games.every(game => typeof baseline[game.id] === "boolean");
          const old = games.some(game => baseline[game.id] === true);
          value = !previous ? local : !known ? local || previous.favorite : local !== old ? local : previous.favorite;
          if (value) summary.localCount++;
          for (const game of games) {
            if (value || previous || baseline[game.id] === true) nextBaseline[game.id] = value;
            if (game.favorite !== value) changes.push({ gameId: game.id, favorite: value });
          }
          if (!previous && !local && old !== true) continue;
        } else {
          const local = games.map(game => game.recent).reduce(mergeRecent);
          value = previous ? mergeRecent(local, previous.recent) : local;
          if (value.lastPlayedAt === null) continue;
          summary.localCount++;
          for (const game of games) if (!sameRecent(game.recent, value)) changes.push({ gameId: game.id, recent: { expected: game.recent, value } });
        }
        const entry = { title: first.title, romFileNames: [...first.romFileNames].sort(), [kind === "favorites" ? "favorite" : "recent"]: value };
        if (!previous || (kind === "favorites" ? previous.favorite !== value : !sameRecent(previous.recent, value))) {
          entries.set(key, entry); remoteChanged = true;
        }
      }
      for (const [key, entry] of remote) if (!groups.has(key)) {
        summary.unmatched++;
        if (summary.unmatchedGames.length < 30) summary.unmatchedGames.push({ platformId, title: entry.title });
      }
      if (remoteChanged) {
        const ordered = [...entries].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0).map(([, entry]) => entry);
        await retromao.storage.write(document.token, { schemaVersion: 1, kind, platformId, entries: ordered });
        summary.uploaded++;
      }
      // 本地状态与同步基线在同一短事务提交，取消后保留已完成批次。
      for (let start = 0; start < changes.length; start += 200) {
        const batch = changes.slice(start, start + 200);
        if (kind === "favorites") for (const edit of batch) baseline[edit.gameId] = edit.favorite;
        await retromao.library.apply(batch, kind === "favorites" ? { [baselineKey]: baseline } : undefined);
        summary.updated += batch.length;
      }
      if (kind === "favorites" && Object.keys(nextBaseline).some(id => nextBaseline[id] !== baseline[id])) {
        await retromao.data.patch({ [baselineKey]: nextBaseline });
      }
      completed++;
      await retromao.tasks.progress(completed, platforms.size, t("syncing") + " · " + platformId);
    }
    summary.finishedAt = Date.now();
    await retromao.data.patch({ lastSync: summary });
    await retromao.tasks.progress(completed, platforms.size, t("complete"));
    return summary;
  }
  global.activitySync = Object.freeze({ run });
})(globalThis);
