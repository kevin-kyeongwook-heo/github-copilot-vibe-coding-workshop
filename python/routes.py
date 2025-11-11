from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Post as PostModel, Comment as CommentModel, Like as LikeModel
from schemas import (
    Post, CreatePostRequest, UpdatePostRequest,
    Comment, CreateCommentRequest, UpdateCommentRequest,
    LikeRequest, LikeResponse
)
from datetime import datetime

router = APIRouter()


# Helper function to convert Post model to response
def post_to_response(post: PostModel, db: Session) -> Post:
    like_count = db.query(LikeModel).filter(LikeModel.post_id == post.id).count()
    comment_count = db.query(CommentModel).filter(CommentModel.post_id == post.id).count()
    
    return Post(
        id=str(post.id),
        username=post.username,
        content=post.content,
        createdAt=post.created_at,
        updatedAt=post.updated_at,
        likeCount=like_count,
        commentCount=comment_count
    )


# Helper function to convert Comment model to response
def comment_to_response(comment: CommentModel) -> Comment:
    return Comment(
        id=str(comment.id),
        postId=str(comment.post_id),
        username=comment.username,
        content=comment.content,
        createdAt=comment.created_at,
        updatedAt=comment.updated_at
    )


# Posts endpoints
@router.get("/posts", response_model=List[Post], tags=["Posts"])
def list_posts(db: Session = Depends(get_db)):
    """List all posts"""
    posts = db.query(PostModel).all()
    return [post_to_response(post, db) for post in posts]


@router.post("/posts", response_model=Post, status_code=201, tags=["Posts"])
def create_post(request: CreatePostRequest, db: Session = Depends(get_db)):
    """Create a new post"""
    post = PostModel(username=request.username, content=request.content)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post_to_response(post, db)


@router.get("/posts/{postId}", response_model=Post, tags=["Posts"])
def get_post(postId: str, db: Session = Depends(get_db)):
    """Get a specific post"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_to_response(post, db)


@router.patch("/posts/{postId}", response_model=Post, tags=["Posts"])
def update_post(postId: str, request: UpdatePostRequest, db: Session = Depends(get_db)):
    """Update a post"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.username = request.username
    post.content = request.content
    post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return post_to_response(post, db)


@router.delete("/posts/{postId}", status_code=204, tags=["Posts"])
def delete_post(postId: str, db: Session = Depends(get_db)):
    """Delete a post"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()
    return None


# Comments endpoints
@router.get("/posts/{postId}/comments", response_model=List[Comment], tags=["Comments"])
def list_comments(postId: str, db: Session = Depends(get_db)):
    """List comments for a post"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comments = db.query(CommentModel).filter(CommentModel.post_id == int(postId)).all()
    return [comment_to_response(comment) for comment in comments]


@router.post("/posts/{postId}/comments", response_model=Comment, status_code=201, tags=["Comments"])
def create_comment(postId: str, request: CreateCommentRequest, db: Session = Depends(get_db)):
    """Create a comment"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = CommentModel(
        post_id=int(postId),
        username=request.username,
        content=request.content
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment_to_response(comment)


@router.get("/posts/{postId}/comments/{commentId}", response_model=Comment, tags=["Comments"])
def get_comment(postId: str, commentId: str, db: Session = Depends(get_db)):
    """Get a specific comment"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = db.query(CommentModel).filter(
        CommentModel.id == int(commentId),
        CommentModel.post_id == int(postId)
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    return comment_to_response(comment)


@router.patch("/posts/{postId}/comments/{commentId}", response_model=Comment, tags=["Comments"])
def update_comment(postId: str, commentId: str, request: UpdateCommentRequest, db: Session = Depends(get_db)):
    """Update a comment"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = db.query(CommentModel).filter(
        CommentModel.id == int(commentId),
        CommentModel.post_id == int(postId)
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    comment.username = request.username
    comment.content = request.content
    comment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(comment)
    return comment_to_response(comment)


@router.delete("/posts/{postId}/comments/{commentId}", status_code=204, tags=["Comments"])
def delete_comment(postId: str, commentId: str, db: Session = Depends(get_db)):
    """Delete a comment"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment = db.query(CommentModel).filter(
        CommentModel.id == int(commentId),
        CommentModel.post_id == int(postId)
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(comment)
    db.commit()
    return None


# Likes endpoints
@router.post("/posts/{postId}/likes", response_model=LikeResponse, status_code=201, tags=["Likes"])
def like_post(postId: str, request: LikeRequest, db: Session = Depends(get_db)):
    """Like a post"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user already liked the post
    existing_like = db.query(LikeModel).filter(
        LikeModel.post_id == int(postId),
        LikeModel.username == request.username
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Post already liked by user")
    
    like = LikeModel(post_id=int(postId), username=request.username)
    db.add(like)
    db.commit()
    db.refresh(like)
    
    return LikeResponse(
        postId=str(like.post_id),
        username=like.username,
        likedAt=like.liked_at
    )


@router.delete("/posts/{postId}/likes", status_code=204, tags=["Likes"])
def unlike_post(postId: str, username: str, db: Session = Depends(get_db)):
    """Unlike a post"""
    post = db.query(PostModel).filter(PostModel.id == int(postId)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    like = db.query(LikeModel).filter(
        LikeModel.post_id == int(postId),
        LikeModel.username == username
    ).first()
    
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    
    db.delete(like)
    db.commit()
    return None
