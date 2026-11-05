import numpy as np

np.random.seed(42)
data = np.random.randn(10037, 4) * 2.5
np.savetxt(
    "data/sensors.csv",
    data,
    delimiter=",",
    fmt="%.8f",
    header="s0,s1,s2,s3",
    comments="",
)
print("Generated data/sensors.csv: 10037 rows x 4 columns")
