import fs from 'fs';
import wasiImport from 'wasi'
const { WASI } = wasiImport;

const cmdWasi = new WASI({
  args: [],
  env: process.env,
  preopens: {
    '.': '.'
  }
});

const libWasi = new WASI({
  args: ["load_model"],
  env: process.env,
  preopens: {
    '.': '.'
  }
});

const cmdImportObject = { wasi_snapshot_preview1: cmdWasi.wasiImport };
const libImportObject = { wasi_snapshot_preview1: libWasi.wasiImport };

const wasm = await WebAssembly.compile(fs.readFileSync('smartcore-wasi.wasm'));
let instance = await WebAssembly.instantiate(wasm, cmdImportObject);
// wasi.initialize(instance);
cmdWasi.start(instance);
instance = await WebAssembly.instantiate(wasm, libImportObject);
libWasi.start(instance);