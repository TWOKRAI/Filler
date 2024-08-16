import numpy as np
from scipy.optimize import curve_fit


# Пример данных
# Пиксельные координаты (x, y)
pixel_points = np.array([
    (0, 15.5),
    (0, 19.5),
    (0, 22.6),
    (0, 25.4),
    (0, 27.5), 
    (0, 29.3), 
    (0, 30.9), 
])

# Реальные координаты (x_real, y_real)
real_points = np.array([
    (0, 12.5),
    (0, 15.5),
    (0, 18.5),
    (0, 21.5),
    (0, 24.5),
    (0, 27.5),
    (0, 30.5),
])

# Функция для подбора
def quadratic_function(y, a, b):
    return a * y + b * y**2

# Подбор коэффициентов
params, _ = curve_fit(quadratic_function, pixel_points[:, 1], real_points[:, 1])
a, b = params

print(f"a = {a}, b = {b}")