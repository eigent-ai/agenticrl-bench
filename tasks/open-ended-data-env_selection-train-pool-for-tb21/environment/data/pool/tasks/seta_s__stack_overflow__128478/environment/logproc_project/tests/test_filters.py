"""Tests for filter imports and functionality."""

def test_filter_chain_importable():
    """Test that FilterChain can be imported from logproc.filters."""
    from logproc.filters import FilterChain
    fc = FilterChain()
    assert hasattr(fc, "apply")


def test_parse_filter_expr_importable():
    """Test that parse_filter_expr can be imported from logproc.filters."""
    from logproc.filters import parse_filter_expr
    result = parse_filter_expr("status:200")
    assert result == {"field": "status", "value": "200"}
