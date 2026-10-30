(function (global) {
  "use strict";
  function connect(send, listen) {
    let sequence = 0, active = 0, definition = null, lastTask = null, closed = false;
    let iconNames = null;
    const pending = new Map(), waiting = [], watchers = new Set();
    function pump() {
      while (active < 4 && waiting.length) {
        const request = waiting.shift();
        active++;
        send(JSON.stringify(request));
      }
    }
    function call(method, params = {}) {
      if (closed) return Promise.reject(new Error("Plugin session closed"));
      return new Promise((resolve, reject) => {
        const id = String(++sequence);
        pending.set(id, { resolve, reject });
        waiting.push({ id, method, params });
        pump();
      });
    }
    function rejectAll(message) {
      closed = true;
      const error = new Error(message);
      for (const request of pending.values()) request.reject(error);
      pending.clear(); waiting.length = 0; active = 0;
    }
    listen(raw => {
      const message = typeof raw === "string" ? JSON.parse(raw) : raw;
      if (message.type === "fatal") { rejectAll(message.error); return; }
      if (message.type === "task") {
        lastTask = message.task;
        for (const watcher of watchers) if (watcher.id === lastTask.id) watcher.callback(lastTask);
        return;
      }
      const request = pending.get(message.id);
      if (!request) return;
      pending.delete(message.id); active--;
      if (message.error != null) request.reject(new Error(message.error)); else request.resolve(message.result);
      pump();
    });
    const api = {
      version: 1,
      icons: Object.freeze({
        list: async () => { await api.ready; if (!iconNames) throw new Error("Public icons require RetroMao 0.9.92 or later"); return iconNames; },
        url: name => {
          if (!iconNames) throw new Error("Await retromao.ready on RetroMao 0.9.92 or later before using public icons");
          if (!iconNames.includes(name)) throw new Error("Unknown public icon: " + name);
          return "/__retromao/icons/" + name + ".svg";
        }
      }),
      library: Object.freeze({
        game: id => call("library.game", { id }),
        games: (query = {}) => call("library.games", { limit: 40, ...query }),
        records: (query = {}) => call("library.records", { limit: 200, ...query }),
        apply: (changes, checkpoint) => call("library.edit", { changes, returnGames: false, ...(checkpoint == null ? {} : { checkpoint }) }),
        edit: (changes, checkpoint) => call("library.edit", { changes, ...(checkpoint == null ? {} : { checkpoint }) })
      }),
      favorites: Object.freeze({
        list: (query = {}) => call("library.games", { limit: 40, ...query, collection: "FAVORITES" }),
        set: (gameId, favorite) => call("library.edit", { changes: [{ gameId, favorite }] })
      }),
      recent: Object.freeze({
        list: (query = {}) => call("library.games", { limit: 40, ...query, collection: "RECENT" }),
        edit: (gameId, expected, value) => call("library.edit", { changes: [{ gameId, recent: { expected, value } }] })
      }),
      media: Object.freeze({
        folders: platformId => call("media.folders", platformId == null ? {} : { platformId }),
        assets: (folderId, afterPath = null, limit = 100) => call("media.assets", { folderId, afterPath, limit }),
        edit: (gameId, media) => call("library.edit", { changes: [{ gameId, media }] })
      }),
      index: Object.freeze({
        patch: (gameId, extensions) => call("library.edit", { changes: [{ gameId, extensions }] })
      }),
      settings: Object.freeze({ get: () => call("settings.get") }),
      data: Object.freeze({ get: () => call("data.get"), patch: values => call("data.patch", values) }),
      emulators: Object.freeze({
        list: () => call("emulators.list"),
        save: (entry, expected = null) => call("emulators.save", { entry, expected }),
        remove: (id, expected) => call("emulators.remove", { id, expected }),
        select: (id, platformId) => call("emulators.select", { id, platformId })
      }),
      storage: Object.freeze({
        sources: () => call("storage.sources"),
        read: (source, key) => call("storage.read", { sourceId: source.id, scope: source.scope, key }),
        write: (token, value) => call("storage.write", { token, value })
      }),
      http: Object.freeze({ request: options => call("http.request", options) }),
      tasks: Object.freeze({
        run: (action, arguments_ = {}) => call("tasks.run", { action, arguments: arguments_ }),
        get: id => call("tasks.get", { id }),
        current: () => call("tasks.current"),
        result: id => call("tasks.result", { id }),
        cancel: id => call("tasks.cancel", { id }),
        progress: (completed, total = null, message = "") => call("tasks.progress", { completed, total, message }),
        watch: (id, callback) => {
          const watcher = { id, callback }; watchers.add(watcher);
          if (lastTask && lastTask.id === id) callback(lastTask);
          return () => watchers.delete(watcher);
        }
      }),
      define: value => {
        if (definition) throw new Error("Plugin entry has already been registered");
        definition = value;
      },
      __dispose: () => { watchers.clear(); rejectAll("Plugin page closed"); },
      __run: async (action, arguments_) => {
        try {
          const execute = action.startsWith("resource:")
            ? definition && definition.resources && definition.resources[action.slice(9)]
            : definition && definition.actions && definition.actions[action];
          if (typeof execute !== "function") throw new Error("Action is not registered: " + action);
          const result = await execute(arguments_);
          send(JSON.stringify({ type: "complete", result: result === undefined ? null : result }));
        } catch (error) {
          send(JSON.stringify({ type: "failure", error: String(error && error.stack || error) }));
        }
      }
    };
    api.ready = call("session.ready").then(environment => {
      if (environment.icons) iconNames = Object.freeze([...environment.icons]);
      return environment;
    });
    Object.defineProperty(global, "retromao", { value: Object.freeze(api), configurable: false, writable: false });
    return api;
  }
  if (typeof android !== "undefined" && typeof android.getNamedPort === "function") {
    (async () => {
      const port = await android.getNamedPort("retromao");
      connect(message => port.postMessage(message), receive => { port.onmessage = event => receive(event.data); });
      port.postMessage(JSON.stringify({ type: "ready" }));
    })();
  } else {
    const native = global.retromaoNative;
    if (!native) throw new Error("RetroMao host bridge is unavailable");
    const api = connect(message => native.postMessage(message), receive => { native.onmessage = event => receive(event.data); });
    api.ready.then(environment => {
      function prepare() {
        const style = document.createElement("link");
        style.rel = "stylesheet"; style.href = "/__retromao/retromao.css"; document.head.appendChild(style);
        for (const [key, value] of Object.entries(environment.colors || {})) document.documentElement.style.setProperty("--retromao-" + key, value);
        document.documentElement.lang = environment.locale || "zh-CN";
      }
      if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", prepare, { once: true }); else prepare();
    });
    document.addEventListener("keydown", event => {
      const directions = { ArrowUp: [0, -1], ArrowDown: [0, 1], ArrowLeft: [-1, 0], ArrowRight: [1, 0] };
      const direction = directions[event.key];
      if (!direction || event.altKey || event.ctrlKey || event.metaKey) return;
      if ((event.key === "ArrowLeft" || event.key === "ArrowRight") && /^(INPUT|TEXTAREA)$/.test(event.target.tagName)) return;
      const scope = document.querySelector("dialog[open]") || document;
      const elements = Array.from(scope.querySelectorAll("button,a[href],input,select,textarea,summary,[tabindex]"))
        .filter(element => !element.disabled && element.tabIndex >= 0 && element.getClientRects().length);
      const current = document.activeElement;
      if (!elements.includes(current)) { if (elements[0]) { elements[0].focus(); event.preventDefault(); } return; }
      const origin = current.getBoundingClientRect(), x = origin.x + origin.width / 2, y = origin.y + origin.height / 2;
      let best = null, score = Infinity;
      for (const element of elements) {
        if (element === current) continue;
        const rect = element.getBoundingClientRect(), dx = rect.x + rect.width / 2 - x, dy = rect.y + rect.height / 2 - y;
        const forward = dx * direction[0] + dy * direction[1];
        const distance = Math.abs(dx * direction[1] - dy * direction[0]) * 2 + forward;
        if (forward > 0 && distance < score) { best = element; score = distance; }
      }
      if (best) { best.focus(); best.scrollIntoView({ block: "nearest" }); event.preventDefault(); }
    });
    global.addEventListener("pagehide", () => api.__dispose());
  }
})(globalThis);
