.PHONY: format clean help

RAW_DIR := data/raw
CLEAN_DIR := data/cleaned
FORMAT_SCRIPT := scripts/format.vim

RAW_FILES := $(wildcard $(RAW_DIR)/*.txt)
CLEAN_FILES := $(patsubst $(RAW_DIR)/%.txt,$(CLEAN_DIR)/%.txt,$(RAW_FILES))

format: $(CLEAN_FILES)

$(CLEAN_DIR)/%.txt: $(RAW_DIR)/%.txt $(FORMAT_SCRIPT)
	@mkdir -p $(CLEAN_DIR)
	vim -es -u ~/.vimrc -S $(FORMAT_SCRIPT) -c 'wq! $@' '$<'

clean:
	rm -f $(CLEAN_DIR)/*.txt

help:
	@echo "Targets:"
	@echo "  format  - Process raw text files and write cleaned output"
	@echo "  clean   - Remove cleaned output files"
	@echo "  help    - Show this help message"
