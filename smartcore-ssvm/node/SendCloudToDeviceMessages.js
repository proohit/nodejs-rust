'use strict';

const Client = require('azure-iothub').Client;
const Message = require('azure-iot-common').Message;
const Registry = require('azure-iothub').Registry;
const { readFileSync } = require('fs');
const config = JSON.parse(readFileSync('config.json'));
const hubConnectionString = config.hubConnection;
const hubDevicesConnectionString = config.registryReadConnection;
let targetDevices = [];
const onDevicesQuery = (err, results) => {
  if (err) {
    console.error('Failed to fetch the results: ' + err.message);
  } else {
    targetDevices = results.map(twin => twin.deviceId);
    console.log(targetDevices);
  }
};
Registry.fromConnectionString(hubDevicesConnectionString).createQuery('SELECT * FROM devices').nextAsTwin(onDevicesQuery);
var serviceClient = Client.fromConnectionString(hubConnectionString);

function printResultFor(op) {
  return function printResult(err, res) {
    if (err) console.log(op + ' error: ' + err.toString());
    if (res) console.log(op + ' status: ' + res.constructor.name);
  };
}
function receiveFeedback(err, receiver) {
  receiver.on('message', function (msg) {
    console.log('Feedback message:');
    console.log(msg.getData().toString('utf-8'));
  });
}
serviceClient.open(function (err) {
  if (err) {
    console.error('Could not connect: ' + err.message);
  } else {
    console.log('Service client connected');
    serviceClient.getFeedbackReceiver(receiveFeedback);
    const modelBuf = readFileSync('iris_knn.model');
    var message = new Message(modelBuf);
    message.ack = 'full';
    message.messageId = 'My Message ID';
    console.log('Sending message: ' + message.getData());
    for (const targetDevice of targetDevices) {
      serviceClient.send(targetDevice, message, printResultFor('send'));
    }
  }
});
