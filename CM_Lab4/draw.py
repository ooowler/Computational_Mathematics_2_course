import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import matrix


def get_dots(func: str, a: float, b: float, count: float) -> tuple[list, list]:
    x = Symbol("x")
    func = simplify(func)
    step = (b - a) / count

    x_dots = list(np.arange(a, b + step, step))
    y_dots = [func.subs({x: x0}) for x0 in x_dots]
    return x_dots, y_dots


def draw_function(
    func: str, a: float, b: float, count: int, color="k", subplot: int = 111
) -> None:
    x = Symbol("x")
    func = simplify(func)
    x_dots, y_dots = get_dots(func, a, b, count)

    plt.subplot(subplot)
    plt.plot(x_dots, y_dots, color)


def get_splines_functions_from_function(
    func: str, a: float, b: float, count: int
) -> list:
    x = Symbol("x")
    func = simplify(func)
    x_dots = get_dots(func, a, b, count)[0]
    y_dots = [func.subs({x: x0}) for x0 in x_dots]
    n = len(x_dots) - 1
    a_list = [y_dots[i] for i in range(n + 1)]
    b_list = [float(0) for _ in range(n)]
    c_list = [float(0) for _ in range(n)]
    d_list = [float(0) for _ in range(n)]

    h_list = [x_dots[0]]
    for i in range(n):
        h_list.append(x_dots[i + 1] - x_dots[i])

    # get c_list
    arr = [[float(0) for _ in range(n - 1)] for _ in range(n - 1)]
    B = [float(0) for _ in range(n - 1)]
    for i in range(n - 1):
        B[i] = 3 * float(
            ((a_list[i + 2] - a_list[i + 1]) / h_list[i + 2])
            - ((a_list[i + 1] - a_list[i]) / h_list[i + 1])
        )
        if i == 0:
            arr[i][i] = 2 * float(h_list[i + 1] + h_list[i + 2])
            arr[i][i + 1] = float(h_list[i + 2])
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


def draw_function_cubic_spline_interpolation(
    func: str, a: float, b: float, count: int
) -> None:
    x = Symbol("x")
    func = simplify(func)
    count -= 1
    dots = get_dots(func, a, b, count)
    x_dots = dots[0]
    y_dots = dots[1]
    plt.scatter(x_dots, y_dots, color="red")

    spline_functions = get_splines_functions_from_function(func, a, b, count)

    step = 1e-2
    for i, func in enumerate(spline_functions):
        left = x_dots[i]
        right = x_dots[i + 1]

        x_spline_points = np.arange(left, right + step, step)
        y_spline_points = [func.subs({x: x0}) for x0 in x_spline_points]

        plt.plot(x_spline_points, y_spline_points, "b")


def draw_array_cubic_spline_interpolation(
    array: list[list], color: str = "b", subplot: int = 111
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
    plt.scatter(x_dots, y_dots, color="red")
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
    func: str, array: list[list], color="gray", subplot: int = 111
) -> None:
    x = Symbol("x")
    func = simplify(func)
    n = len(array)
    x_dots = [array[i][0] for i in range(n)]
    y_dots_interpolation = [array[i][1] for i in range(n)]
    deviations = [
        abs(func.subs({x: x_dots[i]}).evalf() - y_dots_interpolation[i])
        for i in range(n)
    ]

    plt.subplot(subplot)
    plt.plot(x_dots, deviations, color=color)


def pop_max_deviation(func: str, array: list[list], subplot: int = 111) -> None:
    x = Symbol("x")
    func1 = simplify(func)
    a, b = get_coefficients_approximating_function(array)
    func2 = simplify(f"{a} * x + {b}")
    n = len(array)
    x_dots = [array[i][0] for i in range(n)]

    deviations = [
        abs(func1.subs({x: x_dots[i]}) - func2.subs({x: x_dots[i]})) for i in range(n)
    ]
    max_deviation = max(deviations)
    index_max_deviation = deviations.index(max_deviation)

    min_deviation = min(deviations)
    index_min_deviation = deviations.index(min_deviation)

    if index_max_deviation == index_min_deviation:
        return

    plt.subplot(subplot)
    plt.scatter(
        x_dots[index_max_deviation],
        func1.subs({x: x_dots[index_max_deviation]}),
        color="blue",
    )
    # delete the point
    array.pop(index_max_deviation)


def get_coefficients_approximating_function(array: list[list]) -> tuple:
    n = len(array)
    x_dots = [array[i][0] for i in range(n)]
    y_dots = [array[i][1] for i in range(n)]

    sum_xy = sum([x_dots[i] * y_dots[i] for i in range(n)])
    sum_x = sum(x_dots)
    sum_y = sum(y_dots)
    sum_x2 = sum([x_dots[i] ** 2 for i in range(n)])

    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    b = (sum_y - a * sum_x) / (n)

    return a, b


def draw_approximating_function(
    array: list[list], left, right, color="red", subplot: int = 121
) -> None:
    x = Symbol("x")
    a, b = get_coefficients_approximating_function(array)
    func = simplify(f"{a} * x + {b}")
    draw_function(func, left, right, 10000, color, subplot)


def get_approximating_func(array: list[list]) -> str:
    a, b = get_coefficients_approximating_function(array)
    return f"{round(a, 2)} * x + {round(b, 2)}"


def get_correlation_coefficient(array: list[list]) -> float:
    n = len(array)
    x_dots = [array[i][0] for i in range(n)]
    y_dots = [array[i][1] for i in range(n)]

    sum_xy = sum([x_dots[i] * y_dots[i] for i in range(n)])
    sum_x = sum(x_dots)
    sum_y = sum(y_dots)
    sum_x2 = sum([x_dots[i] ** 2 for i in range(n)])
    sum_y2 = sum([y_dots[i] ** 2 for i in range(n)])
    x_avg = sum_x / n
    y_avg = sum_y / n

    sigm_x = sqrt(sum_x2 / n - x_avg**2)
    sigm_y = sqrt(sum_y2 / n - y_avg**2)

    r = (sum_xy / n - sum_x * sum_y / n**2) / (sigm_x * sigm_y)
    r = round(float(r), 2)

    return r


def get_R(array: list[list]) -> float:
    r = get_correlation_coefficient(array)
    return r**2
