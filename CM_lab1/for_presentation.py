from matrix import Matrix
from solve_matrix import Solution

matrix = Matrix([[10, 2, 3, 4],  # sum 19
                 [1, 15, 3, 5],  # sum 24
                 [-3, -2, -12, -2],  # sum -19
                 [-1, -2, -3, 8]],

                 [19, 24, -19, 2])  # solutions must be: [1, 1, 1, 1]

solution = Solution(matrix, 1e-7)

solution.solve_matrix()
print()
solution.print_solution_vector(accuracy=5)
print()
solution.is_solution_correct()

