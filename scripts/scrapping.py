"""Modulo para realizar scrapping do site."""

# %%
import requests
from bs4 import BeautifulSoup

INDEX_URL = "https://books.toscrape.com/index.html"

BASE_URL = "https://books.toscrape.com/"


# %%
def scrapper(urls: list[str] | str) -> BeautifulSoup:
    """Faz a raspagem simples do site e retorna um objeto BeautifulSoup.

    Parametros:
    ----------

    url : str = Endereço em string do site a ser raspado

    Return:
    ------
    sopa : BeautifulSoup = Obejeto com o conteúdo do site

    """
    if isinstance(urls, str):
        urls = [urls]
    html = ""
    for url in urls:
        dado_raspado = requests.get(url=url, timeout=300).text
        html = html + dado_raspado
        extracoes = BeautifulSoup(html, "html.parser")

    return extracoes


# %%


def get_categories_links(sopa: BeautifulSoup) -> dict[str, str]:
    """Captura as links das categorias do site.

    Parametros:
    ----------
    sopa : BeautifulSoup = Objeto BeautifulSoup com as extrações

    Return:
    ------
    categorias : list[str] = Lista com as categorias do site

    """
    seletor = ".side_categories ul li ul a"
    tags_de_categoria = sopa.select(seletor)

    categorias = {}

    # Iteramos sobre cada tag <a> que encontramos
    for tag in tags_de_categoria:
        # Extrai o texto e remove espaços extras
        texto_categoria = tag.get_text().strip()
        # Extrai o atributo href
        link_categoria = str(tag.get("href"))
        categorias[texto_categoria] = BASE_URL + link_categoria
    return categorias


# %%


def get_tittles(sopa: BeautifulSoup) -> list[dict]:
    """Captura os títulos dos livros.

    Parâmetros:
    ----------

    sopa : BeautifulSoup = Objeto BeautifulSoup com as extrações

    Return:
    ------
    titulos : list[str] = Lista com os nomes dos livros

    """
    livros = []
    articles = sopa.find_all("article", class_="product_pod")
    for article in articles:
        titulo = article.h3.a["title"]
        preco = article.select_one("p.price_color").text
        avaliacao = article.select_one("p.star-rating")["class"][1]
        livros.append({"titulo": titulo, "preco": preco, "avaliacao": avaliacao})
    return livros


# %%
def get_prices(sopa: BeautifulSoup) -> list[str]:
    """Captura os valores dos livros.

    Parâmetros:
    ----------

    sopa: BeautifulSoup = Objeto BeautifulSoup com as extrações

    """
    valores = []
    headers = sopa.find_all("p.price_color")
    for price in headers:
        print(price)
    return None


# %%

if __name__ == "__main__":
    categorias = scrapper(INDEX_URL)
    links_categorias = get_categories_links(categorias)


# %%
