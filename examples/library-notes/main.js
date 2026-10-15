retromao.define({
  actions: {
    async favorites() {
      const page = await retromao.favorites.list({ limit: 40 });
      await retromao.tasks.progress(page.games.length, page.games.length);
      return page.games.map(game => ({ id: game.id, title: game.metadata.title }));
    }
  }
});
