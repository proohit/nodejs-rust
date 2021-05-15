from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler
import os


__dir__ = os.path.dirname(os.path.realpath(__file__))
wasm_bytes = open(__dir__ + '/smartcore-wasi.wasm', 'rb').read()
store = Store(engine.JIT(Compiler))
module = Module(store, wasm_bytes)
wasi_version = wasi.get_version(module, strict=True)
wasi_env_cmd = \
    wasi.StateBuilder('smartcore-wasi-cmd'). \
        preopen_directory("."). \
        finalize()
wasi_env_lib = \
    wasi.StateBuilder('smartcore-wasi-lib'). \
        argument('load_model'). \
        preopen_directory("."). \
        finalize()
cmd_import_object = wasi_env_cmd.generate_import_object(store, wasi_version)
lib_import_object = wasi_env_lib.generate_import_object(store, wasi_version)

instance = Instance(module, cmd_import_object)
instance.exports._start()

instance = Instance(module, lib_import_object)
instance.exports._start()