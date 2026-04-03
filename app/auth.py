from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.auth import get_password_hash
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str = None

@router.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            raise HTTPException(400, "Email already registered")
        hashed = get_password_hash(user_data.password)
        new_user = User(email=user_data.email, password_hash=hashed, full_name=user_data.full_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"id": new_user.id, "email": new_user.email, "full_name": new_user.full_name}
    except Exception as e:
        raise HTTPException(500, str(e))
