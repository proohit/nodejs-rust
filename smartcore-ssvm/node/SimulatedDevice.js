// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

'use strict';

// The device connection string to authenticate the device with your IoT hub.
//
// NOTE:
// For simplicity, this sample sets the connection string in code.
// In a production environment, the recommended approach is to use
// an environment variable to make it available to your application
// or use an HSM or an x509 certificate.
// https://docs.microsoft.com/azure/iot-hub/iot-hub-devguide-security
//
// Using the Azure CLI:
// az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
const { readFileSync, mkdirSync, createWriteStream, existsSync, rmdirSync } = require('fs')

const config = JSON.parse(readFileSync('config.json'));
const connectionString = config.deviceConnection;

// Using the Node.js Device SDK for IoT Hub:
//   https://github.com/Azure/azure-iot-sdk-node
// The sample connects to a device-specific MQTT endpoint on your IoT Hub.
var Mqtt = require('azure-iot-device-mqtt').Mqtt;
var DeviceClient = require('azure-iot-device').Client;

var client = DeviceClient.fromConnectionString(connectionString, Mqtt);
const fetch = require('node-fetch');

client.on('message', function (msg) {
  console.log(`Received MessageId: ${msg.messageId}`);
  const res = JSON.parse(msg.data);
  console.log('Parsed Body: ', res);
  const hasJs = res.runtimes.includes('js');
  const { action, version, url } = res;
  if (hasJs && action === 'update') {
    const moduleUrl = `${url}/${version}/js.tar`;
    console.log('Fetching: ', moduleUrl);
    if (existsSync('./lib/js')) {
      rmdirSync('./lib/js')
    }
    mkdirSync('./lib/js');

    fetch(moduleUrl).then(response => {
      response.body.pipe(require('tar').x({ cwd: './lib/js', sync: true }));
      client.complete(msg, function (err) {
        if (err) {
          console.error('complete error: ' + err.toString());
        } else {
          console.log('complete sent');
        }
      });
    });
  }
});


const http = require('http');
const hostname = '0.0.0.0';
const port = 3001;
let load_model;
const server = http.createServer((req, res) => {
  if(!load_model) {
    load_model = require('./lib/js/ssvm_nodejs_starter_lib.js').load_model;
  }
  res.end(load_model());
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});