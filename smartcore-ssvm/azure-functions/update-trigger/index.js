module.exports = async function (context, req) {
  const { release, repository, action } = req.body;
  const { tag_name } = release;
  const { html_url } = repository;

  if (action !== "published") {
    return;
  }

  const Client = require("azure-iothub").Client;
  const Message = require("azure-iot-common").Message;
  const Registry = require("azure-iothub").Registry;
  const { readFileSync } = require("fs");
  const config = JSON.parse(readFileSync(`${__dirname}/config.json`));
  const hubConnectionString = config.hubConnection;
  const hubDevicesConnectionString = config.registryReadConnection;
  let serviceClient = Client.fromConnectionString(hubConnectionString);

  function printResultFor(op) {
    return function printResult(err, res) {
      if (err) console.log(op + " error: " + err.toString());
      if (res) console.log(op + " status: " + res.constructor.name);
    };
  }
  function receiveFeedback(err, receiver) {
    receiver.on("message", function (msg) {
      console.log("Feedback message:");
      console.log(msg.getData().toString("utf-8"));
    });
  }
  serviceClient.open(async (err) => {
    if (err) {
      console.error("Could not connect: " + err.message);
    } else {
      const { result: devices } = await Registry.fromConnectionString(
        hubDevicesConnectionString
      )
        .createQuery("SELECT * FROM devices")
        .nextAsTwin();
      const targetDevices = devices.map((twin) => twin.deviceId);
      console.log(targetDevices);
      console.log("Service client connected");
      serviceClient.getFeedbackReceiver(receiveFeedback);
      var message = new Message(
        JSON.stringify({
          action: "update",
          url: `${html_url}/releases/download`,
          version: tag_name,
          runtimes: ["js", "python"],
        })
      );
      message.ack = "full";
      message.messageId = "My Message ID";
      console.log("Sending message: " + message.getData());
      for (const targetDevice of targetDevices) {
        serviceClient.send(targetDevice, message, printResultFor("send"));
      }
    }
  });
};
