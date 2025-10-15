import csv
import requests
from bs4 import BeautifulSoup

url_lab = "https://www.labirint.ru/search/Дюна%20Фрэнк%20Герберт/?stype=0"
url_chit = "https://www.chitai-gorod.ru/search?phrase=Дюна+Фрэнк+Герберт"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def clean_price(price_text):
    chars_to_remove = "₽ "
    for char in chars_to_remove:
        price_text = price_text.replace(char, "")
    price_text = price_text.replace('\u00a0', '').replace('\u202f', '').replace('\u2009', '')
    return price_text

def parse_labirint(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    count = 0
    mag = "Лабиринт"
    books = soup.find_all("div", class_="product-card")
    for book in books:
        raw_name = book.find("a", class_="product-card__name")
        if raw_name:
            name = raw_name.text.strip()
        else:
            name = "Название не найдено"
        raw_price = book.find("div", class_="product-card__price-current")
        if raw_price:
            price = clean_price(raw_price.text.strip())
        else:
            price = "Цена не найдена"
        results.append({"Магазин": mag,"Название": name, "Цена": price})
        count += 1
        if count == 5:
            break
    return results
    
def parse_chitai_gorod(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    count = 0
    mag = "Читай город"
    books = soup.find_all("article", class_="product-card")
    for book in books:
        raw_name = book.find("a", class_="product-card__title")
        if raw_name:
            name = raw_name.text.strip()
        else:
            name = "Название не найдено"
        raw_price = book.find("span", class_="product-mini-card-price__price")
        if raw_price:
            price = clean_price(raw_price.text.strip())
        else:
            price = "Цена не найдена"
        results.append({"Магазин": mag,"Название": name, "Цена": price})
        count += 1
        if count == 5:
            break
    return results

all_results = []

print("Собираем данные с Лабиринта...")
labirint_data = parse_labirint(url_lab)
all_results.extend(labirint_data)
print(f"Собрано {len(labirint_data)} позиций.")

print("\nСобираем данные с Читай город...")
chitai_gorod_data = parse_chitai_gorod(url_chit)
all_results.extend(chitai_gorod_data)
print(f"Собрано {len(chitai_gorod_data)} позиций.")

print(f"\nВсего собрано: {len(all_results)} позиций.")
print(f"\nСохраняем всё в csv файл.")

with open("parser_price.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["Магазин", "Название", "Цена"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_results)

print("Файл parser_price.csv усешно создан!")

     







