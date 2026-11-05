import sqlite3
import random

random.seed(42)

conn = sqlite3.connect("data/samples.db")
conn.execute(
    "CREATE TABLE samples (id INTEGER PRIMARY KEY, text TEXT, label INTEGER)"
)

distribution = [(0, 800), (1, 2400), (2, 400), (3, 1600)]
rows = []
for label, count in distribution:
    for i in range(count):
        rows.append((f"sample_{label}_{i}", label))

random.shuffle(rows)
conn.executemany("INSERT INTO samples (text, label) VALUES (?, ?)", rows)
conn.commit()
conn.close()
print("Database created.")
