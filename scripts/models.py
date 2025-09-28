# %%
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

USER = os.getenv("user")
PASSWORD = quote_plus(os.getenv("password"))
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
# %%
db_url = (
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"
)
# %%
engine = create_engine(db_url)

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    rating = Column(Integer)
    availability = Column(String)
    category = Column(String)
    image_url = Column(String)
    description = Column(String)
    upc = Column(String)
    product_type = Column(String)
    number_of_reviews = Column(Integer)
    currency = Column(String)

    def __repr__(self):
        return f"Book(id={self.id}, title={self.title}, price={self.price})"


class CategoryStats(Base):
    __tablename__ = "categorias"

    category = Column(String, primary_key=True)
    quantidade_livros = Column(Integer)
    media_precos = Column(Float)
    max_precos = Column(Float)
    min_precos = Column(Float)
    rating_medio = Column(Float)

    def __repr__(self):
        return (
            f"CategoryStats(category='{self.category}', books={self.quantidade_livros})"
        )


class Overview(Base):
    __tablename__ = "overview"

    total_livros = Column(Integer, primary_key=True)
    preco_medio = Column(Float)
    total_rating_5 = Column(Integer)
    total_rating_4 = Column(Integer)
    total_rating_3 = Column(Integer)
    total_rating_2 = Column(Integer)
    total_rating_1 = Column(Integer)

    def __repr__(self):
        return f"Overview(total_livros={self.total_livros}, preco_medio={self.preco_medio:.2f})"


class Top15Price(Base):
    __tablename__ = "top15_price"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    rating = Column(Integer)
    availability = Column(String)
    category = Column(String)
    image_url = Column(String)
    description = Column(String)
    upc = Column(String)
    product_type = Column(String)
    number_of_reviews = Column(Integer)
    currency = Column(String)

    def __repr__(self):
        return f"Top15Price(title='{self.title}', price={self.price})"


class TopRated(Base):
    __tablename__ = "top_rated"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    rating = Column(Integer)

    def __repr__(self):
        return f"TopRated(id={self.id}, title='{self.title}')"


Session = sessionmaker(bind=engine)


if __name__ == "__main__":
    with Session() as session:
        print("--- Exemplo de Consultas ---")

        # 1. Consulta na view 'overview' (deve retornar um único resultado)
        overview_data = session.query(Overview).one()
        print(
            f"\n[Visão Geral] Total de livros: {overview_data.total_livros}, Preço Médio: £{overview_data.preco_medio:.2f}"
        )

        # 2. Consulta na view 'categorias'
        print("\n[Estatísticas por Categoria]")
        stats = (
            session.query(CategoryStats)
            .order_by(CategoryStats.quantidade_livros.desc())
            .limit(5)
            .all()
        )
        for stat in stats:
            print(
                f"- Categoria '{stat.category}': {stat.quantidade_livros} livros, Rating Médio: {stat.rating_medio}"
            )

        # 3. Consulta na view 'top_rated'
        print("\n[Top 5 Livros com Rating 5]")
        top_rated_books = session.query(TopRated).limit(5).all()
        for book in top_rated_books:
            print(f"- {book.title}")

        # 4. Consulta na view 'top15_price'
        print("\n[Top 5 Livros Mais Caros]")
        top_price_books = session.query(Top15Price).limit(5).all()
        for book in top_price_books:
            print(f"- {book.title} (£{book.price})")

# %%
