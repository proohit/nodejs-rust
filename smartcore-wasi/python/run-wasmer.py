from wasmer import engine, wasi, Store, Module, ImportObject, Instance
from wasmer_compiler_cranelift import Compiler
import os

__dir__ = os.path.dirname(os.path.realpath(__file__))
wasm_bytes = open(__dir__ + '/smartcore_wasi_lib.wasm', 'rb').read()

store = Store(engine.JIT(Compiler))

module = Module(store, wasm_bytes)

wasi_version = wasi.get_version(module, strict=True)

wasi_env = \
    wasi.StateBuilder('smartcore-wasi'). \
        preopen_directory("."). \
        finalize()

import_object = wasi_env.generate_import_object(store, wasi_version)

instance = Instance(module, import_object)

instance.exports.load_model()