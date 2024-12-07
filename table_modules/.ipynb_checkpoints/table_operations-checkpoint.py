def get_rows_by_number(table, start, stop = None, copy_table = False):
    """
    Возвращает строки таблицы по номеру (одна строка или интервал).
    """
    rows = table['rows'][start:stop]
    return {"header": table['header'], "rows": rows.copy()} if copy_table else {"header": table['header'], "rows": rows}

def get_rows_by_index(table, *values, copy_table=False):
    """
    Возвращает строки таблицы, где значения в первом столбце совпадают с переданными аргументами.
    """
    filtered_rows = [row for row in table['rows'] if row[0] in values]
    return {"header": table['header'], "rows": filtered_rows.copy()} if copy_table else {"header": table['header'], "rows": filtered_rows}

def get_column_types(table, by_number=True):
    """
    Возвращает словарь с типами значений для каждого столбца.
    """
    column_types = {}
    for i, col in enumerate(table['header']):
        values = [row[i] for row in table['rows'] if row[i] != ""]
        if all(v.isdigit() for v in values):
            column_type = int
        elif all(is_float(v) for v in values):
            column_type = float
        elif all(v.lower() in ("true", "false") for v in values):
            column_type = bool
        else:
            column_type = str
        column_types[i if by_number else col] = column_type
    return column_types

def set_column_types(table, types_dict, by_number=True):
    """
    Задаёт типы значений для столбцов.
    """
    for key, col_type in types_dict.items():
        col_index = key if by_number else table['header'].index(key)
        for row in table['rows']:
            try:
                row[col_index] = col_type(row[col_index])
            except ValueError:
                raise ValueError(f"Невозможно преобразовать значение '{row[col_index]}' в {col_type.__name__}")

def get_values(table, column=0):
    """
    Возвращает список значений из указанного столбца.
    """
    col_index = column if isinstance(column, int) else table['header'].index(column)
    return [row[col_index] for row in table['rows']]

def get_value(table, column=0):
    """
    Возвращает одно значение из столбца для таблицы с одной строкой.
    """
    if len(table['rows']) != 1:
        raise ValueError("Функция get_value() применима только для таблицы с одной строкой.")
    col_index = column if isinstance(column, int) else table['header'].index(column)
    return table['rows'][0][col_index]

def set_values(table, values, column=0):
    """
    Устанавливает список значений в указанный столбец.
    """
    col_index = column if isinstance(column, int) else table['header'].index(column)
    if len(values) != len(table['rows']):
        raise ValueError("Количество значений не совпадает с количеством строк в таблице.")
    for i, row in enumerate(table['rows']):
        row[col_index] = values[i]

def set_value(table, value, column=0):
    """
    Устанавливает одно значение в столбец для таблицы с одной строкой.
    """
    if len(table['rows']) != 1:
        raise ValueError("Функция set_value() применима только для таблицы с одной строкой.")
    col_index = column if isinstance(column, int) else table['header'].index(column)
    table['rows'][0][col_index] = value

def print_table(table):
    """
    Печатает таблицу в консоль.
    """
    print("\t".join(table['header']))
    for row in table['rows']:
        print("\t".join(map(str, row)))

def concat(table1, table2):
    """
    Склеивает две таблицы по строкам, если у них совпадают заголовки.
    """
    if table1['header'] != table2['header']:
        raise ValueError("Таблицы имеют разные заголовки и не могут быть объединены.")

    new_table = {
        'header': table1['header'],
        'rows': table1['rows'] + table2['rows']  # Добавляем строки из второй таблицы
    }
    return new_table

def split(table, row_number):
    """
    Разбивает таблицу на две по номеру строки.
    """
    if row_number < 0 or row_number > len(table['rows']):
        raise IndexError("Номер строки выходит за пределы таблицы.")

    table1 = {
        'header': table['header'],
        'rows': table['rows'][:row_number]  # Строки до row_number
    }
    table2 = {
        'header': table['header'],
        'rows': table['rows'][row_number:]  # Строки с row_number и дальше
    }
    return table1, table2

def auto_detect_column_types(table):
    """
    Автоматически определяет типы столбцов на основе их значений.

    Args:
        table (dict): Таблица с ключами 'header' и 'rows'.

    Returns:
        dict: Словарь с определенными типами для каждого столбца.
    """
    column_types = {}

    for col_index, col_name in enumerate(table['header']):
        column_values = [row[col_index] for row in table['rows']]
        try:
            # Попробуем все значения преобразовать в int
            if all(isinstance(int(value), int) for value in column_values):
                column_types[col_name] = int
                continue
        except ValueError:
            pass

        try:
            # Попробуем все значения преобразовать в float
            if all(isinstance(float(value), float) for value in column_values):
                column_types[col_name] = float
                continue
        except ValueError:
            pass

        try:
            # Проверим, если это булевы значения
            if all(value.lower() in ("true", "false") for value in column_values):
                column_types[col_name] = bool
                continue
        except AttributeError:
            pass

        # Если ничего не подошло, назначаем тип str
        column_types[col_name] = str

    return column_types

def is_float(value):
    """
    Вспомогательная функция для проверки, является ли строка числом с плавающей точкой.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
