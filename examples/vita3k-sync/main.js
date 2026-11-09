"use strict";

const titleIdPattern = /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/;

retromao.define({
  resources: {
    installed({ games }) {
      return games.map(game => {
        const ids = [...new Set(game.romNames.filter(name => /\.psvita$/i.test(name))
          .map(name => name.slice(0, -7)))].sort();
        if (!ids.length || ids.some(id => !titleIdPattern.test(id))) {
          throw new Error("Invalid Vita3K title ID: " + game.gameId);
        }
        return {
          gameId: game.gameId,
          // 65 字符的数字 ID 键与旧版最长 64 字符的原始标题键互不冲突。
          key: /^[0-9]/.test(ids[0]) ? "n" + ids[0].padStart(64, "_") : ids[0],
          paths: ids.flatMap(id => [
            { path: "ux0/app/" + id, required: true },
            { path: "ux0/patch/" + id },
            { path: "ux0/addcont/" + id },
            { path: "ux0/license/" + id }
          ])
        };
      });
    }
  }
});
