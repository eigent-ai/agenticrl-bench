"""Load measurement and price datasets."""

import pandas as pd

measurements_df = pd.read_csv("measurements.csv")
prices_df = pd.read_csv("prices.csv")
