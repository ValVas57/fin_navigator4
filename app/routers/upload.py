from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User
from pydantic import BaseModel
import openai
import os

router = APIRouter(prefix="/chat", tags=["chat"])

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    message: str

@router.post("/message")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not openai.api_key:
        raise HTTPException(500, "OpenAI API key not configured")
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — финансовый ассистент ФинНавигатор. Помогай пользователю с вопросами о финансах."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"Ошибка AI: {str(e)}")
