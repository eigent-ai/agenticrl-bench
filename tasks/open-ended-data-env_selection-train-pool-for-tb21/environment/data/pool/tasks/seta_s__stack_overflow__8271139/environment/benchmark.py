"""Benchmark runner for function pairs."""
import timeit
from functions import *


PAIRS = [
    ('compute_with_else', 'compute_without_else'),
    ('validate_data', 'validate_data_alt'),
    ('transform_record', 'transform_record_fast'),
    ('classify_value', 'classify_value_v2'),
    ('check_bounds', 'check_bounds_alt'),
]

TEST_INPUTS = {
    'compute_with_else': (42,),
    'compute_without_else': (42,),
    'validate_data': ([1, 2, 3],),
    'validate_data_alt': ([1, 2, 3],),
    'transform_record': ({'name': 'Test', 'value': 5},),
    'transform_record_fast': ({'name': 'Test', 'value': 5},),
    'classify_value': (50,),
    'classify_value_v2': (50,),
    'check_bounds': (5, 0, 10),
    'check_bounds_alt': (5, 0, 10),
}


def run_benchmark(func_name, iterations=10000):
    """Benchmark a function by name."""
    func = globals()[func_name]
    args = TEST_INPUTS[func_name]

    timer = timeit.Timer(lambda: func(*args))
    times = timer.repeat(3, iterations)
    return min(times) / iterations


def benchmark_all():
    """Run benchmarks for all function pairs."""
    results = []
    for name1, name2 in PAIRS:
        time1 = run_benchmark(name1)
        time2 = run_benchmark(name2)
        ratio = time1 / time2 if time2 > 0 else float('inf')
        results.append({
            'pair': [name1, name2],
            'times': [time1, time2],
            'timing_ratio': ratio
        })
    return results


if __name__ == '__main__':
    import json
    results = benchmark_all()
    print(json.dumps(results, indent=2))
