import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import os

# Создаем папку для сохранения файлов
os.makedirs('industries', exist_ok=True)

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
    # Добавьте остальные отрасли и URL сюда
}

# Список прокси-серверов с логином и паролем
proxies_list = [
    'http://user237924:4l5emu@85.8.187.136:1569',
    'http://user237924:4l5emu@45.128.131.63:1569',
    'http://user237924:4l5emu@45.88.211.158:1569',
    'http://user237924:4l5emu@45.86.3.71:1569',
    'http://user237924:4l5emu@85.8.187.121:1569'
]

# Функция для выбора случайного прокси
def get_random_proxy():
    proxy = random.choice(proxies_list)
    return {
        'http': proxy,
        'https': proxy
    }

# Заголовки для имитации браузера
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

# Инициализируем сессию для повторного использования соединений
session = requests.Session()

# Функция для парсинга данных с одной страницы
def parse_industry(url):
    response = session.get(url, headers=headers, proxies=get_random_proxy())
    soup = BeautifulSoup(response.content, "html.parser")

    # Найдем таблицу с компаниями
    companies_table = soup.find("table", class_="sortable cwiki_table")

    # Сохраним данные о компаниях
    company_data = []

    # Ищем все строки таблицы, которые содержат данные о компаниях
    for row in companies_table.find_all("tr"):
        columns = row.find_all("td")
        
        # Если строка не пустая (есть данные о компании)
        if columns:
            company_name_tag = columns[0].find("a")  # Ссылка на страницу компании
            if company_name_tag:
                company_name = company_name_tag.get_text(strip=True)
                city = columns[1].get_text(strip=True)
                project_count = columns[2].get_text(strip=True)

                # Пропускаем строки, если город пустой
                if not city:
                    continue
                
                # Фильтруем компании, у которых количество проектов меньше 5
                if project_count.isdigit() and int(project_count) <= 5:
                    # Добавляем компанию в список
                    company_data.append({
                        "name": company_name,
                        "city": city
                    })
    return company_data

# Парсим данные для каждой отрасли и сохраняем в файлы
for industry, url in industries.items():
    company_data = parse_industry(url)
    
    # Сохраняем данные о компаниях в CSV
    file_path = os.path.join("industries", f"{industry}.csv")
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Заголовки CSV
        writer.writerow(["Компания", "Город"])
        
        # Записываем данные о компаниях
        for company in company_data:
            writer.writerow([company["name"], company["city"]])

    print(f"Парсинг завершен. Данные сохранены в '{file_path}'.")
