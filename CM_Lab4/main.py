from draw import *
import matplotlib.pyplot as plt

# func = input("Введите функцию: ")
# a, b, k = map(float, input("Введите интервал [a; b] и шаг [k]: ").split())

# func = "cos(x ** 2 - 4 * x + 1)"
# a, b, k = -5, 5, 50
#
# draw_function(func, a, b, 100 * k)
# draw_function_cubic_spline_interpolation(func, a, b, k)
draw_array_cubic_spline_interpolation([[1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36], [7, 49], [8, 64], [9, 81], [10, 100]])
plt.show()

# draw_function(func, a, b, 100 * k)
# draw_functions_deviation(func, a, b, k)=

# func = "cos(x)"
# array = [[1, 2], [2, 3], [4, 1], [7, 4], [11, 2], [13, 20], [20, -3], [25, -2]]

# func = "x ^ 2 - 2 * x"
# func = "cos(x ** 2 - 4 * x + 1)"
# points = [[1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36], [7, 49], [8, 64], [9, 81], [10, 100]]


def run_analysis(function: str, array: list[list]) -> None:
    draw_function(function, array[0][0], array[-1][0], 100 * len(array), subplot=131)
    draw_array_cubic_spline_interpolation(array, color="b", subplot=131)
    draw_approximating_function(
        array, array[0][0], array[-1][0], color="red", subplot=131
    )

    draw_deviations(function, array, color="gray", subplot=133)

    plt.subplot(131)
    plt.text(
        array[0][0],
        0.95 * max([array[i][1] for i in range(len(array))]),
        f"Before: {get_approximating_func(array)}"
        f"\nr: {get_correlation_coefficient(array)}"
        f"\nR^2: {get_R(array)}",
    )

    # delete the point from array
    pop_max_deviation(function, array, subplot=131)

    draw_function(function, array[0][0], array[-1][0], 100 * len(array), subplot=132)
    draw_array_cubic_spline_interpolation(array, color="b", subplot=132)
    draw_approximating_function(
        array, array[0][0], array[-1][0], color="y", subplot=132
    )

    draw_deviations(function, array, color="black", subplot=133)

    plt.subplot(132)
    plt.text(
        array[0][0],
        0.95 * max([array[i][1] for i in range(len(array))]),
        f"After: {get_approximating_func(array)}"
        f"\nr: {get_correlation_coefficient(array)}"
        f"\nR^2: {get_R(array)}",
    )

    plt.show()


# run_analysis(func, points)
# run_analysis(function='x', array=[[1, 3], [2, 5], [3, 7], [4, 9], [5, 8]])
# run_analysis(function='log(x)',
#              array=[[1, 0.1], [2, 0.8], [3, 1.2], [4, 1.4], [10, 3]])
# run_analysis(function='cos(x ** 2 - 4 * x + 1)', array=[[1, 0], [2, -0.2], [3, 0.3], [4, 0.8], [5, -0.1]])
