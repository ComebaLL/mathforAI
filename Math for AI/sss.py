import numpy as np

def gaussian_elimination(matrix):
    """
    Приводит матрицу к виду, где под главной диагональю нули,
    используя перестановки строк и элементарные преобразования.

    Args:
        matrix: Входная матрица (list of lists или numpy array)

    Returns:
        Матрица в приведенном виде (numpy array)
    """
    # Преобразуем входные данные в numpy array для удобства
    A = np.array(matrix, dtype=float)
    num_rows, num_cols = A.shape

    # i - индекс ведущего столбца и ведущей строки
    for i in range(min(num_rows, num_cols)):
        # Шаг 1: Поиск опорного элемента (максимального по модулю) в текущем столбце, начиная с i-й строки
        max_row_index = i
        for k in range(i + 1, num_rows):
            if abs(A[k, i]) > abs(A[max_row_index, i]):
                max_row_index = k

        # Шаг 2: Перестановка строк (если необходимо)
        if max_row_index != i:
            # Меняем местами строку i и строку max_row_index
            A[[i, max_row_index]] = A[[max_row_index, i]]
            print(f"Переставили строки {i} и {max_row_index}:")
            print(A, "\n")

        # Если после перестановки опорный элемент всё ещё ноль, пропускаем столбец
        if abs(A[i, i]) < 1e-10: # Используем малое число для сравнения с нулем
            print(f"Элемент A[{i}, {i}] слишком мал, пропускаем столбец.")
            continue

        # Шаг 3: Обнуление элементов ниже ведущего
        for j in range(i + 1, num_rows):
            # Вычисляем множитель для строки j: на что умножить ведущую строку i, чтобы обнулить элемент A[j, i]
            multiplier = A[j, i] / A[i, i]
            print(f"Умножаем строку {i} на {multiplier:.2f} и вычитаем из строки {j}")

            # Вычитаем из строки j ведущую строку i, умноженную на множитель
            # Это эквивалентно: A[j] = A[j] - multiplier * A[i]
            A[j, i:] = A[j, i:] - multiplier * A[i, i:]
            # Явно обнуляем элемент, чтобы избежать ошибок округления (например, -0.0)
            A[j, i] = 0.0

            print(A, "\n")

    return A

# --- Пример использования ---
if __name__ == "__main__":
    # Пример матрицы
    input_matrix = [
        [0, -4, -1, 1 ,2, 1],
        [-4, 0, -4, -3, 0, -4],
        [-1, -4, 0, 1, 1, 4],
        [1, -3, 1, 0, 0, -2],
        [2, 0, 1, 0, 0, -3]
    ]

    print("Исходная матрица:")
    print(np.array(input_matrix), "\n")

    result = gaussian_elimination(input_matrix)

    print("\nКонечный результат (под главной диагональю ~0):")
    print(result)