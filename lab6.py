import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#  Ввод размерности
while True:
    try:
        n = int(input("Введите размерность матрицы - n(от 4 до 50):\n"))
        if 4 <= n <= 50:
            break
        else:
            print("Недопустимая размерность")
    except ValueError:
        print("Недопустимая размерность")
ndiv2 = n // 2

#  Ввод числа k
while True:
    try:
        k = int(input("Введите K (целое число):\n"))
        break
    except ValueError:
        print("Введенно некорректное значение")

start = time.time()

#  Создание матрицы А
A = np.random.randint(-10, 10, (n, n))
print(f"Сгенерированная матрица А: \n{A}")

#  Иницилизация матрицы F
F = np.copy(A)
print(f"\nМатрица F до преобразований: \n{F}")

#  Подсчет нулевых элементов в С
count1, count2 = 0, 0
for i in range(n):
    for j in range(n):
        if j > (ndiv2 - (n - 1) % 2) and i < ndiv2:
            if F[i][j] == 0 and j % 2 == 0:
                count1 += 1
            elif F[i][j] == 0 and j % 2 != 0:
                count2 += 1

#  Преобразование матрицы F согласно условию
if count1 > count2:  # Если верно, то меняем местами С и В симметрично
    for i in range(ndiv2):
        F[i] = F[i][::-1]
else:  # Иначе, меняем C и E несимметрично
    for i in range(n):
        for j in range(n):
            if j > (ndiv2 - (n - 1) % 2) and i < ndiv2:
                if n % 2 == 0:
                    F[i][j] = F[i + ndiv2][j]
                    F[i + ndiv2][j] = A[i][j]
                else:
                    F[i][j] = F[i + ndiv2 + 1][j]
                    F[i + ndiv2 + 1][j] = A[i][j]
print(f"\nМатрица F после преобразований: \n{F}")

#  Вычисление согласно условию
if np.linalg.det(A) == 0 or np.linalg.det(F) == 0:  # Проверка определителей матриц
    print("\nМатрица F и(или) матрица A вырождена")
else:
    if np.linalg.det(A) > np.trace(F):  # Если верно, то вычисляем A*AT – K * FТ
        result = A * A.T - k * F.T
        print(f"\nФинальный результат: \n{result}")
    else:  # Иначе, вычисляем (AТ +G-F^-1)*K
        result = (A.T + np.tril(A) - np.linalg.inv(F)) * k
        print(f"\nФинальный результат: \n{result}")

#  matplotlib
fig, ax = plt.subplots()
ax.set(xlabel='Столбец', ylabel='Значение')
ax.grid()
for j in range(n):
    ax.plot([i for i in range(n)], result[j][::])
plt.show()

#  seaborn
sns.set_theme(style='darkgrid')
sns.lineplot(data=result)
plt.xlabel('Строка')
plt.ylabel('Значение')
plt.show()

sns.boxplot(data=result)
plt.xlabel('Столбец')
plt.ylabel('Значение')
plt.show()

finish = time.time()
print(f"Время работы программы: {finish - start} секунд")
