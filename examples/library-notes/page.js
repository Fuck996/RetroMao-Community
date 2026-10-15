"use strict";
const elements = Object.fromEntries(["all", "favorites", "background", "cancel", "error", "result", "games", "next"].map(id => [id, document.getElementById(id)]));
let collection = "ALL", cursor = null, task = null, stopWatching = null;
async function perform(action) {
  elements.error.textContent = "";
  try { await action(); } catch (error) { elements.error.textContent = String(error.message || error); }
}
function render(game, settings) {
  const article = document.createElement("article"), title = document.createElement("h2"), note = document.createElement("input"), save = document.createElement("button"), favorite = document.createElement("button"), row = document.createElement("div");
  const stored = game.metadata.extensions?.["example.library-notes"] || {};
  title.textContent = game.metadata.title;
  note.setAttribute("aria-label", game.metadata.title + "的笔记");
  note.value = typeof stored.note === "string" ? stored.note : settings.suggestedNote;
  save.textContent = "保存笔记"; favorite.textContent = game.favorite ? "取消收藏" : "收藏";
  save.onclick = () => perform(async () => {
    save.disabled = true;
    try {
      const patch = { value: note.value };
      if (Object.prototype.hasOwnProperty.call(stored, "note")) patch.expected = stored.note;
      await retromao.index.patch(game.id, { note: patch });
      stored.note = note.value; elements.result.textContent = "笔记已保存";
    } finally { save.disabled = false; }
  });
  favorite.onclick = () => perform(async () => {
    favorite.disabled = true;
    try {
      const [updated] = await retromao.favorites.set(game.id, !game.favorite);
      game.favorite = updated.favorite; favorite.textContent = game.favorite ? "取消收藏" : "收藏";
    } finally { favorite.disabled = false; }
  });
  row.className = "row"; row.append(save, favorite); article.append(title, note, row); return article;
}
async function load(next = false) {
  elements.next.disabled = true;
  try {
    const [page, settings] = await Promise.all([retromao.library.games({ collection, after: next ? cursor : null, limit: 20 }), retromao.settings.get()]);
    if (!next) elements.games.replaceChildren();
    for (const game of page.games) elements.games.append(render(game, settings));
    cursor = page.next; elements.next.hidden = !cursor;
    if (!next && !page.games.length) elements.result.textContent = "暂无游戏";
  } finally { elements.next.disabled = false; }
}
elements.all.onclick = () => perform(async () => { collection = "ALL"; await load(); });
elements.favorites.onclick = () => perform(async () => { collection = "FAVORITES"; await load(); });
elements.next.onclick = () => perform(() => load(true));
elements.cancel.onclick = () => perform(() => retromao.tasks.cancel(task.id));
elements.background.onclick = () => perform(async () => {
  elements.background.disabled = true;
  try {
    task = await retromao.tasks.run("favorites");
    if (stopWatching) stopWatching();
    stopWatching = retromao.tasks.watch(task.id, update => {
      elements.result.textContent = update.state + (update.message ? " · " + update.message : "");
      elements.cancel.hidden = !["WAITING", "RUNNING", "CANCELLING"].includes(update.state);
      if (update.state === "SUCCEEDED") perform(async () => { elements.result.textContent = (await retromao.tasks.result(task.id)).map(game => game.title).join("\n") || "暂无收藏"; });
    });
  } finally { elements.background.disabled = false; }
});
perform(async () => { await retromao.ready; await load(); });
