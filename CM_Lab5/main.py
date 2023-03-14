from milne_method import milne_method
import lab_4
import matplotlib.pyplot as plt
import math
import time

print('Привет, смотри какие красивые!')
print("1. y' = a * x * y^2")
print("2. y' = a * x^2 * y")
print("3. y' = a * exp(x)")
ans = int(input('Выбери вариант функции для анализа: '))
answers = [1, 2, 3]
while ans not in answers:
    ans = int(input('Введи правильно! '))

f = None
a, b = None, None
if ans == 1:
    a = float(input('Введи [а]: '))
elif ans == 2:
    a = float(input('Введи [а]: '))
elif ans == 3:
    a = float(input('Введи [а]: '))

funcs_str = {1: f'{a} * x * y^2',
             2: f'{a} * x^2 * y',
             3: f'{a} * x + {b} * y',
             4: f'{a} * exp(x)'}

funcs = {1: lambda x, y: a * x * y ** 2,
         2: lambda x, y: a * x ** 2 * y,
         3: lambda x, y: a * math.exp(x)}

expected_funcs = {1: lambda x: -2 / (a * x ** 2 + (-2 / y0 - a * x0 ** 2)),
                  2: lambda x: (y0 / math.exp(a * x0 ** 3 / 3)) * math.exp(a * x ** 3 / 3),
                  3: lambda x: a * math.exp(x) + (y0 - a * math.exp(x0))}

f = funcs[ans]

x0, y0 = map(float, input('Теперь введи [х0] и значение функции в этой точке [y(x0)]: ').split())
x_end = float(input('Задай конец интервала [x_end]: '))
h = float(input('А еще шаг [h]: '))
print(f'Отлично, твоя функция: {funcs_str[ans]}')
print(f'x0: {x0}, y0: {y0}, x_end: {x_end}, step: {h}')
print('Вычисляю... ')
time.sleep(1)

# y' = -2xy^2
# Устанавливаем начальные значения
# f = lambda x, y: -2 * x * y ** 2
# x0 = 0
# y0 = 1
# x_end = 100
# h = 0.05

# f = lambda x, y: -2 * x * y ** 2
# x0 = 0
# y0 = 1
# x_end = 100
# h = 0.1

# ---

# f = lambda x, y: 1 * x^2 * y
# x0 = 0
# y0 = 1
# x_end = 3
# h = 0.5

# f = lambda x, y: 1 * x^2 * y
# x0 = 0
# y0 = 1
# x_end = 3
# h = 0.01


# Вызываем метод Милна
x, y = milne_method(f, x0, y0, x_end, h)
expected_y = []
for i in range(len(x)):
    expected_y.append((expected_funcs[ans])(x[i]))
    print(f"x: {round(x[i], 2)}, y: {round(y[i], 2)}")

# Выводим результаты при помощи интерполяции из ЛР4
input_array = list(zip(x, y))
expected_array = list(zip(x, expected_y))
lab_4.draw_array_cubic_spline_interpolation(expected_array, color='red', subplot=121)
lab_4.draw_array_cubic_spline_interpolation(input_array, color='blue', subplot=121)
lab_4.draw_deviations(expected_funcs[ans], input_array, color='gray', subplot=122)

plt.xlabel("x")
plt.ylabel("y")
plt.show()
