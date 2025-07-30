from pydantic import BaseModel, EmailStr
from typing import Literal
from typing import Optional

class UserProfileUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]

class UpdateRoleRequest(BaseModel):
    role: Literal["reporter", "developer", "manager"]
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
    class Config:
        orm_mode = True
