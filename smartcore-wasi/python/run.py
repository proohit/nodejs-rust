import wasmtime

wasm_cfg = wasmtime.Config()
wasm_cfg.cache = True

wasi_cfg = wasmtime.WasiConfig()
wasi_cfg.argv = ()
wasi_cfg.preopen_dir(".", "/")
wasi_cfg.inherit_stdin()
wasi_cfg.inherit_stdout()
wasi_cfg.inherit_stderr()

store = wasmtime.Store(wasmtime.Engine(wasm_cfg))
linker = wasmtime.Linker(store)
wasi = linker.define_wasi(wasmtime.WasiInstance(store,
    "wasi_snapshot_preview1", wasi_cfg))
smartcore_wasi = linker.instantiate(wasmtime.Module(store.engine,
    open('smartcore_wasi_lib.wasm', 'rb').read()))

smartcore_wasi.exports["load_model"]()
