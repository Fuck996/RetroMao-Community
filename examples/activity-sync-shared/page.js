(async function () {
  "use strict";
  const $ = id => document.getElementById(id), { locale } = await retromao.ready;
  const t = key => activitySyncText(locale, activitySyncKind, key);
  document.title = t("title");
  for (const id of ["title", "author", "help", "privacy", "sync", "cancel", "retained"]) $(id).textContent = t(id);
  for (const key of ["source", "local", "updated", "uploaded"]) $(key === "source" ? "sourceLabel" : key + "Label").textContent = t(key);
  $("status").textContent = t("ready");
  let current = null, destination = null, unwatch = null, busy = false;
  const active = task => task && ["WAITING", "RUNNING", "CANCELLING"].includes(task.state);
  function controls() {
    const running = active(current);
    $("sync").disabled = running || busy || !destination;
    $("cancel").hidden = !running;
    $("cancel").disabled = current && current.state === "CANCELLING";
  }
  function summary(result) {
    if (!destination || !result || result.scope !== destination.scope) result = null;
    $("last").textContent = result ? t("last") + " · " + new Date(result.finishedAt).toLocaleString(locale) : t("empty");
    for (const key of ["localCount", "updated", "uploaded"]) $(key).textContent = result ? String(result[key]) : "—";
    $("unmatched").hidden = !result || !result.unmatched;
    $("unmatchedLabel").textContent = t("unmatched") + " · " + (result ? result.unmatched : 0);
    $("games").replaceChildren();
    for (const game of result && result.unmatchedGames || []) { const item = document.createElement("li"); item.textContent = game.platformId + " · " + game.title; $("games").appendChild(item); }
    $("skipped").textContent = result && result.skipped ? t("skipped") + " · " + result.skipped : "";
  }
  async function taskChanged(task) {
    current = task; controls();
    $("status").textContent = t(task.state) + (task.message ? " · " + task.message : "");
    $("progress").hidden = !active(task);
    if (task.total > 0) { $("progress").max = task.total; $("progress").value = task.completed; } else $("progress").removeAttribute("value");
    if (task.state === "FAILED") $("error").textContent = task.message;
    if (task.state === "SUCCEEDED") {
      try { summary(await retromao.tasks.result(task.id)); } catch (error) { $("error").textContent = error.message; }
    }
  }
  $("sync").addEventListener("click", async () => {
    busy = true; controls(); $("error").textContent = "";
    try {
      current = await retromao.tasks.run("sync");
      if (unwatch) unwatch();
      await taskChanged(current);
      unwatch = retromao.tasks.watch(current.id, taskChanged);
    } catch (error) { $("error").textContent = error.message; }
    finally { busy = false; controls(); }
  });
  $("cancel").addEventListener("click", async () => {
    try { await retromao.tasks.cancel(current.id); } catch (error) { $("error").textContent = error.message; }
  });
  try {
    const [connections, data, task] = await Promise.all([retromao.storage.sources(), retromao.data.get(), retromao.tasks.current()]);
    destination = data.destination && connections.find(source => source.id === data.destination.id && source.scope === data.destination.scope);
    $("source").textContent = destination ? destination.name + " · " + destination.provider : t("select");
    $("connectionHint").textContent = !connections.length ? t("noSources") : data.destination && !destination ? t("unavailable") : !destination ? t("chooseSource") : "";
    summary(destination && data.lastSync && data.lastSync.scope === destination.scope ? data.lastSync : null);
    if (task) { await taskChanged(task); unwatch = retromao.tasks.watch(task.id, taskChanged); }
    controls();
    document.querySelector(!$("sync").disabled ? "#sync" : "#title").focus();
  } catch (error) { $("error").textContent = error.message; }
  window.addEventListener("pagehide", () => { if (unwatch) unwatch(); }, { once: true });
})();
