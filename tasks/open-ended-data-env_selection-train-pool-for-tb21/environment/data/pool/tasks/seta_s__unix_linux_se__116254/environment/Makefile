BUILD_TYPE ?= debug

.PHONY: all check clean

all: qt_check.final

check: all
	ifeq ($(BUILD_TYPE),release)
	@echo "=== Release Build ==="
	else
	@echo "=== Debug Build ==="
	endif
	@echo "Build type verified."
	@cat qt_check.final

clean:
	@rm -f qt_check.final qt_check.processed qt_check.raw

%.final: %.processed
	@grep -q "Qt version 6" $< || { echo "ERROR: Qt 6 required but found: $$(cat $<)"; exit 1; }
	@cp $< $@
	@echo "Build type: $(BUILD_TYPE)" >> $@

%.processed: %.raw
	@grep "Qt version" $< > $@

%.raw:
	@qmake --version > $@
