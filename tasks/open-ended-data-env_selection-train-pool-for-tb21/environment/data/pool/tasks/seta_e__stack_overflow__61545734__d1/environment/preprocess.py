import pandas as pd
import sys


def parse_sparse_features(feature_rows):
    """
    Parse sparse feature vectors in 'index:value' format into a dense DataFrame.
    Missing indices are filled with zero.
    Columns are named f_XXXX where XXXX is the zero-padded feature index.
    """
    # Collect all feature indices present in any row
    all_indices = sorted(set(
        item.strip().split(':')[0]
        for row in feature_rows
        for item in row
    ))

    data = {idx: [] for idx in all_indices}

    for row in feature_rows:
        seen = set()
        for item in row:
            idx, val = item.strip().split(':')
            data[idx].append(float(val))
            seen.add(idx)
        for idx in all_indices:
            if idx not in seen:
                data[idx].append(None)

    df = pd.DataFrame(data)
    df.columns = [f"f_{col}" for col in df.columns]
    return df


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else 'data/train.tsv'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'data/output.csv'

    df_raw = pd.read_csv(input_path, sep='\t')
    feature_rows = [row.split() for row in df_raw['features']]

    df_out = parse_sparse_features(feature_rows)
    df_out.to_csv(output_path, index=False)
    print(f"Saved {len(df_out)} rows x {len(df_out.columns)} columns to {output_path}")


if __name__ == '__main__':
    main()
