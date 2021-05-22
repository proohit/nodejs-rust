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


def get_string_from_ptr(ptr, instance):
    memory = instance.exports["memory"]
    memory_length = memory.data_len
    output = []
    curr_ptr = ptr

    while curr_ptr < memory_length:
        byte = memory.data_ptr[curr_ptr]

        if byte == 0:
            break

        output.append(byte)
        curr_ptr += 1
    length_of_output = curr_ptr

    return (bytes(output).decode(), length_of_output)


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


def load_model():
    output_ptr = smartcore_wasi.exports["load_model"]()
    (output, output_len) = get_string_from_ptr(output_ptr, smartcore_wasi)
    smartcore_wasi.exports["deallocate"](output_ptr, output_len)
    return output
