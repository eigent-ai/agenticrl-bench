# Data Transformation Pipeline

A C++ template-based data transformation pipeline library with benchmarks.

## Components

- `pipeline.hpp` — Header-only template library for applying transformations to vectors
- `main.cpp` — Unit driver that tests the pipeline functions
- `benchmark.cpp` — Performance benchmark comparing iterator vs lambda summation approaches

## Building

```bash
make all      # Build main and benchmark
make test     # Build and run all tests
make clean    # Remove build artifacts
```

## Requirements

- g++ 13 with C++17 support
- GNU Make
