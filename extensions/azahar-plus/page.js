(async function () {
  "use strict";
  const $ = id => document.getElementById(id);
  let active = true;
  window.addEventListener("pagehide", () => { active = false; });
  const environment = await retromao.ready;
  if (!active) return;
  const text = key => environment.messages[key];
  document.documentElement.lang = environment.locale;
  document.title = text("title");
  document.querySelectorAll("[data-text]").forEach(element => { element.textContent = text(element.dataset.text); });
  function sizeViewport() {
    document.documentElement.style.setProperty("--page-height", visualViewport.height + "px");
  }
  sizeViewport();
  visualViewport.addEventListener("resize", sizeViewport);
  window.addEventListener("pagehide", () => visualViewport.removeEventListener("resize", sizeViewport));
  $("entries").setAttribute("aria-label", text("title"));
  let catalog, expected = null, deleting = null, busy = false;
  const clone = entry => JSON.parse(JSON.stringify(entry));
  function button(label, action, disabled = false) {
    const element = document.createElement("button");
    element.textContent = text(label); element.disabled = disabled;
    element.addEventListener("click", action); return element;
  }
  function render(next) {
    catalog = next; $("entries").replaceChildren();
    $("platform").replaceChildren(...catalog.platforms.map(platform => {
      const option = document.createElement("option"); option.value = platform.id; option.textContent = platform.name; return option;
    }));
    for (const status of catalog.entries) {
      const entry = status.entry, card = document.createElement("article"); card.className = "entry";
      const top = document.createElement("div"); top.className = "entry-top";
      const title = document.createElement("h2"); title.textContent = entry.name;
      const badge = document.createElement("span"); badge.className = "badge";
      badge.textContent = text(status.selectedPlatforms.length ? "selected" : status.installed ? "installed" : "missing");
      top.append(title, badge);
      const platform = document.createElement("p"); platform.textContent = entry.platforms.map(id => catalog.platforms.find(item => item.id === id)?.name || id).join(" · ");
      const component = document.createElement("p"); component.className = "component"; component.textContent = entry.packageName + "\n" + entry.activity;
      const actions = document.createElement("div"); actions.className = "entry-actions";
      actions.append(button("edit", () => edit(entry)), button("use", () => select(entry), !status.installed || status.selectedPlatforms.length > 0), button("delete", () => confirmDelete(entry)));
      card.append(top, platform, component, actions); $("entries").append(card);
    }
    $("empty").hidden = catalog.entries.length !== 0;
    $("add").disabled = catalog.entries.length >= 16;
  }
  function fill(entry) {
    $("platform").value = entry.platforms[0]; $("name").value = entry.name;
    $("package").value = entry.packageName; $("activity").value = entry.activity;
    $("action").value = entry.action ?? "android.intent.action.VIEW";
    $("mime").value = entry.mimeType ?? ""; $("rom-data").checked = entry.romData ?? true;
    $("extras").value = JSON.stringify(entry.extras ?? {}, null, 2);
    document.querySelectorAll(".flags input").forEach(input => { input.checked = (entry.flags ?? []).includes(input.value); });
  }
  function edit(entry = null) {
    if (busy) return;
    expected = entry ? clone(entry) : null;
    fill(entry ?? catalog.defaults[0]); $("form-error").textContent = "";
    document.querySelector(".advanced").open = !!entry && (Object.keys(entry.extras ?? {}).length > 0 || (entry.flags ?? []).length > 0);
    $("editor-title").textContent = text(entry ? "edit" : "add");
    sizeViewport(); $("editor").showModal(); $("platform").focus();
  }
  function lock(value) {
    busy = value;
    for (const control of document.querySelectorAll("button,input,select,textarea,summary")) {
      if (value) control.dataset.wasDisabled = String(control.disabled ?? false);
      if ("disabled" in control) control.disabled = value || control.dataset.wasDisabled === "true";
    }
  }
  async function select(entry) {
    if (busy) return;
    lock(true); $("error").hidden = true;
    try { const next = await retromao.emulators.select(entry.id, entry.platforms[0]); if (!active) return; lock(false); render(next); $("notice").textContent = text("selectedNotice"); }
    catch (error) { if (!active) return; lock(false); $("error").textContent = error.message; $("error").hidden = false; }
  }
  function confirmDelete(entry) {
    if (busy) return;
    deleting = clone(entry); $("delete-detail").textContent = entry.name; $("delete-error").textContent = "";
    $("confirmation").showModal(); document.querySelector("#confirmation button[value=cancel]").focus();
  }
  $("add").addEventListener("click", () => edit());
  $("preset").addEventListener("click", () => { fill(catalog.defaults[0]); $("form-error").textContent = ""; });
  $("cancel").addEventListener("click", () => $("editor").close());
  $("form").addEventListener("submit", async event => {
    event.preventDefault(); if (busy) return;
    let entry;
    try {
      const extras = JSON.parse($("extras").value);
      if (extras === null || Array.isArray(extras) || typeof extras !== "object") throw new Error(text("objectRequired"));
      const flags = [...document.querySelectorAll(".flags input:checked")].map(input => input.value);
      if (flags.includes("CLEAR_TASK") && !flags.includes("NEW_TASK")) throw new Error(text("taskRequired"));
      entry = { id: expected?.id ?? "entry-" + crypto.randomUUID().replaceAll("-", ""), name: $("name").value.trim(),
        platforms: [$("platform").value], packageName: $("package").value.trim(), activity: $("activity").value.trim(),
        action: $("action").value.trim(), mimeType: $("mime").value.trim() || null, romData: $("rom-data").checked, extras, flags };
    } catch (error) { $("form-error").textContent = error.message; return; }
    lock(true); $("save").textContent = text("saving"); $("form-error").textContent = "";
    try {
      const next = await retromao.emulators.save(entry, expected); if (!active) return; lock(false); render(next); $("editor").close(); $("notice").textContent = text("saved"); $("add").focus();
    } catch (error) { if (!active) return; lock(false); $("form-error").textContent = error.message; }
    finally { if (active) $("save").textContent = text("save"); }
  });
  $("delete-confirm").addEventListener("click", async () => {
    if (busy) return; lock(true);
    try { const next = await retromao.emulators.remove(deleting.id, deleting); if (!active) return; lock(false); render(next); $("confirmation").close(); $("notice").textContent = text("deleted"); $("add").focus(); }
    catch (error) { if (!active) return; lock(false); $("delete-error").textContent = error.message; }
  });
  for (const dialog of document.querySelectorAll("dialog")) dialog.addEventListener("cancel", event => { if (busy) event.preventDefault(); });
  async function load() {
    $("notice").textContent = text("loading");
    try { const next = await retromao.emulators.list(); if (!active) return; render(next); $("notice").textContent = ""; $("error").hidden = true; }
    catch (error) { if (!active) return; $("error").textContent = error.message; $("error").hidden = false; $("notice").textContent = ""; }
  }
  document.addEventListener("visibilitychange", () => { if (!document.hidden && !busy && !document.querySelector("dialog[open]")) load(); });
  await load(); if (active) $("add").focus();
})();
