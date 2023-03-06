import math
import time
import threading
from math import log, log2
from math import exp
from typing import Optional

from numpy import linalg as LA
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

# def func_(x):
#     return x ** 3 - 6 * x + 2

# def func_(x):
#     return exp(x) - 10 * x


# print(type(func))
# func_ = input('input your function: ')
# func_ = compile(func_, "<string>", "eval")
# interval_left_ = input('input left border of the interval: ')
# interval_right_ = input('input right border of the interval: ')
# step_ = input('input step: ')
RESULT = {}


def print_matrix(matrix: list[list]):
    for i in range(len(matrix)):
        print(f'{i + 1}. ', end='')
        for j in range(len(matrix[i])):
            print(matrix[i][j], end=' ')

        print()


def print_solution_vector(vector: list):
    for i in range(len(vector)):
        print(f'x{i + 1}: {vector[i]}')


def draw_function_graph(func, interval_left, interval_right, step):
    interval_left = float(interval_left)
    interval_right = float(interval_right)
    step = float(step)

    if interval_left > interval_right:
        raise IOError('input the correct intervals')

    dots_x = np.arange(interval_left, interval_right + step, step)
    dots_y = []
    for x in dots_x:
        try:
            if str(func.__class__) == "<class 'code'>":
                dots_y.append(eval(func))
            elif str(func.__class__) == "<class 'function'>":
                dots_y.append(func(x))
            else:
                raise IOError('Failed to recognize the function')
        except:
            dots_y.append(None)

    if dots_y.count(None) == len(dots_y):
        raise ArithmeticError(f'Can not draw function on the interval: [{interval_left}; {interval_right}]')

    plt.plot(dots_x, dots_y, 'r')
    plt.plot(dots_x, [0 for _ in range(len(dots_x))], 'g')
    plt.show()


def check_sign_derivative_on_interval(func, a, b):
    dots_x = np.arange(a, b + 0.1, 0.1)
    sign = -1 if calculate_derivative(func, a) < 0 else 1
    for x in dots_x:
        next_sign = -1 if calculate_derivative(func, x) < 0 else 1
        if sign != next_sign:
            return False

    return True


def bisection_method(func, a, b, eps):
    if eps < 0:
        raise IOError('Input correct eps')

    # is_monotone = check_sign_derivative_on_interval(func, a, b)
    # if not is_monotone:
    #     print('Function must be monotone')
    #     return

    # if not func(a) * func(b) < 0:
    #     print('No solutions')
    #     return

    c = (a + b) / 2  # middle AB
    ab_len = b - a  # len AB
    f_a = func(a)
    f_c = func(c)
    res = f_a * f_c

    while ab_len >= eps:
        if res < 0:
            b = c
        else:
            a = c

        c = (a + b) / 2
        ab_len = b - a
        f_a = func(a)
        f_c = func(c)
        res = f_a * f_c

    RESULT['bisection_method'] = c
    return c


def calculate_derivative(func, x):
    dx = 1e-7
    return (func(x + dx) - func(x)) / dx


def calculate_determinant(matrix: list[list]) -> int:
    return LA.det(matrix)


def iterative_method(func, a, b, eps):
    is_monotone = check_sign_derivative_on_interval(func, a, b)
    if not is_monotone:
        RESULT['iterative_method'] = None
        print('Function must be monotone')
        return

    derivative_sign = -1 if calculate_derivative(func, a) < 0 else 1
    d_a = abs(calculate_derivative(func, a))
    d_b = abs(calculate_derivative(func, b))
    m = min(d_a, d_b)
    M = max(d_a, d_b)

    lam = 1 / M
    alpha = 1 - (m / M)
    if not 0 <= alpha < 1:
        print('The convergence condition is not met')
        RESULT['iterative_method'] = None
        return

    x0 = a
    x1 = a + 2 * eps

    while abs(x1 - x0) > eps:
        x0 = x1
        if not a <= x1 <= b:
            print('No solutions')
            RESULT['iterative_method'] = None
            return

        if derivative_sign > 0:
            x1 = x0 - lam * func(x0)
        else:
            x1 = x0 + lam * func(x0)

    if not a <= x1 <= b:
        print('no solutions')
        RESULT['iterative_method'] = None
        return

    RESULT['iterative_method'] = x1
    return x1


