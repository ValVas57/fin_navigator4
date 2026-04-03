from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/message")
async def chat(request: ChatRequest):
    # Простой ответ-заглушка
    answers = [
        "Хороший вопрос! Рекомендую откладывать 10% от дохода.",
        "Покупка ноутбука за 50 000 ₽ — это разумно, если он нужен для работы.",
        "Чтобы накопить, попробуйте сократить расходы на кафе и подписки.",
        "Финансовая подушка должна составлять 3-6 месяцев расходов.",
        "Инвестировать лучше после создания резервного фонда."
    ]
    reply = random.choice(answers) + f" (Ваш вопрос: {request.message})"
    return {"response": reply}
