import pandas as pd
df = pd.read_csv("/tmp/raw_uber_data.csv")
df.columns = [c.replace('*', '') for c in df.columns]
df.to_csv("/data/uber_drives.csv", index=False)
