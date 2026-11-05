"""Python wrapper around the _fastmath C extension module."""

from datacrunch._fastmath import fast_sum, fast_mean, fast_dot_product

__all__ = ["fast_sum", "fast_mean", "fast_dot_product"]
