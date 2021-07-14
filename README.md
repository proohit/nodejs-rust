# Smartcore-WASI

This project is a demonstration of a WASI module that's being used in several programming languages. Current demonstration shows the integration in:

- Python (see [python](./python/README.md))
- Go (see [go](./go/README.md))
- JavaScript (nodejs) (see [node](./node/README.md))

The project defines source code written in Rust, that gets compiled to a WebAssembly binary which uses WASI functions to abstract sys-calls to FS.

## Prerequisites

- Rust and Cargo
- rustup
- wasm32-wasi as a build target. Add with `rustup target add wasm32-wasi`

## Build

In contrast to normal execution (WASI +FS), we need to specify rust to compile the library module:

`cargo build --release --target=wasm32-wasi --lib`

Results in `target/wasm32-wasi/release` folder, which includes the WASM library module `smartcore_wasi_lib.wasm`.

Tested with rust v.1.54.0 and v.1.52.1
