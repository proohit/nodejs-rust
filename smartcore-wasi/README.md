# Smartcore-Wasi

## Build

In contrast to normal execution (WASI +FS), we need to specify rust to compile the library module:

`cargo build --release --target=wasm32-wasi --lib`

Tested with rust v.1.54.0 and v.1.52.1
