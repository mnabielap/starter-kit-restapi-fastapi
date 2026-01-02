from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils import email as email_utils

router = APIRouter()

@router.post("/register", response_model=schemas.AuthResponse, status_code=201)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Register a new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already taken")
    
    user_in.role = "user"
    
    user = crud.user.create(db, obj_in=user_in)
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_MINUTES)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)
    
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    refresh_token = security.create_refresh_token(user.id, expires_delta=refresh_token_expires)
    
    crud.token.create(
        db, 
        token=refresh_token, 
        user_id=user.id, 
        type="refresh", 
        expires=datetime.utcnow() + refresh_token_expires
    )

    return {
        "user": user,
        "tokens": {
            "access": {"token": access_token, "expires": datetime.utcnow() + access_token_expires},
            "refresh": {"token": refresh_token, "expires": datetime.utcnow() + refresh_token_expires}
        }
    }

@router.post("/login", response_model=schemas.AuthResponse)
def login(
    db: Session = Depends(deps.get_db),
    email: str = Body(...),
    password: str = Body(...)
) -> Any:
    user = crud.user.authenticate(db, email=email, password=password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_MINUTES)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)
    
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    refresh_token = security.create_refresh_token(user.id, expires_delta=refresh_token_expires)
    
    crud.token.create(
        db, 
        token=refresh_token, 
        user_id=user.id, 
        type="refresh", 
        expires=datetime.utcnow() + refresh_token_expires
    )
    
    return {
        "user": user,
        "tokens": {
            "access": {"token": access_token, "expires": datetime.utcnow() + access_token_expires},
            "refresh": {"token": refresh_token, "expires": datetime.utcnow() + refresh_token_expires}
        }
    }

@router.post("/logout", status_code=204)
def logout(
    refreshToken: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db)
) -> None:
    refresh_token_doc = crud.token.get_by_token(db, token=refreshToken, type="refresh")
    if not refresh_token_doc:
        raise HTTPException(status_code=404, detail="Not found")
    
    crud.token.blacklist_token(db, refreshToken, "refresh")
    return None

@router.post("/refresh-tokens", response_model=schemas.AuthTokens)
def refresh_tokens(
    refreshToken: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db)
) -> Any:
    try:
        payload = security.jwt.decode(refreshToken, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
    except:
         raise HTTPException(status_code=401, detail="Please authenticate")

    refresh_token_doc = crud.token.get_by_token(db, token=refreshToken, type="refresh")
    if not refresh_token_doc:
         raise HTTPException(status_code=401, detail="Please authenticate")
    
    crud.token.blacklist_token(db, refreshToken, "refresh")
    
    user = crud.user.get(db, id=refresh_token_doc.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_EXPIRATION_MINUTES)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)
    
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    new_refresh_token = security.create_refresh_token(user.id, expires_delta=refresh_token_expires)
    
    crud.token.create(
        db, 
        token=new_refresh_token, 
        user_id=user.id, 
        type="refresh", 
        expires=datetime.utcnow() + refresh_token_expires
    )
    
    return {
        "access": {"token": access_token, "expires": datetime.utcnow() + access_token_expires},
        "refresh": {"token": new_refresh_token, "expires": datetime.utcnow() + refresh_token_expires}
    }

@router.post("/forgot-password", status_code=204)
def forgot_password(
    email: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db)
) -> None:
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="No users found with this email")
    
    expires = timedelta(minutes=settings.JWT_RESET_PASSWORD_EXPIRATION_MINUTES)
    reset_token = security.create_token(user.id, expires_delta=expires, type="resetPassword")
    
    crud.token.create(
        db, 
        token=reset_token, 
        user_id=user.id, 
        type="resetPassword", 
        expires=datetime.utcnow() + expires
    )
    
    email_utils.send_reset_password_email(email, reset_token)
    return None

@router.post("/reset-password", status_code=204)
def reset_password(
    token: str = Query(...),
    password: str = Body(..., embed=True),
    db: Session = Depends(deps.get_db)
) -> None:
    try:
        token_doc = crud.token.get_by_token(db, token, "resetPassword")
        if not token_doc:
            raise HTTPException(status_code=401, detail="Password reset failed")
        
        user = crud.user.get(db, id=token_doc.user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Password reset failed")
            
        crud.user.update(db, db_obj=user, obj_in={"password": password})
        crud.token.delete_tokens_by_user(db, user.id, "resetPassword")
    except Exception:
        raise HTTPException(status_code=401, detail="Password reset failed")
    
    return None

@router.post("/send-verification-email", status_code=204)
def send_verification_email(
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> None:
    expires = timedelta(minutes=settings.JWT_VERIFY_EMAIL_EXPIRATION_MINUTES)
    verify_token = security.create_token(current_user.id, expires_delta=expires, type="verifyEmail")
    
    crud.token.create(
        db, 
        token=verify_token, 
        user_id=current_user.id, 
        type="verifyEmail", 
        expires=datetime.utcnow() + expires
    )
    
    email_utils.send_verification_email(current_user.email, verify_token)
    return None

@router.post("/verify-email", status_code=204)
def verify_email(
    token: str = Query(...),
    db: Session = Depends(deps.get_db)
) -> None:
    token_doc = crud.token.get_by_token(db, token, "verifyEmail")
    if not token_doc:
        raise HTTPException(status_code=401, detail="Email verification failed")
    
    user = crud.user.get(db, id=token_doc.user_id)
    if not user:
         raise HTTPException(status_code=401, detail="Email verification failed")
         
    crud.user.update(db, db_obj=user, obj_in={"is_email_verified": True})
    crud.token.delete_tokens_by_user(db, user.id, "verifyEmail")
    return None