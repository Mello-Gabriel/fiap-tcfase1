"""Modulo para realizar scrapping do site."""

# %%
import os
from urllib.parse import urljoin

import dotenv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from tqdm import tqdm
from word2number import w2n

INDEX_URL = "https://books.toscrape.com/index.html"

BASE_URL = "https://books.toscrape.com/"

dotenv.load_dotenv()

db_url = os.getenv("db_url")


# %%

engine = create_engine(db_url)


# %%
def scrapper(url: str, *, iterate: bool) -> list[BeautifulSoup] | BeautifulSoup:
    """Faz a raspagem de uma url retornando um objeto BeautifulSoup.

    Se houver um link para próxima página no site,
    ele faz a raspagem até o fim dos nexts.

    Parametros:
    ----------

    url : str = Endereço em string do site a ser raspado
    iterate : bool = Define se deve iterar entre as páginas do site. Default = True


    Return:
    ------
    soups : list[BeautifulSoup] = Lista com objetos BeautifulSoup do site
            ou apenas um objeto BeautifulSoup se iterate = False


    """
    if not isinstance(url, str):
        msg = "Url must be a string"
        raise TypeError(msg)

    soups: list[BeautifulSoup] = []
    current_url: str | None = url
    try:
        while current_url:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content.decode("utf-8"), "html.parser")
            soups.append(soup)
            if not iterate:
                return soups[0]
            next_link_tag = soup.select_one("li.next > a, a[rel='next']")
            if next_link_tag and next_link_tag.has_attr("href"):
                next_link_relative = next_link_tag["href"]
                if next_link_relative and next_link_relative != "#":
                    current_url = urljoin(current_url, str(next_link_relative))
                else:
                    current_url = None
            else:
                current_url = None

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {current_url}: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return soups


# %%
def get_books_links(sopas: list[BeautifulSoup]) -> dict[str, str]:
    """Get the books links."""
    if not isinstance(sopas, list):
        msg = "Must be a list"
        raise TypeError(msg)

    for item in sopas:
        if not isinstance(item, BeautifulSoup):
            msg = "All items in the list must be BeautifulSoup objects"
            raise TypeError(msg)

    book_links: dict = {}
    for sopa in sopas:
        books = sopa.find_all("h3")
        for book in books:
            name = book.a["title"]
            link = book.a["href"].split("/")[-2:]
            book_links[name] = BASE_URL + "catalogue/" + "/".join(link)
    return book_links


# %%


def get_book_details(sopa: BeautifulSoup, page_url: str) -> dict:
    """Extract various details from a book's detail page."""

    def get_text_or_na(element):
        return element.get_text(strip=True) if element else "N/A"

    # Helper for product table
    def get_product_info(field_name):
        th_element = sopa.find("th", string=field_name)
        if th_element:
            td_element = th_element.find_next_sibling("td")
            return get_text_or_na(td_element)
        return "N/A"

    title_element = sopa.select_one("div.product_main h1")
    price_element = sopa.select_one("p.price_color")
    rating_element = sopa.select_one("p.star-rating")
    availability_element = sopa.select_one("p.instock.availability")
    category_element = sopa.select_one("ul.breadcrumb li:nth-of-type(3) a")
    image_element = sopa.select_one("#product_gallery img")
    description_element = sopa.select_one("#product_description + p")

    title = get_text_or_na(title_element)
    price = get_text_or_na(price_element)
    availability = get_text_or_na(availability_element)
    availability = availability.replace("In stock (", "").replace(" available)", "")
    category = get_text_or_na(category_element)
    description = get_text_or_na(description_element)

    rating = (
        str(rating_element["class"][1])
        if rating_element and len(rating_element.get("class", [])) > 1
        else "N/A"
    )
    rating = w2n.word_to_num(rating) if rating != "N/A" else "N/A"

    image_url = "N/A"
    if image_element and image_element.has_attr("src"):
        image_url = urljoin(page_url, str(image_element["src"]))

    # Product Information
    upc = get_product_info("UPC")
    product_type = get_product_info("Product Type")
    num_reviews = get_product_info("Number of reviews")

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category,
        "image_url": image_url,
        "description": description,
        "upc": upc,
        "product_type": product_type,
        "number_of_reviews": num_reviews,
    }


def main() -> tuple[pd.DataFrame, dict]:
    """Orquestra as funções."""
    books_data = {}
    soups = scrapper(INDEX_URL, iterate=True)
    book_links = get_books_links(soups)
    for title, link in tqdm(book_links.items()):
        book_soup = scrapper(link, iterate=False)
        books_data[title] = get_book_details(book_soup, link)
    books_table = pd.DataFrame(books_data).transpose().reset_index(drop=True)
    books_table["currency"] = books_table["price"].str.extract(r"([^\d\.]+)")
    books_table["price"] = books_table["price"].str.extract(r"(\d+\.\d+)")
    books_table.to_csv("../data/books.csv", index=False, encoding="utf-8")
    table["price"] = table["price"].astype(float)
    table["rating"] = table["rating"].astype(int)
    table["number_of_reviews"] = table["number_of_reviews"].astype(int)
    table.to_sql("books", engine, if_exists="replace", index=False)
    return books_table, books_data


# %%

if __name__ == "__main__":
    table, dic = main()
# %%
