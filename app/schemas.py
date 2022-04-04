# Below Class Defintion will specify what a Request and Response should look like.
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostRequest(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    published: bool
    created_at: datetime

class PostResponseWithLikes(PostResponse):
    likes: int

class UserRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class VoteData(BaseModel):
    post_id: int
    vote_dir: bool