import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import csv
import random
import os
import pandas as pd

industries = {
    "torgovlya": "https://www.tadviser.ru/index.php/Категория:Торговля?ptype=comp_otr#ttop",
    "transport": "https://www.tadviser.ru/index.php/Категория:Транспорт?ptype=comp_otr#ttop",
    "finansovye_uslugi": "https://www.tadviser.ru/index.php/Категория:Финансовые_услуги,_инвестиции_и_аудит?ptype=comp_otr#ttop",
    # и далее полный список ссылок на каждую отрасль
}

proxies_list = [
    'http://user:password@127.0.0.1:8080'
    # и далее список прокси-серверов в формате 'http://user:password@ip:port'
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    # и далее список user-agent'ов
]

def get_random_proxy():
    proxy = random.choice(proxies_list)
    return {
        'http': proxy,
        'https': proxy
    }

def get_random_user_agent():
    return random.choice(user_agents)

headers = {
    'User-Agent': get_random_user_agent(),
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

session = requests.Session()

def save_companies_data(companies_data, filename):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for company in companies_data:
            for impl in company["digital_passport"]:
                writer.writerow([company["name"], company["city"],
                                 impl["product"], impl["technology"], impl["year"]])

def load_existing_companies(filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename, header=None)
        df.columns = ['Компания', 'Город', 'Продукт', 'Технология', 'Год']
        existing_companies = set(df['Компания'].str.replace('"', '').str.strip())
    else:
        existing_companies = set()
    return existing_companies

def load_companies_without_passport(filename):
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        companies_without_passport = set(df['Компания'].str.replace('"', '').str.strip())
    else:
        companies_without_passport = set()
    return companies_without_passport


#  Обработчик запросов с обработкой ошибок
def safe_request(url, headers, proxies, timeout=30, retries=3):
    attempt = 0
    while attempt < retries:
        try:
            response = session.get(url, headers=headers, proxies=proxies, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            attempt += 1
            print(f"Запрос на {url} превысил время ожидания. Попытка {attempt} из {retries}.")
            if attempt < retries:
                time.sleep(random.uniform(1, 3))
            else:
                print(f"Не удалось загрузить {url} после {retries} попыток.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}. Попытка {attempt + 1} из {retries}.")
            attempt += 1
            if attempt < retries:
                time.sleep(random.uniform(1, 3))
            else:
                print(f"Не удалось загрузить {url} после {retries} попыток.")
                return None

for industry, url in industries.items():
    unique_file = f"matched_results/unique_{industry}.csv"
    if not os.path.exists(unique_file):
        print(f"Файл {unique_file} не найден, пропуск отрасли {industry}")
        continue

    unilist = list(pd.read_csv(unique_file)['Компания'])

    existing_companies = load_existing_companies(f"passports/companies_passport_{industry}.csv")
    companies_without_passport = load_companies_without_passport(f"npass/companies_data_without_passport_{industry}.csv")

    response = safe_request(url, headers, get_random_proxy())
    soup = BeautifulSoup(response.content, "html.parser")

    companies_table = soup.find("table", class_="sortable cwiki_table")

    company_links = []

    for row in companies_table.find_all("tr"):
        columns = row.find_all("td")
        if columns:
            company_name_tag = columns[0].find("a")
            if company_name_tag:
                company_name = company_name_tag.get_text(strip=True)
                if company_name not in unilist:
                    continue
                city = columns[1].get_text(strip=True)
                project_count = columns[2].get_text(strip=True)
                if project_count.isdigit() and int(project_count) <= 5:
                    company_link = "https://www.tadviser.ru" + company_name_tag["href"]
                    company_links.append({
                        "name": company_name,
                        "city": city,
                        "link": company_link
                    })

    limit = 10000
    company_links = company_links[:limit]

    companies_data = []
    for company in tqdm(company_links, desc=f"Парсинг компаний {industry}", unit="компания"):
        if company["name"] in existing_companies or company["name"] in companies_without_passport or company["name"] not in unilist:
            continue
        
        company_page = session.get(company["link"], headers=headers, proxies=get_random_proxy())
        company_soup = BeautifulSoup(company_page.content, "html.parser")
        
        digital_passport_section = company_soup.find("div", {"id": "pasport"})
        if digital_passport_section:
            it_systems_table = company_soup.find("table", {"class": "sortable cwiki_table"})
            implementations = []
            
            if it_systems_table:
                rows = it_systems_table.find_all("tr")
                
                for row in rows[1:]:
                    columns = row.find_all("td")
                    if len(columns) >= 5:
                        project = columns[0].get_text(strip=True)
                        product = columns[2].get_text(strip=True)
                        technology = columns[3].get_text(strip=True)
                        year = columns[4].get_text(strip=True)
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

        companies_data.append({
            "name": company["name"],
            "city": company["city"],
            "digital_passport": company["digital_passport"]
        })

        save_companies_data([company], filename=f"passports/companies_passport_{industry}.csv")
        
        time.sleep(random.uniform(1, 5))

    print(f"Парсинг отрасли {industry} завершен. Данные сохранены в 'companies_passport_{industry}.csv'.")
