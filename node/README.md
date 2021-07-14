# Smartcore-WASI NodeJS

This example demonstrates using the WASM Module in NodeJS. It uses the WebAssembly VM included in V8.

There are two example scripts: [run-device.js](./run-device.js) and [run.js](./run.js). `run-device.js` includes an integration with Microsoft Azure to receive realtime updates from IoT Hub regarding a new version of the WASM Package. For reference, the WASM Package is included in [lib/js](./lib/js).

## Prerequisites

In order to use WASI in NodeJS, we need at least v12.22.1, the recommended version is v16.2.0

## Run

From node version 15.14.0 downwards, use

`node --experimental-wasi-unstable-preview1 --experimental-wasm-bigint run.js`

All versions above can ommit the `--experimental-wasm-bigint` flag.

`node --experimental-wasi-unstable-preview1 run.js`

## Performance

Performance for the WASM Module can be measured with the script [perf.js](./perf.js). It expects the WASM Package to be in `lib/js`. To configure the number of executions, provide an environment variable `noe`.

Example:

```sh
noe=10000 node --experimental-wasi-unstable-preview1 perf.js
```
