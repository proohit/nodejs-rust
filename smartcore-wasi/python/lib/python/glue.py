from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler


def get_string_ptr(string, instance):
    prepared_string = bytes(string, 'utf-8')
    length_of_string = len(prepared_string) + 1
    string_ptr = instance.exports.allocate(length_of_string)
    memory = instance.exports.memory.uint8_view(string_ptr)
    memory[0:length_of_string] = prepared_string
    memory[length_of_string] = 0
    return (string_ptr, length_of_string)


def get_string_from_ptr(ptr, instance):
    memory = instance.exports.memory.uint8_view(ptr)
    memory_length = len(memory)
    output = []
    nth = 0

    while nth < memory_length:
        byte = memory[nth]

        if byte == 0:
            break

        output.append(byte)
        nth += 1
    length_of_output = nth

    return (bytes(output).decode(), length_of_output)


relative_dir = 'lib/python'

wasm_bytes = open(f'{relative_dir}/smartcore_wasi_lib.wasm', 'rb').read()
store = Store(engine.JIT(Compiler))
module = Module(store, wasm_bytes)
wasi_version = wasi.get_version(module, strict=True)
wasi_env = wasi.StateBuilder(
    'smartcore-wasi-lib').preopen_directory(".").finalize()

import_object = wasi_env.generate_import_object(store, wasi_version)

instance = Instance(module, import_object)
(file_ptr, file_len) = get_string_ptr(
    f'{relative_dir}/iris_knn.model', instance)
instance.exports.init(file_ptr)


def load_model():
    output_ptr = instance.exports.load_model()
    (output, output_len) = get_string_from_ptr(output_ptr, instance)
    instance.exports.deallocate(output_ptr, output_len)
    return output
