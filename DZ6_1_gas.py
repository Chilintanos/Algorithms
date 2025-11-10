import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from datetime import datetime
import matplotlib.dates as mdates
from scipy import interpolate



df = pd.read_csv('zap_data_22.csv')

df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')


def safe_json_extract(json_str, key):
    if pd.isna(json_str):
        return None
    try:
        data = json.loads(json_str)
        return data.get(key, None)
    except (json.JSONDecodeError, KeyError):
        return None

df['LLS_0'] = df['can_data'].apply(lambda x: safe_json_extract(x, 'LLS_0'))
df['xLLS_71'] = df['can_data'].apply(lambda x: safe_json_extract(x, 'xLLS_71'))


df_fuel = df[df['LLS_0'].notna()].copy()

# 1 Графики скорости от времени
plt.figure(figsize=(15, 10))

# Фильтрация данных со скоростью
speed_data = df[df['speed'].notna()]

if not speed_data.empty:

    for i in range(12):
        plt.subplot(4, 3, i+1)
        
        # Разделение данных на 12 временных интервалов
        time_range = pd.date_range(start=speed_data['datetime'].min(), 
                                  end=speed_data['datetime'].max(), periods=13)
        
        time_chunk = speed_data[(speed_data['datetime'] >= time_range[i]) & 
                               (speed_data['datetime'] < time_range[i+1])]
        
        if not time_chunk.empty:
            plt.plot(time_chunk['datetime'], time_chunk['speed'])
            plt.title(f'Скорость: {time_range[i].strftime("%Y-%m-%d %H:%M")} - {time_range[i+1].strftime("%H:%M")}')
            plt.ylabel('Скорость')
            plt.xticks(rotation=45)
            plt.grid(True)
        else:
            plt.text(0.5, 0.5, 'Нет данных', ha='center', va='center', transform=plt.gca().transAxes)

    plt.tight_layout()
    plt.show()
else:
    print("Нет данных о скорости для построения графиков")

# 2. Улучшенный алгоритм обнаружения заправок и сливов
def detect_refuels_drains(fuel_data, time_data, threshold=10, min_duration=10):
    """
        fuel_data: данные уровня топлива
        time_data: временные метки
        threshold: порог изменения для обнаружения
        min_duration: минимальная продолжительность изменения (в секундах)
    """
    refuels = []
    drains = []
    
    for i in range(1, len(fuel_data)):
        if i >= len(fuel_data) - 1:
            continue
            
        current_fuel = fuel_data.iloc[i]
        prev_fuel = fuel_data.iloc[i-1]
        
        # Проверяем, что данные существуют
        if pd.isna(current_fuel) or pd.isna(prev_fuel):
            continue
            
        diff = current_fuel - prev_fuel
        
        # Проверяем продолжительность изменения
        if i > 0 and i < len(time_data) - 1:
            time_diff = (time_data.iloc[i] - time_data.iloc[i-1]).total_seconds()
            
            if diff > threshold and time_diff < min_duration:  
                refuels.append(i)
            elif diff < -threshold and time_diff < min_duration:  
                drains.append(i)
    
    return refuels, drains

