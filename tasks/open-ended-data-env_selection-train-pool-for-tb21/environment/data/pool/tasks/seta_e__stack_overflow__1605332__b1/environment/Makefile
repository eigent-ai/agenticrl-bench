.PHONY: all build run clean

all: run

build:
	mkdir -p bin
	go build -o bin/filechecker src/filechecker.go

run: build
	./bin/filechecker

clean:
	rm -f bin/filechecker output/copy_section.bin output/copy_buffer.bin output/report.json
