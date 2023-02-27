import random


class Matrix:
    A = []
    B = []

    def __init__(self, matrix_init: list[list] = None, solutions_vector: list = None) -> None:
        if matrix_init is None and solutions_vector is None:
            init_matrix_length = 20
            self.create_random_square_matrix(init_matrix_length)

        elif matrix_init is not None and solutions_vector is not None:
            self.B = solutions_vector
            self.A = matrix_init

        else:
            raise IOError('Not enough args to create the matrix')

        self.__matrix_is_valid()

    def create_random_square_matrix(self, n: int, max_abs_value: int = 10) -> None:
        '''
        :param max_abs_value: all values will be in [- max_abs_value; + max_abs_value]
        :param n: matrix length
        :return: create a square matrix with length - 20
        '''

        for _ in range(n):
            self.A.append([random.randint(-max_abs_value, max_abs_value) for _ in range(n)])

        for i in range(n):
            self.A[i][i] = sum(map(abs, self.A[i])) * random.randint(2, 3)  # diagonal predominance

        for _ in range(n):
            self.B.append(random.randint(-max_abs_value, max_abs_value))

    def is_square(self) -> bool:
        rows_count = len(self.A)
        column_count = len(self.A[0])

        return rows_count == column_count

    def __matrix_is_valid(self) -> None:
        if len(self.A) == 0:
            raise IOError('Matrix is empty')

        column_count = len(self.A[0])
        for i in range(len(self.A)):
            if column_count != len(self.A[i]):
                raise IOError('The number of columns in the matrix must be the same!')

    def get_row_num(self) -> int:
        return len(self.A)

    def get_column_num(self) -> int:
        return len(self.B)
