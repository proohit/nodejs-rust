const fs = require("fs");
const wasiImport = require("wasi");
const { performance } = require("perf_hooks");
const { WASI } = wasiImport;
const os = require("os");

const getStringPointer = (data, instance) => {
  var enc = new TextEncoder(); // always utf-8
  var length = data.length + 1;
  const targetMem = new Uint8Array(length);
  enc.encodeInto(data, targetMem);
  targetMem[length - 1] = 0;

  var ptr = instance.exports.allocate(length);
  var mem = new Uint8Array(instance.exports.memory.buffer, ptr, length);
  mem.set(targetMem);
  return { ptr, len: length };
};

const wasi = new WASI({
  args: [],
  env: process.env,
  preopens: {
    ".": ".",
  },
});

const importObject = { wasi_snapshot_preview1: wasi.wasiImport };
const relativeDir = "lib/js";

let instance;

const initialize = async () => {
  console.log("Initializing module");
  const wasm = await WebAssembly.compile(
    fs.readFileSync(`${relativeDir}/smartcore_wasi_lib.wasm`)
  );
  instance = await WebAssembly.instantiate(wasm, importObject);
  wasi.initialize(instance);
  let { ptr: fileToCopyPtr, len: len1 } = getStringPointer(
    `${relativeDir}/iris_knn.model`,
    instance
  );
  instance.exports.init(fileToCopyPtr);
  console.log("Initialization complete");
};

initialize().then(() => {
  const performances = [];
  let startTime = new Date();

  for (let i = 0; i < 1000; i++) {
    const t0 = process.hrtime.bigint();
    instance.exports.load_model();
    const t1 = process.hrtime.bigint();
    performances.push(t1 - t0);
  }
  const endTime = new Date();
  const content = `startTime:${startTime.toUTCString()}\nendTime:${endTime.toUTCString()}\ndata:[${performances}]`;
  require("fs").writeFileSync("data-js.csv", content);
});
