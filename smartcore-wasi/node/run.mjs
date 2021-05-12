import fs from 'fs';
import wasiImport from 'wasi'
const { WASI } = wasiImport;

const wasi = new WASI({
  args: process.argv,
  env: process.env,
  preopens: {
    '/': '.'
  }
});

const importObject = { wasi_snapshot_preview1: wasi.wasiImport };

const wasm = await WebAssembly.compile(fs.readFileSync('smartcore_wasi_lib.wasm'));
const instance = await WebAssembly.instantiate(wasm, importObject);
wasi.initialize(instance);
instance.exports.load_model()