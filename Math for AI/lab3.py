import math
import random

def f(x):
    """
    Функция f(x1, x2, x3) = sqrt(0.4(x1-0.6)**2 + 0.4(x2-0.5)**2 + 0.8(x3-0.3)**2 + 8)
    """
    x1, x2, x3 = x
    return math.sqrt(0.4 * (x1 - 0.6)**2 + 0.4 * (x2 - 0.5)**2 + 0.8 * (x3 - 0.3)**2 + 8)

def simulated_annealing():
    # Инициализация переменных - задаем все три координаты
    x_old = [-1.3, 2.7, 1.0]  # x1 = -1.3, x2 = 2.7, x3 = 1.0
    x_new = [0.0, 0.0, 0.0]
    
    t = 1000
    t_min = 0.001
    max_step = 1.1
    k = 0
    
    # Вывод заголовка таблицы
    print("k    | t        | x1       | x2       | x3       | f(x)     | df       | P(перех) | сообщение")
    print("-" * 90)
    
    # Вывод начальной точки
    print(f"{k:4d} | {t:8.3f} | {x_old[0]:8.3f} | {x_old[1]:8.3f} | {x_old[2]:8.3f} | {f(x_old):8.3f} | {'0':>8} | {'0':>8} | начальная точка")
    
    results = []
    results.append([k, t, x_old[0], x_old[1], x_old[2], f(x_old), 0, 0, "начальная точка"])
    
    while t > t_min:
        k += 1
        t = 0.9 * t
        
        # Генерация случайного шага для всех трех координат
        a = max_step * (random.random() - 0.5)
        b = max_step * (random.random() - 0.5)
        c = max_step * (random.random() - 0.5)  # шаг для x3
        
        x_new[0] = x_old[0] + a
        x_new[1] = x_old[1] + b
        x_new[2] = x_old[2] + c
        
        df = f(x_new) - f(x_old)
        
        if df <= 0:
            # Переход в новую точку (улучшение)
            x_old = x_new.copy()
            exp_prob = 0
            message = "перешли в новую точку с уменьшением f(x)"
        else:
            # Вероятностный переход (ухудшение)
            exp_prob = math.exp(-df / t)
            if random.random() < exp_prob:
                x_old = x_new.copy()
                message = "перешли в новую точку с увеличением f(x)"
            else:
                message = "остались в старой точке"
                exp_prob = math.exp(-df / t)  
        
        # Вывод текущей итерации
        print(f"{k:4d} | {t:8.3f} | {x_old[0]:8.3f} | {x_old[1]:8.3f} | {x_old[2]:8.3f} | {f(x_old):8.3f} | {df:8.3f} | {exp_prob:8.3f} | {message}")
        
        results.append([k, t, x_old[0], x_old[1], x_old[2], f(x_old), df, exp_prob, message])
    
    return results

# Запуск алгоритма
if __name__ == "__main__":
    
    results = simulated_annealing()
    
    # Вывод финального результата
    final_point = results[-1]
    print(f"\nФинальный результат после {len(results)-1} итераций:")
    print(f"x* = ({final_point[2]:.6f}, {final_point[3]:.6f}, {final_point[4]:.6f})")
    print(f"f(x*) = {final_point[5]:.6f}")
    
    # Сравнение с истинным минимумом
    true_min = math.sqrt(8)
    true_min_point = (0.6, 0.5, 0.3)
    distance = math.sqrt((final_point[2] - 0.6)**2 + (final_point[3] - 0.5)**2 + (final_point[4] - 0.3)**2)
    
    print(f"\nТочка минимума:")
    print(f"x_true = {true_min_point}")
    print(f"f(x_true) = {true_min:.6f}")
    print(f"Расстояние до точки минимума: {distance:.6f}")
    print(f"Разница значений функции: {abs(final_point[5] - true_min):.6f}")