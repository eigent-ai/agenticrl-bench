DATA_DIR    := data
BUILD_DIR   := build
SCRIPTS_DIR := scripts

SOURCES   := $(wildcard $(DATA_DIR)/*.csv)
BASENAMES := $(notdir $(SOURCES))
STEMS     := $(BASENAMES:.csv=)

NORMALIZED := $(patsubst %, $(BUILD_DIR)/normalized/%.csv, $(STEMS))
ANALYZED   := $(patsubst %, $(BUILD_DIR)/analyzed/%.json, $(STEMS))
REPORT     := $(BUILD_DIR)/report.txt

ANALYZED_FILES := $(wildcard $(BUILD_DIR)/analyzed/*.json)

.PHONY: all clean

all: $(REPORT)

$(BUILD_DIR)/normalized/%.csv: $(DATA_DIR)/%.csv
	python3 $(SCRIPTS_DIR)/normalize.py $< $@

$(BUILD_DIR)/analyzed/%.json: %.csv
	python3 $(SCRIPTS_DIR)/analyze.py $< $@

$(REPORT): $(ANALYZED_FILES)
	python3 $(SCRIPTS_DIR)/report.py $@ $^

clean:
	rm -rf $(BUILD_DIR)
