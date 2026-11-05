#!/usr/bin/env python3
import os
import yaml
from augment import augment_audio
from manifest_gen import generate_manifest


def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    input_dir = config["input_dir"]
    output_dir = config["output_dir"]

    os.makedirs(output_dir, exist_ok=True)

    print(f"Processing audio files from {input_dir}...")
    all_results = []
    for filename in sorted(os.listdir(input_dir)):
        if not filename.lower().endswith(".wav"):
            continue
        audio_path = os.path.join(input_dir, filename)
        print(f"  Augmenting {filename}...")
        results = augment_audio(audio_path, config)
        all_results.extend(results)

    print(f"Generated {len(all_results)} augmented audio files in {output_dir}")

    print("Generating manifest...")
    entries = generate_manifest(config)
    print(f"Manifest written with {len(entries)} entries to {config['manifest_path']}")

    print("Pipeline complete!")


if __name__ == "__main__":
    main()
