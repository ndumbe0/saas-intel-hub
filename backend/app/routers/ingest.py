from fastapi import APIRouter, Depends, Query, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from app.database import SessionLocal
from app.utils.ingest import load_checkpoint, ingest_full

router = APIRouter(prefix="/api/ingest", tags=["ingest"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/progress")
def progress():
    return load_checkpoint()

@router.post("/start")
def start_ingest(background_tasks: BackgroundTasks, file_path: str = Query(None), db: Session = Depends(get_db)):
    if file_path is None:
        file_path = str(Path(__file__).parent.parent.parent.parent / "data" / "Micro-SaaS Ideas Database [Starter Story].xlsx")
    path = Path(file_path)
    if not path.exists():
        raise HTTPException(404, f"File not found: {file_path}")
    background_tasks.add_task(ingest_full, db, str(path))
    return {"status": "started", "file": str(path)}
