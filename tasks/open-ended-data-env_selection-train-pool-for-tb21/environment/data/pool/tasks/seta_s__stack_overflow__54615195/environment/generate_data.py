import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os

rng = np.random.default_rng(42)
n = 100_000

device_types = ['mobile', 'desktop', 'tablet', 'tv', 'wearable']
regions = ['US', 'EU', 'APAC', 'LATAM', 'MEA', 'CA', 'AU', 'IN', 'JP', 'BR']

df = pd.DataFrame({
    'session_id':  np.arange(n),
    'user_id':     rng.integers(0, 10000, n),
    'device_type': rng.choice(device_types, n),
    'region':      rng.choice(regions, n),
    'duration_sec': rng.uniform(10, 3600, n).astype('float32'),
    'page_views':   rng.integers(1, 51, n),
    'clicks':       rng.integers(0, 21, n),
    'conversions':  rng.integers(0, 6, n),
    'revenue':      rng.uniform(0, 500, n).astype('float32'),
    'bounce':       rng.integers(0, 2, n),
})

os.makedirs('/opt/pipeline/data', exist_ok=True)
table = pa.Table.from_pandas(df, preserve_index=False)
pq.write_to_dataset(table, '/opt/pipeline/data/sessions.parquet',
                    partition_cols=None,
                    use_legacy_dataset=False)
print(f"Generated {n} rows → /opt/pipeline/data/sessions.parquet")
