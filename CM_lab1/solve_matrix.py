from matrix import Matrix
from typing import Optional


class Solution:
    matrix = None
    eps = None
    solution_vector = None

    def __init__(self, matrix_init: Matrix = None, eps: float = 1e-6):
        self.eps = eps

        if matrix_init is None:
            self.matrix = Matrix()
        else:
            self.matrix = matrix_init

    def solve_matrix(self) -> Optional[list]:
        '''
        Description: method gauss seidel
        :return: the list of roots of the matrix
        '''
        if self.matrix.is_square():
            return self.__solve_square_matrix(self.matrix)

        return self.__solve_not_square_matrix(self.matrix)

    def __solve_square_matrix(self, matrix: Matrix) -> Optional[list]:
        self.__check_square_matrix()

        n = len(matrix.A)
        init_vector = [self.matrix.B[i] / self.matrix.A[i][i] for i in range(n)]
        prev_vector = init_vector[:]
        error = self.eps + 1
        iteration = 1
        solution_vector = []

        while error > self.eps:
            solution_vector = []
            for i in range(n):
                normalize = self.matrix.A[i][i]
                new_value = self.matrix.B[i] / normalize

                for k in range(i):
                    new_value -= solution_vector[k] * (self.matrix.A[i][k] / normalize)

                for k in range(i + 1, n):
                    new_value -= prev_vector[k] * (self.matrix.A[i][k] / normalize)

                solution_vector.append(new_value)

            new_error = max(abs(solution_vector[i] - prev_vector[i]) for i in range(n))
            if iteration > 5 and new_error > error:
                print(
                    f'{"-" * 10}\nDoes not converge\nThe error increased by {round(100 * new_error / error, 1)}%\n{"-" * 10}')

                self.solution_vector = None
                return

            error = new_error

            prev_vector = solution_vector[:]
            iteration += 1

        print('SUCCESS!')
        print(f'Total count of iteration is: {iteration}')

        self.solution_vector = solution_vector[:]
        return solution_vector

    def print_solution_vector(self, accuracy: int = 10) -> None:
        if not self.solution_vector:
            print('No Solution')
            return

        for i in range(len(self.solution_vector)):
            print(f'x{i + 1}: {round(self.solution_vector[i], accuracy)}')

    def is_solution_correct(self) -> Optional[bool]:
        if not self.matrix.A:
            print('Matrix is None')
            return

        if not self.eps:
            print('please, solve the matrix firstly')
            return

        for i in range(len(self.matrix.A)):
            A_sum = 0
            sum_error = 0

            for j in range(len(self.matrix.A[i])):
                A_sum += self.matrix.A[i][j] * self.solution_vector[j]
                sum_error += abs(self.matrix.A[i][j]) * self.eps

            if not (self.matrix.B[i] - sum_error <= A_sum <= self.matrix.B[i] + sum_error):
                print('Solution is incorrect!')
                return False

        print('Solution is correct!')
        print(f'your accuracy is {self.eps}')
        return True

    def __solve_not_square_matrix(self, matrix: Matrix) -> Optional[list]:
        rows = len(matrix.A)
        columns = len(matrix.A[0])
        if columns > rows:
            print('Probably inf solutions')
            return

        sub_A = self.matrix.A[:columns]
        self.matrix = Matrix(sub_A, self.matrix.B)
        self.__check_square_matrix()
        res = self.__solve_square_matrix(self.matrix)
        if not res:
            print('Can not solve matrix')
            return

        self.solution_vector = res[:]
        self.matrix = matrix

        if self.is_solution_correct():
            print(f'\n{"-" * 10}')
            print(f'Solution correct for your {rows}x{columns} matrix!')
            print(f'{"-" * 10}')
            return self.solution_vector
        else:
            self.solution_vector = None
            print('Can not solve matrix')
            return

    def __check_square_matrix(self) -> None:
        for i in range(self.matrix.get_row_num()):
            if self.matrix.A[i][i] == 0:
                raise IOError('Method Gauss Seidel work only with not 0 values in diagonal')

            if 2 * abs(self.matrix.A[i][i]) < sum(map(abs, self.matrix.A[i])):
                raise Exception('The condition for applying the method is not met - [diagonal predominance]')
