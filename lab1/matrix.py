from math import sqrt

from utils import *


class Matrix(list):

    def __init__(self):
        super().__init__()

    def fill_zeroes(self, m: int, n: int):
        super().clear()
        for i in range(m):
            super().append([0 for i in range(n)])

    @staticmethod
    def from_list(origin: list):
        res = Matrix()
        res.fill_zeroes(len(origin), len(origin))
        for i in range(len(res)):
            res[i] = origin[i].copy()
        return res

    def is_square(self) -> bool:
        width = -1
        for s in self:
            if width == -1:
                width = len(s)
            if len(s) != width:
                return False
        return len(self) == width

    def get_norm(self) -> float:
        res = 0
        for i in self:
            for j in i:
                res += j ** 2
        return sqrt(res)

    def get_determinant(self) -> float:
        # self.is_square()
        res = 1
        a = self.copy()
        for i in range(len(a) - 1):
            k = a[i][i]
            if k == 0:
                for j in range(i + 1, len(a)):
                    if a[j][i] != 0:
                        k = a[j][i]
                        swap(a, i, j)
                        res *= -1
                        break
                else:
                    return 0
            res *= k
            for j in range(i + 1, len(a)):
                t = mul_vec(a[i], - a[j][i] / k)
                a[j] = sum_vec(a[j], t)
        res *= a[-1][-1]
        return res

    # def get_determinant(self):
    #     if not self.is_square():
    #         return -1
    #
    #     for i in self:
    #         if len(i) != len(self) or len(i) != len(self[0]):
    #             return -1
    #     perms = list(permutations(range(len(self))))
    #
    #     res = 0
    #     for perm in perms:
    #         t = 1
    #         for j in range(len(self)):
    #             t *= self[j][perm[j]]
    #         if not parity_permutation(perm):
    #             t *= -1
    #         res += t
    #     return res

    def is_diagonal_dominance(self) -> bool:
        for i in range(len(self)):
            summ = sum(abs(self[i][j]) for j in range(len(self)) if i != j)
            if not self[i][i] >= summ:
                return False

        return True

    def _max_column_index(self, column: int) -> int:
        return max(enumerate(self), key=lambda x: x[1][column])[0]

    def swap(self, i: int, j: int):
        swap(self, i, j)

    def reduce_diagonal_dominance(self, b: list):
        potential_places = get_potential_places(self)

        empty_rows = set(range(len(self)))
        unused_rows = set(range(len(self)))
        new_matrix = Matrix()
        new_matrix.fill_zeroes(len(self), len(self))
        new_b = [0 for _ in range(len(b))]

        # paths = get_unique_sequence(potential_places)
        #
        # if paths is not None:
        #     new_matrix = Matrix()
        #     new_matrix.fill_zeroes(len(self), len(self))
        #     new_b = [0 for i in range(len(b))]
        #
        #     for original_row, new_row in paths:
        #         new_matrix[new_row] = self[original_row]
        #         new_b[new_row] = b[original_row]
        #
        #     self = Matrix.from_list(new_matrix)
        #     b = new_b.copy()

        # Rows
        changed = True
        while changed:
            changed = False
            for row_i in range(len(potential_places) - 1, -1, -1):
                if len(potential_places[row_i]) == 1:
                    index = potential_places[row_i][0]

                    new_matrix[index] = self[row_i].copy()
                    new_b[index] = b[row_i]

                    potential_places[row_i].clear()
                    del_from_row(potential_places, index)
                    empty_rows.remove(index)
                    unused_rows.remove(row_i)

                    changed = True

            if changed:
                continue
            # Columns
            empty_rows = list(empty_rows)
            unused_rows = list(unused_rows)

            for column_i in range(len(empty_rows) - 1, -1, -1):
                column = empty_rows[column_i]
                potential_row = -1
                for row in range(len(potential_places)):
                    if column in potential_places[row]:
                        if potential_row == -1:
                            potential_row = row
                        else:
                            break
                else:
                    if potential_row != -1:
                        index = potential_row

                        new_matrix[column] = self[index].copy()
                        new_b[column] = b[index]

                        potential_places[index].clear()
                        empty_rows.remove(column)
                        unused_rows.remove(index)

                        changed = True
            if changed:
                continue

            for i in unused_rows:
                if len(potential_places[i]) == 2:
                    del potential_places[i][0]
                    changed = True
                    break

        # remaining rows
        for i in range(len(empty_rows)):
            new_matrix[empty_rows[i]] = self[unused_rows[i]]

        return new_matrix, new_b


def get_potential_places(a: Matrix):
    res = list()
    for row in a:
        res.append(list())
        s = sum([abs(i) for i in row])
        for i in range(len(row)):
            if abs(row[i]) >= s - abs(row[i]):
                res[-1].append(i)
    return res


if __name__ == '__main__':
    a = Matrix()
    for i in range(1, 14, 4):
        a.append([j ** 2 for j in list(range(i, i + 4))])
    print(a)
    print(a.get_determinant())
