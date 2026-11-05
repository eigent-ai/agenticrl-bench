#!/usr/bin/env python3
"""Generate product recommendations from similarity matrix and models."""

import json
import pickle
import sys

import numpy as np
import pandas as pd
import yaml
from gensim.models import Doc2Vec, Word2Vec


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def get_category_keywords(model_wv, category_terms):
    """Get average vector for category keywords using word vectors."""
    vectors = []
    for term in category_terms:
        try:
            vectors.append(model_wv[term])
        except KeyError:
            continue
    if vectors:
        return np.mean(vectors, axis=0)
    return None


def main():
    config = load_config()

    preprocessed_file = config["data"]["preprocessed_file"]
    w2v_model_path = config["word2vec"]["model_path"]
    d2v_model_path = config["doc2vec"]["model_path"]
    top_n = config["similarity"]["top_n"]
    output_file = config["similarity"]["output_file"]

    print("Loading models...")
    try:
        w2v_model = Word2Vec.load(w2v_model_path)
    except FileNotFoundError:
        print(f"Error: Word2Vec model not found: {w2v_model_path}", file=sys.stderr)
        sys.exit(1)

    try:
        d2v_model = Doc2Vec.load(d2v_model_path)
    except FileNotFoundError:
        print(f"Error: Doc2Vec model not found: {d2v_model_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading preprocessed data from {preprocessed_file}...")
    with open(preprocessed_file, "rb") as f:
        df = pickle.load(f)

    similarity_path = preprocessed_file.replace("preprocessed.pkl", "similarity_matrix.npy")
    ids_path = similarity_path.replace(".npy", "_ids.pkl")

    print(f"Loading similarity matrix...")
    similarity_matrix = np.load(similarity_path)
    with open(ids_path, "rb") as f:
        product_ids = pickle.load(f)

    id_to_idx = {pid: idx for idx, pid in enumerate(product_ids)}
    id_to_row = {row["id"]: row for _, row in df.iterrows()}

    category_terms = {
        "Electronics": ["digital", "wireless", "smart", "electronic", "camera", "bluetooth"],
        "Kitchen": ["cooking", "kitchen", "steel", "food", "heat", "electric"],
        "Sports": ["fitness", "training", "sport", "exercise", "outdoor", "running"],
        "Books": ["programming", "guide", "design", "learning", "development", "software"],
        "Clothing": ["cotton", "waterproof", "lightweight", "comfortable", "fit", "breathable"],
    }

    category_vectors = {}
    for cat, terms in category_terms.items():
        vec = get_category_keywords(d2v_model.wv, terms)
        if vec is not None:
            category_vectors[cat] = vec

    recommendations = {}
    for pid in product_ids:
        idx = id_to_idx[pid]
        row = id_to_row[pid]

        sim_scores = similarity_matrix[idx]
        scored_indices = [(i, sim_scores[i]) for i in range(len(product_ids)) if i != idx]
        scored_indices.sort(key=lambda x: x[1], reverse=True)

        top_recs = []
        for rec_idx, score in scored_indices[:top_n]:
            rec_pid = product_ids[rec_idx]
            rec_row = id_to_row[rec_pid]
            top_recs.append({
                "product_id": int(rec_pid),
                "name": rec_row["name"],
                "category": rec_row["category"],
                "similarity_score": round(float(score), 4),
            })

        recommendations[str(pid)] = {
            "product_id": int(pid),
            "name": row["name"],
            "category": row["category"],
            "recommendations": top_recs,
        }

    with open(output_file, "w") as f:
        json.dump(recommendations, f, indent=2)

    print(f"Recommendations saved to {output_file}")
    print(f"Total products with recommendations: {len(recommendations)}")


if __name__ == "__main__":
    main()
