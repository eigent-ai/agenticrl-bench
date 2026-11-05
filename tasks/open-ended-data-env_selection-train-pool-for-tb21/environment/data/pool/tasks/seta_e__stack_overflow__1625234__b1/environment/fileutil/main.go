package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 4 {
		fmt.Fprintln(os.Stderr, "Usage: fileutil append <file> <text>")
		fmt.Fprintln(os.Stderr, "       fileutil insert <file> <offset> <text>")
		os.Exit(1)
	}

	command := os.Args[1]
	switch command {
	case "append":
		if err := AppendToFile(os.Args[2], os.Args[3]); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	case "insert":
		if len(os.Args) < 5 {
			fmt.Fprintln(os.Stderr, "Usage: fileutil insert <file> <offset> <text>")
			os.Exit(1)
		}
		offset, err := strconv.ParseInt(os.Args[3], 10, 64)
		if err != nil {
			fmt.Fprintf(os.Stderr, "invalid offset: %v\n", err)
			os.Exit(1)
		}
		if err := InsertAt(os.Args[2], offset, []byte(os.Args[4])); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
	default:
		fmt.Fprintf(os.Stderr, "Unknown command: %s\n", command)
		os.Exit(1)
	}
}
