from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")
