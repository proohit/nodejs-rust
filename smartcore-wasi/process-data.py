import sys
import argparse
import csv


parser = argparse.ArgumentParser()
parser.add_argument("csv", type=str)
parser.add_argument("device", type=str)
parser.add_argument("arch", type=str)
parser.add_argument("os", type=str)
parser.add_argument("osVersion", type=str)
parser.add_argument("runtime", type=str)
parser.add_argument("kernel", type=str)

args = parser.parse_args()
file = args.csv
print(file)
raw = open(file, 'r').read()

st_idx = raw.find('startTime:')
et_idx = raw.find('endTime:')
data_idx = raw.find('data:')
start_time = raw[st_idx:et_idx].replace('\n', '').replace('startTime:', '')
end_time = raw[et_idx:data_idx].replace('\n', '').replace('endTime:', '')
data = raw[data_idx::].replace('\n', '').replace('data:', '').replace(
    '[', '').replace(']', '').replace(' ', '').split(',')
with open(f'prepared-{file}', 'w') as output:
    field_names = ['startTime (UTC)', 'endTime (UTC)', 'device', 'arch',
                   'os', 'osVersion', 'runtime', 'kernel', 'time (ns)']
    wrt = csv.DictWriter(output, delimiter=",", fieldnames=field_names)
    wrt.writeheader()
    for date in data:
        wrt.writerow(
            {
                'startTime (UTC)': start_time,
                'endTime (UTC)': end_time,
                'device': args.device,
                'arch': args.arch,
                'os': args.os,
                'osVersion': args.osVersion,
                'runtime': args.runtime,
                'kernel': args.kernel,
                'time (ns)': date
            }
        )
