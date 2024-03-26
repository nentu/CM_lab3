# some_file.py
from math import *

from lab1 import cli
from lab1.utils import *
from matrix import Matrix
from slae_solver import gauss


def solve_system_2(matrix: Matrix, b: list):
    a = matrix.copy()
    n = len(a)

    res = [0 for _ in range(n)]

    if a[0][0] == 0:
        swap(a, 0, 1)
        swap(b, 0, 1)

    k = - a[1][0] / a[0][0]
    t_v = mul_vec(a[0], k)
    a[1] = sum_vec(a[1], t_v)
    b[1] += b[0] * k

    res[1] = b[1] / a[1][1]

    res[0] = (b[0] - res[1] * a[0][1]) / a[0][0]
    return res


def f(x: float, y: float) -> float:
    return tan(x) * y - x ** 2


def g(x: float, y: float) -> float:
    return 0.8 * x ** 2 + 2 * y ** 2 - 1


def f_x(x: float, y: float) -> float:
    return (y / (cos(x) ** 2) + 2 * x)


def f_y(x: float, y: float) -> float:
    return tan(y)


def g_x(x: float, y: float) -> float:
    return 1.6 * x


def g_y(x: float, y: float) -> float:
    return 4 * y

# def f(x: float, y: float) -> float:
#     return x ** 2 + y ** 2 - 4
#
#
# def g(x: float, y: float) -> float:
#     return - 3 * x ** 2 + y
#
#
# def f_x(x: float, y: float) -> float:
#     return 2 * x
#
#
# def f_y(x: float, y: float) -> float:
#     return 2 * y
#
#
# def g_x(x: float, y: float) -> float:
#     return -6 * x
#
#
# def g_y(x: float, y: float) -> float:
#     return 1


def get_matrix(x_0: float, y_0: float) -> Matrix:
    res = Matrix()
    res.fill_zeroes(2, 2)
    res[0][0] = f_x(x_0, y_0)
    res[0][1] = f_y(x_0, y_0)
    res[1][0] = g_x(x_0, y_0)
    res[1][1] = g_y(x_0, y_0)
    return res


def solve_system(x: float, y: float, epsilon: float) -> list:
    max_delta = epsilon * 3
    while max_delta >= epsilon:
        print(f'При x={round(x, 3)}, y={round(y, 3)} наша система: ')
        A = get_matrix(x, y)
        b = [
            -1 * f(x, y),
            -1 * g(x, y)
        ]
        cli.print_matrix(A, b)

        # A, b = A.reduce_diagonal_dominance(b)

        delta = solve_system_2(A, b)
        print(f'Решив её мы получаем dx={delta[0]} и dy={delta[1]}')
        max_delta = max([abs(i) for i in delta])

        if delta is not None:
            x += delta[0]
            y += delta[1]
            print(f'Тогда новые координаты:{[x, y]} ')
        else:
            return None
    print(f'Так как максимальное приращение {max_delta} < epsilon, то можем остановить расчёты.')
    return [x, y]


if __name__ == '__main__':
    x, y = (0.67, 0.56)
    epsilon = 0.01
    res = solve_system(x, y, epsilon)
    if res is not None:
        print(res)
