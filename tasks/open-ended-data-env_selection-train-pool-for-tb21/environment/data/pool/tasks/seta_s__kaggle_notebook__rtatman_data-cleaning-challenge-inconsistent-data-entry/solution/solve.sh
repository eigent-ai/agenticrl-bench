#!/bin/bash

cat << 'PYSCRIPT' > /home/user/data/clean_pipeline.py
#!/usr/bin/env python3
"""Data cleaning pipeline for Pakistan incidents dataset."""

import json
import os
import chardet
import pandas as pd
from thefuzz import fuzz


def detect_encoding(filepath):
    """Detect file encoding using chardet."""
    with open(filepath, "rb") as f:
        raw = f.read()
    result = chardet.detect(raw)
    return result["encoding"]


def fuzzy_merge_values(values, threshold=90):
    """Group similar values using fuzzy matching.
    Returns a mapping from original value to canonical form."""
    mapping = {}
    canonical = []

    for val in sorted(values):
        matched = False
        for canon in canonical:
            if fuzz.ratio(val, canon) >= threshold:
                mapping[val] = canon
                matched = True
                break
        if not matched:
            canonical.append(val)
            mapping[val] = val

    return mapping


def clean_text_column(series, fuzzy_threshold=None):
    """Clean a text column: strip whitespace, title case.
    Optionally apply fuzzy matching."""
    cleaned = series.copy()

    # Strip whitespace
    cleaned = cleaned.str.strip()

    # Replace whitespace-only strings with NaN
    cleaned = cleaned.replace(r'^\s*$', pd.NA, regex=True)

    # Lowercase first for dedup, then title case
    mask = cleaned.notna()
    lower_vals = cleaned[mask].str.lower().str.strip()

    # Build mapping from lowercase to title case canonical
    unique_lower = lower_vals.unique()
    lower_to_title = {v: v.title() for v in unique_lower}

    # Apply
    cleaned[mask] = lower_vals.map(lower_to_title)

    if fuzzy_threshold is not None:
        unique_after = cleaned.dropna().unique().tolist()
        fuzzy_map = fuzzy_merge_values(unique_after, threshold=fuzzy_threshold)
        cleaned[mask] = cleaned[mask].map(fuzzy_map)

    return cleaned


def clean_column_with_explicit_map(series, explicit_map):
    """Clean a text column with explicit value mappings after basic normalization."""
    cleaned = series.copy()
    cleaned = cleaned.str.strip()
    cleaned = cleaned.replace(r'^\s*$', pd.NA, regex=True)

    mask = cleaned.notna()
    lower_vals = cleaned[mask].str.lower().str.strip()
    unique_lower = lower_vals.unique()
    lower_to_title = {v: v.title() for v in unique_lower}
    cleaned[mask] = lower_vals.map(lower_to_title)

    # Apply explicit mappings
    cleaned = cleaned.replace(explicit_map)

    return cleaned


