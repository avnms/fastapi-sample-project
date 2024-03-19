from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from typing import List
from . import schemas
from . import models
from .database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products", response_model=List[schemas.DisplayProduct])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.get("/product/{id}", response_model=schemas.DisplayProduct)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    return product


@app.post("/product", status_code=status.HTTP_201_CREATED)
def add_product(request: schemas.Product, db: Session = Depends(get_db)):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


@app.put("/product/{id}")
def update_product(request: schemas.Product, id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if not product.first():
        pass
    product.update(request.model_dump())
    db.commit()
    return {"message": "Product updated successfully"}


@app.delete("/product/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db.query(models.Product).filter(models.Product.id == id).delete(
        synchronize_session=False
    )
    db.commit()
    return {"message": "Product deleted successfully."}
