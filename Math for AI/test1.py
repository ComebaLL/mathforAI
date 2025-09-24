__author__ = "Kuvykin N.D" 


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(x):
    """
    Функция x**4/4 + 4*x**3/3 - 17*x**2/2 - 60*x + y**4/4 - y**3 - 3*y**2 + 8*y
    x - массив из двух элементов [x, y]
    """
    return (x[0]**4/4 + 4*x[0]**3/3 - 17*x[0]**2/2 - 60*x[0] + 
            x[1]**4/4 - x[1]**3 - 3*x[1]**2 + 8*x[1])

def GradF(x):
    """
    Градиент функции f(x, y)
    """
    grad = np.zeros(2)
    # Производная по x
    grad[0] = x[0]**3 + 4*x[0]**2 - 17*x[0] - 60
    # Производная по y
    grad[1] = x[1]**3 - 3*x[1]**2 - 6*x[1] + 8
    return grad

def Plus(a, b):
    return a + b

def Minus(a, b):
    return a - b

def Mult(a, t):
    return a * t

def ScalProd(a, b):
    return np.dot(a, b)

def Length(a):
    return np.linalg.norm(a)

def Swenn(x, d):
    t = 0
    x_l = Minus(x, Mult(GradF(x), t - d))
    x_c = Minus(x, Mult(GradF(x), t))
    x_h = Minus(x, Mult(GradF(x), t + d))
    
    a = 0
    b = 0
    
    if (f(x_l) < f(x_c)) and (f(x_c) > f(x_h)):
        print("Функция не унимодальна!!!")
        a = 0
        b = 0
    elif (f(x_l) > f(x_c)) and (f(x_c) < f(x_h)):
        a = t - d
        b = t + d
    else:
        if (f(x_l) > f(x_c)) and (f(x_c) > f(x_h)):
            h = d
        elif (f(x_l) < f(x_c)) and (f(x_c) < f(x_h)):
            h = -d
        else:
            h = d
            
        t_prev = t - h
        x_prev = Minus(x, Mult(GradF(x), t_prev))
        t_curr = t
        x_curr = Minus(x, Mult(GradF(x), t_curr))
        t_next = t + h
        x_next = Minus(x, Mult(GradF(x), t_next))
        
        while not ((f(x_prev) > f(x_curr)) and (f(x_curr) < f(x_next))):
            h = 2 * h
            t_prev = t_curr
            x_prev = x_curr
            t_curr = t_next
            x_curr = x_next
            t_next = t + h
            x_next = Minus(x, Mult(GradF(x), t_next))
            
        if h > 0:
            a = t_prev
            b = t_next
        else:
            a = t_next
            b = t_prev
            
    return np.array([a, b])

def HalfDivision(x, ab, eps):
    k = 0
    t0 = ab[0]
    x0 = Minus(x, Mult(GradF(x), t0))
    t4 = ab[1]
    x4 = Minus(x, Mult(GradF(x), t4))
    
    while t4 - t0 >= 2 * eps:
        t1 = (3 * t0 + t4) / 4
        x1 = Minus(x, Mult(GradF(x), t1))
        t2 = (2 * t0 + 2 * t4) / 4
        x2 = Minus(x, Mult(GradF(x), t2))
        t3 = (t0 + 3 * t4) / 4
        x3 = Minus(x, Mult(GradF(x), t3))
        
        if (f(x1) > f(x2)) and (f(x2) < f(x3)):
            t0 = t1
            t4 = t3
        elif (f(x1) > f(x2)) and (f(x2) > f(x3)):
            t0 = t2
        elif (f(x1) < f(x2)) and (f(x2) < f(x3)):
            t4 = t2
            
        k += 1
        
    return (t0 + t4) / 2

def plot_3d_function_and_points(history_points):
    """
    Упрощенная визуализация: только 3D график с точками оптимизации
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Создаем сетку для построения поверхности
    x = np.linspace(-10, 10, 100)
    y = np.linspace(-10, 10, 100)
    X, Y = np.meshgrid(x, y)
    Z = f([X, Y])
    
    # 3D поверхность функции
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6, edgecolor='none')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(x,y)')
    ax.set_title('3D поверхность функции')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Отмечаем точки оптимизации
    history_x = [point[0] for point in history_points]
    history_y = [point[1] for point in history_points]
    history_z = [f(point) for point in history_points]
    
    # Траектория оптимизации
    ax.plot(history_x, history_y, history_z, 'r-', linewidth=2, alpha=0.7, label='Траектория')
    
    # Все точки оптимизации
    ax.scatter(history_x, history_y, history_z, c='red', s=30, alpha=0.8)
    
    # Начальная точка
    ax.scatter(history_x[0], history_y[0], history_z[0], 
              c='blue', s=150, marker='*', label='Начальная точка')
    
    # Конечная точка (найденный минимум)
    ax.scatter(history_x[-1], history_y[-1], history_z[-1], 
              c='green', s=150, marker='D', label='Найденный минимум')
    
    ax.legend()
    plt.tight_layout()
    plt.show()

def Main():
    """
    Основная функция градиентного спуска с визуализацией
    """
    # Начальное приближение [x, y]
    x_new = np.array([5.081, 2.921])
    k = 0
    
    
    history_points = [x_new.copy()]
    
    print(f"Itr {k}: x = {x_new[0]:.6f}, y = {x_new[1]:.6f}, f(x,y) = {f(x_new):.6f}")
    
    while True:
        x_old = x_new.copy()
        alpha = HalfDivision(x_old, Swenn(x_old, 0.01), 0.0001)
        x_new = Minus(x_old, Mult(GradF(x_old), alpha))
        k += 1
        
        history_points.append(x_new.copy())
        
        print(f"Iteration {k}: x = {x_new[0]:.6f}, y = {x_new[1]:.6f}, f(x,y) = {f(x_new):.6f}")
        
        # Критерии остановки
        grad_norm = Length(GradF(x_new))
        step_norm = Length(Minus(x_new, x_old))
        
        if grad_norm < 0.000001 or step_norm < 0.00001 or k >=4:
            break
    
    # Визуализация
    plot_3d_function_and_points(history_points)


if __name__ == "__main__":
    Main()