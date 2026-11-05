#!/bin/bash
cd /opt/tennis_sim
julia --project=. benchmark/run_benchmarks.jl
exit $?
