import numpy as np


def solve_matrix(matrix: list[list], b: list) -> list:
    return list(np.linalg.solve(matrix, b))


def matrix_print(matrix: list[list]) -> None:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=" ")

        print()
