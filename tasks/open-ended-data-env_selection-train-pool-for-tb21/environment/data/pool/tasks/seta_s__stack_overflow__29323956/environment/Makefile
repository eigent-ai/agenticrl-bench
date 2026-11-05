SRC_DIR=source
BUILD_DIR=build
MAIN_CLASS=contrast.Main

SOURCES=$(shell find $(SRC_DIR) -name '*.java')

.PHONY: build clean run

build:
	mkdir -p $(BUILD_DIR)
	javac -d $(BUILD_DIR) $(SOURCES)

clean:
	rm -rf $(BUILD_DIR)

run:
	java -cp $(BUILD_DIR) $(MAIN_CLASS)
