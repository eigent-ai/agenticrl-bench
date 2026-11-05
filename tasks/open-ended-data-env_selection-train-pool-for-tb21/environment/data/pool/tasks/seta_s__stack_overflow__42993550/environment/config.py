# Configuration for ML pipeline

PARAM_GRID = {
    'xgb__n_estimators': [50, 100],
    'xgb__max_depth': [3, 5],
    'pca__n_components': [3, 5, 7],
}

SCORING = 'mean_absolute_error'

CV_SPLITS = 3
EARLY_STOPPING_ROUNDS = 10
TEST_SIZE = 0.2
RANDOM_STATE = 42
