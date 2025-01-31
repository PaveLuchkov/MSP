import pandas as pd
import os

def load_existing_companies(filename):
    # Проверим, существует ли файл
    if os.path.exists(filename):
        # Прочитаем CSV, указывая, что первая строка — это не заголовок
        df = pd.read_csv(filename, header=None)
        print(f"Загружено {len(df)} строк из {filename}")

        # Выводим заголовки
        print(f"Заголовки: {df.columns.tolist()}")  # Покажем список заголовков, которые будут числовыми

        # Устанавливаем собственные названия колонок
        df.columns = ['Компания', 'Город', 'Продукт', 'Технология', 'Год']  # Указываем корректные названия колонок

        # Проверяем, что колонка 'Компания' существует
        if 'Компания' in df.columns:
            # Убираем кавычки вокруг названий компаний и преобразуем в set
            existing_companies = set(df['Компания'].str.replace('"', '').str.strip())  # Убираем кавычки и пробелы
        else:
            print("Колонка 'Компания' не найдена!")
            existing_companies = set()
    else:
        print(f"Файл {filename} не найден!")
        existing_companies = set()
    
    return existing_companies

def load_unique_companies(filename):
    if os.path.exists(filename):
        # Прочитаем CSV и вернем список уникальных компаний
        df = pd.read_csv(filename)
        unique_companies = set(df['Компания'].str.replace('"', '').str.strip())  # Убираем кавычки и пробелы
    else:
        print(f"Файл {filename} не найден!")
        unique_companies = set()
    
    return unique_companies

# Пример использования
industry = "torgovlya"  # Пример отрасли, укажи свою
filename_passport = os.path.join("passports", f"companies_passport_{industry}.csv")
filename_unique = os.path.join("matched_results", f"unique_{industry}.csv")

# Загружаем данные
existing_companies = load_existing_companies(filename_passport)
unique_companies = load_unique_companies(filename_unique)

# Находим компании, которые есть в списке паспортов, но отсутствуют в списке уникальных
companies_in_passport_not_in_unique = existing_companies - unique_companies

# Находим компании, которые есть в списке уникальных, но отсутствуют в списке паспортов
companies_in_unique_not_in_passport = unique_companies - existing_companies

# Выводим результаты
print(f"Компании, которые есть в паспорте, но нет в уникальном списке:")
for company in companies_in_passport_not_in_unique:
    print(company)

print(f"\nКомпании, которые есть в уникальном списке, но нет в паспорте:")
for company in companies_in_unique_not_in_passport:
    print(company)

print(f"\nНайдено {len(companies_in_passport_not_in_unique)} компаний, которых нет в уникальном списке.")
print(f"Найдено {len(companies_in_unique_not_in_passport)} компаний, которых нет в списке паспортов.")
