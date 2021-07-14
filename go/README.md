# Smartcore-WASI Go example

This example demonstrates using the WASM Module in Go. It uses the WebAssembly VM [Wasmer-Go](https://github.com/wasmerio/wasmer-go).

## Run

`go run main.go`

## Build

`go build`

## Performance

Performance for the WASM Module can be measured with the program [./perf.go](./perf.go). It expects the WASM Package to be in `./lib/go`. To configure the number of executions, provide an environment variable `noe`.

Example:

```sh
noe=10000 go run perf.go
```
