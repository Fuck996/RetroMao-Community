retromao.define({ actions: {
  async count() {
    let after = null, total = 0;
    do {
      const page = await retromao.library.records({ after, limit: 200 });
      total += page.games.length;
      after = page.next;
      await retromao.tasks.progress(total);
    } while (after);
    return { total };
  }
} });
