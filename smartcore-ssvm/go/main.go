package main

import (
	"os"

	"github.com/second-state/WasmEdge-go/wasmedge"
)

func main() {
	/// Set not to print debug info
	wasmedge.SetLogErrorLevel()

	/// Create configure
	var conf = wasmedge.NewConfigure(wasmedge.REFERENCE_TYPES)
	conf.AddConfig(wasmedge.WASI)

	/// Create VM with configure
	var vm = wasmedge.NewVMWithConfig(conf)

	/// Init WASI (test)
	var wasi = vm.GetImportObject(wasmedge.WASI)
	wasi.InitWasi(
		[]string{"load_model"}, /// The args
		os.Environ(),           /// The envs
		[]string{""},           /// The mapping directories
		[]string{"/", "."},     /// The preopens will be empty
	)
	vm.LoadWasmFile("../pkg/ssvm_nodejs_starter_bg.wasm")
	vm.Validate()
	vm.Instantiate()
	vm.Execute("_start")

	vm.Delete()
	conf.Delete()
}
