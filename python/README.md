# Smartcore-WASI Python example

This example demonstrates using the WASM Module in Go. It can be used with two WebAssembly VMs:

- [wasmtime-py](https://github.com/bytecodealliance/wasmtime-py) (see [glue_wasmtime.py](./lib/python/glue_wasmtime.py))
- [wasmer-py](https://github.com/wasmerio/wasmer-python) (see [glue_wasmer.py](./lib/python/glue_wasmer.py)).

There are two example scripts: [run-device.py](./run-device.py) and [run.py](./run.py). `run-device.py` includes an integration with Microsoft Azure to receive realtime updates from IoT Hub regarding a new version of the WASM Package. For reference, the WASM Package is included in [lib/python](./lib/python).

## Install

Use virtual env

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Run

There are two examples to runtimes whose supported platforms are considered: One uses Wasmer and the other one uses Wasmtime as the underlying WASM VM.

```bash
python run.py
```

```bash
python run-device.py
```
