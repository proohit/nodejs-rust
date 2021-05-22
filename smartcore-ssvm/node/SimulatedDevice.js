"use strict";
const { readFileSync, mkdirSync, existsSync, rmSync } = require("fs");

const config = JSON.parse(readFileSync("config.json"));
const connectionString = config.deviceConnection;

var Mqtt = require("azure-iot-device-mqtt").Mqtt;
var DeviceClient = require("azure-iot-device").Client;

var client = DeviceClient.fromConnectionString(connectionString, Mqtt);
const fetch = require("node-fetch");

function resetLib() {
  if (existsSync("./lib/js")) {
    console.log("deleting lib dir");
    rmSync("./lib/js", { recursive: true, force: true });
  }
  console.log("creating lib dir");
  mkdirSync("./lib/js", { recursive: true });
  delete require.cache[require.resolve("./lib/js/ssvm_nodejs_starter_lib.js")];
  load_model = undefined;
}

client.on("message", function (msg) {
  console.log(
    `Received MessageId: ${msg.messageId} on ${new Date().toISOString()}`
  );
  const res = JSON.parse(msg.data);
  console.log("Parsed Body: ", res);
  const hasJs = res.runtimes.includes("js");
  const { action, version, url } = res;
  if (hasJs && action === "update") {
    const moduleUrl = `${url}/${version}/js.tar`;
    console.log("Fetching: ", moduleUrl);
    resetLib();
    fetch(moduleUrl).then((response) => {
      response.body.pipe(require("tar").x({ cwd: "./lib/js", sync: true }));
      client.complete(msg, function (err) {
        if (err) {
          console.error("complete error: " + err.toString());
        } else {
          console.log("complete sent");
        }
      });
    });
  }
});

const http = require("http");
const hostname = "0.0.0.0";
const port = 3001;
let load_model;

const server = http.createServer((req, res) => {
  if (!load_model) {
    load_model = require("./lib/js/ssvm_nodejs_starter_lib.js").load_model;
  }
  res.end(load_model());
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
