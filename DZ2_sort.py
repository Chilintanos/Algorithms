import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 1
def task1():
    numbers = [5, 2, 9, 1, 5]
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] < numbers[j]:
                numbers[i], numbers[j] = numbers[j], numbers[i]
    return print(numbers)


# 2
def task2():
    words = ["apple", "banana", "kiwi", "pear"]
    return print(sorted(words, key=lambda x: len(x)))



# 3
def task3():
    numbers = [123, 45, 6, 789]
    def digit_sum(n):
        return sum(int(d) for d in str(abs(n)))
    return print(sorted(numbers, key=digit_sum))


# 4
def task4():
    words = ["apple", "banana", "apple", "cherry", "banana"]
    freq = {word: words.count(word) for word in set(words)}
    return print(sorted(freq, key=lambda x: (-freq[x], x)))



# 5
def task5():
    numbers = [5, 2, 9, 1]
    indexed = list(enumerate(numbers))
    for i in range(len(indexed)):
        for j in range(i + 1, len(indexed)):
            if indexed[i][1] > indexed[j][1]:
                indexed[i], indexed[j] = indexed[j], indexed[i]
    return print(indexed)


# 6
def task6():
    numbers = [5, 2, 9, 1, 5, 2]
    unique = []
    for n in numbers:
        if n not in unique:
            unique.append(n)
    return print(sorted(unique))


# 7
def task7():
    grades = [4, 5, 3, 4, 5, 5, 4, 3, 2, 4]
    plt.hist(grades, bins=range(2, 7), color='skyblue', edgecolor='black')
    plt.title("Распределение оценок студентов")
    plt.xlabel("Оценка")
    plt.ylabel("Количество студентов")
    plt.show()


# 8
def task8():
    x = np.linspace(-10, 10, 200)
    y = x ** 2
    plt.plot(x, y, color='red', linewidth=2)
    plt.title("График функции y = x²")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()



# 9
def task9():
    categories = ['Одежда', 'Техника', 'Продукты', 'Игрушки']
    sales = [40, 25, 20, 15]
    plt.pie(sales, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title("Распределение продаж по категориям")
    plt.show()


# 10
def task10():
    x = np.linspace(-2 * math.pi, 2 * math.pi, 400)
    y1 = np.sin(x)
    y2 = np.cos(x)
    plt.plot(x, y1, label='sin(x)', color='blue', linestyle='-')
    plt.plot(x, y2, label='cos(x)', color='red', linestyle='--')
    plt.title("Функции sin(x) и cos(x)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()



# 11
def task11():
    x = np.arange(1, 6)
    y = [3, 7, 2, 8, 5]
    plt.plot(x, y, 'o-', label='Линия', alpha=0.7)
    plt.bar(x, y, color='orange', alpha=0.4, label='Столбцы')
    plt.scatter(x, y, color='red', label='Точки', zorder=5)
    plt.title("Комбинированный график")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()

# 12
def task12():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(-4, 4, 100)
    y = np.linspace(-4, 4, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X ** 2 + Y ** 2))
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9)
    ax.set_title("3D-график z = sin(√(x² + y²))")
    plt.show()


def main():
    tasks = {i: globals()[f"task{i}"] for i in range(1,13)}
    print("Выберите номер упражнения (1–12): ")
    num = int(input("> "))
    if num in tasks:
        tasks[num]()
    else:
        print("Нет такого задания!")

if __name__ == "__main__":
    main()