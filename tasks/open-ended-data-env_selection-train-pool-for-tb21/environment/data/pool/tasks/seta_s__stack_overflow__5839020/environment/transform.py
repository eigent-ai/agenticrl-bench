"""Transform symbolic expressions by switching LambertW branch parameters."""


def switch_lambertw_branch(expr_str):
    """Switch LambertW expressions from default/0 branch to branch -1."""
    result = expr_str.replace("LambertW(", "LambertW(-1, ")
    return result


def transform_all(expressions):
    """Transform all expressions in the list and return the transformed list."""
    return [switch_lambertw_branch(e) for e in expressions]
