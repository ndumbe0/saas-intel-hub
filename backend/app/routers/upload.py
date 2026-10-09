from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

router = APIRouter(prefix="/api/upload", tags=["upload"])

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = Path(__file__).parent.parent.parent.parent / "data" / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "size": dest.stat().st_size}
