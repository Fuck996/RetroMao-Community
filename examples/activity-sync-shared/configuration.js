(async function () {
  "use strict";
  const $ = id => document.getElementById(id), { locale } = await retromao.ready;
  const t = key => activitySyncText(locale, activitySyncKind, key);
  document.title = t("title");
  $("sourceLabel").textContent = t("source"); $("author").textContent = t("author");
  let sources = [], destination = null;
  $("source").addEventListener("change", async () => {
    $("source").disabled = true; $("error").textContent = ""; $("connectionHint").textContent = t("saving");
    try {
      const selected = sources.find(source => source.id === $("source").value);
      await retromao.data.patch({ destination: selected || null });
      destination = selected; $("connectionHint").textContent = "";
    } catch (error) {
      $("error").textContent = error.message; $("source").value = destination ? destination.id : "";
      $("connectionHint").textContent = "";
    } finally { $("source").disabled = !sources.length; }
  });
  try {
    const [connections, data] = await Promise.all([retromao.storage.sources(), retromao.data.get()]);
    sources = connections;
    const empty = document.createElement("option"); empty.value = ""; empty.textContent = t("select"); $("source").appendChild(empty);
    for (const source of sources) { const option = document.createElement("option"); option.value = source.id; option.textContent = source.name + " · " + source.provider; $("source").appendChild(option); }
    destination = data.destination && sources.find(source => source.id === data.destination.id && source.scope === data.destination.scope);
    $("source").value = destination ? destination.id : "";
    $("connectionHint").textContent = !sources.length ? t("noSources") : data.destination && !destination ? t("unavailable") : "";
    $("source").disabled = !sources.length;
  } catch (error) { $("error").textContent = error.message; }
})();
