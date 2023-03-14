import numpy as np
import matplotlib.pyplot as plt
import lab_4
import math


def milne_method(function, x0, y0, x_end, h):
    # Определяем количество шагов
    n = int((x_end - x0) / h)

    # Создаем массивы для хранения значений x и y
    x = np.zeros(n + 1)
    y = np.zeros(n + 1)

    # Устанавливаем начальные значения
    x[0] = x0
    y[0] = y0

    # Используем метод Рунге-Кутты четвертого порядка для получения первых 4 точек
    for i in range(3):
        k1 = h * function(x[i], y[i])
        k2 = h * function(x[i] + h / 2, y[i] + k1 / 2)
        k3 = h * function(x[i] + h / 2, y[i] + k2 / 2)
        k4 = h * function(x[i] + h, y[i] + k3)

        y[i + 1] = y[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x[i + 1] = x[i] + h

    # Используем метод Милна для получения остальных точек
    for i in range(4, n + 1):
        x[i] = x[i - 1] + h
        first_solution = y[i - 4] + 4 / 3 * h * (
                2 * function(x[i - 3], y[i - 3])
                - function(x[i - 2], y[i - 2])
                + 2 * function(x[i - 1], y[i - 1])
        )
        second_solution = y[i - 2] + h / 3 * (
                function(x[i], first_solution)
                + 4 * function(x[i - 1], y[i - 1])
                + function(x[i - 2], y[i - 2])
        )
        y[i] = second_solution

    return x, y
