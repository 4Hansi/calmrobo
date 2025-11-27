# backend/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from pydantic import BaseModel

from .database import SessionLocal
from . import models

router = APIRouter()

SECRET_KEY = "SUPER_SECRET_JWT_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 1440  # 1 day

# Use argon2 to avoid bcrypt Windows issues
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# Pydantic model for request body
class AuthRequest(BaseModel):
    email: str
    password: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup")
def signup(data: AuthRequest, db: Session = Depends(get_db)):
    email = data.email
    password = data.password

    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(data: AuthRequest, db: Session = Depends(get_db)):
    email = data.email
    password = data.password

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
