from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    username: str
    password: str

class Post(BaseModel):
    title: str
    content: str
    author: str