# Применение алгоритма к данным с топливом
if not df_fuel.empty:
    refuels, drains = detect_refuels_drains(df_fuel['LLS_0'], df_fuel['datetime'])
    
    print(f"Обнаружено заправок: {len(refuels)}")
    print(f"Обнаружено сливов: {len(drains)}")
    
    # 3. Графики уровня топлива с заправками и сливами
    plt.figure(figsize=(15, 12))
    
    for i in range(12):
        plt.subplot(4, 3, i+1)
        
        # Разделение данных на 12 интервалов
        time_range = pd.date_range(start=df_fuel['datetime'].min(), 
                                  end=df_fuel['datetime'].max(), periods=13)
        
        time_chunk = df_fuel[(df_fuel['datetime'] >= time_range[i]) & 
                           (df_fuel['datetime'] < time_range[i+1])]
        
        if not time_chunk.empty:
            # Построение графика уровня топлива
            plt.plot(time_chunk['datetime'], time_chunk['LLS_0'], 
                    label='Уровень топлива', linewidth=1)
            
            # Отметка заправок и сливов в этом интервале
            chunk_refuels = [idx for idx in refuels if idx in time_chunk.index]
            chunk_drains = [idx for idx in drains if idx in time_chunk.index]
            
            if chunk_refuels:
                plt.scatter(time_chunk.loc[chunk_refuels, 'datetime'], 
                           time_chunk.loc[chunk_refuels, 'LLS_0'], 
                           color='green', s=30, label='Заправки', zorder=5, marker='^')
            
            if chunk_drains:
                plt.scatter(time_chunk.loc[chunk_drains, 'datetime'], 
                           time_chunk.loc[chunk_drains, 'LLS_0'], 
                           color='red', s=30, label='Сливы', zorder=5, marker='v')
            
            plt.title(f'Уровень топлива: {time_range[i].strftime("%m-%d %H:%M")} - {time_range[i+1].strftime("%H:%M")}')
            plt.ylabel('Уровень топлива')
            plt.legend(fontsize=8)
            plt.xticks(rotation=45, fontsize=8)
            plt.grid(True, alpha=0.3)
        else:
            plt.text(0.5, 0.5, 'Нет данных', ha='center', va='center', transform=plt.gca().transAxes)
    
    plt.tight_layout()
    plt.show()
    
    # 4. Сводный график всего периода
    plt.figure(figsize=(15, 6))
    plt.plot(df_fuel['datetime'], df_fuel['LLS_0'], linewidth=1, label='Уровень топлива')
    
    if refuels:
        plt.scatter(df_fuel.iloc[refuels]['datetime'], 
                   df_fuel.iloc[refuels]['LLS_0'], 
                   color='green', s=50, label='Заправки', zorder=5, marker='^')
    
    if drains:
        plt.scatter(df_fuel.iloc[drains]['datetime'], 
                   df_fuel.iloc[drains]['LLS_0'], 
                   color='red', s=50, label='Сливы', zorder=5, marker='v')
    
    plt.title('Уровень топлива за весь период с заправками и сливами')
    plt.ylabel('Уровень топлива')
    plt.xlabel('Время')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

else:
    print("Нет данных об уровне топлива для анализа")

# 5. Функция интерполяции для преобразования значений датчика в литры
def create_calibration_function(device_port=2):

    try:
        # Загрузка данных калибровки
        calib_df = pd.read_csv('calib.csv')
        
        # Поиск калибровочных данных для указанного порта
        calib_data = calib_df[calib_df['deviceid_port'] == device_port]['calibrating_data']
        
        if calib_data.empty:
            print(f"Не найдены калибровочные данные для порта {device_port}")
            return None
        
        # Парсинг JSON строки с калибровочными данными
        calib_json = calib_data.iloc[0]
        calib_points = json.loads(calib_json)
        
        # Извлечение значений input_value и output_value
        input_values = [point['input_value'] for point in calib_points]
        output_values = [point['output_value'] for point in calib_points]
        
        # Создание функции интерполяции
        calib_func = interpolate.interp1d(
            input_values, 
            output_values, 
            kind='linear', 
            bounds_error=False, 
            fill_value="extrapolate"
        )
        
        print(f"Загружена калибровочная кривая для порта {device_port}")
        print(f"Калибровочные точки: {len(calib_points)}")
        print(f"Диапазон входных значений: {min(input_values)} - {max(input_values)}")
        print(f"Диапазон выходных значений: {min(output_values)} - {max(output_values)}")
        
        return calib_func
        
    except FileNotFoundError:
        print("Файл calib.csv не найден")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке калибровочных данных: {e}")
        return None

# Создание функции калибровки
calib_func = create_calibration_function(device_port=2)  # Можно изменить на нужный порт

# Применение калибровки к данным
if not df_fuel.empty and calib_func is not None:
    df_fuel['liters'] = df_fuel['LLS_0'].apply(lambda x: calib_func(x) if pd.notna(x) else None)
    
    print("\nДополнительная информация:")
    print(f"Общий период данных: {df['datetime'].min()} - {df['datetime'].max()}")
    if not speed_data.empty:
        print(f"Максимальная скорость: {speed_data['speed'].max()}")
    print(f"Средний уровень топлива: {df_fuel['LLS_0'].mean():.2f}")
    if 'liters' in df_fuel.columns:
        print(f"Средний объем топлива: {df_fuel['liters'].mean():.2f} л")
        print(f"Минимальный объем: {df_fuel['liters'].min():.2f} л")
        print(f"Максимальный объем: {df_fuel['liters'].max():.2f} л")
else:
    print("Не удалось применить калибровку к данным")