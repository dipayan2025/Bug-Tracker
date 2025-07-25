from pydantic import BaseModel, EmailStr
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    username: str
    role: Literal["reporter", "developer", "manager"]
