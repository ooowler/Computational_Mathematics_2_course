from draw_func import draw_function_graph
from simpson_method import simpson_method
from function import Function

my_func = Function()
left_interval = -1
right_interval = 1
n = 100
eps = 1

draw_function_graph(my_func, left_interval, right_interval)

print()
print('your function is:', my_func.print_function())
print()
print('Simpson answer', simpson_method(my_func, left_interval, right_interval, n, eps, percent=True))
print('Current answer: ', my_func.get_value_integrate(left_interval, right_interval))

# examples
# sin(x) [0; 1]
# sin(x) [-1; 1]
# sin(x) [-100; 100] n = 100, n = 1000
# 5 * x ** 3 + 2 * x ** 2 - 10 * x + 3 [0; 4]
# log(x) [-1; 1]
# 2.7 ** (1 / x) [-1; 1]
# 2 * x * (abs(x + 3) / (x + 3)) + 6 [-4; -2]
# 2 * x * (abs(x + 3) / (x + 3)) + 6 [-3.2; -2.8] n = 10000, n = 100 + idea
# 2 * x * (abs(x + 3) / (x + 3)) + 6 [-3; -2]
