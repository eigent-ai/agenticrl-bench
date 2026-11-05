"""Data preprocessing module with ColumnTransformer pipeline."""
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_feature_config(config_path):
    """Load feature configuration from YAML file."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config['categorical_features'], config['numeric_features']


def build_preprocessor(config_path):
    """Build the ColumnTransformer preprocessing pipeline."""
    categorical_features, numeric_features = load_feature_config(config_path)

    preprocessor = ColumnTransformer(
        transformers=[
            ('encoder', OneHotEncoder(sparse_output=False, handle_unknown='ignore'),
             categorical_features),
            ('scaler', StandardScaler(), numeric_features),
        ],
        remainder='drop'
    )

    return preprocessor, categorical_features, numeric_features
