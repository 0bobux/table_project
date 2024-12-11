import csv
from .table_operations import auto_detect_column_types

def load_table(file_path, auto_detect_types=False):
    """
    Загружает таблицу из CSV файла.

    Args:
        file_path (str): Путь к CSV файлу.
        auto_detect_types (bool): Если True, автоматически определяет типы столбцов.

    Returns:
        dict: Таблица с ключами 'header' и 'rows'.

    Raises:
        ValueError: Если возникает ошибка при загрузке файла.
    """
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file) # reader для чтения строк
            header = next(reader) # читаем 1 строку как заголовок
            rows = [row for row in reader] # список списков каждый внутренний список представляет одну строку из CSV

        table = {"header": header, "rows": rows} # внутреннее представление таблицы

        if auto_detect_types: # если параметр auto_detect_types=True
            table['column_types'] = auto_detect_column_types(table) # функция создает новый ключ и возвращает вложеный словарь с определёнными типами данных для каждого столбца

        return table
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке CSV файла {file_path}: {e}")

def save_table(table, file_path):
    """
    Сохраняет таблицу в CSV-файл.

    Args:
        table (dict): Таблица в виде словаря с ключами header и rows.
        file_path (str): Путь, куда нужно сохранить файл.

    Returns:
        None: Функция ничего не возвращает.

    Raises:
        ValueError: Если возникает ошибка при сохранении файла.
    """
    try:
        with open(file_path, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file) # для записи данных в файл.
            writer.writerow(table['header']) # записывает список заголовков как первую строку.
            writer.writerows(table['rows']) # записывает все строки таблицы.
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении файла {file_path}: {e}")
        
