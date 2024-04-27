import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# Функція для отримання даних про автора зі сторінки "about"
def scrape_author_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    author_info = {
        "fullname": soup.find("h3", class_="author-title").get_text(),
        "born_date": soup.find("span", class_="author-born-date").get_text(),
        "born_location": soup.find("span", class_="author-born-location").get_text(),
        "description": soup.find("div", class_="author-description").get_text().strip(),
    }
    return author_info


# Функція для отримання даних зі сторінки з цитатами
def scrape_quotes_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    author_about_links = set()
    for q in soup.find_all("div", class_="quote"):
        quote = {
            "tags": [tag.get_text() for tag in q.find_all("a", class_="tag")],
            "author": q.find("small", class_="author").get_text(),
            "quote": q.find("span", class_="text").get_text(),
        }
        quotes.append(quote)
        # Отримати повний URL сторінки "about" автора
        author_about_link = urljoin(url, q.find("a")["href"])
        author_about_links.add(author_about_link)
    return quotes, author_about_links


# Функція для збереження даних у JSON файл
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Основна функція для скрапінгу цитат
def scrape_quotes():
    base_url = "http://quotes.toscrape.com"
    url = base_url
    all_quotes = []
    all_authors = set()

    while url:
        quotes, author_about_links = scrape_quotes_page(url)
        all_quotes.extend(quotes)
        all_authors.update(author_about_links)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        url = soup.find("li", class_="next")
        if url:
            url = url.find("a")["href"]
            url = urljoin(base_url, url)

    return all_quotes, all_authors


if __name__ == "__main__":
    quotes, all_authors = scrape_quotes()

    # Збираємо дані про кожного автора
    authors = []
    for about_link in all_authors:
        authors.append(scrape_author_info(about_link))

    # Збереження цитат у quotes.json
    save_to_json(quotes, "quotes.json")

    # Збереження інформації про авторів у authors.json
    save_to_json(authors, "authors.json")

    print("Дані успішно зібрані та збережені.")
