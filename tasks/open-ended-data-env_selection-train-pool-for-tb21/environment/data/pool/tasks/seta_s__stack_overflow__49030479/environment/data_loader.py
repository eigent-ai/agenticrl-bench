import pandas as pd
from sklearn.model_selection import train_test_split


def load_data(data_path="data/dataset.csv", test_size=0.2, random_state=42):
    """Load dataset from CSV and split into train/test sets."""
    df = pd.read_csv(data_path)
    X = df.drop(columns=["target"])
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test
