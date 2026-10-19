(async () => {
  const { messages } = await retromao.ready;
  const title = document.getElementById("title"), run = document.getElementById("run");
  const status = document.getElementById("status"), error = document.getElementById("error");
  title.textContent = messages.title;
  run.textContent = messages.run;
  let stopWatching = null;
  window.addEventListener("pagehide", () => { if (stopWatching) stopWatching(); });
  try {
    const page = await retromao.library.records({ limit: 200 });
    const list = document.getElementById("games");
    for (const game of page.games) {
      const row = document.createElement("li");
      row.textContent = game.title;
      list.append(row);
    }
    if (!page.games.length) status.textContent = messages.empty;
    run.disabled = false;
    run.onclick = async () => {
      error.textContent = "";
      run.disabled = true;
      try {
        const task = await retromao.tasks.run("count");
        if (stopWatching) stopWatching();
        stopWatching = retromao.tasks.watch(task.id, async current => {
          status.textContent = String(current.completed);
          if (current.state === "FAILED") { error.textContent = current.message; run.disabled = false; }
          if (current.state === "CANCELLED") run.disabled = false;
          if (current.state === "SUCCEEDED") {
            try {
              const result = await retromao.tasks.result(current.id);
              status.textContent = messages.count + ": " + result.total;
            } catch (failure) { error.textContent = failure.message; }
            run.disabled = false;
          }
        });
      } catch (failure) { error.textContent = failure.message; run.disabled = false; }
    };
  } catch (failure) { error.textContent = failure.message; }
})().catch(failure => { document.getElementById("error").textContent = failure.message; });
