import argparse
import csv
import os

runtimes = {
    'go': 'wasmer-go1.0.3',
    'node': 'nodejs16.2.0',
    'rust': 'rust1.52.1',
    'python': 'wasmtime-py0.26.0'
}
runtimes.update({'js': runtimes['node']})
runtimes.update({'py': runtimes['python']})
runtimes.update({'golang': runtimes['go']})
runtimes.update({'native': runtimes['rust']})

parser = argparse.ArgumentParser()
parser.add_argument("folder", type=str)
parser.add_argument("arch", type=str)
parser.add_argument("os", type=str)
parser.add_argument("osVersion", type=str)
parser.add_argument("kernel", type=str)

args = parser.parse_args()
folder = args.folder
print(folder)
files = os.listdir(folder)


def determine_runtime(runtimes, file_name):
    runtime = None
    for tmp_runtime in runtimes:
        if tmp_runtime in file_name:
            runtime = runtimes[tmp_runtime]
            break
    return runtime


for file in files:
    print(f"preparing {file}")
    raw = open(f"{folder}/{file}", 'r').read()

    st_idx = raw.find('startTime:')
    et_idx = raw.find('endTime:')
    data_idx = raw.find('data:')
    start_time = raw[st_idx:et_idx].replace('\n', '').replace('startTime:', '')
    end_time = raw[et_idx:data_idx].replace('\n', '').replace('endTime:', '')
    data = raw[data_idx::].replace('\n', '').replace('data:', '').replace(
        '[', '').replace(']', '').replace(' ', '').split(',')
    with open(f'prepared-data/prepared-{file}', 'w', newline='') as output:
        field_names = ['startTime (UTC)', 'endTime (UTC)', 'arch',
                       'os', 'osVersion', 'runtime', 'kernel', 'time (ns)']
        wrt = csv.DictWriter(output, delimiter=",", fieldnames=field_names)
        wrt.writeheader()
        runtime = determine_runtime(runtimes, file)
        for date in data:
            wrt.writerow(
                {
                    'startTime (UTC)': start_time,
                    'endTime (UTC)': end_time,
                    'arch': args.arch,
                    'os': args.os,
                    'osVersion': args.osVersion,
                    'runtime': runtime,
                    'kernel': args.kernel,
                    'time (ns)': date
                }
            )
