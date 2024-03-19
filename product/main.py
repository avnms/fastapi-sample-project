from fastapi import FastAPI
from .schemas import Product
from . import models
from .database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.post("/product")
def add_product(request: Product):
    return request
