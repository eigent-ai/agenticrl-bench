import sympy
from sympy.abc import x, y, n


def render_expression():
    expr = (a * b) ** n
    unicode_art = sympy.pretty(expr, use_unicode=True)
    latex_str = sympy.latex(expr)
    return {"unicode": unicode_art, "latex": latex_str}
