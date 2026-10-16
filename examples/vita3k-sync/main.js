"use strict";

retromao.define({
  resources: {
    installed({ games }) {
      return games.map(game => {
        const ids = [...new Set(game.romNames.filter(name => /\.psvita$/i.test(name))
          .map(name => name.slice(0, -7)))].sort();
        if (!ids.length || ids.some(id => !/^[A-Za-z][A-Za-z0-9._-]{0,63}$/.test(id))) {
          throw new Error("Invalid Vita3K title ID: " + game.gameId);
        }
        return {
          gameId: game.gameId,
          key: ids[0],
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
