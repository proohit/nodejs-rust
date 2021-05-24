import platform
arch = platform.machine()

print(f"Running on {arch}")

wasmer_supported_machines = ['x86_64']
wasmtime_supported_machines = ['aarch64', 'x86_64']

if arch in wasmer_supported_machines:
    print(f"importing for {arch} using wasmer")
    import lib.python.glue_wasmer as glue
elif arch in wasmtime_supported_machines:
    print(f"importing for {arch} using wasmtime")
    import lib.python.glue_wasmtime as glue
else:
    RuntimeError("Platform not supported")

output = glue.load_model()

print(output)

# May be used for dynamic lib loading
# import time
# import importlib

# for i in range(5):
#     output = glue.load_model()
#     print(output)
#     importlib.reload(glue)
#     time.sleep(5)
