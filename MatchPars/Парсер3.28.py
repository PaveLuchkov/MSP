import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import csv
import random
import os
import pandas as pd

# Словарь с названиями отраслей и соответствующими URL
industries = {
    "torgovlya": "https://www.tadviser.ru/index.php/Категория:Торговля?ptype=comp_otr#ttop",
    "transport": "https://www.tadviser.ru/index.php/Категория:Транспорт?ptype=comp_otr#ttop",
    "finansovye_uslugi": "https://www.tadviser.ru/index.php/Категория:Финансовые_услуги,_инвестиции_и_аудит?ptype=comp_otr#ttop",
    "gosudarstvennye_struktury": "https://www.tadviser.ru/index.php/Категория:Государственные_и_социальные_структуры?ptype=comp_otr#ttop",
    "mashinostroenie": "https://www.tadviser.ru/index.php/Категория:Машиностроение_и_приборостроение?ptype=comp_otr#ttop",
    "stroitelstvo": "https://www.tadviser.ru/index.php/Категория:Строительство_и_промышленность_строительных_материалов?ptype=comp_otr#ttop",
    "pishhevaya_promyshlennost": "https://www.tadviser.ru/index.php/Категория:Пищевая_промышленность?ptype=comp_otr#ttop",
    "telekommunikaciya": "https://www.tadviser.ru/index.php/Категория:Телекоммуникация_и_связь?ptype=comp_otr#ttop",
    "energetika": "https://www.tadviser.ru/index.php/Категория:Энергетика?ptype=comp_otr#ttop",
    "obrazovanie": "https://www.tadviser.ru/index.php/Категория:Образование_и_наука?ptype=comp_otr#ttop",
    "informacionnye_tehnologii": "https://www.tadviser.ru/index.php/Категория:Информационные_технологии?ptype=comp_otr#ttop",
    "informacionnaya_bezopasnost": "https://www.tadviser.ru/index.php/Категория:Информационная_безопасность?ptype=comp_otr#ttop",
    "farmacevtika": "https://www.tadviser.ru/index.php/Категория:Фармацевтика,_медицина,_здравоохранение?ptype=comp_otr#ttop",
    "zhkh": "https://www.tadviser.ru/index.php/Категория:ЖКХ,_сервисные_и_бытовые_услуги?ptype=comp_otr#ttop",
    "neftyanaya_promyshlennost": "https://www.tadviser.ru/index.php/Категория:Нефтяная_промышленность?ptype=comp_otr#ttop",
    "konsalting": "https://www.tadviser.ru/index.php/Категория:Консалтинг,_включая_управленческий_и_кадровый?ptype=comp_otr#ttop",
    "himicheskaya_promyshlennost": "https://www.tadviser.ru/index.php/Категория:Химическая_промышленность?ptype=comp_otr#ttop",
    "metallurgicheskaya_promyshlennost": "https://www.tadviser.ru/index.php/Категория:Металлургическая_промышленность?ptype=comp_otr#ttop",
    "turizm": "https://www.tadviser.ru/index.php/Категория:Туризм,_гостиничный_и_ресторанный_бизнес?ptype=comp_otr#ttop",
    "logistika": "https://www.tadviser.ru/index.php/Категория:Логистика_и_дистрибуция?ptype=comp_otr#ttop",
    "dobycha_poleznyh_iskopaemyh": "https://www.tadviser.ru/index.php/Категория:Добыча_полезных_ископаемых?ptype=comp_otr#ttop",
    "gazovaya_promyshlennost": "https://www.tadviser.ru/index.php/Категория:Газовая_промышленность?ptype=comp_otr#ttop",
    "legkaya_promyshlennost": "https://www.tadviser.ru/index.php/Категория:Легкая_промышленность?ptype=comp_otr#ttop",
    "strahovanie": "https://www.tadviser.ru/index.php/Категория:Страхование?ptype=comp_otr#ttop",
    "smi": "https://www.tadviser.ru/index.php/Категория:СМИ,_теле-_и_радиовещание?ptype=comp_otr#ttop",
    "elektrotehnika": "https://www.tadviser.ru/index.php/Категория:Электротехника_и_микроэлектроника?ptype=comp_otr#ttop",
    "industriya_razvlecheniy": "https://www.tadviser.ru/index.php/Категория:Индустрия_развлечений,_досуг,_спорт?ptype=comp_otr#ttop",
    "reklama": "https://www.tadviser.ru/index.php/Категория:Реклама,_PR_и_маркетинг?ptype=comp_otr#ttop",
    "tovary_narodnogo_potrebleniya": "https://www.tadviser.ru/index.php/Категория:Товары_народного_потребления?ptype=comp_otr#ttop",
    "selskoe_hozyaystvo": "https://www.tadviser.ru/index.php/Категория:Сельское_хозяйство_и_рыболовство?ptype=comp_otr#ttop",
    "lesnoe_hozyaystvo": "https://www.tadviser.ru/index.php/Категория:Лесное_и_деревообрабатывающее_хозяйство?ptype=comp_otr#ttop",
    "nedvizhimost": "https://www.tadviser.ru/index.php/Категория:Недвижимость?ptype=comp_otr#ttop",
    "poligraficheskaya_deyatelnost": "https://www.tadviser.ru/index.php/Категория:Полиграфическая_деятельность?ptype=comp_otr#ttop",
    "obshchestvennye_struktury": "https://www.tadviser.ru/index.php/Категория:Общественные_и_некоммерческие_структуры?ptype=comp_otr#ttop",
    "vpk": "https://www.tadviser.ru/index.php/Категория:ВПК?ptype=comp_otr#ttop",
    "internet_servisy": "https://www.tadviser.ru/index.php/Категория:Интернет-сервисы?ptype=comp_otr#ttop",
    "yurisprudenciya": "https://www.tadviser.ru/index.php/Категория:Юриспруденция?ptype=comp_otr#ttop",
    "yuvelirnaya_promyshlennost": "https://www.tadviser.ru/index.php/Категория:Ювелирная_промышленность?ptype=comp_otr#ttop",
    "orgtehnika": "https://www.tadviser.ru/index.php/Категория:Оргтехника_и_офисные_принадлежности?ptype=comp_otr#ttop",
    "kosmicheskaya_otrasl": "https://www.tadviser.ru/index.php/Категория:Космическая_отрасль?ptype=comp_otr#ttop"
}

