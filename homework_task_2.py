from bs4 import BeautifulSoup
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests

client = MongoClient("mongodb+srv://4attye:upEIrWRmbcF1WVtn@clusters.s150f.mongodb.net/", server_api=ServerApi('1'))
db = client.qoutes
url = "http://quotes.toscrape.com"
qoutes_data = []
authors_data = []


def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    born_date = soup.find('span', class_='author-born-date').text
    born_location = soup.find('span', class_='author-born-location').text
    description = soup.find('div', class_='author-description').text.strip()
    return born_date, born_location, description


def write_json():
    with open('authors.json', 'w', encoding="utf-8") as a:
        json.dump(authors_data, a, ensure_ascii=False, indent=4)
    with open('qoutes.json', 'w', encoding="utf-8") as q:
        json.dump(qoutes_data, q, ensure_ascii=False, indent=4)


def insert_data():
    with open('authors.json', 'r', encoding='utf-8') as a :
        authors = json.load(a)
        db.authors.insert_many(authors)
    with open('qoutes.json', 'r', encoding='utf-8') as q:
        authors = json.load(q)
        db.qoutes.insert_many(authors)


def main ():
    page = 1
    while True:
        response = requests.get(f"{url}/page/{page}/")
        soup = BeautifulSoup(response.text, "lxml")
        qoutes = soup.find_all("div", class_="quote")

        if not qoutes:
            break

        for qoute in qoutes:
            text = qoute.find("span", class_="text")
            author = qoute.find("small", class_="author").text
            tags = [tag.text for tag in qoute.find_all("a", class_="tag")]
            author_url = url + qoute.find("a")["href"]

            qoutes_data.append({
                "tags": tags,
                "author": author,
                "quote": text.text
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

    write_json()
    insert_data()


if __name__ == '__main__':
    main ()

