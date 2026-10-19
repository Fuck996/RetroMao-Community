"use strict";
let receive;
globalThis.android = { async getNamedPort() {
  return { postMessage: raw => postMessage(raw), set onmessage(callback) { receive = callback; } };
} };
onmessage = event => {
  if (!event.data.start) { receive({ data: event.data }); return; }
  const start = event.data;
  importScripts("/__retromao/retromao.js");
  retromao.ready.then(() => {
    importScripts(start.entry);
    return retromao.__run(start.action, start.arguments);
  }).catch(error => postMessage(JSON.stringify({ type: "failure", error: error.message })));
};
