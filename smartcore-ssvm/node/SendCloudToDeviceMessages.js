'use strict';

const Client = require('azure-iothub').Client;
const Message = require('azure-iot-common').Message;
const {readFileSync} = require('fs');
const config = JSON.parse(readFileSync('config.json'));
const connectionString = config.hubConnectionString;
const targetDevice = config.targetDevice;

var serviceClient = Client.fromConnectionString(connectionString);

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
    serviceClient.send(targetDevice, message, printResultFor('send'));
  }
});
