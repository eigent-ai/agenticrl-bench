from sklearn.model_selection import KFold


def get_cv_splitter(config):
    """Create a cross-validation splitter based on configuration."""
    cv_config = config["cross_validation"]
    n_splits = cv_config["n_splits"]

    splitter = KFold(n_splits=n_splits)

    return splitter


def get_total_folds(config):
    """Calculate total number of folds for the CV strategy."""
    cv_config = config["cross_validation"]
    total = cv_config["n_splits"] + cv_config["n_repeats"]
    return total
