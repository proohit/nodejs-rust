# nodejs-rust
## Motivation
The goal was to implement machine learning functions in Rust and use them from JavaScript using WebAssembly.

## Build
We need `wasm-pack` to build the module.

`wasm-pack build --target nodejs`

It outputs the module including JS bindings into `pkg` folder. Then run

`npm install --save`

to setup the node dependencies.

## Run

After building and installing the depdenceny, run `node index.js` which then outputs the calculated predictions from the model.