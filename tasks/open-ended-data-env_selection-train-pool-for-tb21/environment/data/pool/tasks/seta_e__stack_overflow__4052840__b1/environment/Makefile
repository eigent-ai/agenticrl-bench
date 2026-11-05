.PHONY: all build run clean

BUILD_DIR = build

all: build run

build:
	mkdir -p $(BUILD_DIR)
	go build -o $(BUILD_DIR)/transformer .

run: build
	mkdir -p output
	$(BUILD_DIR)/transformer data/fields.txt output/result.txt

clean:
	rm -rf $(BUILD_DIR) output/
