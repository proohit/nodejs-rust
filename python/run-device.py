from datetime import datetime
import json
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio
import platform
import importlib
import requests
import tarfile
import os
import shutil
from pathlib import Path

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
    raise RuntimeError("Platform not supported")

print(glue.load_model())


async def run():

    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    conn_str = config['deviceConnection']
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    await device_client.connect()

    # define behavior for receiving a message
    # NOTE: this could be a function or a coroutine
    def message_received_handler(message):
        res = json.loads(message.data)
        print(f'Received message on {datetime.now()}')
        print("Parsed Body: ", res)
        hasPython = "python" in res['runtimes']
        action = res['action']
        version = res['version']
        url = res['url']
        if hasPython and action == "update":
            module_url = f'{url}/{version}/python.tar'
            print("Fetching: ", module_url)
            reset_lib(module_url)

    def reset_lib(module_url):
        response = requests.get(module_url, stream=True)
        if response.status_code == 200:
            with open("./python.tar", 'wb') as f:
                f.write(response.raw.read())
            folder = 'lib/python'
            print("Deleting lib...")
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            print("Preparing lib...")
            Path("lib/python").mkdir(parents=True, exist_ok=True)
            file = tarfile.open("python.tar")
            print("Extracting update...")
            file.extractall('lib/python')
            importlib.reload(glue)
            print(glue.load_model())

    # set the mesage received handler on the client
    device_client.on_message_received = message_received_handler

    # define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)

    # Wait for user to indicate they are done listening for messages
    await user_finished

    # Finally, shut down the client
    await device_client.shutdown()

asyncio.run(run())
