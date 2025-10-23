from sqlalchemy import Column, String, Float, Integer, create_engine, Boolean, Float, ForeignKey
from db import Base
from sqlalchemy.orm import declarative_base, relationship

db_user = create_engine("sqlite:///banco.db")
Base_user = declarative_base()

class Book(Base):
    __tablename__ = "books"

   
    id = Column(Integer, primary_key=True) 
    title = Column(String)
    price = Column(Float)
    rating = Column(Integer)
    availability = Column(Integer)
    category = Column(String)
    image_url = Column(String)
    description = Column(String)
    upc = Column(String)
    product_type = Column(String)
    number_of_reviews = Column(Integer)
    currency = Column(String)

class Usuario(Base_user):
    __tablename__ = "usuarios"
    id = Column("id",Integer,primary_key = True, autoincrement = True)
    nome = Column("nome", String)
    email = Column("email",String)
    senha = Column("senha", String)
    admin = Column("admin", Boolean, default = False)

    def __init__(self,nome,email,senha, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin    