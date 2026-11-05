from calculator import add, subtract
from math_ops import multiply

def combined_operation(a, b, c):
    result = add(a, b)
    result = multiply(result, c)
    return result
