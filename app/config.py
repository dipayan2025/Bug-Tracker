from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI")
    DB_NAME: str = os.getenv("DB_NAME")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # default to HS256

    # File upload settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 * 1024))  # default 5MB
    ALLOWED_FILE_TYPES: set = {
        "image/png", "image/jpeg", "application/pdf", "text/plain"
    }

    def ensure_upload_dir(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

settings = Settings()
settings.ensure_upload_dir()
