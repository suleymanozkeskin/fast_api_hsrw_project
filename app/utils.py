from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # bcrypt as default hashing algorithm

def hash(password: str):
    
    return pwd_context.hash(password)