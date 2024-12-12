def get_rows_by_number(table, start, stop = None, copy_table = False):
    """
    Возвращает строки таблицы по номеру (одна строка или интервал).

    Args:
        table (dict): Словарь, представляющий таблицу. В нём должны быть ключи.
        start (int): Индекс, с которого начинается выборка строк.
        stop (int, optional): Индекс, до которого продолжается выборка строк (не включая stop). 
                              Если stop не указан (None), выборка идёт до конца списка строк.
        copy_table (bool, optional): Флаг, который определяет, нужно ли копировать строки таблицы перед возвратом.

    Returns:
        dict: Словарь с двумя ключами.
    """
    rows = table['rows'][start:stop] # выполняет срез строк таблицы
    # создание словаря с теми же заголовками таблицы и строками из среза.
    return {"header": table['header'], "rows": rows.copy()} if copy_table else {"header": table['header'], "rows": rows}

def get_rows_by_index(table, *values, copy_table=False):
    """
    Возвращает строки таблицы, где значения в первом столбце совпадают с переданными аргументами.

    Args:
        table (dict): Таблица с ключами.
        *values: Несколько значений, с которыми будут сравниваться значения в первом столбце таблицы. Это может быть одно или несколько значений.
        copy_table (bool, optional): Если True, возвращается копия строк таблицы. Если False, возвращаются строки по ссылке.

    Returns:
        dict: Словарь с двумя ключами.
    """
    filtered_rows = [row for row in table['rows'] if row[0] in values] # сравниваем строки с переданными значениями.
    # создание нового словаря с найдеными индексами.
    return {"header": table['header'], "rows": filtered_rows.copy()} if copy_table else {"header": table['header'], "rows": filtered_rows}

def get_column_types(table, by_number=True):
    """
    Возвращает словарь с типами значений для каждого столбца.
    Определяет типы данных по требованию для уже загруженной таблицы.

    Args:
        table (dict): Таблица с ключами 'header' и 'rows'.
        by_number (bool): Если True, ключами будут индексы столбцов.
                          Если False, ключами будут названия столбцов.

    Returns:
        dict: Словарь с типами данных для каждого столбца.
    """
    column_types = {}
    for i, col in enumerate(table['header']):
        values = [row[i] for row in table['rows'] if row[i] != ""]  # cчитываем все значения столбца
        if all(v.isdigit() for v in values): # если все значения цифры
            column_type = int
        elif all(is_float(v) for v in values): # если все значения можно преобразовать в float
            column_type = float
        elif all(v.lower() in ("true", "false") for v in values): # если все значения True/False
            column_type = bool
        else: # в остальных случаях это строка
            column_type = str
        column_types[i if by_number else col] = column_type # здесь выбирается, что будет ключом: индекс столбца или его название
    return column_types

def set_column_types(table, types_dict, by_number=True):
    """
    Задаёт типы значений для столбцов.

    Args:
        table: Словарь, представляющий таблицу.
        types_dict: Словарь, в котором ключи — это индексы или имена столбцов, а значения — это типы данных.
        by_number (по умолчанию True): Если этот параметр равен True, то ключи в types_dict будут интерпретироваться как индексы столбцов. 
                                       Если False, то ключи будут интерпретироваться как имена столбцов.

    Returns:
        None

    Raises:
         ValueError: Если невозможно преобразовать значение.
    """
    for key, col_type in types_dict.items(): # перебираем все ключи и значения
        col_index = key if by_number else table['header'].index(key) # если by_number — True, то key используется как индекс столбца. Иначе как название столбца
        for row in table['rows']:
            try:
                row[col_index] = col_type(row[col_index]) # ищем по индексу столбца значение в строке и преобразовываем его тип данных в тип данных из col_type.
            except ValueError:
                raise ValueError(f"Невозможно преобразовать значение '{row[col_index]}' в {col_type.__name__}")

def get_values(table, column=0):
    """
    Возвращает список значений из указанного столбца.

    Args:
        table: Это словарь, представляющий таблицу.
        column: Это индекс столбца, из которого нужно извлечь значения. По умолчанию column = 0
        
    Returns:
        list: список значений указанного столбца.
    """
    col_index = column if isinstance(column, int) else table['header'].index(column) # если column - число, то это индекс. Иначе ищет индекс этого столбца в списке заголовков. 
    return [row[col_index] for row in table['rows']] # для каждой строки извлекается значение из столбца с индексом.

