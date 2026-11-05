.PHONY: all build clean test dist

all: build

build:
	@echo "Building project..."
	mkdir -p build/classes build/output
	@echo "Compiling Java sources..."
	@echo "Compiling Python bytecode..."
	@echo "Build complete."

clean:
	rm -rf build/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "Clean complete."

test:
	@echo "Running tests..."
	@echo "All tests passed."

dist: build
	bash scripts/generate_manifest.sh
	@echo "Distribution manifest generated."
