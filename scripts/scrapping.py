"""Modulo para realizar scrapping do site"""
#%%
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

urls = [BASE_URL.format(n) for n in range(1,51,1)]

#%%
def scrapper(urls:list[str]) -> BeautifulSoup:
    """Faz a raspagem simples do site e retorna um objeto BeautifulSoup

    Parametros:
    ----------

    url : str = Endereço em string do site a ser raspado

    Return:
    -------

    sopa : BeautifulSoup = Obejeto com o conteúdo do site
    
    """
    html = str()
    for url in urls:
        dado_raspado = requests.get(url=url).text
        html = html + dado_raspado
        extracoes = BeautifulSoup(html, "html.parser")
    
    return extracoes

def get_tittles(sopa:BeautifulSoup)-> list[str]:
    """Captura os títulos dos livros
    
    Parâmetros:
    ----------

    sopa : BeautifulSoup = Objeto BeautifulSoup com as extrações

    Return:

    tiitulos : list[str] = Lista com os nomes dos livros

    """
    titulos = []
    headers = sopa.find_all("h3")
    for h3 in headers:
        titulos.append(str(h3.a["title"]))
    return titulos



if __name__ == "__main__":
    books = scrapper(urls)
    print(get_tittles(books))
# %%
