from function import Function
from Exceptions import AccuracyException, BreakPoint2ndType
import numpy as np


def check_the_break_point(func: Function, x: float) -> int:
    dx = 1e-10
    inf = 1e20

    left_lim = func.get_value(x - dx)
    right_lim = func.get_value(x + dx)

    if str(func.get_value(x)) == 'nan' or str(left_lim) == 'nan' or str(right_lim) == 'nan':
        if abs(left_lim) > inf or abs(right_lim) > inf:
            return 2

        if left_lim != right_lim:
            return 1

    if abs(left_lim) > inf or abs(right_lim) > inf:
        return 2

    return 0


def simpson_method(
        func: Function, left: float, right: float, n: int, eps: float, percent=False
) -> float:
    n = ((n + 1) // 2) * 2  # to even
    h = (right - left) / n
    x_dots = list(np.arange(left, right + h, h))
    y_dots = []
    for index, x in enumerate(x_dots):
        res = func.get_value(x)
        point_type = check_the_break_point(func, x)

        if str(res) != 'nan' and point_type == 0:
            y_dots.append(res)
        else:
            if point_type == 2:
                raise BreakPoint2ndType(
                    f"abscissa of the point: {x} ≈ {round(x, 3)}"
                )

            if point_type == 1:
                print(f'First type break was met x ≈ {x}, choose the option [1/2]: ')
                print('Option 1: calculate 2 integrals (ignore the point)')
                print('Option 2: f(x) = (f(x - dx) + f(x + dx)) / 2')
                option = input('Enter the option: ').replace(' ', '')
                while not (option == '1' or option == '2'):
                    option = input('Enter the option one more time: ').replace(' ', '')

                if option == '1':
                    y_dots.append(0)

                if option == '2':
                    dx = 1e-10
                    y_dots.append((func.get_value(x - dx) + func.get_value(x + dx)) / 2)

    even_sum_h = sum([y_dots[i] for i in range(2, len(y_dots) - 1, 2)])
    odd_sum_h = sum([y_dots[i] for i in range(1, len(y_dots) - 1, 2)])

    even_sum_2h = sum([y_dots[i] for i in range(2 * 2, len(y_dots) - 1, 2 * 2)])
    odd_sum_2h = sum([y_dots[i] for i in range(1 * 2, len(y_dots) - 1, 2 * 2)])

    I_h = (h / 3) * (y_dots[0] + y_dots[-1] + 2 * even_sum_h + 4 * odd_sum_h)
    I_2h = (2 * h / 3) * (y_dots[0] + y_dots[-1] + 2 * even_sum_2h + 4 * odd_sum_2h)

    accuracy = abs(I_2h - I_h) / 15
    R = (
                (-1) * ((right - left) * h ** 4) / 180
        ) * func.get_max_value_in_range_nth_derivative(4, right, left)
    real_error = min(abs(R), accuracy)
    I_estimated = I_h + (I_h - I_2h) / 15

    if percent:
        eps *= abs(I_h) / 100

    if real_error > eps:
        raise AccuracyException(
            f"please, enter more steps-[n] for better accuracy, answer was about {I_estimated}"
        )

    return I_h if R < accuracy else I_estimated
