"""FilterChain implementation."""


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
