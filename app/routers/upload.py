from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User
import openpyxl
from io import BytesIO
from datetime import datetime

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Загрузить Excel файл с расходами"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(400, "Файл должен быть в формате Excel (.xlsx, .xls)")
    
    try:
        contents = await file.read()
        workbook = openpyxl.load_workbook(BytesIO(contents))
        sheet = workbook.active
        
        expenses = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] and row[1]:
                expenses.append({
                    "category": row[0],
                    "amount": float(row[1]),
                    "date": str(row[2]) if row[2] else datetime.now().strftime("%Y-%m-%d")
                })
        
        return {
            "status": "ok",
            "message": f"Файл {file.filename} обработан",
            "rows": len(expenses),
            "data": expenses[:10]
        }
    except Exception as e:
        raise HTTPException(500, f"Ошибка обработки файла: {str(e)}")
