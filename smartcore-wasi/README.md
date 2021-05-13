# Smartcore-Wasi

## Build

Build to library mode with reactor:

`cargo rustc --release --target wasm32-wasi -- -Z wasi-exec-model=reactor`