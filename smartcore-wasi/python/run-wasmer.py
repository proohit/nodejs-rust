from wasmer import engine, wasi, Store, Module, Instance
from wasmer_compiler_cranelift import Compiler
import os


def get_string_ptr(string, instance):
    prepared_string = bytes(string, 'utf-8')
    length_of_string = len(prepared_string) + 1
    # Allocate memory for the subject, and get a pointer to it.
    string_ptr = instance.exports.allocate(length_of_string)

    # Write the subject into the memory.
    memory = instance.exports.memory.uint8_view(string_ptr)
    memory[0:length_of_string] = prepared_string
    memory[length_of_string] = 0  # C-string terminates by NULL.
    return (string_ptr, length_of_string)


def invoke_fn_with_params(fn, instance, *param_ptrs):
    instance.exports[fn](*param_ptrs)


__dir__ = os.path.dirname(os.path.realpath(__file__))
wasm_bytes = open(__dir__ + '/smartcore_wasi_lib.wasm', 'rb').read()
store = Store(engine.JIT(Compiler))
module = Module(store, wasm_bytes)
wasi_version = wasi.get_version(module, strict=True)
wasi_env = wasi.StateBuilder(
    'smartcore-wasi-lib').preopen_directory("./").finalize()

import_object = wasi_env.generate_import_object(store, wasi_version)

instance = Instance(module, import_object)
(ptr_file_to_copy, len1) = get_string_ptr('test1.txt', instance)
(ptr_target, len2) = get_string_ptr('test2.txt', instance)

instance.exports.load_model(ptr_file_to_copy, ptr_target)
instance.exports.deallocate(ptr_file_to_copy, len1)
instance.exports.deallocate(ptr_target, len2)

# # Run the `greet` function. Give the pointer to the subject.
# output_pointer = instance.exports.greet(ftcPtr)

# # Read the result of the `greet` function.
# memory = instance.exports.memory.uint8_view(output_pointer)
# memory_length = len(memory)

# output = []
# nth = 0

# while nth < memory_length:
#     byte = memory[nth]

#     if byte == 0:
#         break

#     output.append(byte)
#     nth += 1

# length_of_output = nth

# print(bytes(output).decode())

# # Deallocate the subject, and the output.
# instance.exports.deallocate(ftcPtr, length_of_filename)
# instance.exports.deallocate(output_pointer, length_of_output)
