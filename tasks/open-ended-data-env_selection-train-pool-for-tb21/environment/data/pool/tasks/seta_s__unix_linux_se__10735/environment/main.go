package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
)

type Config struct {
	Message string `json:"message"`
}

func main() {
	ln, err := net.Listen("tcp", ":80")
	if err != nil {
		log.Fatalf("cannot bind to port 80: %v", err)
	}
	defer ln.Close()

	data, err := os.ReadFile("/etc/apiserver/config.json")
	if err != nil {
		log.Fatalf("config read error: %v", err)
	}
	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		log.Fatalf("config parse error: %v", err)
	}

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprintf(w, `{"status":"ok","message":%q}`+"\n", cfg.Message)
	})

	log.Printf("Listening on :80")
	if err := http.Serve(ln, nil); err != nil {
		log.Fatalf("serve error: %v", err)
	}
}
