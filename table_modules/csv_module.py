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
    """
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = [row for row in reader]

        table = {"header": header, "rows": rows}

        if auto_detect_types:
            table['column_types'] = auto_detect_column_types(table)

        return table
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке CSV файла {file_path}: {e}")

def save_table(table, file_path):
    """
    Сохраняет таблицу в CSV-файл.
    """
    try:
        with open(file_path, mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(table['header'])
            writer.writerows(table['rows'])
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении файла {file_path}: {e}")
        