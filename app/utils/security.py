from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "MY_SECRET_KEY"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Create JWT token
def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")