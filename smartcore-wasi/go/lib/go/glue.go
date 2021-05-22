package glue

import (
	"fmt"
	"io/ioutil"

	wasmer "github.com/wasmerio/wasmer-go/wasmer"
)

var instance *wasmer.Instance
var relativeDir string = "lib/go"

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

func initialize() {
	wasmBytes, _ := ioutil.ReadFile(fmt.Sprintf("%s/smartcore_wasi_lib.wasm", relativeDir))
	engine := wasmer.NewEngine()
	store := wasmer.NewStore(engine)

	// Compiles the module
	module, _ := wasmer.NewModule(store, wasmBytes)

	wasiEnv, _ := wasmer.NewWasiStateBuilder("smartcore-wasi-go").
		PreopenDirectory(".").
		Finalize()

	importObject, _ := wasiEnv.GenerateImportObject(store, module)
	newInstance, _ := wasmer.NewInstance(module, importObject)

	instance = newInstance
	init, _ := instance.Exports.GetFunction("init")
	filePtr, _ := getStringPointer(fmt.Sprintf("%s/iris_knn.model", relativeDir), instance)
	init(filePtr)
}

func getStringFromPointer(ptr int32, instance *wasmer.Instance) (string, int) {
	memory, _ := instance.Exports.GetMemory("memory")
	memoryData := memory.Data()[ptr:]
	len := len(memoryData)
	lengthOfString := 0
	for ; lengthOfString < len; lengthOfString++ {
		if memoryData[lengthOfString] == 0 {
			break
		}
	}
	return string(memoryData[0:lengthOfString]), lengthOfString
}

func Load_model() string {

	if instance == nil {
		initialize()
	}
	load_model, _ := instance.Exports.GetFunction("load_model")
	deallocate, _ := instance.Exports.GetFunction("deallocate")
	outputPtr, _ := load_model()
	output, outputLen := getStringFromPointer(outputPtr.(int32), instance)
	deallocate(outputPtr, outputLen)
	return output
}
