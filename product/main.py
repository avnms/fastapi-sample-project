from fastapi import FastAPI
from .models import Product

app = FastAPI()


@app.post("/product")
def add_product(request: Product):
    return request
