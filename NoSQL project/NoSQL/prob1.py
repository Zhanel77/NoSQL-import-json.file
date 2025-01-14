import urllib3
import json
from bs4 import BeautifulSoup
import random
import time
from urllib3.exceptions import NewConnectionError, MaxRetryError

# Отключение предупреждений о сертификатах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Инициализация пула соединений
http = urllib3.PoolManager()

# Базовый URL сайта
base_url = "https://www.asos.com"

# URL страницы с товарами (предполагается, что пагинация выглядит как ?page=1, ?page=2 и т.д.)
products_url_template = "https://www.asos.com/bershka/bershka-clothing/cat/?cid=1234&page={}"

def get_urls(page_url):
    try:
        response = http.request('GET', page_url)
        print(f"Fetching: {page_url}, Status: {response.status}")
        if response.status != 200:
            return []
        
        soup = BeautifulSoup(response.data, 'html.parser')
        links = []
        
        # Поиск всех ссылок на товары по указанному классу
        # Убедитесь, что класс актуален
        for product in soup.find_all("a", {"class": "product-card__link"}):  
            href = product.get("href")
            if href:
                # Проверка, является ли ссылка абсолютной или относительной
                if href.startswith("http"):
                    links.append(href)
                else:
                    links.append(base_url + href)
        return links
    except (NewConnectionError, MaxRetryError) as e:
        print(f"Ошибка подключения: {e}")
        return []

def get_info(product_url):
    try:
        response = http.request('GET', product_url)
        print(f"Fetching details from: {product_url}, Status: {response.status}")
        if response.status != 200:
            return {"error": response.status}
        
        soup = BeautifulSoup(response.data, 'html.parser')
        details = {}
    
        # Извлечение данных о товаре
        # Обновленные классы для поиска заголовка и цены
        title = soup.find("h1", class_="jcdpl")  
        price = soup.find("span", {"class": "MwTOW", "data-testid": "current-price"})  
        color = soup.find("p", class_="aKxaq hEVA6")  # Новый элемент для цвета
    
        details["title"] = title.get_text(strip=True) if title else "Unknown"
        details["price"] = price.get_text(strip=True) if price else "Unknown"
        details["color"] = color.get_text(strip=True) if color else "Unknown"
    
        # Дополнительные поля
        details["url"] = product_url
        return details
    except Exception as e:
        print(f"Ошибка при обработке {product_url}: {e}")
        return {"error": str(e)}

def main():
    links = []
    total_pages = 10  # Пример: парсинг первых 10 страниц
    
    print("Сбор ссылок на товары...")
    for i in range(1, total_pages + 1):
        page_url = products_url_template.format(i)
        page_links = get_urls(page_url)
        print(f"Найдено {len(page_links)} ссылок на странице {i}.")
        links.extend(page_links)
        time.sleep(random.randint(2, 5))  # Случайная задержка между запросами
    
    # Удаление дубликатов ссылок
    links = list(set(links))
    print(f"Всего уникальных ссылок на товары: {len(links)}")
    
    product_data = []
    print("Сбор информации о товарах...")
    for idx, link in enumerate(links):
        print(f"Обработка товара {idx + 1}/{len(links)}: {link}")
        product_details = get_info(link)
        product_data.append(product_details)
        time.sleep(random.randint(2, 5))  # Случайная задержка между запросами
    
    # Сохранение данных в JSON-файл
    with open('products_data.json', 'w', encoding='utf-8') as file:
        json.dump(product_data, file, ensure_ascii=False, indent=4)
    
    print(f"Собрано {len(product_data)} товаров. Данные сохранены в 'products_data.json'.")

if __name__ == "__main__":
    main()
