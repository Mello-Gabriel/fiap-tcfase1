"""Modulo para realizar scrapping do site."""

# %%
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

urls = [BASE_URL.format(n) for n in range(1, 51, 1)]


# %%
def scrapper(urls: list[str]) -> BeautifulSoup:
    """Faz a raspagem simples do site e retorna um objeto BeautifulSoup

    Parametros:
    ----------

    url : str = Endereço em string do site a ser raspado

    Return:
    ------
    sopa : BeautifulSoup = Obejeto com o conteúdo do site

    """
    html = ""
    for url in urls:
        dado_raspado = requests.get(url=url).text
        html = html + dado_raspado
        extracoes = BeautifulSoup(html, "html.parser")

    return extracoes


def get_tittles(sopa: BeautifulSoup) -> list[str]:
    """Captura os títulos dos livros

    Parâmetros:
    ----------

    sopa : BeautifulSoup = Objeto BeautifulSoup com as extrações

    Return:
    tiitulos : list[str] = Lista com os nomes dos livros

    """
    livros = []
    articles = sopa.find_all("article", class_="product_pod")
    for article in articles:
        titulo = article.h3.a["title"]
        preco = article.select_one('p.price_color').text
        avaliacao = article.select_one('p.star-rating')['class'][1]
        livros.append({
            "titulo":"titulo",
            "preco"
        })
    return titulos
# %%
def get_prices(sopa: BeautifulSoup)-> list[str]:
    """Captura os valores dos livros

    Parâmetros:
    ----------

    sopa: BeautifulSoup = Objeto BeautifulSoup com as extrações

    """
    valores = []
    headers = sopa.find_all("p.price_color")
    for price in headers:
        print(price)
    return None

print(get_prices(books))
# %%

if __name__ == "__main__":
    books = scrapper(urls)
    print(get_tittles(books))
# %%
