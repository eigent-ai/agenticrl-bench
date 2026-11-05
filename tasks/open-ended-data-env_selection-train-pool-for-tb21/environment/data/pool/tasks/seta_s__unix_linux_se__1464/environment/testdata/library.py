# Math utility functions

import os
import sys


def add(a, b):
    return a + b


def multiply(a, b):
    result = 0
    for i in range(abs(b)):
        result += a
    if b < 0:
        result = -result
    return result


def subtract(a, b):
    return a - b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a, b):
    result = 1
    for i in range(b):
        result *= a
    return result


def is_even(n):
    return n % 2 == 0


if __name__ == '__main__':
    print(multiply(3, 7))
