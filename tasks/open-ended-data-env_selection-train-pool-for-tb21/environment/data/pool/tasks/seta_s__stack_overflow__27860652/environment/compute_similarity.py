#!/usr/bin/env python3
"""Compute pairwise document similarity using Doc2Vec vectors."""

import pickle
import sys

import numpy as np
import yaml
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    preprocessed_file = config["data"]["preprocessed_file"]
    d2v_model_path = config["doc2vec"]["model_path"]

    print(f"Loading Doc2Vec model from {d2v_model_path}...")
    try:
        model = Doc2Vec.load(d2v_model_path)
    except FileNotFoundError:
        print(f"Error: Doc2Vec model not found: {d2v_model_path}", file=sys.stderr)
        print("Run train_doc2vec.py first.", file=sys.stderr)
        sys.exit(1)

    print(f"Loading preprocessed data from {preprocessed_file}...")
    with open(preprocessed_file, "rb") as f:
        df = pickle.load(f)

    product_ids = df["id"].tolist()
    doc_vectors = []

    for pid in product_ids:
        vec = model.dv[str(pid)]
        doc_vectors.append(vec)

    doc_matrix = np.array(doc_vectors)
    print(f"Computing pairwise similarity for {len(product_ids)} products...")

    cos_sim_matrix = cosine_similarity(doc_matrix)

    similarity = 1.0 - cos_sim_matrix

    output_path = config["data"]["preprocessed_file"].replace("preprocessed.pkl", "similarity_matrix.npy")
    np.save(output_path, similarity)

    with open(output_path.replace(".npy", "_ids.pkl"), "wb") as f:
        pickle.dump(product_ids, f)

    print(f"Similarity matrix saved to {output_path}")
    print(f"Matrix shape: {similarity.shape}")


if __name__ == "__main__":
    main()