def iterative_method_matrix_nxn(matrix: list[list], free_column: list, x0, eps, debug_info: bool = None) -> Optional[list]:
    if len(matrix) == 0:
        raise IOError('No matrix')

    if len(matrix) != len(matrix[0]):
        raise IOError('Matrix must be a square')

    max_error = eps + 1
    x1 = []
    count_of_iteration = 1
    while max_error > eps:
        f_x0 = []
        for i in range(len(matrix)):
            funcs_x0 = [func(x0[j]) for j, func in enumerate(matrix[i])]
            funcs_x0.append((-1) * free_column[i])
            f_x0.append(sum(funcs_x0))

        f_der_x0 = []
        for i in range(len(matrix)):
            f_der_x0.append([calculate_derivative(func, x0[j]) for j, func in enumerate(matrix[i])])

        det_f_der_x0 = calculate_determinant(f_der_x0)
        if det_f_der_x0 == 0:
            print('The special matrix was met')
            return

        inverse_matrix_f_der_x0 = list(LA.inv(f_der_x0))
        for i in range(len(f_der_x0)):
            inverse_matrix_f_der_x0[i] = list(inverse_matrix_f_der_x0[i])

        inverse_multiple_func = np.matmul(inverse_matrix_f_der_x0, f_x0)
        x1 = [x0[i] - inverse_multiple_func[i] for i in range(len(x0))]
        max_error = max([abs(x1[i] - x0[i]) for i in range(len(x0))])
        x0 = x1[:]

        count_of_iteration += 1

    if debug_info is True:
        print(f'count of iterations: {count_of_iteration}')
        print(f'max error: {max_error}')

        colors = ['r', 'b', 'g', 'y', 'c']
        if len(matrix) <= len(colors):
            dots_x = np.arange(-x0[0] * 5, x0[0] * 5 + 0.1, 0.1)

            for row in range(len(matrix)):
                dots_y = []
                for x in dots_x:
                    res = 0
                    for column in range(len(matrix[row])):
                        func = matrix[row][column]
                        res += func(x)

                    res -= free_column[row]
                    dots_y.append(res)

                plt.plot(dots_x, dots_y, colors[row])

            plt.plot(dots_x, [0 for _ in range(len(dots_x))], 'g')
            plt.show()

        print()

    return x1


def solve_both_methods(func, interval_left, interval_right, step):
    thread_bisection = Thread(target=bisection_method, args=(func, interval_left, interval_right, 1e-5))
    thread_iterative = Thread(target=iterative_method, args=(func, interval_left, interval_right, 1e-5))

    thread_bisection.start()
    thread_iterative.start()

    while thread_bisection.is_alive() and thread_iterative.is_alive():
        pass

    if not thread_bisection.is_alive() and thread_iterative.is_alive():
        print(f'[first] {list(RESULT.keys())[0]}: {list(RESULT.values())[0]}')
        print()
        thread_iterative.join()

    if thread_bisection.is_alive() and not thread_iterative.is_alive():
        print(f'[first] {list(RESULT.keys())[0]}: {list(RESULT.values())[0]}')
        print()
        thread_bisection.join()

    print(f'bisection_method: {RESULT["bisection_method"]}')
    print(f'iterative_method {RESULT["iterative_method"]}')
    draw_function_graph(func, interval_left, interval_right, step)


solve_both_methods(func=lambda x: exp(-x) - math.sin(x) ** 2 / 2,
                   interval_left=-1,
                   interval_right=2.4,
                   step=1e-5)

system_of_equations = [[lambda x: x ** 2, lambda x: x ** 2],
                       [lambda x: x ** 3, lambda x: (-1) * x]]
free_column = [1, 0]

res = iterative_method_matrix_nxn(matrix=system_of_equations,
                                  free_column=free_column,
                                  x0=[100, 100],
                                  eps=1e-5,
                                  debug_info=True)
if res:
    print_solution_vector(res)
else:
    print('No solution')
