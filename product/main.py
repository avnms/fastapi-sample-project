from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, seller, login

app = FastAPI(
    title="Products API",
    description="Get details for all the products on our website",
    terms_of_service="http://www.google.com",
    contact={
        "Developer name": "Sarma",
        "Website": "http://www.google.com",
        "Email": "sarma@abc.com",
    },
    license_info={
        "name": "OpenSource",
        "url": "http://www.google.com",
    },
    docs_url="/documentation",
    redoc_url=None,
)

app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

models.Base.metadata.create_all(engine)
