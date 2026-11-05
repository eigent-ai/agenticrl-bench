#!/usr/bin/env python3
"""Train Word2Vec model on preprocessed product tokens."""

import pickle
import sys

import yaml
from gensim.models import Word2Vec


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    preprocessed_file = config["data"]["preprocessed_file"]
    w2v_config = config["word2vec"]

    print(f"Loading preprocessed data from {preprocessed_file}...")
    try:
        with open(preprocessed_file, "rb") as f:
            df = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: Preprocessed file not found: {preprocessed_file}", file=sys.stderr)
        print("Run preprocess.py first.", file=sys.stderr)
        sys.exit(1)

    sentences = df["tokens"].tolist()
    print(f"Training Word2Vec on {len(sentences)} documents...")

    model = Word2Vec(
        sentences=sentences,
        vector_size=w2v_config["vector_size"],
        window=w2v_config["window"],
        min_count=w2v_config["min_count"],
        sg=0,
        negative=w2v_config["negative"],
        hs=w2v_config["hs"],
        epochs=w2v_config["epochs"],
        seed=w2v_config["seed"],
        workers=w2v_config["workers"],
    )

    model_path = w2v_config["model_path"]
    model.save(model_path)
    print(f"Word2Vec model saved to {model_path}")
    print(f"Vocabulary size: {len(model.wv)}")


if __name__ == "__main__":
    main()
