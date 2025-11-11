from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Post schemas
class CreatePostRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)


class UpdatePostRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=1000)


class Post(BaseModel):
    id: str
    username: str
    content: str
    createdAt: datetime
    updatedAt: datetime
    likeCount: int = Field(ge=0)
    commentCount: int = Field(ge=0)

    class Config:
        from_attributes = True


# Comment schemas
class CreateCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=500)


class UpdateCommentRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1, max_length=500)


class Comment(BaseModel):
    id: str
    postId: str
    username: str
    content: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# Like schemas
class LikeRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)


class LikeResponse(BaseModel):
    postId: str
    username: str
    likedAt: datetime

    class Config:
        from_attributes = True


# Error schema
class Error(BaseModel):
    error: str
    message: str
    details: Optional[str] = None
