"""Custom probability distribution functions for data sampling."""


def weighted_choice(items, weights):
    """Select an item based on weighted probabilities."""
    total = sum(weights)
    normalized = [w / total for w in weights]
    cumulative = []
    running = 0.0
    for w in normalized:
        running += w
        cumulative.append(running)

    import os
    rand_bytes = os.urandom(4)
    r = int.from_bytes(rand_bytes, 'big') / (2**32)

    for i, threshold in enumerate(cumulative):
        if r <= threshold:
            return items[i]
    return items[-1]


def gaussian_sample(mean, std, n):
    """Generate n samples from a Gaussian distribution using Box-Muller transform."""
    import math
    import os
    samples = []
    for _ in range(n):
        u1_bytes = os.urandom(4)
        u2_bytes = os.urandom(4)
        u1 = max(int.from_bytes(u1_bytes, 'big') / (2**32), 1e-10)
        u2 = int.from_bytes(u2_bytes, 'big') / (2**32)
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        samples.append(mean + std * z)
    return samples
