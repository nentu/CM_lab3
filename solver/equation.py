from sympy import limit, zoo, Rel, sqrt, latex
from sympy.polys.polyfuncs import interpolate as interpol
import numpy as np
from gui.constants import *


def integral(f, a, b, c=None):
    F = f.integrate(x)
    if c is None or c < a or c > b:
        return (F.subs(x, b) - F.subs(x, a)).evalf()
    else:
        res = limit(F, x, b) - limit(F, x, c)
        res += limit(F, x, c) - limit(F, x, a)

        if res.is_finite:
            return res.evalf()
        else:
            return None


def generalMethod(func, a, b, k):
    X = np.linspace(a, b, k)
    vecF = np.vectorize(lambda x1: func.subs(x, x1))
    Y = vecF(X)
    f = interpol(list(zip(X, Y)), x)
    return integral(f, a, b), X, Y, f


def left_rectangle(f, a, b):
    return (b - a) * f.subs(x, a).evalf()


def center_rectangle(f, a, b):
    h = (b - a)
    l = f.subs(x, (a + b) / 2).evalf()
    return h * l


def right_rectangle(f, a, b):
    return (b - a) * f.subs(x, b).evalf()


def trapezoid(f, a, b):
    return generalMethod(f, a, b, 2)[0]


def simpson(f, a, b):
    return generalMethod(f, a, b, 3)[0]


def solve(f, method, a, b, n):
    parts = np.linspace(a, b, n + 1)
    res = 0
    for i in range(parts.size - 1):
        res = res + method(f, parts[i], parts[i + 1])
    return res


def rungeIteration(f, method, a, b, epsilon):
    n = N_START
    prev_res = solve(f, method, a, b, n)
    while True:
        n *= 2
        res = solve(f, method, a, b, n)
        if abs(prev_res - res) < epsilon:
            return res, n
        prev_res = res


if __name__ == '__main__':
    formula = formulas[1]
    print(generalMethod(formula, 0, 2, 6))
