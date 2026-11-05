#!/usr/bin/env python3
"""
Benchmark runner for prime sieve implementations.
Times each sieve for N=1000000 and prints a formatted table.
"""

import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from primes import (
    rwh_primes, rwh_primes1, rwh_primes2,
    sieveOfEratosthenes,
    ambi_sieve_plain, sundaram3,
    primesfrom2to, primesfrom3to,
    segmented_sieve,
)

N = 1000000
RUNS = 3


def benchmark(name, fn, n):
    times = []
    result = None
    for _ in range(RUNS):
        start = time.perf_counter()
        result = fn(n)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg = sum(times) / len(times)
    count = len(result) if hasattr(result, '__len__') else len(list(result))
    return avg, count


def main():
    sieves = [
        ("rwh_primes", rwh_primes),
        ("rwh_primes1", rwh_primes1),
        ("rwh_primes2", rwh_primes2),
        ("ambi_sieve_plain", ambi_sieve_plain),
        ("sundaram3", sundaram3),
        ("primesfrom2to", primesfrom2to),
        ("primesfrom3to", primesfrom3to),
    ]

    print(f"\nBenchmark: finding primes < {N}")
    print(f"{'Sieve':<25} {'Avg Time (s)':>14} {'Prime Count':>13}")
    print("-" * 55)

    errors = []
    for name, fn in sieves:
        try:
            avg_time, count = benchmark(name, fn, N)
            print(f"{name:<25} {avg_time:>14.6f} {count:>13}")
        except Exception as e:
            errors.append(f"{name}: {type(e).__name__}: {e}")
            print(f"{name:<25} {'ERROR':>14} {'---':>13}")

    print("-" * 55)

    print(f"\nBenchmark: segmented_sieve(900000, 1000000)")
    try:
        start = time.perf_counter()
        result = segmented_sieve(900000, 1000000)
        elapsed = time.perf_counter() - start
        print(f"{'segmented_sieve':<25} {elapsed:>14.6f} {len(result):>13}")
    except Exception as e:
        errors.append(f"segmented_sieve: {type(e).__name__}: {e}")
        print(f"{'segmented_sieve':<25} {'ERROR':>14} {'---':>13}")

    if errors:
        print(f"\n{len(errors)} sieve(s) failed:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)

    print("\nAll benchmarks completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
