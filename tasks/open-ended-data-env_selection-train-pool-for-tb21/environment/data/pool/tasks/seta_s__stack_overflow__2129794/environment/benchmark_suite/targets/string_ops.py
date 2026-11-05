"""String operation benchmark targets."""

import random
import string


def palindrome_check():
    """Check if randomly generated strings are palindromes."""
    results = []
    for _ in range(100):
        s = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 20)))
        cleaned = s.lower().replace(" ", "")
        results.append(cleaned == cleaned[::-1])
    return results


def anagram_check():
    """Check if pairs of randomly generated strings are anagrams."""
    results = []
    for _ in range(100):
        s1 = ''.join(random.choices(string.ascii_lowercase, k=8))
        s2 = ''.join(random.choices(string.ascii_lowercase, k=8))
        results.append(sorted(s1) == sorted(s2))
    return results
