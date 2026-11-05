import pandas as pd

df = pd.read_csv("/tmp/train_v2_drcat_02.csv")
df = df.drop_duplicates(subset=['text']).reset_index(drop=True)
df = df[['text', 'label', 'prompt_name', 'source']]

# Stratified subsample of ~8000 rows
samples = []
for label_val, group in df.groupby('label'):
    n = min(len(group), int(8000 * len(group) / len(df)))
    samples.append(group.sample(n=n, random_state=42))
sample = pd.concat(samples, ignore_index=True)
sample = sample.sample(frac=1, random_state=42).reset_index(drop=True)
sample.to_csv("/data/essays.csv", index=False)
print(f"Created essays.csv with {len(sample)} rows")
print(f"Columns: {list(sample.columns)}")
print(f"Label distribution:\n{sample['label'].value_counts()}")
