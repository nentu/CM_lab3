import numpy as np
from PyQt5.QtWidgets import QMessageBox
from sympy.abc import x


def answers(f_syp, a, b):
    x_val = np.linspace(a, b, int(50))
    f = lambda val_x: f_syp.subs(x, val_x).evalf()
    return [x_val[i] for i in range(1, len(x_val)) if (f(x_val[i]) * f(x_val[i - 1]) < 0 or f(x_val[i - 1]) == 0)]





if __name__ == '__main__':
    print(answers(x ** 2 - 1, -5, 5))
