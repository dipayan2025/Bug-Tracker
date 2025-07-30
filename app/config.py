
# app/config.py

from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    DB_NAME: str = os.getenv("DB_NAME")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # default to HS256

settings = Settings()
