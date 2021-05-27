#!/bin/bash

MACHINE=$1
NUM_EXEC=$2
echo "Running bench for $MACHINE"

set -x
cd go
noe=$NUM_EXEC /usr/local/go/bin/go run perf.go
cd ../node
noe=$NUM_EXEC node --experimental-wasi-unstable-preview1 perf.js
cd ../python
set +x
source env/bin/activate
set -x
noe=$NUM_EXEC python perf-wasmtime.py
cd ..
noe=$NUM_EXEC cargo run --release

sudo mount /dev/sda1 /mnt/usb1
sudo cp go/data-go-wasmer.csv /mnt/usb1/data-go-wasmer-$MACHINE.csv
sudo cp node/data-js.csv /mnt/usb1/data-js-$MACHINE.csv
sudo cp python/data-py-wasmtime.csv /mnt/usb1/data-py-wasmtime-$MACHINE.csv
sudo cp data-native.csv /mnt/usb1/data-native-$MACHINE.csv
sudo umount /mnt/usb1
