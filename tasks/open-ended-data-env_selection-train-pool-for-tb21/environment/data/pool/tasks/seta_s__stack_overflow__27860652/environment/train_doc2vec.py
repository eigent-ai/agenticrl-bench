#!/usr/bin/env python3
"""Train Doc2Vec model on preprocessed product documents."""

import pickle
import sys

import yaml
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument


def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    preprocessed_file = config["data"]["preprocessed_file"]
    d2v_config = config["doc2vec"]

    print(f"Loading preprocessed data from {preprocessed_file}...")
    try:
        with open(preprocessed_file, "rb") as f:
            df = pickle.load(f)
    except FileNotFoundError:
        print(f"Error: Preprocessed file not found: {preprocessed_file}", file=sys.stderr)
        print("Run preprocess.py first.", file=sys.stderr)
        sys.exit(1)

    documents = []
    for idx, row in df.iterrows():
        doc = TaggedDocument(words=row["tokens"], tags=[str(row["id"])])
        documents.append(doc)

    print(f"Training Doc2Vec on {len(documents)} documents...")

    model = Doc2Vec(
        documents=documents,
        vector_size=d2v_config["vector_size"],
        window=d2v_config["window"],
        min_count=d2v_config["min_count"],
        dm=d2v_config["dm"],
        dbow_words=d2v_config["dbow_words"],
        epochs=d2v_config["epochs"],
        seed=d2v_config["seed"],
        workers=d2v_config["workers"],
    )

    model_path = d2v_config["model_path"]
    model.save(model_path)
    print(f"Doc2Vec model saved to {model_path}")
    print(f"Document vectors: {len(model.dv)}")
    if hasattr(model, 'wv') and len(model.wv) > 0:
        print(f"Word vectors: {len(model.wv)}")
    else:
        print("Note: No word vectors trained in this configuration")


if __name__ == "__main__":
    main()
