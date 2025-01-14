import urllib3
import json
from bs4 import BeautifulSoup
import random
import time

import urllib3
from urllib3.exceptions import NewConnectionError, MaxRetryError

http = urllib3.PoolManager()

def get_urls(page_url):
    try:
        response = http.request('GET', page_url)
        return response.data
    except (NewConnectionError, MaxRetryError) as e:
        print(f"Ошибка подключения: {e}")
        return None


http = urllib3.PoolManager()
base_url = "https://avtorynok.kz"
cars_url = "https://avtorynok.kz/cars&city=38&marka=89"

def get_urls(page_url):
    response = http.request('GET', page_url)
    print(f"Fetching: {page_url}, Status: {response.status}")
    if response.status != 200:
        return []
    
    soup = BeautifulSoup(response.data, 'html.parser')
    links = []
    for car in soup.find_all("a", {"class": "a-card__link"}):  # Используем найденный класс
        links.append(base_url + car.get("href"))
    return links

def get_info(car_url):
    response = http.request('GET', car_url)
    print(f"Fetching details from: {car_url}, Status: {response.status}")
    if response.status != 200:
        return {"error": response.status}
    
    soup = BeautifulSoup(response.data, 'html.parser')
    details = {}

    # Извлечение данных о машине
    title = soup.find("h5", class_="a-card__title")  
    price = soup.find("span", class_="a-card__price")  

    details["title"] = title.get_text(strip=True) if title else "Unknown"
    details["price"] = price.get_text(strip=True) if price else "Unknown"

    # Дополнительные поля
    details["url"] = car_url
    return details

links = []
for i in range(1, 11):  # Пример: парсинг первых 10 страниц
    page_links = get_urls(cars_url + str(i))
    links.extend(page_links)
    time.sleep(random.randint(2, 5))

car_data = []
for idx, link in enumerate(links):
    print(f"Processing car {idx + 1}/{len(links)}")
    car_details = get_info(link)
    car_data.append(car_details)
    time.sleep(random.randint(2, 5))

# Сохранение данных в JSON-файл
with open('cars_data.json', 'w', encoding='utf-8') as file:
    json.dump(car_data, file, ensure_ascii=False, indent=4)

print(f"Scraped {len(car_data)} cars.")
