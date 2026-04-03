from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import authenticate_user, create_access_token, get_password_hash, get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str = None

@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(400, "Email already registered")
    hashed = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, password_hash=hashed, full_name=user_data.full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "email": new_user.email, "full_name": new_user.full_name}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer", "user_id": user.id}

@router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "full_name": current_user.full_name}
