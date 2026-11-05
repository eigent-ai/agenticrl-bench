# flopbench — Floating-Point Benchmark

Measures DAXPY throughput (`y[i] += alpha * x[i]`) in double precision and compares
it to the equivalent 64-bit integer operation.

## Expected Performance

Modern x86-64 hardware with proper compiler optimisation should achieve:

| Metric           | Target     |
|------------------|-----------|
| Double MFLOPS    | > 300      |
| Integer MOPS     | > 300      |
| Float/Int ratio  | < 2.0      |

If you see MFLOPS far below 300 — or a Float/Int ratio greater than 3 — check
your compiler flags.  Common culprits:

- No optimisation flag (must use at least `-O1`)
- `-ffloat-store` — forces every FP intermediate to be written to memory; harmless
  for debugging precision but catastrophic for throughput
- `-fno-tree-vectorize` — disables SIMD auto-vectorisation

## Build and Run

    make
    ./flopbench

Results are written to `/tmp/bench_results.txt` in key=value format.
