from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import auth, profile, goals, chat
from app.routers import auth, profile, goals, chat, upload
from app.routers import auth, profile, goals, chat, excel_upload

app = FastAPI(title="FinNavigator", docs_url="/docs", redoc_url="/redoc")
app.include_router(upload.router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(goals.router)
app.include_router(chat.router)

# Эндпоинты ДО статики
@app.get("/health")
async def health():
    return {"status": "ok"}

# Подключаем статические файлы (ДОЛЖНО БЫТЬ ПОСЛЕДНИМ!)
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
