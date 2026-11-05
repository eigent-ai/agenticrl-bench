def fixed_point(f, start, tolerance=1e-9, max_iter=10000):
    """Find x such that f(x) == x within tolerance."""
    x = float(start)
    for _ in range(max_iter):
        next_x = f(x)
        if abs(next_x - x) < tolerance:
            return next_x
        x = next_x
    raise RuntimeError(
        f"fixed_point did not converge after {max_iter} iterations "
        f"(last two values: {x:.6f}, {next_x:.6f})"
    )


def sqrt_via_fixed_point(n):
    """Compute sqrt(n) using fixed-point iteration of f(x) = n/x."""
    if n < 0:
        raise ValueError("sqrt undefined for negative numbers")
    return fixed_point(lambda x: n / x, 1.0)


def cube_root_via_fixed_point(n):
    """Compute cube root of n using f(x) = n / x**2."""
    return fixed_point(lambda x: n / (x * x), 1.0 if n >= 0 else -1.0)