# Список прокси-серверов с логином и паролем
proxies_list = [
    'http://user237924:4l5emu@85.8.187.136:1569',
    'http://user237924:4l5emu@45.128.131.63:1569',
    'http://user237924:4l5emu@45.88.211.158:1569',
    'http://user237924:4l5emu@45.86.3.71:1569',
    'http://user237924:4l5emu@85.8.187.121:1569'
]

# Список user-agents для имитации разных браузеров
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
]

# Функция для выбора случайного прокси
def get_random_proxy():
    proxy = random.choice(proxies_list)
    return {
        'http': proxy,
        'https': proxy
    }

# Функция для получения случайного user-agent
def get_random_user_agent():
    return random.choice(user_agents)

# Заголовки для имитации браузера
headers = {
    'User-Agent': get_random_user_agent(),
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

# Инициализируем сессию для повторного использования соединений
session = requests.Session()

# Функция для сохранения данных с паспортами в CSV
def save_companies_data(companies_data, filename):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for company in companies_data:
            for impl in company["digital_passport"]:
                writer.writerow([company["name"], company["city"],
                                 impl["product"], impl["technology"], impl["year"]])

# Загрузка уже обработанных компаний из файла companies_data_{industry}.csv
def load_existing_companies(filename):
    if os.path.exists(filename):
        # Используем pandas для быстрого поиска
        df = pd.read_csv(filename, header=None)
        # Устанавливаем правильные названия колонок вручную
        df.columns = ['Компания', 'Город', 'Продукт', 'Технология', 'Год']
        # Убираем кавычки вокруг названий компаний и преобразуем в set
        existing_companies = set(df['Компания'].str.replace('"', '').str.strip())  # Убираем кавычки и пробелы
    else:
        existing_companies = set()
    return existing_companies

# Загрузка компаний без паспорта
def load_companies_without_passport(filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        companies_without_passport = set(df['Компания'].str.replace('"', '').str.strip())  # Убираем кавычки и пробелы
    else:
        companies_without_passport = set()
    return companies_without_passport

def safe_request(url, headers, proxies, timeout=30, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            # Попытка сделать запрос с тайм-аутом
            response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
            response.raise_for_status()  # Проверяем, не возникла ли ошибка HTTP
            return response
        except requests.exceptions.Timeout:
            attempt += 1
            print(f"Запрос на {url} превысил время ожидания (timeout). Попытка {attempt} из {retries}.")
            if attempt < retries:
                time.sleep(random.uniform(1, 3))  # Небольшая задержка перед повторной попыткой
            else:
                print(f"Не удалось загрузить {url} после {retries} попыток.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}. Попытка {attempt + 1} из {retries}.")
            attempt += 1
            if attempt < retries:
                time.sleep(random.uniform(1, 3))  # Небольшая задержка перед повторной попыткой
            else:
                print(f"Не удалось загрузить {url} после {retries} попыток.")
                return None

# Основной цикл по отраслям
for industry, url in industries.items():
    unique_file = f"matched_results/unique_{industry}.csv"
    if not os.path.exists(unique_file):
        print(f"Файл {unique_file} не найден, пропуск отрасли {industry}")
        continue

    unilist = list(pd.read_csv(unique_file)['Компания'])

    # Загрузка уже обработанных компаний
    existing_companies = load_existing_companies(f"passports/companies_passport_{industry}.csv")
    companies_without_passport = load_companies_without_passport(f"npass/companies_data_without_passport_{industry}.csv")

    # Запрос к странице с прокси
    response = safe_request(url, headers, get_random_proxy())
    soup = BeautifulSoup(response.content, "html.parser")

    # Найдем таблицу с компаниями
    companies_table = soup.find("table", class_="sortable cwiki_table")

    # Сохраним ссылки на страницы компаний
    company_links = []

    # Ищем все строки таблицы, которые содержат данные о компаниях
    for row in companies_table.find_all("tr"):
        columns = row.find_all("td")
        
        # Если строка не пустая (есть данные о компании)
        if columns:
            company_name_tag = columns[0].find("a")  # Ссылка на страницу компании
            if company_name_tag:
                company_name = company_name_tag.get_text(strip=True)
                if company_name not in unilist:
                    continue
                city = columns[1].get_text(strip=True)
                project_count = columns[2].get_text(strip=True)

                # Фильтруем компании, у которых количество проектов больше 5
                if project_count.isdigit() and int(project_count) <= 5:
                    company_link = "https://www.tadviser.ru" + company_name_tag["href"]
                    company_links.append({
                        "name": company_name,
                        "city": city,
                        "link": company_link
                    })

    # Ограничиваем количество компаний для парсинга (например, первые 10000 компаний)
    limit = 10000
    company_links = company_links[:limit]

    # Прогресс по списку компаний
    companies_data = []  # Список для хранения данных всех компаний
    for company in tqdm(company_links, desc=f"Парсинг компаний {industry}", unit="компания"):
        # Проверяем, была ли компания уже обработана
        if company["name"] in existing_companies or company["name"] in companies_without_passport or company["name"] not in unilist:
            continue  # Пропускаем, если компания уже есть в списке паспортов или без паспорта или нет в unique_{industry}.csv
        
        # Переходим по ссылке на компанию
        company_page = session.get(company["link"], headers=headers, proxies=get_random_proxy())
        company_soup = BeautifulSoup(company_page.content, "html.parser")
        
        # Ищем блок с цифровым паспортом
        digital_passport_section = company_soup.find("div", {"id": "pasport"})
        if digital_passport_section:
            it_systems_table = company_soup.find("table", {"class": "sortable cwiki_table"})
            implementations = []
            
            if it_systems_table:
                rows = it_systems_table.find_all("tr")
                
                for row in rows[1:]:  # Пропускаем заголовок таблицы
                    columns = row.find_all("td")
                    if len(columns) >= 5:
                        project = columns[0].get_text(strip=True)
                        product = columns[2].get_text(strip=True)
                        technology = columns[3].get_text(strip=True)
                        year = columns[4].get_text(strip=True)
                        
                        # Фильтруем проекты
                        if year and year.isdigit() and int(year) >= 2013:
                            if product and technology:
                                implementations.append({
                                    "product": product,
                                    "technology": technology,
                                    "year": year
                                })

            company["digital_passport"] = implementations
        else:
            company["digital_passport"] = []

        # Добавляем данные компании в общий список
        companies_data.append({
            "name": company["name"],
            "city": company["city"],
            "digital_passport": company["digital_passport"]
        })

        # Сохраняем данные с паспортами на каждом шаге
        save_companies_data([company], filename=f"passports/companies_passport_{industry}.csv")
        
        time.sleep(random.uniform(1, 5))  # Задержка от 1 до 5 секунд

    # Сохраняем данные без паспортов в отдельный CSV
    with open(f"npass/companies_data_without_passport_{industry}.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Компания", "Город"])
        for company in companies_data:
            writer.writerow([company["name"], company["city"]])

    print(f"Парсинг отрасли {industry} завершен. Данные сохранены в 'companies_passport_{industry}.csv'.")