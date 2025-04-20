# app/schemas/user.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class User(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True
