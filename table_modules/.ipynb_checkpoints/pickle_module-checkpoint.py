import pickle
from .table_operations import auto_detect_column_types

def load_table(file_path, auto_detect_types=False):
    """
    Загружает таблицу из Pickle файла.

    Args:
        file_path (str): Путь к Pickle файлу.
        auto_detect_types (bool): Если True, автоматически определяет типы столбцов.

    Returns:
        dict: Таблица с ключами 'header' и 'rows'.
    """
    try:
        with open(file_path, mode="rb") as file:
            table = pickle.load(file)

        if auto_detect_types:
            table['column_types'] = auto_detect_column_types(table)

        return table
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке Pickle файла {file_path}: {e}")

def save_table(table, file_path):
    """
    Сохраняет таблицу в Pickle-файл.
    """
    try:
        with open(file_path, mode='wb') as file:
            pickle.dump(table, file)
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении Pickle файла {file_path}: {e}")
        