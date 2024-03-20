from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext
from . import schemas
from . import models
from .database import engine, SessionLocal

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

models.Base.metadata.create_all(engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products", response_model=List[schemas.DisplayProduct], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.get("/product/{id}", response_model=schemas.DisplayProduct, tags=["Products"])
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found."
        )
    return product


@app.post("/product", status_code=status.HTTP_201_CREATED, tags=["Products"])
def add_product(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=1,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


@app.put("/product/{id}", tags=["Products"])
def update_product(request: schemas.Product, id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return {"message": "Product updated successfully"}


@app.delete("/product/{id}", tags=["Products"])
def delete_product(id: int, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()
    return {"message": "Product deleted successfully."}


@app.post("/seller", response_model=schemas.DisplaySeller, tags=["Seller"])
def create_seller(request: schemas.Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password)
    new_seller = models.Seller(
        username=request.username,
        email=request.email,
        password=hashed_password,
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller
