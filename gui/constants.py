import dataclasses

from sympy.abc import x
from sympy import sqrt, cos

N_START = 4
EPSILON = 1e-2


class Inpropred:
    def __init__(self, f, crit):
        self.formula, self.crit = f, crit


formulas = [
    cos(x ** 2) - cos(x),
    (3 * x ** 3 - 2 * x ** 2 - 7 * x - 8),
    3 * x ** 3 + 1.7 * x ** 2 - 15.42 * x + 6.89
]

inproped = [
    Inpropred(1 / x, 0),
    Inpropred(1 / sqrt(x), 0),
    Inpropred(1 / (1 - x), 1)
]
