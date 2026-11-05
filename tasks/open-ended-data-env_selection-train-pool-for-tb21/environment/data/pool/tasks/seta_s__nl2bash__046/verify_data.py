"""Helper script to verify expected values for the task data."""

def fingerprint(word):
    """Correct fingerprint: strip spaces, lowercase, sort chars, join."""
    return ''.join(sorted(c.lower() for c in word if c != ' '))

# 12 anagram pairs
anagrams = [
    ('listen', 'silent'),
    ('enlist', 'tinsel'),
    ('inlets', 'tinsel'),
    ('dusty', 'study'),
    ('stressed', 'desserts'),
    ('dog', 'god'),
    ('cat', 'act'),
    ('arc', 'car'),
    ('race', 'care'),
    ('evil', 'vile'),
    ('veil', 'live'),
    ('Astronomer', 'Moon starer'),
]

# 8 non-anagram pairs
non_anagrams = [
    ('tac', 'cat'),       # wait - tac IS an anagram of cat!
    ('night', 'thing'),   # wait - these ARE anagrams!
    ('post', 'stop'),     # wait - these ARE anagrams!
    ('tops', 'pots'),
    ('opts', 'stop'),
    ('acre', 'race'),
    ('hello', 'world'),
    ('fast', 'slow'),
]

print("=== ANAGRAM PAIRS ===")
for a, b in anagrams:
    fa = fingerprint(a)
    fb = fingerprint(b)
    status = "OK" if fa == fb else "FAIL"
    print(f"  [{status}] '{a}'/'{b}'  fp_a='{fa}' fp_b='{fb}'")

print("\n=== TESTING NON-ANAGRAM PAIRS ===")
for a, b in non_anagrams:
    fa = fingerprint(a)
    fb = fingerprint(b)
    status = "OK" if fa != fb else "FAIL - THESE ARE ANAGRAMS!"
    print(f"  [{status}] '{a}'/'{b}'  fp_a='{fa}' fp_b='{fb}'")

# Now compute what the original 19-pair dataset gives
print("\n=== ORIGINAL 19 UNIQUE PAIRS ANALYSIS ===")
original_pairs = [
    ('listen', 'silent'),
    ('enlist', 'tinsel'),
    ('inlets', 'listen'),
    ('dusty', 'study'),
    ('night', 'thing'),
    ('stressed', 'desserts'),
    ('dog', 'god'),
    ('cat', 'act'),
    ('tac', 'cat'),
    ('arc', 'car'),
    ('race', 'care'),
    ('acre', 'race'),
    ('post', 'stop'),
    ('tops', 'pots'),
    ('opts', 'stop'),
    ('evil', 'vile'),
    ('veil', 'live'),
    ('Astronomer', 'Moon starer'),
    ("Election results", "Lies let's recount"),
]

ana_count = 0
non_count = 0
for a, b in original_pairs:
    fa = fingerprint(a)
    fb = fingerprint(b)
    if fa == fb:
        ana_count += 1
        print(f"  ANA: '{a}'/'{b}'")
    else:
        non_count += 1
        print(f"  NON: '{a}'/'{b}'  fp_a='{fa}' fp_b='{fb}'")

print(f"\nTotal: {len(original_pairs)}, Anagram: {ana_count}, Non-anagram: {non_count}")

# Now compute family sizes with extra_words.txt
print("\n=== FAMILY SIZES ===")
from collections import defaultdict

extra_words = ['enlist', 'silent', 'tinsel', 'crate', 'trace', 'react', 'cream', 'study', 'dusty', 'stop']

seen_words = set()
for a, b in original_pairs:
    seen_words.add(a)
    seen_words.add(b)
for w in extra_words:
    seen_words.add(w)

fp_to_words = defaultdict(set)
for word in seen_words:
    fp = fingerprint(word)
    fp_to_words[fp].add(word)

families = {fp: words for fp, words in fp_to_words.items() if len(words) >= 2}
print(f"Families with 2+ members ({len(families)}):")
for fp, words in sorted(families.items(), key=lambda x: -len(x[1])):
    print(f"  fp='{fp}': {sorted(words)} (size={len(words)})")
print(f"Max family size: {max(len(w) for w in families.values())}")
