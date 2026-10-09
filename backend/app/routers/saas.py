from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pathlib import Path
import json
import io

from app.database import SessionLocal, engine
from app.models.saas import SaaSIdea
from app.schemas.saas import SaaSIdea as SaaSIdeaSchema
from app.utils.ingest import ingest_file, compute_dedup_key

router = APIRouter(prefix="/api/saas", tags=["saas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[SaaSIdeaSchema])
def list_saas(
    skip: int = 0,
    limit: int = 100,
    q: Optional[str] = None,
    min_score: Optional[int] = None,
    max_score: Optional[int] = None,
    min_revenue: Optional[float] = None,
    max_revenue: Optional[float] = None,
    has_traffic: Optional[bool] = None,
    has_cost: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SaaSIdea)
    if q:
        qlow = f"%{q.lower()}%"
        query = query.filter(
            (SaaSIdea.idea.ilike(qlow)) |
            (SaaSIdea.icp.ilike(qlow)) |
            (SaaSIdea.growth_tactics.ilike(qlow))
        )
    if min_score is not None:
        query = query.filter(SaaSIdea.solopreneur_score >= min_score)
    if max_score is not None:
        query = query.filter(SaaSIdea.solopreneur_score <= max_score)
    if min_revenue is not None:
        query = query.filter(SaaSIdea.monthly_revenue >= min_revenue)
    if max_revenue is not None:
        query = query.filter(SaaSIdea.monthly_revenue <= max_revenue)
    if has_traffic is not None:
        if has_traffic:
            query = query.filter(SaaSIdea.monthly_traffic.isnot(None))
        else:
            query = query.filter(SaaSIdea.monthly_traffic.is_(None))
    if has_cost is not None:
        if has_cost:
            query = query.filter(SaaSIdea.starting_costs.isnot(None))
        else:
            query = query.filter(SaaSIdea.starting_costs.is_(None))
    items = query.offset(skip).limit(limit).all()
    return items

@router.get("/facets")
def facets(db: Session = Depends(get_db)):
    items = db.query(SaaSIdea).all()
    icps = {}
    tactics = {}
    for it in items:
        if it.icp:
            for tok in str(it.icp).split(','):
                tok = tok.strip().lower()
                if tok:
                    icps[tok] = icps.get(tok, 0) + 1
        if it.growth_tactics:
            try:
                arr = json.loads(it.growth_tactics) if isinstance(it.growth_tactics, str) else it.growth_tactics
                if isinstance(arr, list):
                    for t in arr:
                        t = str(t).strip().lower()
                        if t:
                            tactics[t] = tactics.get(t, 0) + 1
            except:
                pass
    return {"icps": icps, "tactics": tactics}

@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    items = db.query(SaaSIdea).all()
    total = len(items)
    scores = [i.solopreneur_score for i in items if i.solopreneur_score is not None]
    revs = [float(i.monthly_revenue) for i in items if i.monthly_revenue is not None]
    return {
        "total": total,
        "avg_score": sum(scores)/len(scores) if scores else 0,
        "max_revenue": max(revs) if revs else 0,
        "total_revenue": sum(revs) if revs else 0
    }

@router.post("/ingest")
def ingest(
    file: UploadFile = File(...),
    dry_run: bool = False,
    db: Session = Depends(get_db)
):
    uploads = Path(__file__).parent.parent.parent.parent / "data" / "uploads"
    uploads.mkdir(parents=True, exist_ok=True)
    path = uploads / file.filename
    with open(path, "wb") as f:
        f.write(file.file.read())
    try:
        res = ingest_file(db, str(path), dry_run=dry_run)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ingest/cli")
def ingest_cli(path: str = Query(...), dry_run: bool = False, db: Session = Depends(get_db)):
    try:
        res = ingest_file(db, path, dry_run=dry_run)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
