package main

import (
	"io/ioutil"

	wasmer "github.com/wasmerio/wasmer-go/wasmer"
)

func getStringPointer(data string, instance *wasmer.Instance) (int32, int) {
	// Set the subject to greet.
	dataPrepared := []byte(data)
	lengthOfSubject := len(dataPrepared) + 1

	// Allocate memory for the subject, and get a pointer to it.
	allocate, _ := instance.Exports.GetFunction("allocate")
	allocateResult, _ := allocate(lengthOfSubject)
	ptr := allocateResult.(int32)

	// Write the subject into the memory.
	memory, _ := instance.Exports.GetMemory("memory")
	memoryData := memory.Data()[ptr:]

	for nth := 0; nth < lengthOfSubject-1; nth++ {
		memoryData[nth] = dataPrepared[nth]
	}

	// C-string terminates by NULL.
	memoryData[lengthOfSubject-1] = 0

	return ptr, lengthOfSubject
}

func main() {
	wasmBytes, _ := ioutil.ReadFile("smartcore_wasi_lib.wasm")

	engine := wasmer.NewEngine()
	store := wasmer.NewStore(engine)

	// Compiles the module
	module, _ := wasmer.NewModule(store, wasmBytes)

	wasiEnv, _ := wasmer.NewWasiStateBuilder("smartcore-wasi-go").
		PreopenDirectory(".").
		Finalize()

	importObject, _ := wasiEnv.GenerateImportObject(store, module)
	instance, _ := wasmer.NewInstance(module, importObject)

	file := "test1.txt"
	target := "test2.txt"
	filePtr, fileLen := getStringPointer(file, instance)
	targetPtr, targetLen := getStringPointer(target, instance)

	// Gets the `sum` exported function from the WebAssembly instance.
	load_model, _ := instance.Exports.GetFunction("load_model")
	deallocate, _ := instance.Exports.GetFunction("deallocate")

	load_model(filePtr, targetPtr)
	deallocate(filePtr, fileLen)
	deallocate(targetPtr, targetLen)
}
