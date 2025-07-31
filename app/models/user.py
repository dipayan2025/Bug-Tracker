from beanie import Document
from pydantic import Field, EmailStr
from typing import Literal, Optional
from datetime import datetime

class User(Document):
    email: EmailStr
    username: str
    password: str  # Hashed
    role: Literal['reporter', 'developer', 'manager'] = 'reporter'
    disabled: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # MongoDB collection name

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "user123",
                "password": "hashedpassword",
                "role": "developer",
                "disabled": False
            }
        }
