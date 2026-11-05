import math


def compute_step(state, param_value, step_num):
    """Compute the next simulation state deterministically."""
    return state * (1 - param_value * 0.01) + math.sin(step_num * param_value) * 0.1


def format_row(step, state):
    """Format a CSV row for the results file."""
    return f"{step},{state:.10f}"
