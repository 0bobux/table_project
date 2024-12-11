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

    Raises:
        ValueError: Если возникает ошибка при загрузке файла.
    """
    try:
        with open(file_path, mode="rb") as file: # (read binary), т.к. Pickle сохраняет данные в бинарном формате.
            table = pickle.load(file) # восстанавливает объект из бинарного файла.

        if auto_detect_types:
            table['column_types'] = auto_detect_column_types(table)

        return table
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке Pickle файла {file_path}: {e}")

def save_table(table, file_path):
    """
    Сохраняет таблицу в Pickle-файл.

    Args:
        table (dict): Таблица, представленная в виде словаря с ключами.
        file_path (str): Путь к файлу, в который будет сохранена таблица.

    Raises:
        ValueError: Если возникает ошибка при сохранении файла (например, проблемы с доступом к файлу).
    """
    try:
        with open(file_path, mode='wb') as file: # (write binary)
            pickle.dump(table, file) # сериализует переданный объект table и записывает его в файл.
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении Pickle файла {file_path}: {e}")
        
