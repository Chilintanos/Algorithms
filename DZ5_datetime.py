from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta  # нужно установить: pip install python-dateutil


# 1
def get_current_datetime(user_date=None):
    return user_date if user_date else datetime.now()


# 2
def convert_string_to_datetime(date_string: str):
    return datetime.strptime(date_string, "%b %d %Y %I:%M%p")


# 3
def subtract_week(given_date: datetime):
    return given_date - timedelta(days=7)


# 4
def format_date_russian(given_date: datetime):
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    return f"{days[given_date.weekday()]}, {given_date.day} {months[given_date.month - 1]} {given_date.year} г."


# 5
def get_weekday_name(given_date: datetime):
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    return days[given_date.weekday()]


# 6
def add_week_and_hours(given_date: datetime):
    return given_date + timedelta(days=7, hours=12)


# 7
def current_time_in_milliseconds():
    return int(datetime.now().timestamp() * 1000)


# 8
def datetime_to_string(given_date: datetime):
    return given_date.strftime("%Y-%m-%d %H:%M:%S")


# 9
def add_four_months(given_date: date):
    return given_date + relativedelta(months=4)


# 10
def days_between(date_1: datetime, date_2: datetime):
    return abs((date_2 - date_1).days)



def main():
    user_input = input("Введите сегодняшнюю дату (в формате ГГГГ-ММ-ДД) или просто Enter для текущей: ").strip()

    if user_input:
        current_date = datetime.strptime(user_input, "%Y-%m-%d")
    else:
        current_date = datetime.now()
        print(f" Используется текущая дата: {current_date.strftime('%Y-%m-%d')}")

    print("\n=== РЕЗУЛЬТАТЫ ===")

    # 1
    print("1 Текущая дата и время:", get_current_datetime(current_date))

    # 2
    date_str = "Feb 25 2020 4:20PM"
    print("2 Преобразовано из строки:", convert_string_to_datetime(date_str))

    # 3
    print("3 Неделя назад:", subtract_week(current_date).date())

    # 4
    print("4 Форматированный вывод:", format_date_russian(current_date))

    # 5
    print("5 День недели:", get_weekday_name(current_date))

    # 6
    print("6 Через 7 дней и 12 часов:", add_week_and_hours(current_date))

    # 7
    print("7 Время в миллисекундах:", current_time_in_milliseconds())

    # 8
    print("8 В строку:", datetime_to_string(current_date))

    # 9
    print("9 Через 4 месяца:", add_four_months(current_date.date()))

    # 10
    d1 = datetime(2020, 2, 25)
    d2 = datetime(2020, 9, 17)
    print("10 Разница между", d1.date(), "и", d2.date(), "=", days_between(d1, d2), "дней")

if __name__ == "__main__":
    main()