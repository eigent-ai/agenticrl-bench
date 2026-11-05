"""
Prime number sieve implementations.
Ported from a collection of fastest prime sieve algorithms.
"""

import numpy as np
import math


def rwh_primes(n):
    """Returns a list of primes < n"""
    sieve = [True] * (n/2)
    for i in xrange(3, int(n**0.5) + 1, 2):
        if sieve[i/2]:
            sieve[i*i/2::i] = [False] * ((n - i*i - 1)/(2*i) + 1)
    return [2] + [2*i + 1 for i in xrange(1, n/2) if sieve[i]]


def rwh_primes1(n):
    """Returns a list of primes < n"""
    sieve = [True] * (n/2)
    for i in xrange(3, int(n**0.5) + 1, 2):
        if sieve[i/2]:
            sieve[i*i/2::i] = [False] * ((n - i*i - 1)/(2*i) + 1)
    return [2] + [2*i + 1 for i in xrange(1, n/2) if sieve[i]]


def rwh_primes2(n):
    """Returns a list of primes < n using bytearray sieve"""
    sieve = bytearray([True]) * (n/2)
    for i in xrange(3, int(n**0.5) + 1, 2):
        if sieve[i/2]:
            sieve[i*i/2::i] = bytearray((n - i*i - 1)/(2*i) + 1)
    return [2] + [2*i + 1 for i in xrange(1, n/2) if sieve[i]]


def sieveOfEratosthenes(n):
    """Returns a list of primes < n"""
    primes = list(range(2, n))
    for i in range(2, int(n**0.5) + 1):
        primes = [x for x in primes if x == i or x % i != 0]
    return primes


def sieveOfAtkin(limit):
    """Returns a list of primes < limit using the Sieve of Atkin"""
    is_prime = [False] * (limit + 1)
    sqrt_limit = int(math.sqrt(limit)) + 1

    for x in range(1, sqrt_limit):
        for y in range(1, sqrt_limit):
            n = 4 * x * x + y * y
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                is_prime[n] = not is_prime[n]

            n = 3 * x * x + y * y
            if n <= limit and n % 12 == 7:
                is_prime[n] = not is_prime[n]

            n = 3 * x * x - y * y
            if x > y and n <= limit and n % 12 == 11:
                is_prime[n] = not is_prime[n]

    for n in range(5, sqrt_limit):
        if is_prime[n]:
            for k in range(n * n, limit + 1, n * n):
                is_prime[k] = False

    primes = [2, 3]
    for n in range(5, limit):
        if is_prime[n]:
            primes.append(n)
    return primes


def ambi_sieve_plain(n):
    """Returns a list of primes < n"""
    s = list(range(3, n, 2))
    for m in xrange(3, int(n**0.5) + 1, 2):
        if s[(m - 3)/2]:
            for t in xrange((m*m - 3)/2, (n >> 1) - 1, m):
                s[t] = 0
    return [2] + [x for x in s if x]


def sundaram3(max_n):
    """Returns a list of primes < max_n using Sieve of Sundaram"""
    numbers = list(range(3, max_n + 1, 2))
    half = max_n / 2
    initial = 4

    for step in xrange(3, max_n + 1, 2):
        for i in xrange(initial, half, step):
            numbers[i - 1] = 0
        initial += 2 * (step + 1)
        if initial > half:
            result = [2] + filter(None, numbers)
            return result

    return [2] + filter(None, numbers)


def primesfrom3to(n):
    """Returns an array of primes, 3 <= p < n using numpy"""
    sieve = np.ones(n/3 + (n % 6 == 2), dtype=np.bool)
    for i in xrange(1, int(n**0.5)/3 + 1):
        if sieve[i]:
            k = 3*i + 1 | 1
            sieve[k*k/3::2*k] = False
            sieve[k*(k - 2*(i & 1) + 4)/3::2*k] = False
    return np.r_[3, ((3*np.nonzero(sieve)[0][1:] + 1) | 1)]


def primesfrom2to(n):
    """Returns an array of primes, 2 <= p < n using numpy"""
    sieve = np.ones(n/3 + (n % 6 == 2), dtype=np.bool)
    for i in xrange(1, int(n**0.5)/3 + 1):
        if sieve[i]:
            k = 3*i + 1 | 1
            sieve[k*k/3::2*k] = False
            sieve[k*(k - 2*(i & 1) + 4)/3::2*k] = False
    return np.r_[2, 3, ((3*np.nonzero(sieve)[0][1:] + 1) | 1)]


def segmented_sieve(lower, upper):
    """Returns a list of primes in the range [lower, upper] (inclusive)."""
    limit = int(upper**0.5)
    small_primes = []
    is_prime = [True] * (limit + 1)
    for i in range(2, limit):
        if is_prime[i]:
            small_primes.append(i)
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False

    candidates = list(range(lower, upper))
    is_candidate_prime = [True] * len(candidates)

    for p in small_primes:
        start = ((lower + p - 1) // p) * p
        if start == p:
            start += p
        for j in range(start, upper, p):
            idx = j - lower
            if 0 <= idx < len(is_candidate_prime):
                is_candidate_prime[idx] = False

    result = []
    for i, val in enumerate(candidates):
        if is_candidate_prime[i] and val >= 2:
            result.append(val)
    return result
