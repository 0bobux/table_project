from table_modules import load_csv, save_csv, load_pickle, save_pickle, save_text
from table_modules import (
    get_rows_by_number, get_rows_by_index, get_column_types, set_column_types,
    get_values, get_value, set_values, set_value, print_table, concat, split
)

# Тестовые таблицы
test_table = {
    "header": ["Имя", "Возраст", "Зарплата"],
    "rows": [
        ["Алиса", "30", "50000"],
        ["Иван", "25", "45000"],
        ["Тимур", "35", "60000"],
        ["Денис", "40", "70000"]
    ]
}

table1 = {
    'header': ['Имя', 'Возраст', 'Зарплата'],
    'rows': [['Полина', '30', '50000'], ['Марк', '25', '45000']]
}

table2 = {
    'header': ['Имя', 'Возраст', 'Зарплата'],
    'rows': [['Андрей', '35', '60000'], ['Илья', '40', '70000']]
}

# 1. Тест сохранения и загрузки в CSV
print("=== Тест CSV ===")
save_csv(test_table, "test_table.csv")
# Загрузка с автоматическим определением типов
print("\n=== Загрузка CSV с автоопределением типов ===")
loaded_csv_table = load_csv("test_table.csv", auto_detect_types=True)
print_table(loaded_csv_table)
print("Определенные типы столбцов:", loaded_csv_table.get("column_types"))

# 2. Тест сохранения и загрузки в Pickle
print("\n=== Тест Pickle ===")
save_pickle(test_table, "test_table.pkl")
# Загрузка таблицы из Pickle с автоопределением типов
print("\n=== Загрузка Pickle с автоопределением типов ===")
loaded_pickle_table = load_pickle('test_table.pkl', auto_detect_types=True)
print_table(loaded_pickle_table)
print("Определенные типы столбцов:", loaded_pickle_table.get("column_types"))

# 3. Тест сохранения в текстовый файл
print("\n=== Тест Text ===")
save_text(test_table, "test_table.txt")
print("Таблица сохранена в текстовый файл: test_table.txt")

# 4. Тест операций над таблицей
print("\n=== Тест операций над таблицей ===")

# Получение строк по номеру
print("\nСтроки с 1 по 3:")
subset = get_rows_by_number(test_table, 0, 3, copy_table=True)
print_table(subset)

# Получение строк по значению в первом столбце
print("\nСтрока, где Имя = 'Иван':")
subset = get_rows_by_index(test_table, "Иван", copy_table=True)
print_table(subset)

# Получение типов столбцов
print("\nТипы столбцов:")
column_types = get_column_types(test_table)
print(column_types)

# Установка типов столбцов
print("\nУстановка типов столбцов:")
set_column_types(test_table, {1: int, 2: float}, by_number=True)
print_table(test_table)

# Получение значений столбца
print("\nЗначения столбца 'Возраст':")
ages = get_values(test_table, "Возраст")
print(ages)

# Установка значений в столбец
print("\nОбновляем значения в столбце 'Возраст':")
set_values(test_table, [31, 26, 36, 41], "Возраст")
print_table(test_table)

# Получение одного значения для таблицы с одной строкой
print("\nПолучение одного значения из столбца 'Зарплата':")
one_row_table = {"header": test_table["header"], "rows": [test_table["rows"][0]]}
salary = get_value(one_row_table, "Зарплата")
print("Значение:", salary)

# Обновляем значение в столбце 'Зарплата' для таблицы с одной строкой
#print("\nОбновляем значение в столбце 'Зарплата' для таблицы с одной строкой:")
#one_row_table = {"header": test_table["header"], "rows": [test_table["rows"][0]]}
#print("До обновления:")
#print_table(one_row_table)

#set_value(one_row_table, 75000, "Зарплата")
#print("После обновления:")
#print_table(one_row_table)

# Тест функции concat
print("\n=== Тест concat ===")
concat_table = concat(table1, table2)
print_table(concat_table)

# Тест функции split
print("\n=== Тест split ===")
split_table1, split_table2 = split(test_table, 2)
print("Первая таблица:")
print_table(split_table1)
print("Вторая таблица:")
print_table(split_table2)
