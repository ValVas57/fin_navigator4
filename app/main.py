from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="FinNavigator")

@app.get("/")
async def root():
    return {"message": "FinNavigator is running!"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# Статика (HTML)
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
