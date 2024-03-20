from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: int


class DisplaySeller(BaseModel):
    username: str
    email: str


class DisplayProduct(BaseModel):
    name: str
    description: str
    seller: DisplaySeller


class Seller(BaseModel):
    username: str
    email: str
    password: str
