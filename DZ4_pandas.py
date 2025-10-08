import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def create_sales_csv():
    data = {
        'date': pd.date_range('2023-01-01', periods=100),
        'city': np.random.choice(['Москва', 'СПб', 'Екатеринбург'], 100),
        'category': np.random.choice(['Электроника', 'Одежда', 'Продукты'], 100),
        'product_id': np.random.randint(1000, 2000, 100),
        'sales': np.random.randint(1000, 30000, 100),
        'quantity': np.random.randint(1, 10, 100),
        'price': np.random.randint(500, 5000, 100)
    }
    df = pd.DataFrame(data)
    df.to_csv('sales.csv', index=False)
    print("✅ Файл 'sales.csv' создан!")



# 2
def read_data():
    df = pd.read_csv('sales.csv', parse_dates=['date'])
    print("Первые 5 строк:")
    print(df.head())

    print("\n Проверка пропущенных значений:")
    print(df.isna().sum())

    print("\n Основная статистика:")
    print(df.describe())

    return df



# 3
def filter_data(df):
    print("\n Продажи больше 1000:")
    print(df[df['sales'] > 1000].head())

    print("\n Записи за период 2023-01-10 — 2023-01-23:")
    mask = (df['date'] >= '2023-01-10') & (df['date'] <= '2023-01-20')
    print(df[mask].head())

    print("\n Фильтрация по городу и категории:")
    filtered = df[(df['city'] == 'Москва') & (df['category'] == 'Электроника')]
    print(filtered.head())


# 4
def group_data(df):
    print("\n Суммарные продажи по городам:")
    print(df.groupby('city')['sales'].sum())

    print("\n Средний чек по категориям:")
    df['check'] = df['sales'] / df['quantity']
    print(df.groupby('category')['check'].mean())

    print("\n Топ-5 по продажам:")
    print(df.sort_values('sales', ascending=False).head(5))


# 5.
def handle_nan(df):
    # Искусственно создадим пропуски
    df.loc[5:10, 'sales'] = np.nan
    print("\nДо заполнения пропусков:\n", df.isna().sum())

    df['sales'] = df['sales'].fillna(df['sales'].mean())
    print("\nПосле заполнения средним:\n", df.isna().sum())

    df_clean = df.dropna()
    print(f"\n После удаления NaN осталось строк: {len(df_clean)}")

    df['total'] = df['sales'] * df['quantity']
    print("\nНовый столбец 'total':")
    print(df[['sales', 'quantity', 'total']].head())

    return df

# 6
def time_series(df):
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    print("\n Добавлены столбцы month и year:")
    print(df[['date', 'month', 'year']].head())

    print("\n Скользящее среднее:")
    df['rolling_sales'] = df['sales'].rolling(window=7).mean()
    print(df[['date', 'sales', 'rolling_sales']].head(15))

    print("\n Агрегация по кварталам:")
    quarterly = df.resample('Q', on='date')['sales'].sum()
    print(quarterly)


# 7
def visualize(df):
    plt.figure(figsize=(16, 8))

    # График продаж по времени
    plt.subplot(2, 2, 1)
    plt.plot(df['date'], df['sales'], label='Продажи')
    plt.title('Продажи по времени')
    plt.xlabel('Дата')
    plt.ylabel('Продажи')
    plt.legend()

    # Гистограмма
    plt.subplot(2, 2, 2)
    plt.hist(df['sales'], bins=15, color='skyblue', edgecolor='black')
    plt.title('Распределение продаж')

    # Корреляция
    plt.subplot(2, 1, 2)
    corr = df[['sales', 'quantity', 'price', 'total']].corr()
    plt.imshow(corr, cmap='coolwarm', interpolation='none')
    plt.colorbar(label='Коэффициент корреляции')
    plt.xticks(range(len(corr.columns)), corr.columns)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title('Корреляция между показателями')

    plt.tight_layout()
    plt.show()


# ---------------------------------------
# Главное меню
# ---------------------------------------
def main():
    print("\n=== Анализ данных о продажах ===")
    print("1. Создать CSV-файл")
    print("2. Загрузить и просмотреть данные")
    print("3. Фильтрация данных")
    print("4. Группировка данных")
    print("5. Работа с NaN и создание нового столбца")
    print("6. Временные ряды")
    print("7. Визуализация")
    print("0. Выход")

    df = None
    while True:
        try:
            choice = int(input("\nВведите номер задачи: "))
            if choice == 1:
                create_sales_csv()
            elif choice == 2:
                df = read_data()
            elif choice == 3 and df is not None:
                filter_data(df)
            elif choice == 4 and df is not None:
                group_data(df)
            elif choice == 5 and df is not None:
                df = handle_nan(df)
            elif choice == 6 and df is not None:
                time_series(df)
            elif choice == 7 and df is not None:
                visualize(df)
            elif choice == 0:
                print("Выход...")
                break
            else:
                print("⚠ Сначала загрузите данные (выберите 2)")
        except ValueError:
            print("Введите число!")


if __name__ == "__main__":
    main()
