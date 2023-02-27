from matrix import Matrix
from solve_matrix import Solution


def my_test_20x20() -> None:
    matrix = Matrix()
    solution = Solution(matrix)
    solution.solve_matrix()
    print()
    solution.print_solution_vector()
    print()
    solution.is_solution_correct()


def my_test_not_square_matrix() -> None:
    matrix = Matrix([[6, 2, 3],
                     [2, 8, 1],
                     [2, 3, 9],
                     [1, 1, 2]],

                    [11, 11, 14, 4])
    solution = Solution(matrix)
    solution.solve_matrix()
    print()
    solution.print_solution_vector()


my_test_not_square_matrix()
