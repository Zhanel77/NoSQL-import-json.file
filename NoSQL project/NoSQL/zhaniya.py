import urllib3
from bs4 import BeautifulSoup
import json

# Инициализация HTTP-менеджера
http = urllib3.PoolManager()

# Указанный URL продукта на Amazon
url = "https://www.amazon.com/TRENDOUX-Winter-Texting-Smartphone-Driving/dp/B07JYJM6JT?ref=dlx_winte_dg_dcl_B07JYJM6JT_dt_sl14_14&pf_rd_r=MBR4QYQ4GTBDM1YKE81T&pf_rd_p=7718e94b-eb10-4da7-8b5a-b2c83a406914"

# Запрос к странице
response = http.request('GET', url)
print(response.status)

# Парсинг HTML с помощью BeautifulSoup
soup = BeautifulSoup(response.data, 'html.parser')

# Извлечение данных
price = soup.find("span", class_="a-offscreen")
product_title = soup.find("span", class_="a-size-large product-title-word-break")
color = soup.find("span", class_="selection")

# Составление данных для записи в JSON
product_data = {
    "price": price.get_text() if price else "Цена не найдена",
    "product_title": product_title.get_text() if product_title else "Название продукта не найдено",
    "color": color.get_text() if color else "Цвет не найден"
}

# Сохранение данных в JSON файл
with open('product_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(product_data, json_file, ensure_ascii=False, indent=4)

print("Данные сохранены в файл 'product_data.json'")
