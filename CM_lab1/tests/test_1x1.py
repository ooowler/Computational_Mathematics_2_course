from matrix import Matrix
from solve_matrix import Solution


def test_1x1():
    matrix = Matrix([[1]], [1])
    solution = Solution(matrix)
    solution.solve_matrix()
    res: bool = solution.is_solution_correct()

    assert res is True
