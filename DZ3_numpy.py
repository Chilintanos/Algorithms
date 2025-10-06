import numpy as np

# 1
def task1():
    a = np.zeros(10)
    print(a)

# 2
def task2():
    a = np.ones(10)
    print(a)

# 3
def task3():
    a = np.full(10, 2.5)
    print(a)

# 4
def task4():
    a = np.zeros(10)
    a[4] = 1
    print(a)

# 5
def task5():
    a = np.arange(10, 50)
    print(a)

# 6.
def task6():
    a = np.arange(10, 50)
    print("Исходный:", a)
    print("Развернутый:", a[::-1])

# 7
def task7():
    a = np.arange(9).reshape(3, 3)
    print(a)

# 8
def task8():
    a = np.array([1, 2, 0, 0, 4, 0])
    indices = np.nonzero(a)
    print("Массив:", a)
    print("Ненулевые индексы:", indices)

# 9
def task9():
    a = np.random.random((3, 3, 3))
    print(a)

# 10
def task10():
    a = np.random.random((10, 10))
    print("Минимум:", a.min())
    print("Максимум:", a.max())

# 11
def task11():
    a = np.ones((5, 5))
    a[1:-1, 1:-1] = 0
    print(a)

# 12
def task12():
    a = np.zeros((8, 8), dtype=int)
    a[1::2, ::2] = 1
    a[::2, 1::2] = 1
    print(a)

# 13
def task13():
    a = np.random.randint(1, 10, (5, 3))
    b = np.random.randint(1, 10, (3, 2))
    print("A:\n", a)
    print("B:\n", b)
    c = np.dot(a, b)
    print("Результат A×B:\n", c)

# 14
def task14():
    a = np.random.randint(1, 100, (5, 7))
    print("Исходная матрица:\n", a)
    a = np.delete(a, [3, 5], axis=1)
    print("После удаления колонок 3 и 5:\n", a)

# 15
def generate():
    for x in range(10):
        yield x

def task15():
    a = np.fromiter(generate(), dtype=int)
    print(a)

def task16():
    lst = [[1, 2, 3], [4, 5, 6]] 
    arr = np.array(lst, dtype=np.int32)   
    print("Исходный список:", lst)
    print("Массив NumPy (int32):\n", arr)
    print("Тип данных:", arr.dtype)

def task17():
    a = np.array([1, 2, 3])
    b = np.array([1, 2, 3])
    c = np.array([1, 2, 4])
    
    print("a и b", np.array_equal(a, b)) 
    print("a и c", np.array_equal(a, c))  

def task18():
    arr = np.arange(5)
    print("Исходный массив:", arr)

    arr.flags.writeable = False

    print("Попробуем изменить элемент и получаем...")
    try:
        arr[0] = 99
    except ValueError as e:
        print("Ошибка:", e)

def main():
    tasks = {i: globals()[f"task{i}"] for i in range(1,19)}
    print("Выберите номер упражнения (1–18): ")
    num = int(input("> "))
    if num in tasks:
        tasks[num]()
    else:
        print("Нет такого задания!")

if __name__ == "__main__":
    main()