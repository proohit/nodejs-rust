import time
import datetime
import wasmtime


def get_string_ptr(string, instance):
    prepared_string = bytes(string, 'utf-8')
    length_of_string = len(prepared_string) + 1
    string_ptr = instance.exports["allocate"](length_of_string)
    memory = instance.exports["memory"]
    for idx in range(length_of_string-1):
        memory.data_ptr[string_ptr+idx] = prepared_string[idx]
    memory.data_ptr[string_ptr+length_of_string] = 0
    return (string_ptr, length_of_string)


relative_dir = 'lib/python'

wasm_cfg = wasmtime.Config()
wasm_cfg.cache = True

wasi_cfg = wasmtime.WasiConfig()
wasi_cfg.argv = ()
wasi_cfg.preopen_dir(".", "/")
wasi_cfg.inherit_stdin()
wasi_cfg.inherit_stdout()
wasi_cfg.inherit_stderr()

wasm_bytes = open(f'{relative_dir}/smartcore_wasi_lib.wasm', 'rb').read()
store = wasmtime.Store(wasmtime.Engine(wasm_cfg))
linker = wasmtime.Linker(store)
module = wasmtime.Module(store.engine, wasm_bytes)
wasi = linker.define_wasi(wasmtime.WasiInstance(
    store, "wasi_snapshot_preview1", wasi_cfg))
smartcore_wasi = linker.instantiate(module)

(file_ptr, file_len) = get_string_ptr(
    f'{relative_dir}/iris_knn.model', smartcore_wasi)
smartcore_wasi.exports["init"](file_ptr)


perfomances = []
start_time = datetime.datetime.now()
for i in range(1000):
    t1 = time.monotonic_ns()
    smartcore_wasi.exports["load_model"]()
    t2 = time.monotonic_ns()
    perfomances.append(t2-t1)
end_time = datetime.datetime.now()
content = f"""startTime:{start_time}
endTime:{end_time}
data:{perfomances}
"""
with open("data-py-wasmtime.csv", "w") as file:
    file.write(content)
