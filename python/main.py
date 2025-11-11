from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import yaml
import uuid

from database import get_db, init_db
import models

# OpenAPI 문서 로드
with open("openapi.yaml", "r", encoding="utf-8") as f:
    openapi_schema = yaml.safe_load(f)

app = FastAPI(
    title=openapi_schema["info"]["title"],
    description=openapi_schema["info"]["description"],
    version=openapi_schema["info"]["version"],
    servers=openapi_schema["servers"]
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터베이스 초기화
@app.on_event("startup")
def startup_event():
    init_db()

# OpenAPI 스키마 오버라이드
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# ==================== Posts Endpoints ====================

@app.get("/api/posts", tags=["Posts"])
def get_posts(db: Session = Depends(get_db)):
    """게시물 목록 조회"""
    posts = db.query(models.Post).all()
    return [
        {
            "id": post.id,
            "username": post.username,
            "content": post.content,
            "likes": post.likes,
            "createdAt": post.created_at.isoformat(),
            "updatedAt": post.updated_at.isoformat()
        }
        for post in posts
    ]


@app.post("/api/posts", status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create_post(request: dict, db: Session = Depends(get_db)):
    """게시물 생성"""
    username = request.get("username")
    content = request.get("content")
    
    if not username or not content:
        raise HTTPException(
            status_code=400,
            detail={"message": "username과 content는 필수입니다.", "code": "BAD_REQUEST"}
        )
    
    post_id = str(uuid.uuid4())
    new_post = models.Post(
        id=post_id,
        username=username,
        content=content,
        likes=0
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {
        "id": new_post.id,
        "username": new_post.username,
        "content": new_post.content,
        "likes": new_post.likes,
        "createdAt": new_post.created_at.isoformat(),
        "updatedAt": new_post.updated_at.isoformat()
    }


@app.get("/api/posts/{postId}", tags=["Posts"])
def get_post_by_id(postId: str, db: Session = Depends(get_db)):
    """단일 게시물 조회"""
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"message": "게시물을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    return {
        "id": post.id,
        "username": post.username,
        "content": post.content,
        "likes": post.likes,
        "createdAt": post.created_at.isoformat(),
        "updatedAt": post.updated_at.isoformat()
    }


@app.patch("/api/posts/{postId}", tags=["Posts"])
def update_post(postId: str, request: dict, db: Session = Depends(get_db)):
    """게시물 업데이트"""
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"message": "게시물을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    username = request.get("username")
    content = request.get("content")
    
    if not username or not content:
        raise HTTPException(
            status_code=400,
            detail={"message": "username과 content는 필수입니다.", "code": "BAD_REQUEST"}
        )
    
    post.username = username
    post.content = content
    post.updated_at = datetime.now()
    
    db.commit()
    db.refresh(post)
    
    return {
        "id": post.id,
        "username": post.username,
        "content": post.content,
        "likes": post.likes,
        "createdAt": post.created_at.isoformat(),
        "updatedAt": post.updated_at.isoformat()
    }


@app.delete("/api/posts/{postId}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
def delete_post(postId: str, db: Session = Depends(get_db)):
    """게시물 삭제"""
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"message": "게시물을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    db.delete(post)
    db.commit()
    return None


# ==================== Comments Endpoints ====================

@app.get("/api/posts/{postId}/comments", tags=["Comments"])
def get_comments(postId: str, db: Session = Depends(get_db)):
    """게시물의 댓글 목록 조회"""
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"message": "게시물을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    comments = db.query(models.Comment).filter(models.Comment.post_id == postId).all()
    
    return [
        {
            "id": comment.id,
            "postId": comment.post_id,
            "username": comment.username,
            "content": comment.content,
            "createdAt": comment.created_at.isoformat(),
            "updatedAt": comment.updated_at.isoformat()
        }
        for comment in comments
    ]


@app.post("/api/posts/{postId}/comments", status_code=status.HTTP_201_CREATED, tags=["Comments"])
def create_comment(postId: str, request: dict, db: Session = Depends(get_db)):
    """댓글 생성"""
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"message": "게시물을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    username = request.get("username")
    content = request.get("content")
    
    if not username or not content:
        raise HTTPException(
            status_code=400,
            detail={"message": "username과 content는 필수입니다.", "code": "BAD_REQUEST"}
        )
    
    comment_id = str(uuid.uuid4())
    new_comment = models.Comment(
        id=comment_id,
        post_id=postId,
        username=username,
        content=content
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return {
        "id": new_comment.id,
        "postId": new_comment.post_id,
        "username": new_comment.username,
        "content": new_comment.content,
        "createdAt": new_comment.created_at.isoformat(),
        "updatedAt": new_comment.updated_at.isoformat()
    }


@app.get("/api/posts/{postId}/comments/{commentId}", tags=["Comments"])
def get_comment_by_id(postId: str, commentId: str, db: Session = Depends(get_db)):
    """특정 댓글 조회"""
    comment = db.query(models.Comment).filter(
        models.Comment.id == commentId,
        models.Comment.post_id == postId
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=404,
            detail={"message": "댓글을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    return {
        "id": comment.id,
        "postId": comment.post_id,
        "username": comment.username,
        "content": comment.content,
        "createdAt": comment.created_at.isoformat(),
        "updatedAt": comment.updated_at.isoformat()
    }


@app.patch("/api/posts/{postId}/comments/{commentId}", tags=["Comments"])
def update_comment(postId: str, commentId: str, request: dict, db: Session = Depends(get_db)):
    """댓글 업데이트"""
    comment = db.query(models.Comment).filter(
        models.Comment.id == commentId,
        models.Comment.post_id == postId
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=404,
            detail={"message": "댓글을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    username = request.get("username")
    content = request.get("content")
    
    if not username or not content:
        raise HTTPException(
            status_code=400,
            detail={"message": "username과 content는 필수입니다.", "code": "BAD_REQUEST"}
        )
    
    comment.username = username
    comment.content = content
    comment.updated_at = datetime.now()
    
    db.commit()
    db.refresh(comment)
    
    return {
        "id": comment.id,
        "postId": comment.post_id,
        "username": comment.username,
        "content": comment.content,
        "createdAt": comment.created_at.isoformat(),
        "updatedAt": comment.updated_at.isoformat()
    }


@app.delete("/api/posts/{postId}/comments/{commentId}", status_code=status.HTTP_204_NO_CONTENT, tags=["Comments"])
def delete_comment(postId: str, commentId: str, db: Session = Depends(get_db)):
    """댓글 삭제"""
    comment = db.query(models.Comment).filter(
        models.Comment.id == commentId,
        models.Comment.post_id == postId
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=404,
            detail={"message": "댓글을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    db.delete(comment)
    db.commit()
    return None


# ==================== Likes Endpoints ====================

@app.post("/api/posts/{postId}/likes", status_code=status.HTTP_201_CREATED, tags=["Likes"])
def like_post(postId: str, request: dict, db: Session = Depends(get_db)):
    """게시물 좋아요"""
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"message": "게시물을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    username = request.get("username")
    
    if not username:
        raise HTTPException(
            status_code=400,
            detail={"message": "username은 필수입니다.", "code": "BAD_REQUEST"}
        )
    
    # 이미 좋아요를 눌렀는지 확인
    existing_like = db.query(models.Like).filter(
        models.Like.post_id == postId,
        models.Like.username == username
    ).first()
    
    if existing_like:
        return {
            "postId": postId,
            "username": username,
            "liked": True
        }
    
    # 좋아요 추가
    new_like = models.Like(
        post_id=postId,
        username=username
    )
    
    db.add(new_like)
    post.likes += 1
    db.commit()
    
    return {
        "postId": postId,
        "username": username,
        "liked": True
    }


@app.delete("/api/posts/{postId}/likes", status_code=status.HTTP_204_NO_CONTENT, tags=["Likes"])
def unlike_post(postId: str, username: str, db: Session = Depends(get_db)):
    """게시물 좋아요 취소"""
    post = db.query(models.Post).filter(models.Post.id == postId).first()
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"message": "게시물을 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    like = db.query(models.Like).filter(
        models.Like.post_id == postId,
        models.Like.username == username
    ).first()
    
    if not like:
        raise HTTPException(
            status_code=404,
            detail={"message": "좋아요를 찾을 수 없습니다.", "code": "NOT_FOUND"}
        )
    
    db.delete(like)
    post.likes -= 1
    db.commit()
    return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
