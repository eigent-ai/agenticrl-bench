"""Pytest fixtures providing seeded random data for reproducibility."""

import numpy as np
import pytest


@pytest.fixture
def standard_normal_data():
    """10000 points from N(0, 1) with fixed seed."""
    rng = np.random.default_rng(12345)
    return rng.normal(loc=0, scale=1, size=10000)


@pytest.fixture
def shifted_normal_data():
    """5000 points from N(5, 2) with fixed seed."""
    rng = np.random.default_rng(23456)
    return rng.normal(loc=5, scale=2, size=5000)


@pytest.fixture
def far_shifted_normal_data():
    """5000 points from N(50, 10) with fixed seed."""
    rng = np.random.default_rng(34567)
    return rng.normal(loc=50, scale=10, size=5000)


@pytest.fixture
def lognormal_data():
    """5000 points from LogNormal(mu=2, sigma=0.5) with fixed seed."""
    rng = np.random.default_rng(45678)
    return rng.lognormal(mean=2, sigma=0.5, size=5000)


@pytest.fixture
def small_normal_data():
    """50 points from N(0, 1) with fixed seed."""
    rng = np.random.default_rng(56789)
    return rng.normal(loc=0, scale=1, size=50)
