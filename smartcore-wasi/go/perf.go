package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"

	wasmer "github.com/wasmerio/wasmer-go/wasmer"
)

var instance *wasmer.Instance
var relativeDir string = "lib/go"

func main() {
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

	loadModel, _ := instance.Exports.GetFunction("load_model")
	startTime := time.Now().UTC().String()
	performances := []int64{}
	numberOfExecutions := 1000
	if os.Getenv("noe") != "" {
		numberOfExecutions, _ = strconv.Atoi(os.Getenv("noe"))
	}
	println("Executing " + strconv.Itoa(numberOfExecutions) + " times")
	for i := 0; i < numberOfExecutions; i++ {
		t0 := time.Now()
		loadModel()
		performances = append(performances, time.Since(t0).Nanoseconds())
	}
	endTime := time.Now().UTC().String()
	stringData := strings.Join(strings.Fields(fmt.Sprint(performances)), ",")
	content := fmt.Sprintf("startTime:%s\nendTime:%s\ndata:%s", startTime, endTime, stringData)
	ioutil.WriteFile("data-go-wasmer.csv", []byte(content), 0644)
}

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
