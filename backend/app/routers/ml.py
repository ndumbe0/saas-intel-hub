from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter(prefix="/api/ml", tags=["ml"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/status")
def status():
    return {"status": "ready", "note": "ML models not trained yet"}
