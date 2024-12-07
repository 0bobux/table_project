def save_table(table, file_path):
    """
    Сохраняет таблицу в текстовый файл в удобном для чтения виде.
    """
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            file.write('\t'.join(table['header']) + '\n')
            for row in table['rows']:
                file.write('\t'.join(row) + '\n')
    except Exception as e:
        raise ValueError(f"Ошибка при сохранении текстового файла {file_path}: {e}")
        