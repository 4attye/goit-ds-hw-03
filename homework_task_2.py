from bs4 import BeautifulSoup
import json
import requests


url = "http://quotes.toscrape.com"
quotes_data = []
authors_data = []


def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    born_date = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text.strip()
    return born_date, born_location, description


def get_quotes():
    page = 1
    while True:
        response = requests.get(f"{url}/page/{page}/")
        soup = BeautifulSoup(response.text, "lxml")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            break

        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            author_url = url + quote.find("a")["href"]

            quotes_data.append({
                "tags": tags,
                "author": author,
                "quote": text
            })

            if not any(a['fullname'] == author for a in authors_data):
                born_date, born_location, description = get_author_details(author_url)
                authors_data.append({
                    "fullname": author,
                    "born_date": born_date,
                    "born_location": born_location[3:],
                    "description": description
                })
        page += 1


if __name__ == '__main__':
    get_quotes()
    with open('authors.json', 'w', encoding="utf-8") as f:
        json.dump(authors_data, f, indent=4)
    with open('quotes.json', 'w', encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=4)
