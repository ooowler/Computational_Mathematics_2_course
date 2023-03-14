import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import matrix


def draw_array_cubic_spline_interpolation(
        array: list, color: str = "b", subplot: int = 111
) -> None:
    x = Symbol("x")
    spline_functions = get_splines_functions_from_array(array)
    x_dots = [array[i][0] for i in range(len(array))]

    step = 1e-2
    for i, func in enumerate(spline_functions):
        left = x_dots[i]
        right = x_dots[i + 1]

        x_spline_points = np.arange(left, right + step, step)
        y_spline_points = [func.subs({x: x0}) for x0 in x_spline_points]

        plt.subplot(subplot)
        plt.plot(x_spline_points, y_spline_points, color)


def get_splines_functions_from_array(array: list[list]) -> list:
    x_dots = [array[i][0] for i in range(len(array))]
    y_dots = [array[i][1] for i in range(len(array))]
    plt.scatter(x_dots, y_dots, color="red", s=1)
    n = len(x_dots) - 1
    a_list = [y_dots[i] for i in range(n + 1)]
    b_list = [0 for _ in range(n)]
    c_list = [0 for _ in range(n)]
    d_list = [0 for _ in range(n)]

    h_list = [x_dots[0]]
    for i in range(n):
        h_list.append(x_dots[i + 1] - x_dots[i])

    # get c_list
    arr = [[0 for _ in range(n - 1)] for _ in range(n - 1)]
    B = [0 for _ in range(n - 1)]
    for i in range(n - 1):
        B[i] = 3 * (
                ((a_list[i + 2] - a_list[i + 1]) / h_list[i + 2])
                - ((a_list[i + 1] - a_list[i]) / h_list[i + 1])
        )
        if i == 0:
            arr[i][i] = 2 * (h_list[i + 1] + h_list[i + 2])
            arr[i][i + 1] = h_list[i + 2]
            continue

        if i == n - 2:
            arr[i][i - 1] = h_list[i + 1]
            arr[i][i] = 2 * (h_list[i + 1] + h_list[i + 2])
            continue

        arr[i][i - 1] = h_list[i + 1]
        arr[i][i] = 2 * (h_list[i + 1] + h_list[i + 2])
        arr[i][i + 1] = h_list[i + 2]

    c_solution = matrix.solve_matrix(arr, B)
    for i, solution in enumerate(c_solution):
        c_list[i + 1] = solution

    # d_list
    for i in range(n):
        if i == n - 1:
            d_list[i] = (-1) * (c_list[i]) / (3 * h_list[i + 1])
            continue

        d_list[i] = (c_list[i + 1] - c_list[i]) / (3 * h_list[i + 1])

    # b_list
    for i in range(n - 1):
        b_list[i + 1] = ((a_list[i + 1] - a_list[i]) / h_list[i + 1]) + (
                h_list[i + 1] * (2 * c_list[i + 1] + c_list[i]) / 3
        )

    b_list[0] = b_list[1] - 3 * d_list[0] * h_list[1] ** 2

    splines_functions = []
    for i in range(n):
        splines_functions.append(
            sympify(
                f"{a_list[i]} + {b_list[i]} * (x - {x_dots[i]}) + {c_list[i]} * (x - {x_dots[i]}) ** 2 + {d_list[i]} * (x - {x_dots[i]}) ** 3"
            )
        )

    return splines_functions


def draw_deviations(
        func, array: list, color="gray", subplot: int = 111
) -> None:
    n = len(array)
    x_dots = [array[i][0] for i in range(n)]
    y_dots_interpolation = [array[i][1] for i in range(n)]
    deviations = [
        abs(func(array[i][0]) - y_dots_interpolation[i])
        for i in range(n)
    ]

    plt.subplot(subplot)
    plt.plot(x_dots, deviations, color=color)
