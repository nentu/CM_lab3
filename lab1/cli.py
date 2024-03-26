from dataclasses import dataclass
from random import shuffle
from typing import Any, List

from matrix import Matrix
from my_constants import *
from utils import *


@dataclass
class Respond:
    msg: str
    action: Any


@dataclass
class Question:
    question: str
    responds: List[Respond]


def back():
    pass


def request(question: Question) -> bool:
    while True:
        print(question.question)
        for i in range(len(question.responds)):
            print(f'{i + 1}) ' + question.responds[i].msg)

        ans = input()
        if ans.isdigit() and int(ans) in range(1, len(question.responds) + 1):
            resp = question.responds[int(ans) - 1]
            if type(resp.action) == Question:
                if not request(resp.action):  # not back command
                    return False
            elif callable(resp.action):
                resp.action()
                return resp.action == back
        else:
            print(WRONG_ACTION)


def string_to_vec(s: str) -> list:
    try:
        return list(map(float, s.replace(',', '.').split()))
    except:
        return None


def _read_matrix(a: Matrix, b: list, epsilon_list: list, input_func, repeatable=True):
    while True:
        epsilon_str = input_func(ENTER_EPSILON)
        if str_is_float(epsilon_str):
            break
        if not repeatable:
            error_exit(PARSE_ERROR)

        print(PARSE_ERROR)

    epsilon_list.append(float(epsilon_str.replace(',', '.')))

    while True:
        dim_str = input_func(MATRIX_DIM)
        if dim_str.isdigit() and 1 <= int(dim_str) <= DIM_MAX:
            break
        if not repeatable:
            error_exit(PARSE_ERROR)
        print(DIM_INPUT_ERROR)

    dim = int(dim_str)

    if repeatable:
        print(ENTER_MATRIX_OPTION)

    for i in range(dim):
        while True:
            s = input_func()
            vec = string_to_vec(s)
            if (not vec is None) and len(vec) > 0:
                a.append(vec[:-1])
                b.append(vec[-1])
                break

            if not repeatable:
                error_exit(PARSE_ERROR)
            print(PARSE_ERROR)


def read_matrix_file(a: Matrix, b: list, epsilon: list):
    while True:
        path = input(ENTER_FILE_NAME)
        try:
            f = open(path, 'r')
        except:
            print(INVALID_PATH)
            continue
        _read_matrix(a, b, epsilon, lambda *x: f.readline().strip(), False)
        break


def read_matrix_console(a: Matrix, b: list, epsilon: list):
    _read_matrix(a, b, epsilon, input, True)


def random_matrix(a: Matrix, b: list, epsilon_list: list):
    while True:
        epsilon_str = input(ENTER_EPSILON)
        if str_is_float(epsilon_str):
            break

        print(PARSE_ERROR)

    epsilon_list.append(float(epsilon_str))

    while True:
        dim_str = input(MATRIX_DIM)
        if dim_str.isdigit() and 1 <= int(dim_str) <= DIM_MAX:
            break
        print(DIM_INPUT_ERROR)

    dim = int(dim_str)

    diagonal_index = list(range(0, dim))
    shuffle(diagonal_index)

    for i in diagonal_index:
        a.append(random_vec_with_dominance(dim, i))
        b.append(random() * 8 - 4)


def print_matrix(a: Matrix, b: list):
    print('*====')
    for i in range(len(a)):
        for j in range(len(a[i])):
            print(f'{round(a[i][j], 3)}*x_{j + 1}', end=' + ' if j != len(a) - 1 else ' = ')
        print(round(b[i], 3))
    print('*====')


BACK_OPTION = Respond(BACK_RESPOND_MSG, back)


def print_iteration_result(x: list, epoch: int, metric: float, matrix: list, b: list):
    print(RESULT, end=': ')
    for i in range(len(x)):
        print(f'x_{i + 1}=' + str(x[i]), end=', ' if i != len(x) - 1 else '\n')
    print(EPOCHS + ':', epoch)
    print(ERROR + ':', metric)
    print(B_MAE + ':', residual(matrix, x, b))


if __name__ == '__main__':
    # request(
    #     Question(
    #         'Привет',
    #         [Respond('Привет',
    #                  Question(
    #                      'Как дела?',
    #                      [Respond('Хорошо', lambda: print('Ok')),
    #                       Respond('Плохо', lambda: print('Not ok')),
    #                       BACK_OPTION]
    #                  )),
    #          Respond('Пока',
    #                  exit
    #                  )]
    #     )
    # )
    a, b = Matrix(), list()
    epsilon_list = []

    random_matrix(a, b, epsilon_list)
    print_matrix(a, b)
    epsilon = epsilon_list[0]
