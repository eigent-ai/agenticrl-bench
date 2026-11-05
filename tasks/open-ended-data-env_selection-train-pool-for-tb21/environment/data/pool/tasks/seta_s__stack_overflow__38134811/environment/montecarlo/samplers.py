import numpy as np


class RandomSampler:
    """Random number sampler with configurable seed and distribution methods."""

    def __init__(self, seed=None):
        self.seed = seed
        self.rng = np.random.default_rng()

    def discrete_uniform(self, low, high, n):
        """Generate n discrete uniform random integers in [low, high).

        Uses the floor-based method: floor((high - low) * U + low)
        where U ~ Uniform(0, 1).
        """
        raw = self.rng.random(n)
        samples = np.floor((high - low + 1) * raw + low).astype(int)
        return samples

    def sample_with_replacement(self, population, n):
        """Draw n samples from population with replacement."""
        indices = self.discrete_uniform(0, len(population), n)
        return [population[i] for i in indices]
