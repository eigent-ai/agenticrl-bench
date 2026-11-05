"""Standard mathematical test functions for optimization benchmarking."""

import numpy as np


def rosenbrock(x):
    """Rosenbrock function. Global minimum: f(1, 1) = 0."""
    return sum(100.0 * (x[i+1] - x[i]**2)**2 + (1 - x[i])**2
               for i in range(len(x) - 1))


def rastrigin(x):
    """Rastrigin function. Global minimum: f(0, 0) = 0."""
    n = len(x)
    return 10 * n + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)


def ackley(x):
    """Ackley function. Global minimum: f(0, 0) = 0."""
    n = len(x)
    sum1 = sum(xi**2 for xi in x)
    sum2 = sum(np.cos(2 * np.pi * xi) for xi in x)
    return 20 * np.exp(-0.2 * np.sqrt(sum1 / n)) - np.exp(sum2 / n) + np.e + 20


TEST_FUNCTIONS = [
    {
        "name": "rosenbrock",
        "func": rosenbrock,
        "bounds": [(-5, 10), (-5, 10)],
        "known_minimum": 0.0,
        "dimensions": 2
    },
    {
        "name": "rastrigin",
        "func": rastrigin,
        "bounds": np.array([-5.12, 5.12, -5.12, 5.12]),
        "known_minimum": 0.0,
        "dimensions": 2
    },
    {
        "name": "ackley",
        "func": ackley,
        "bounds": [(-5, 5), (-5, 5)],
        "known_minimum": 0.0,
        "dimensions": 2
    }
]
