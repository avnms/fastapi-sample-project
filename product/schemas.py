from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: int


class DisplayProduct(BaseModel):
    name: str
    description: str


class Seller(BaseModel):
    username: str
    email: str
    password: str


class DisplaySeller(BaseModel):
    username: str
    email: str
