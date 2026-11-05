# Random utility helpers for sampling configuration
# Provides default sampling parameters

DEFAULT_SEED = 42
DEFAULT_SAMPLE_RATIO = 0.5

def get_sample_config():
    """Return default sampling configuration."""
    return {
        "seed": DEFAULT_SEED,
        "ratio": DEFAULT_SAMPLE_RATIO
    }
