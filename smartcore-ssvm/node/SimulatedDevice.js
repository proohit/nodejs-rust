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
const {readFileSync} = require('fs')

const config = JSON.parse(readFileSync('config.json'));
const connectionString = config.deviceConnectionString;
const modelPath = config.modelPath;

// Using the Node.js Device SDK for IoT Hub:
//   https://github.com/Azure/azure-iot-sdk-node
// The sample connects to a device-specific MQTT endpoint on your IoT Hub.
var Mqtt = require('azure-iot-device-mqtt').Mqtt;
var DeviceClient = require('azure-iot-device').Client;

var client = DeviceClient.fromConnectionString(connectionString, Mqtt);

client.on('message', function (msg) {
  console.log('Id: ' + msg.messageId + ' Body: ' + msg.data);
  require('fs').writeFileSync(modelPath, msg.data);
  client.complete(msg, function (err) {
    if (err) {
      console.error('complete error: ' + err.toString());
    } else {
      console.log('complete sent');
    }
  });
});

const { load_model } = require('../pkg/ssvm_nodejs_starter_lib.js');

const http = require('http');
const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {
  res.end(load_model());
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});