#!/bin/bash
# Run all benchmarks and collect timing data

BUILDDIR="build"
OUTFILE="output/timings.csv"

echo "benchmark,compiler,opt,time" > "$OUTFILE"

BENCHMARKS="array_bench math_bench poly_bench"
COMPILERS="gcc clang"
OPTS="O2 O3"

for bench in $BENCHMARKS; do
    for comp in $COMPILERS; do
        for opt in $OPTS; do
            binary="${BUILDDIR}/${bench}_${comp}_${opt}"
            if [ ! -x "$binary" ]; then
                echo "WARNING: $binary not found or not executable" >&2
                continue
            fi

            # Run with time -p and capture timing
            timing_output=$( { time -p "$binary" > /tmp/bench_stdout.txt 2>&1; } 2>&1 )

            # Parse the user time from the output
            real_time=$(echo "$timing_output" | grep "^user" | awk '{print $2}')

            echo "${bench},${comp},${opt},${real_time}" >> "$OUTFILE"
            echo "Ran ${bench}_${comp}_${opt}: ${real_time}s"
        done
    done
done

echo "Results written to $OUTFILE"
