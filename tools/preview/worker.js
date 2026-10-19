"use strict";
let receive;
let launch;
globalThis.android = { async getNamedPort() {
  return { postMessage(raw) {
    if (JSON.parse(raw).type === "ready") {
      retromao.ready.then(() => {
        importScripts(launch.entry);
        return retromao.__run(launch.action, launch.arguments);
      }).catch(error => postMessage(JSON.stringify({ type: "failure", error: error.message })));
    } else postMessage(raw);
  }, set onmessage(callback) { receive = callback; } };
} };
onmessage = event => {
  if (!event.data.start) { receive({ data: event.data }); return; }
  launch = event.data;
  importScripts("/__retromao/retromao.js");
};