def clean_dataset(input_path, output_path, encoding):
    """Clean a single dataset file."""
    df = pd.read_csv(input_path, encoding=encoding)
    original = df.copy()

    audit_columns = {}
    total_cells_modified = 0

    # Province: explicit mapping for known variants
    col = "Province"
    before_unique = df[col].dropna().nunique()
    province_map = {
        "Baluchistan": "Balochistan",
        "Fata": "FATA",
    }
    df[col] = df[col].str.strip()
    df[col] = df[col].replace(province_map)
    after_unique = df[col].dropna().nunique()
    value_mapping = {}
    for old_val in original[col].dropna().unique():
        new_val = old_val.strip()
        new_val = province_map.get(new_val, new_val)
        if old_val != new_val:
            value_mapping[old_val] = new_val
    cells_changed = (original[col].fillna("__NA__") != df[col].fillna("__NA__")).sum()
    total_cells_modified += cells_changed
    audit_columns[col] = {
        "unique_before": int(before_unique),
        "unique_after": int(after_unique),
        "value_mapping": value_mapping,
    }

    # City: lowercase + strip + fuzzy matching
    col = "City"
    before_unique = df[col].dropna().nunique()
    df[col] = clean_text_column(df[col], fuzzy_threshold=90)
    after_unique = df[col].dropna().nunique()
    value_mapping = {}
    for i in range(len(original)):
        old_val = original[col].iloc[i]
        new_val = df[col].iloc[i]
        if pd.notna(old_val) and pd.notna(new_val) and old_val != new_val:
            value_mapping[old_val] = new_val
    cells_changed = 0
    for i in range(len(original)):
        o = original[col].iloc[i]
        n = df[col].iloc[i]
        if (pd.isna(o) != pd.isna(n)) or (pd.notna(o) and pd.notna(n) and o != n):
            cells_changed += 1
    total_cells_modified += cells_changed
    audit_columns[col] = {
        "unique_before": int(before_unique),
        "unique_after": int(after_unique),
        "value_mapping": value_mapping,
    }

    # Open/Closed Space
    col = "Open/Closed Space"
    before_unique = df[col].dropna().nunique()
    df[col] = clean_text_column(df[col])
    after_unique = df[col].dropna().nunique()
    value_mapping = {}
    for i in range(len(original)):
        old_val = original[col].iloc[i]
        new_val = df[col].iloc[i]
        if pd.notna(old_val) and pd.notna(new_val) and old_val != new_val:
            value_mapping[old_val] = new_val
    cells_changed = 0
    for i in range(len(original)):
        o = original[col].iloc[i]
        n = df[col].iloc[i]
        if (pd.isna(o) != pd.isna(n)) or (pd.notna(o) and pd.notna(n) and o != n):
            cells_changed += 1
    total_cells_modified += cells_changed
    audit_columns[col] = {
        "unique_before": int(before_unique),
        "unique_after": int(after_unique),
        "value_mapping": value_mapping,
    }

    # Target Type
    col = "Target Type"
    before_unique = df[col].dropna().nunique()
    df[col] = clean_text_column(df[col])
    after_unique = df[col].dropna().nunique()
    value_mapping = {}
    for i in range(len(original)):
        old_val = original[col].iloc[i]
        new_val = df[col].iloc[i]
        if pd.notna(old_val) and pd.notna(new_val) and old_val != new_val:
            value_mapping[old_val] = new_val
    cells_changed = 0
    for i in range(len(original)):
        o = original[col].iloc[i]
        n = df[col].iloc[i]
        if (pd.isna(o) != pd.isna(n)) or (pd.notna(o) and pd.notna(n) and o != n):
            cells_changed += 1
    total_cells_modified += cells_changed
    audit_columns[col] = {
        "unique_before": int(before_unique),
        "unique_after": int(after_unique),
        "value_mapping": value_mapping,
    }

    # Targeted Sect if any
    col = "Targeted Sect if any"
    before_unique = df[col].dropna().nunique()
    df[col] = clean_text_column(df[col])
    after_unique = df[col].dropna().nunique()
    value_mapping = {}
    for i in range(len(original)):
        old_val = original[col].iloc[i]
        new_val = df[col].iloc[i]
        if pd.notna(old_val) and pd.notna(new_val) and old_val != new_val:
            value_mapping[old_val] = new_val
    cells_changed = 0
    for i in range(len(original)):
        o = original[col].iloc[i]
        n = df[col].iloc[i]
        if (pd.isna(o) != pd.isna(n)) or (pd.notna(o) and pd.notna(n) and o != n):
            cells_changed += 1
    total_cells_modified += cells_changed
    audit_columns[col] = {
        "unique_before": int(before_unique),
        "unique_after": int(after_unique),
        "value_mapping": value_mapping,
    }

    # Location Sensitivity
    col = "Location Sensitivity"
    before_unique = df[col].dropna().nunique()
    df[col] = clean_text_column(df[col])
    after_unique = df[col].dropna().nunique()
    value_mapping = {}
    for i in range(len(original)):
        old_val = original[col].iloc[i]
        new_val = df[col].iloc[i]
        if pd.notna(old_val) and pd.notna(new_val) and old_val != new_val:
            value_mapping[old_val] = new_val
    cells_changed = 0
    for i in range(len(original)):
        o = original[col].iloc[i]
        n = df[col].iloc[i]
        if (pd.isna(o) != pd.isna(n)) or (pd.notna(o) and pd.notna(n) and o != n):
            cells_changed += 1
    total_cells_modified += cells_changed
    audit_columns[col] = {
        "unique_before": int(before_unique),
        "unique_after": int(after_unique),
        "value_mapping": value_mapping,
    }

    # Location Category
    col = "Location Category"
    before_unique = df[col].dropna().nunique()
    df[col] = clean_text_column(df[col])
    after_unique = df[col].dropna().nunique()
    value_mapping = {}
    for i in range(len(original)):
        old_val = original[col].iloc[i]
        new_val = df[col].iloc[i]
        if pd.notna(old_val) and pd.notna(new_val) and old_val != new_val:
            value_mapping[old_val] = new_val
    cells_changed = 0
    for i in range(len(original)):
        o = original[col].iloc[i]
        n = df[col].iloc[i]
        if (pd.isna(o) != pd.isna(n)) or (pd.notna(o) and pd.notna(n) and o != n):
            cells_changed += 1
    total_cells_modified += cells_changed
    audit_columns[col] = {
        "unique_before": int(before_unique),
        "unique_after": int(after_unique),
        "value_mapping": value_mapping,
    }

    return df, audit_columns, total_cells_modified


