#!/usr/bin/env python3
"""Multilingual text-cleaning pipeline.

Reads a messy multilingual CSV dataset, cleans each text field by removing
non-English words and foreign stop words, drops rows with non-ASCII titles,
and writes a cleaned CSV and JSON summary report.
"""

import os
import json
import yaml
import pandas as pd
import nltk
from nltk.corpus import words, stopwords

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_english_words():
    return set(w.lower() for w in words.words('english'))

def get_stopwords_for_languages(languages):
    all_stops = set()
    for lang in languages:
        try:
            all_stops.update(stopwords.words(lang))
        except OSError:
            print(f"Warning: stopwords for '{lang}' not found, skipping.")
    return all_stops

def is_ascii_row(row):
    return str(row).isascii()

def clean_body(text, english_words, foreign_stops, preserve_non_alpha):
    tokens = text.split()
    cleaned = []
    foreign_removed = 0
    for token in tokens:
        lower_tok = token.lower()
        if not token.isalpha():
            if preserve_non_alpha:
                cleaned.append(token)
            continue
        if lower_tok in foreign_stops:
            foreign_removed += 1
            continue
        if lower_tok in english_words:
            cleaned.append(token)
        else:
            foreign_removed += 1
    return " ".join(cleaned), foreign_removed

def main():
    config = load_config()
    input_file = config["input_file"]
    output_file = config["output_file"]
    report_file = config["report_file"]
    stop_languages = config.get("stopword_languages", [])
    preserve_non_alpha = config.get("preserve_non_alpha", True)

    df = pd.read_csv(input_file)
    total_input_rows = len(df)

    english_words = get_english_words()
    foreign_stops = get_stopwords_for_languages(stop_languages)

    ascii_mask = df.apply(is_ascii_row, axis=1)
    dropped_non_ascii = (~ascii_mask).sum()
    df = df[ascii_mask].copy()

    cleaned_bodies = []
    total_foreign_removed = 0
    empty_indices = []

    for idx, row in df.iterrows():
        cleaned_text, removed = clean_body(
            str(row["body"]), english_words, foreign_stops, preserve_non_alpha
        )
        total_foreign_removed += removed
        if cleaned_text.strip() == "":
            empty_indices.append(idx)
            cleaned_bodies.append(cleaned_text)
        else:
            cleaned_bodies.append(cleaned_text)

    df["body"] = cleaned_bodies
    df = df.drop(empty_indices)
    dropped_empty = len(empty_indices)
    output_rows = len(df)

    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
    df.to_csv(output_file, index=False)

    avg_foreign = total_foreign_removed / total_input_rows if total_input_rows > 0 else 0.0

    report = {
        "total_input_rows": total_input_rows,
        "dropped_non_ascii_rows": int(dropped_non_ascii),
        "dropped_empty_body_rows": dropped_empty,
        "output_rows": output_rows,
        "per_row_foreign_words_removed": round(avg_foreign, 4)
    }

    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Pipeline complete. {output_rows} rows written to {output_file}")
    print(f"Report written to {report_file}")

if __name__ == "__main__":
    main()
