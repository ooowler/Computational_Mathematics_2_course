import numpy as np
import matplotlib.pyplot as plt
from function import Function


def draw_function_graph(func: Function, interval_left, interval_right):
    interval_left = float(interval_left)
    interval_right = float(interval_right)
    step = 0.01

    if interval_left > interval_right:
        raise IOError("input the correct intervals")

    dots_x = np.arange(interval_left, interval_right + step, step)
    dots_y = []
    for x in dots_x:
        try:
            res = func.get_value(x)
            if str(res) == 'nan':
                dots_y.append(None)
                continue

            dots_y.append(func.get_value(x))
        except:
            dots_y.append(None)

    if dots_y.count(None) == len(dots_y):
        raise ArithmeticError(
            f"Can not draw function on the interval: [{interval_left}; {interval_right}]"
        )

    plt.plot(dots_x, dots_y, "r")
    plt.plot(dots_x, [0 for _ in range(len(dots_x))], "g")
    plt.show()