def main():
    raw_dir = "/home/user/data/raw"
    cleaned_dir = "/home/user/data/cleaned"
    os.makedirs(cleaned_dir, exist_ok=True)

    # Detect encoding
    input_path = os.path.join(raw_dir, "incidents.csv")
    encoding = detect_encoding(input_path)
    print(f"Detected encoding: {encoding}")

    # Clean main dataset
    df_cleaned, audit_columns, total_cells_modified = clean_dataset(
        input_path,
        os.path.join(cleaned_dir, "incidents_cleaned.csv"),
        encoding,
    )
    df_cleaned.to_csv(
        os.path.join(cleaned_dir, "incidents_cleaned.csv"),
        index=False,
        encoding="utf-8",
    )
    print(f"Cleaned main dataset: {df_cleaned.shape}")
    print(f"City unique: {df_cleaned['City'].dropna().nunique()}")
    print(f"Province unique: {df_cleaned['Province'].dropna().nunique()}")

    # Build audit report
    audit_report = {
        "detected_encoding": encoding,
        "total_cells_modified": int(total_cells_modified),
        "columns": audit_columns,
    }
    with open(os.path.join(cleaned_dir, "audit_report.json"), "w") as f:
        json.dump(audit_report, f, indent=2, default=str)
    print(f"Audit report written. Total cells modified: {total_cells_modified}")

    # Clean V6 dataset
    v6_path = os.path.join(raw_dir, "incidents_v6.csv")
    v6_encoding = detect_encoding(v6_path)
    df_v6_cleaned, _, _ = clean_dataset(
        v6_path,
        os.path.join(cleaned_dir, "incidents_v6_cleaned.csv"),
        v6_encoding,
    )
    df_v6_cleaned.to_csv(
        os.path.join(cleaned_dir, "incidents_v6_cleaned.csv"),
        index=False,
        encoding="utf-8",
    )
    print(f"Cleaned V6 dataset: {df_v6_cleaned.shape}")
    print(f"V6 Province unique: {df_v6_cleaned['Province'].dropna().nunique()}")


if __name__ == "__main__":
    main()
PYSCRIPT

python3 /home/user/data/clean_pipeline.py
