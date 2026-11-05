#!/usr/bin/env python3
"""Fuzzy text search module using difflib.SequenceMatcher."""

from difflib import SequenceMatcher


def fuzzy_search(phrase, text, min_score=0.75):
    """Search for a phrase in text using fuzzy matching.

    Returns a list of match dicts with line number, matched text, and score.
    """
    results = []
    lines = text.split('\n')

    for line_num, line in enumerate(lines, start=1):
        words = line.split()
        if not words:
            continue

        for word in words:
            score = SequenceMatcher(None, phrase.lower(), word.lower()).ratio()
            if score >= min_score:
                results.append({
                    "line": line_num,
                    "matched_text": word,
                    "score": round(score, 4)
                })

    return results
