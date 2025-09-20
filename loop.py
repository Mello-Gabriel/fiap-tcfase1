from bs4 import BeautifulSoup
import requests
url = 'http://books.toscrape.com/'
books_data = []
for page_num in range(1, 51):
    url = f'http://books.toscrape.com/catalogue/page-{page_num}.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = soup.find_all("h3")
    books_extracted = 0
    for book in books: 
        book_url = book.find("a")['href']
        book_response = requests.get('http://books.toscrape.com/catalogue/' + book_url)  
        book_soup = BeautifulSoup(book_response.text, "html.parser")
        title = book_soup.find('h1').text
        category = book_soup.find("ul", class_='breadcrumb').find_all("a")[2].get_text() 
        price = book_soup.find("p", class_ = "price_color").get_text()[2:]
        rating = book_soup.find("p", class_='star-rating')['class'][1]
        availability = book_soup.find("p", class_ = "instock availability").text.strip()

        books_extracted += 1
        books_data.append([title, category, price, rating, availability])
        print(books_data)
   
    print(f"books extracted: {books_extracted}")
