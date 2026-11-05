import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
specs = [("user_0", 45), ("user_1", 62), ("user_2", 38), ("user_3", 71), ("user_4", 29)]
for name, n in specs:
    feats = rng.standard_normal((n, 5))
    tgts  = rng.integers(0, 2, size=n)
    cols  = {f"feat_{i}": feats[:, i] for i in range(5)}
    cols["target"] = tgts
    pd.DataFrame(cols).to_csv(f"/workspace/data/{name}.csv", index=False)
print("Data generated successfully.")
