# profiler_demo

A demo application for performance profiling with gprof.

## Profiling workflow

1. Build with profiling support (requires appropriate compiler flags)
2. Run the binary to collect profiling data
3. Use `gprof` to generate a report from the collected data
4. Use `gprof2dot` + `graphviz` to visualize the call graph
5. Check `profile/` for outputs
