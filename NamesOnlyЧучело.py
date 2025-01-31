import requests
from bs4 import BeautifulSoup
import csv
import random
import os

os.makedirs('industries', exist_ok=True)

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

def get_random_proxy():
    proxy = random.choice(proxies_list)
    return {
        'http': proxy,
        'https': proxy
    }

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

session = requests.Session()

def parse_industry(url):
    response = session.get(url, headers=headers, proxies=get_random_proxy())
    soup = BeautifulSoup(response.content, "html.parser")
    companies_table = soup.find("table", class_="sortable cwiki_table")
    company_data = []
    for row in companies_table.find_all("tr"):
        columns = row.find_all("td")
        if columns:
            company_name_tag = columns[0].find("a")
            if company_name_tag:
                company_name = company_name_tag.get_text(strip=True)
                city = columns[1].get_text(strip=True)
                project_count = columns[2].get_text(strip=True)
                if not city:
                    continue
                if project_count.isdigit() and int(project_count) <= 5:
                    company_data.append({
                        "name": company_name,
                        "city": city
                    })
    return company_data

for industry, url in industries.items():
    company_data = parse_industry(url)
    file_path = os.path.join("industries", f"{industry}.csv")
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Компания", "Город"])
        for company in company_data:
            writer.writerow([company["name"], company["city"]])
    print(f"Парсинг завершен. Данные сохранены в '{file_path}'.")
