# Smartcore-WASI NodeJS

## Prerequisites

In order to use WASI in NodeJS, we need at least v12.22.1, the recommended version is v16.2.0

## Run

From node version 15.14.0 downwards, use

`node --experimental-wasi-unstable-preview1 --experimental-wasm-bigint run.mjs`

All versions above can ommit the `--experimental-wasm-bigint` flag.

`node --experimental-wasi-unstable-preview1 run.mjs`
