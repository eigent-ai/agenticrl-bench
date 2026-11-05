import pandas as pd
from sklearn.preprocessing import StandardScaler


def scale_features(input_path, output_path):
    df = pd.read_csv(input_path)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    result = pd.DataFrame(scaled, columns=df.columns)
    result.to_csv(output_path, index=False)
    return result
