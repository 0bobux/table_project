def save_table(table, file_path):
    """
    Сохраняет таблицу в текстовый файл в удобном для чтения виде.

    Args:
        table (dict): Таблица, представленная в виде словаря с ключами:
        file_path (str): Путь к текстовому файлу, в который будет сохранена таблица.

    Raises:
        ValueError: Если возникает ошибка при сохранении файла (например, проблемы с доступом к файлу).
    """
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write('\t'.join(table['header']) + '\n') # записываем заголовок, объединяя элементы через табуляцию
            for row in table['rows']:
                file.write('\t'.join(row) + '\n') # записываем каждую строку таблицы
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении текстового файла {file_path}: {e}")
        
