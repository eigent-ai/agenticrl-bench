"""
Design a CSV with exactly:
- 20 unique pairs after dedup
- 12 anagram pairs
- 8 non-anagram pairs
- 6 anagram families (2+ members) when combined with extra_words.txt
- max family size = 4

extra_words.txt = 10 words
"""
from collections import defaultdict

def fingerprint(word):
    return ''.join(sorted(c.lower() for c in word if c != ' '))

# Let's design the data carefully.
#
# The key insight is:
# - 12 anagram pairs from 20 unique pairs
# - 8 non-anagram pairs
# - Combined with extra_words.txt, exactly 6 families with 2+ members
# - max family size = 4
#
# I'll design extra_words to carefully control family sizes.

# 12 anagram pairs to use:
anagram_pairs = [
    ('listen', 'silent'),     # fp=eilnst
    ('enlist', 'tinsel'),     # fp=eilnst
    ('dusty', 'study'),       # fp=dstuy
    ('dog', 'god'),           # fp=dgo
    ('cat', 'act'),           # fp=act
    ('arc', 'car'),           # fp=acr
    ('race', 'care'),         # fp=acer
    ('post', 'stop'),         # fp=opst
    ('tops', 'pots'),         # fp=opst
    ('evil', 'vile'),         # fp=eilv
    ('veil', 'live'),         # fp=eilv
    ('Astronomer', 'Moon starer'),  # fp=aemnoorrst
]

# 8 non-anagram pairs:
non_anagram_pairs = [
    ('night', 'magic'),     # ghint vs acgim
    ('stressed', 'dessert'),  # deerssst vs deersst (different!)
    ('hello', 'world'),     # ehllo vs dlorw
    ('fast', 'slow'),       # afst vs losw
    ('black', 'white'),     # abckl vs ehitw
    ('apple', 'orange'),    # aelpp vs aaegnor
    ('fire', 'water'),      # efir vs aertw
    ('stone', 'river'),     # enost vs eirrv
]

# Verify
print("=== VERIFYING PAIRS ===")
all_ok = True
for a, b in anagram_pairs:
    fa = fingerprint(a)
    fb = fingerprint(b)
    if fa != fb:
        print(f"FAIL (should be anagram): '{a}'/'{b}' fp_a='{fa}' fp_b='{fb}'")
        all_ok = False
    else:
        print(f"  ANA OK: '{a}'/'{b}'")

for a, b in non_anagram_pairs:
    fa = fingerprint(a)
    fb = fingerprint(b)
    if fa == fb:
        print(f"FAIL (should be non-anagram): '{a}'/'{b}' fp='{fa}'")
        all_ok = False
    else:
        print(f"  NON OK: '{a}'/'{b}'")

print(f"\nAll OK: {all_ok}")
print(f"Unique pairs: {len(anagram_pairs) + len(non_anagram_pairs)}")

# Now figure out extra_words.txt to get exactly 6 families with 2+ members
# and max size = 4
#
# From 20 unique pairs, the words seen (from CSV) are:
csv_words = set()
for a, b in anagram_pairs + non_anagram_pairs:
    csv_words.add(a)
    csv_words.add(b)

# Compute families from CSV words only
csv_fp = defaultdict(set)
for w in csv_words:
    csv_fp[fingerprint(w)].add(w)

print("\n=== CSV-ONLY FAMILIES ===")
for fp_val, words in sorted(csv_fp.items(), key=lambda x: -len(x[1])):
    if len(words) >= 2:
        print(f"  fp='{fp_val}': {sorted(words)} (size={len(words)})")

# Now design extra_words.txt to achieve:
# - exactly 6 families with 2+ members
# - max family size = 4
#
# Current CSV-only families with 2+ members:
csv_families = {fp_val: words for fp_val, words in csv_fp.items() if len(words) >= 2}
print(f"\nCSV-only families with 2+: {len(csv_families)}")

# If we want 6 total families with 2+, we need to:
# 1. Either grow existing families or add new ones via extra_words.txt
# 2. Keep max size at 4

# Let's add extra words:
# - crate/trace/react have fp=acert (not in CSV) → new family of 3
# - inlets has fp=eilnst (same as listen/silent/enlist/tinsel) → grows that family
# BUT we don't want max size > 4, so be careful with eilnst family (already has 4 from CSV: listen, silent, enlist, tinsel)
#   + inlets would make 5 - too big!
#
# eilnst family from CSV: listen, silent, enlist, tinsel = 4 words → max 4 is already met
# Let's NOT add inlets to extra_words.

# Let's design extra_words to get exactly these 6 families:
# 1. eilnst: listen, silent, enlist, tinsel (from CSV) → size 4 - this is our max
# 2. opst: post, stop, tops, pots (from CSV) → size 4
# 3. eilv: evil, vile, veil, live (from CSV) → size 4
# That's already 3 families of size 4! max would be 4. Good.
# 4. act: cat, act (from CSV) → + tac from extra = 3 words
# 5. acer: race, care (from CSV) → + acre from extra = 3 words
# 6. dgo: dog, god (from CSV) → size 2 (stays at 2)
#
# But wait: arc/car = acr (size 2), dusty/study = dstuy (size 2),
# Astronomer/Moon starer = aemnoorrst (size 2)
# These would be extra families!
#
# We need EXACTLY 6 families with 2+ members from CSV+extra combined.
# CSV already gives many 2-member families. Let me count them:

for fp_val, words in sorted(csv_fp.items(), key=lambda x: -len(x[1])):
    if len(words) >= 2:
        print(f"  Family fp='{fp_val}': {sorted(words)} size={len(words)}")
