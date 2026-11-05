import pickle
import pandas as pd

# Load session 1
with open('session1_history.pkl', 'rb') as f:
    h1 = pickle.load(f)

# Load session 2
with open('session2_history.pkl', 'rb') as f:
    h2 = pickle.load(f)

# Load session 3 from CSV (as saved by Keras CSVLogger)
df3 = pd.read_csv('session3_history.csv')
h3 = df3.to_dict(orient='list')

# Merge all sessions into combined history
combined = {}
combined.update(h1)
combined.update(h2)
combined.update(h3)

with open('combined_history.pkl', 'wb') as f:
    pickle.dump(combined, f)

print("Combined history saved to combined_history.pkl")
