from matrix import Matrix
from solve_matrix import Solution


def test_3x3():
    matrix = Matrix([[6, 2, 3],
                     [2, 8, 1],
                     [2, 3, 9]],

                    [11, 11, 14])
    solution = Solution(matrix)
    solution.solve_matrix()
    res: bool = solution.is_solution_correct()

    assert res is True
