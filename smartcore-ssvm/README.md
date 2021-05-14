# Smartcore-SSVM

This is an example of using `smartcore` lib (machine learning library for rust) inside a WebAssembly Module, whose model is serialized into a file and read upon usage. The WASM binary exposes functions to work with the model. It is used inside NodeJs with `SSVM` and accesses the model.

The are two node apps, which communicate over `Azure`. One (`node/SimulatedDevice.js`) is connected as an IoT Device and receives updated models from the cloud. The other one (`node/SendCloutToDeviceMessages.js`) is a cloud function that sends the model to the device.

Currently only works on `x86_64` architecture.

## Build

1. First install necessary NPM dependencies with 
```bash
smartcore-ssvm$ npm install &&\
cd node &&\
npm install
```
2. Then compile Rust into WebAssembly with `ssvmup build` or `rustwasmc build`.
3. Now build the model for the cloud to send to the server with `cargo run`.

## Run

1. You will need to setup the config inside `node/config.json`. Enter you information there.
2. Cd into the `node` folder, if not already inside. 
3. Run `npm run device` to start the edge device, including the webserver.
4. Now run `npm run cloud` to send the new model to the device.
5. When you run `curl http://localhost:3000`, you should get a number as an output.