def get_value(table, column=0):
    """
    Возвращает одно значение из столбца для таблицы с одной строкой.
    
    Args:
        table (dict): Таблица с ключами 'header' и 'rows'.
        column (int or str): Индекс или имя столбца, из которого нужно получить значение (по умолчанию 0).

    Returns:
        значение из таблицы (тип зависит от типа данных в указанном столбце).
    """
    if len(table['rows']) != 1: # проверка, что таблица содержит только одну строку.
        raise ValueError("Функция get_value() применима только для таблицы с одной строкой.")
    col_index = column if isinstance(column, int) else table['header'].index(column) # так же как в get_values
    return table['rows'][0][col_index] # извлекает значение из первой строки таблицы по индексу столбца col_index

def set_values(table, values, column=0):
    """
    Устанавливает список значений в указанный столбец.
    
    Args:
        table (dict): Таблица с ключами.
        values (list): Список значений, которые нужно установить в столбец.
        column (int or str): Индекс или имя столбца, в который нужно установить значения (по умолчанию 0).

    Returns:
        None

    Raises:
        ValueError: Количество значений не совпадает с количеством строк в таблице.
    """
    col_index = column if isinstance(column, int) else table['header'].index(column) # определение индекса столбца.
    if len(values) != len(table['rows']): # проверка соответствия длины списка значений и количества строк.
        raise ValueError("Количество значений не совпадает с количеством строк в таблице.")
    for i, row in enumerate(table['rows']):
        row[col_index] = values[i] # итерирует по всем строкам таблицы и присваивает значения из списка values.

def set_value(table, value, column=0):
    """
    Устанавливает одно значение в столбец для таблицы с одной строкой.
    
    Args:
        table (dict): Таблица с ключами.
        value (int or str): Значение, которое нужно установить в таблицу.
        column (int or str): Индекс или имя столбца, в который нужно установить значения (по умолчанию 0).

    Returns:
        None

    Raises:
        ValueError: Функция set_value() применима только для таблицы с одной строкой.
    """
    if len(table['rows']) != 1: # проверка, что таблица содержит только одну строку.
        raise ValueError("Функция set_value() применима только для таблицы с одной строкой.")
    col_index = column if isinstance(column, int) else table['header'].index(column) # определение индекса столбца.
    table['rows'][0][col_index] = value # замена значения в строке на переданное значение.

def print_table(table):
    """
    Печатает таблицу в консоль.
    
    Args:
        table (dict): Таблица с ключами.

    Returns:
        Отрисованную таблицу с табуляцией.
    """
    print("\t".join(table['header']))
    for row in table['rows']:
        print("\t".join(map(str, row)))

def concat(table1, table2):
    """
    Склеивает две таблицы по строкам, если у них совпадают заголовки.
    
    Args:
        table1 (dict): Таблица с ключами №1.
        table2 (dict): Таблица с ключами №2.

    Returns:
        table (dict): Объединенная таблица с ключами.

    Raises:
        ValueError: Таблицы имеют разные заголовки и не могут быть объединены.
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
    
    Args:
        table (dict): Таблица с ключами.
        row_number (int): Номер строки, по которой будет разделяться таблица.

    Returns:
        table1 (dict): Таблица с ключами №1.
        table2 (dict): Таблица с ключами №2.

    Raises:
        IndexError: Номер строки выходит за пределы таблицы.
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
    Определяет типы данных при загрузке таблицы из файла.

    Args:
        table (dict): Таблица с ключами 'header' и 'rows'.

    Returns:
        dict: Словарь с определенными типами для каждого столбца.

    Raises:
        ValueError: pass если не получилось преобразовать в нужный тип - пропускаем.
        AttributeError: pass если value не является строкой.
    """
    column_types = {}

    for col_index, col_name in enumerate(table['header']):
        column_values = [row[col_index] for row in table['rows']]
        try:
            # Попробуем все значения преобразовать в int
            if all(isinstance(int(value), int) for value in column_values): # if all() => True
                column_types[col_name] = int # добавляем ключ со значением
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
        except AttributeError: # ловит ситуацию, если value не является строкой.
            pass

        # Если ничего не подошло, назначаем тип str
        column_types[col_name] = str

    return column_types

def is_float(value):
    """
    Вспомогательная функция для проверки, является ли строка числом с плавающей точкой.

    Args:
        value (int or str)

    Returns:
        bool 
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
