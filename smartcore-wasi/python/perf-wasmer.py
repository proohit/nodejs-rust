import time
import datetime
from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler
import os


def get_string_ptr(string, instance):
    prepared_string = bytes(string, 'utf-8')
    length_of_string = len(prepared_string) + 1
    string_ptr = instance.exports.allocate(length_of_string)
    memory = instance.exports.memory.uint8_view(string_ptr)
    memory[0:length_of_string] = prepared_string
    memory[length_of_string] = 0
    return (string_ptr, length_of_string)


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
perfomances = []
num_executions = 1000
if os.environ.get("noe") is not None:
    num_executions = int(os.environ.get("noe"))
print(f"Executing {num_executions} times")
start_time = datetime.datetime.now()
for i in range(num_executions):
    t1 = time.monotonic_ns()
    instance.exports.load_model()
    t2 = time.monotonic_ns()
    perfomances.append(t2-t1)
end_time = datetime.datetime.now()
content = f"""startTime:{start_time}
endTime:{end_time}
data:{perfomances}
"""
with open("data-py-wasmer.csv", "w") as file:
    file.write(content)
