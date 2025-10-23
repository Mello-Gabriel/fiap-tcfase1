from pydantic import BaseModel


class livrosSchema(BaseModel):
    id: int
    title: str
    price: float
    rating: int
    availability: int
    category: str
    image_url: str
    description: str
    upc: str
    product_type: str
    number_of_reviews: int
    currency: str

    class Config:
        from_attributes = True


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    admin: bool = False

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True
