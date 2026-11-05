.PHONY: all lint build test package clean

all: lint build test package
    @echo "=== CI Pipeline completed successfully ==="

lint:
    @echo "[Stage 1] Linting source code..."
    ./scripts/lint.sh

build:
    @echo "[Stage 2] Building application..."
    ./scripts/build.sh

test: build
    @echo "[Stage 3] Running tests..."
    ./scripts/test.sh

package: test
    @echo "[Stage 4] Packaging application..."
    ./scripts/package.sh

clean:
    rm -rf build/ dist/
    @echo "Cleaned build artifacts"
