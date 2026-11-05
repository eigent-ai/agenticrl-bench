PYTHON = python

.PHONY: all build clean configure

all: configure build

configure:
	@echo "Running configuration..."
	bash ./configure.sh

build:
	@echo "Building project..."
	$(PYTHON) setup.py build
	@echo "Running code generator..."
	$(PYTHON) scripts/generate_code.py
	@echo "Build complete!"

clean:
	rm -rf build/ dist/ generated/
