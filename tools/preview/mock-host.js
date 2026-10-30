(function (global) {
  "use strict";
  const clone = value => JSON.parse(JSON.stringify(value));
  const loading = fetch("/__preview/data.json").then(response => {
    if (!response.ok) throw new Error("Preview fixture could not be loaded");
    return response.json();
  });
  let api, worker = null, task = null, result = null, privateData = {}, sequence = 0;
  let activeToken = null;
  let emulatorEntries = null;
  const emulatorDefaults = new Map();
  const tokens = new Map();
  const params = new URLSearchParams(location.search);
  const configuring = params.get("config") === "1";
  function emitTask() { api.onmessage({ data: JSON.stringify({ type: "task", task: clone(task) }) }); }
  function requireCapability(manifest, capability) {
    if (!(manifest.capabilities || []).includes(capability)) throw new Error("Capability required: " + capability);
  }
  function requireTask(id) { if (!task || task.id !== id) throw new Error("Unknown task: " + id); }
  async function dispatch(request, background = false) {
    const data = await loading, manifest = data.manifest, fixtures = data.fixtures;
    const input = request.params || {}, method = request.method;
    if (method.startsWith("emulators.")) {
      requireCapability(manifest, "EMULATORS");
      if (configuring || background || !manifest.editableEmulators) throw new Error("Editable emulator business page required");
      emulatorEntries ??= clone(manifest.emulators || []);
      const platforms = fixtures.platforms || [{ id: "3ds", name: "Nintendo 3DS" }, { id: "nds", name: "Nintendo DS" }, { id: "psp", name: "PlayStation Portable" }];
      if (method === "emulators.save") {
        const previous = emulatorEntries.find(entry => entry.id === input.entry.id) ?? null;
        if (JSON.stringify(previous) !== JSON.stringify(input.expected ?? null)) throw new Error("Entry changed");
        if (input.entry.platforms.length !== 1 || !platforms.some(platform => platform.id === input.entry.platforms[0])) throw new Error("Choose one platform");
        if (!previous && emulatorEntries.length >= 16) throw new Error("At most 16 entries");
        emulatorEntries = previous ? emulatorEntries.map(entry => entry.id === input.entry.id ? clone(input.entry) : entry) : [...emulatorEntries, clone(input.entry)];
      } else if (method === "emulators.remove") {
        if (JSON.stringify(emulatorEntries.find(entry => entry.id === input.id)) !== JSON.stringify(input.expected)) throw new Error("Entry changed");
        emulatorEntries = emulatorEntries.filter(entry => entry.id !== input.id);
      } else if (method === "emulators.select") {
        const entry = emulatorEntries.find(entry => entry.id === input.id);
        if (!entry || !entry.platforms.includes(input.platformId)) throw new Error("Entry does not support platform");
        emulatorDefaults.set(input.platformId, entry.id);
      } else if (method !== "emulators.list") throw new Error("Unknown emulator method");
      if (configuring) throw new Error("Not available on configuration pages");
      return clone({ platforms, defaults: manifest.emulators || [], entries: emulatorEntries.map(entry => ({ entry, installed: true, selectedPlatforms: entry.platforms.filter(id => emulatorDefaults.get(id) === entry.id) })) });
    }
    if (configuring && !background && !["session.ready", "settings.get", "data.get", "data.patch", "storage.sources"].includes(method)) throw new Error("Not available on configuration pages: " + method);
    if (method.startsWith("library.") || method.startsWith("media.")) requireCapability(manifest, method === "library.edit" ? "LIBRARY_WRITE" : "LIBRARY_READ");
    switch (method) {
      case "session.ready": {
        const requested = params.get("locale") || "zh-Hans";
        const locale = requested === manifest.defaultLocale || manifest.localizations?.[requested] ? requested : manifest.defaultLocale;
        const text = locale === manifest.defaultLocale ? manifest : manifest.localizations[locale];
        return { locale, appLocale: requested, defaultLocale: manifest.defaultLocale,
          locales: [manifest.defaultLocale, ...Object.keys(manifest.localizations || {})], messages: text.messages || {}, configuring,
          icons: ["plugin", "star", "history", "sync", "cloud", "library", "image", "language", "palette", "gamepad", "chart", "settings"],
          colors: { background: "#171b24", surface: "#222a36", text: "#edf2f7", primary: "#9cd8cf", muted: "#bac6d4", outline: "#465364" } };
      }
      case "library.game": return fullGame(fixtures.games.find(game => game.id === input.id), manifest);
      case "library.games": case "library.records": {
        if (!Number.isInteger(input.limit) || input.limit < 1 || input.limit > 200) throw new Error("Page size must be 1–200");
        let games = fixtures.games.filter(game => (!input.platformId || game.platformId === input.platformId) &&
          (input.collection !== "FAVORITES" || game.favorite) && (input.collection !== "RECENT" || game.recent.lastPlayedAt != null));
        games.sort(input.collection === "RECENT" ? (a, b) => b.recent.lastPlayedAt - a.recent.lastPlayedAt || a.id.localeCompare(b.id) : (a, b) => a.id.localeCompare(b.id));
        if (input.after) {
          const offset = games.findIndex(game => game.id === input.after.gameId);
          if (offset < 0) throw new Error("Unknown pagination cursor");
          games = games.slice(offset + 1);
        }
        const page = games.slice(0, input.limit);
        return { games: clone(method === "library.records" ? page : page.map(game => fullGame(game, manifest))), next: games.length > page.length ? { gameId: page.at(-1).id, ...(input.collection === "RECENT" ? { lastPlayedAt: page.at(-1).recent.lastPlayedAt } : {}) } : null };
      }
      case "library.edit": {
        if (!Array.isArray(input.changes) || !input.changes.length || input.changes.length > 200) throw new Error("Edit batch must contain 1–200 games");
        const planned = clone(fixtures.games);
        for (const edit of input.changes) {
          const game = planned.find(game => game.id === edit.gameId);
          if (!game) throw new Error("Unknown game: " + edit.gameId);
          if (edit.metadata || edit.media) throw new Error("Metadata/media writes are not implemented by this preview; validate them on the host");
          if (edit.recent) {
            if (JSON.stringify(game.recent) !== JSON.stringify(edit.recent.expected)) throw new Error("Recent record conflict");
            game.recent = clone(edit.recent.value);
          }
          if (edit.favorite != null) game.favorite = edit.favorite;
          if (edit.extensions) {
            game.extensions ||= {};
            for (const [key, change] of Object.entries(edit.extensions)) {
              if (JSON.stringify(game.extensions[key]) !== JSON.stringify(change.expected)) throw new Error("Extension field conflict: " + key);
              if (Object.hasOwn(change, "value")) game.extensions[key] = clone(change.value); else delete game.extensions[key];
            }
          }
        }
        fixtures.games = planned;
        if (input.checkpoint) patch(input.checkpoint);
        return input.returnGames === false ? null : input.changes.map(edit => fullGame(fixtures.games.find(game => game.id === edit.gameId), manifest));
      }
      case "media.folders": return clone(fixtures.folders || []);
      case "media.assets": return clone((fixtures.assets || []).filter(asset => asset.folderId === input.folderId && (!input.afterPath || asset.path > input.afterPath)).slice(0, input.limit));
      case "settings.get": return Object.fromEntries((manifest.settings || []).map(setting => [setting.id, setting.default ?? (setting.kind === "BOOLEAN" ? "false" : "")]));
      case "data.get": return clone(privateData);
      case "data.patch": patch(input); return clone(privateData);
      case "storage.sources": requireCapability(manifest, "STORAGE"); return clone(fixtures.sources);
      case "storage.read": {
        requireCapability(manifest, "STORAGE");
        if (!background) throw new Error("Remote documents are available only in background actions");
        if (!fixtures.sources.some(source => source.id === input.sourceId && source.scope === input.scope)) throw new Error("Storage source identity differs");
        if (!/^[a-zA-Z0-9][a-zA-Z0-9._-]{0,119}\.json$/.test(input.key)) throw new Error("Invalid document name");
        const key = input.scope + "/" + input.key, value = fixtures.documents[key] ?? null, token = String(++sequence);
        tokens.clear(); activeToken = token; tokens.set(token, { key, value: clone(value) });
        return { token, value: clone(value) };
      }
      case "storage.write": {
        requireCapability(manifest, "STORAGE");
        if (!background || input.token !== activeToken || !tokens.has(input.token)) throw new Error("Invalid storage write token");
        const baseline = tokens.get(input.token);
        if (JSON.stringify(fixtures.documents[baseline.key] ?? null) !== JSON.stringify(baseline.value)) throw new Error("Storage document conflict");
        if (!input.value || Array.isArray(input.value) || typeof input.value !== "object" || new TextEncoder().encode(JSON.stringify(input.value)).length > 384 * 1024) throw new Error("Invalid or oversized storage document");
        fixtures.documents[baseline.key] = clone(input.value); tokens.clear(); activeToken = null;
        return null;
      }
      case "http.request": {
        requireCapability(manifest, "NETWORK");
        const url = new URL(input.url);
        if (!(manifest.networkHosts || []).some(host => host === "*" || host === url.host)) throw new Error("Network host not declared: " + url.host);
        if (!Object.hasOwn(fixtures.http, input.url)) throw new Error("No HTTP fixture for " + input.url + "; preview never sends external requests");
        return clone(fixtures.http[input.url]);
      }
      case "tasks.current": return clone(task);
      case "tasks.get": requireTask(input.id); return clone(task);
      case "tasks.result": requireTask(input.id); if (task.state !== "SUCCEEDED") throw new Error("Task has not succeeded"); return clone(result);
      case "tasks.run": {
        if (background) throw new Error("Run tasks from a business page");
        if (task && ["WAITING", "RUNNING", "CANCELLING"].includes(task.state)) throw new Error("One task at a time");
        if (!(manifest.actions || []).some(action => action.id === input.action)) throw new Error("Action not declared");
        task = { id: String(++sequence), pluginId: manifest.id, version: manifest.version, actionId: input.action,
          state: "RUNNING", message: "", completed: 0, total: null, createdAt: Date.now(), updatedAt: Date.now() };
        tokens.clear(); activeToken = null; result = null;
        worker = new Worker("/__preview/worker.js");
        worker.onmessage = async event => {
          const message = JSON.parse(event.data);
          if (message.type === "ready") return;
          if (message.type === "complete" || message.type === "failure") {
            result = message.result ?? null;
            task.state = message.type === "complete" ? "SUCCEEDED" : "FAILED";
            task.message = message.error || "";
            task.updatedAt = Date.now(); emitTask(); worker.terminate(); worker = null; tokens.clear(); activeToken = null;
          } else {
            const active = worker;
            try { const response = await dispatch(message, true); active?.postMessage(JSON.stringify({ id: message.id, result: response })); }
            catch (error) { active?.postMessage(JSON.stringify({ id: message.id, error: error.message })); }
          }
        };
        worker.onerror = event => { task.state = "FAILED"; task.message = event.message; emitTask(); worker.terminate(); worker = null; tokens.clear(); activeToken = null; };
        worker.postMessage({ start: true, entry: "/plugin/" + manifest.entryPoint, action: input.action, arguments: input.arguments || {} });
        return clone(task);
      }
      case "tasks.cancel": requireTask(input.id); worker?.terminate(); worker = null; task.state = "CANCELLED"; task.updatedAt = Date.now(); emitTask(); tokens.clear(); activeToken = null; return null;
      case "tasks.progress": if (!background || !task) throw new Error("No active action"); task.completed = input.completed; task.total = input.total; task.message = input.message; task.updatedAt = Date.now(); emitTask(); return null;
      default: throw new Error("Unsupported preview method: " + method);
    }
  }
  function fullGame(game, manifest) {
    if (!game) return null;
    return { id: game.id, platformId: game.platformId, metadata: { title: game.title, description: "", developer: "", publisher: "", genre: "", releaseDate: "", players: "", rating: null, sortTitle: "", extensions: { [manifest.id]: game.extensions || {} } },
      favorite: game.favorite, recent: clone(game.recent), media: [], hidden: false, localEntryRemoved: false, userEditedFields: [], userEditedMediaRoles: [] };
  }
  function patch(values) { for (const [key, value] of Object.entries(values)) if (value === null) delete privateData[key]; else privateData[key] = clone(value); }
  api = global.retromaoNative = { postMessage(raw) {
    const request = JSON.parse(raw);
    dispatch(request).then(result => api.onmessage({ data: JSON.stringify({ id: request.id, result }) }), error => api.onmessage({ data: JSON.stringify({ id: request.id, error: error.message }) }));
  } };
  global.addEventListener("pagehide", () => { worker?.terminate(); worker = null; });
})(globalThis);
