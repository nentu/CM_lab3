from random import random
import re
import sys

float_pattern = re.compile("\d+((\.|,)\d+)?")


def parity_permutation(perm: list) -> bool:
    res = True
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if perm[j] < perm[i]:
                res = not res
    return res


def mae(vec_a: list, vec_b: list) -> float:
    return max([abs(vec_a[i] - vec_b[i]) for i in range(len(vec_a))])


def residual(a: list, x: list, b: list) -> float:
    answer = list()
    for i in range(len(a)):
        answer.append(sum([a[i][j] * x[j] for j in range(len(x))]))
    return mae(answer, b)


def error_exit(msg: str):
    print(msg, file=sys.stderr)
    exit(1)


def swap(a: list, i: int, j: int):
    a[i], a[j] = a[j], a[i]


def sum_vec(vec1: list, vec2: list) -> list:
    return [vec1[i] + vec2[i] for i in range(len(vec1))]


def mul_vec(vec: list, k: float) -> list:
    return [i * k for i in vec]


def str_is_float(s: str) -> bool:
    m = float_pattern.match(s)
    return (not m is None) and m.start() == 0 and m.end() == len(s)


def del_from_row(a: list, value: float):
    for i in range(len(a)):
        for j in range(len(a[i]) - 1, -1, -1):
            if a[i][j] == value:
                del a[i][j]


def random_vec_with_dominance(length: int, dom_index):
    vec = list()
    small_value = random() * 10 + 2

    for i in range(length):
        if i == dom_index:
            vec.append(2 * random() + small_value * (length - 1))
        else:
            vec.append(2 * (random() * small_value) - small_value)

    return vec



def get_unique_sequence(l: list, prev_list=list(), current_row=0):
    if current_row == len(l):
        return enumerate(prev_list)
    for i in l[current_row]:
        if not i in prev_list:
            res = get_unique_sequence(l, prev_list + [i], current_row + 1)
            if res is not None:
                return res
    return None
