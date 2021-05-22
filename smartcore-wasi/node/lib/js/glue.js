const fs = require("fs");
const wasiImport = require("wasi");

const { WASI } = wasiImport;

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

const getStringFromPointer = (ptr, instance) => {
  var m = new Uint8Array(instance.exports.memory.buffer, ptr);
  let len = m.length;
  let lengthOfString = 0;
  for (; lengthOfString < len; lengthOfString++) {
    let byte = m[lengthOfString];
    if (byte === 0) {
      break;
    }
  }
  var decoder = new TextDecoder("utf-8");
  return {
    result: decoder.decode(m.slice(0, lengthOfString)),
    len: lengthOfString,
  };
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
};

const loadModel = async () => {
  if (!instance) {
    await initialize();
  }
  let outputPtr = instance.exports.load_model();
  let { result: output, len: outputLength } = getStringFromPointer(
    outputPtr,
    instance
  );
  instance.exports.deallocate(outputPtr, outputLength);
  return output;
};

module.exports = { loadModel };
