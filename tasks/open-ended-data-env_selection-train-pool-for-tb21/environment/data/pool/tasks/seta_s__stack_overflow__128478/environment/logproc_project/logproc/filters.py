"""Filter utilities for log processing."""


class FilterChain:
    """Chain of filters to apply to log lines."""

    def __init__(self):
        self.filters = []

    def add(self, filter_fn):
        self.filters.append(filter_fn)

    def apply(self, lines):
        result = lines
        for f in self.filters:
            result = [line for line in result if f(line)]
        return result


def parse_filter_expr(expr):
    """Parse a filter expression string like 'status:200' into a dict."""
    parts = expr.split(":")
    if len(parts) != 2:
        raise ValueError(f"Invalid filter expression: {expr}")
    return {"field": parts[0], "value": parts[1]}
