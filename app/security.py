from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_verification_token(email: str):
    expire = datetime.utcnow() + timedelta(hours=24) # Token vale por 1 dia
    to_encode = {"exp": expire, "sub": email}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)