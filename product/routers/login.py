import os
from fastapi import APIRouter, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from ..database import get_db
from .. import schemas, models

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter(tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    seller = (
        db.query(models.Seller)
        .filter(models.Seller.username == request.username)
        .first()
    )
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Username not found or invalid user.",
        )
    if not pwd_context.verify(request.password, seller.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid password.",
        )
    access_token = generate_token(data={"sub": seller.username})
    return {"access_token": access_token, "token_type": "bearer"}
