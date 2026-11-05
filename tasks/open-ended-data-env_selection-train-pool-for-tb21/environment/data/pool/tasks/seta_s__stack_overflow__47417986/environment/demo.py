"""
Demo script exercising the full KDE sampling pipeline.

Generates synthetic normal and log-normal data, fits KDEs,
produces Monte Carlo samples via inverse CDF, and saves results.
"""

import os
import numpy as np
from kde_sampler import (
    fit_kde,
    generate_samples,
    fit_lognormal_kde,
    generate_samples_lognormal,
)


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Normal data: loc=5, scale=2
    rng_normal = np.random.default_rng(42)
    normal_data = rng_normal.normal(loc=5, scale=2, size=5000)

    kde_normal = fit_kde(normal_data)
    normal_samples = generate_samples(kde_normal, normal_data, 1000, seed=99)

    np.save(os.path.join(output_dir, "normal_samples.npy"), normal_samples)
    print(f"Normal samples: mean={normal_samples.mean():.3f}, "
          f"std={normal_samples.std():.3f}")

    # Log-normal data: mu=2, sigma=0.5
    rng_ln = np.random.default_rng(43)
    ln_data = rng_ln.lognormal(mean=2, sigma=0.5, size=5000)

    kde_ln, log_ln_data = fit_lognormal_kde(ln_data)
    ln_samples = generate_samples_lognormal(kde_ln, log_ln_data, 1000, seed=99)

    np.save(os.path.join(output_dir, "lognormal_samples.npy"), ln_samples)
    print(f"Log-normal samples: mean={ln_samples.mean():.3f}, "
          f"std={ln_samples.std():.3f}")

    print("Demo complete. Output written to", output_dir)


if __name__ == "__main__":
    main()
