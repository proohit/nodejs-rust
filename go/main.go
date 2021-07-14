package main

import (
	glue "smartcore-wasi-go/lib/go"
)

func main() {
	output := glue.Load_model()
	print(output)
}
