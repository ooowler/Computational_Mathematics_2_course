from matrix import Matrix
from solve_matrix import Solution


def test_no_solution_4x3():
    matrix = Matrix([[6, 2, 3],
                     [2, 8, 1],
                     [2, 3, 9],
                     [1, 1, 2]],

                    [11, 11, 14, 3])
    solution = Solution(matrix)
    solution.solve_matrix()
    res: bool = solution.solution_vector is not None
    assert res is False


