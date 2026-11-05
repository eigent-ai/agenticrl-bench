package main

import (
	"dirmanager/pkg/fileops"
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 3 {
		fmt.Fprintln(os.Stderr, "Usage: testdirect <delete|clean> <path>")
		os.Exit(2)
	}
	operation := os.Args[1]
	path := os.Args[2]

	var err error
	switch operation {
	case "delete":
		err = fileops.DeleteRecursively(path)
	case "clean":
		err = fileops.CleanContents(path)
	default:
		fmt.Fprintf(os.Stderr, "Unknown operation: %s\n", operation)
		os.Exit(2)
	}

	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("ok")
	os.Exit(0)
}
