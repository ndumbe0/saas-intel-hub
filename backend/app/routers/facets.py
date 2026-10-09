from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.database import SessionLocal

router = APIRouter(prefix="/api/facets", tags=["facets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total = db.query(func.count()).select_from(text("saas_ideas")).scalar()
    return {"total": total}
