import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
from sqlalchemy.orm import Session

from app.models.saas import SaaSIdea
from app.utils.parsers import (
    clean_currency, clean_decimal, clean_bigint, clean_int,
    clean_float, parse_growth_tactics, normalize_text
)

def compute_dedup_key(idea: str, icp: str) -> str:
    key = normalize_text(idea) + "|" + normalize_text(icp)
    return hashlib.sha256(key.encode('utf-8')).hexdigest()

def ingest_file(db: Session, file_path: str, dry_run: bool = False) -> Dict[str, Any]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    if ext == '.xlsx':
        df = pd.read_excel(path, header=1)
    elif ext == '.csv':
        df = pd.read_csv(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    # Normalize columns
    df.columns = [str(c).strip() for c in df.columns]
    # Map by case-insensitive matching
    colmap = {str(c).lower(): c for c in df.columns}
    
    idea_col = colmap.get('idea')
    rev_col = colmap.get('monthly revenue') or colmap.get('monthly_revenue') or colmap.get('revenue')
    traffic_col = colmap.get('monthly traffic') or colmap.get('monthly_traffic') or colmap.get('traffic')
    rpv_col = colmap.get('revenue per visitor') or colmap.get('revenue_per_visitor') or colmap.get('r pv') or colmap.get('rev per visitor')
    cost_col = colmap.get('starting costs') or colmap.get('starting_costs') or colmap.get('costs')
    score_col = colmap.get('solopreneur score') or colmap.get('solopreneur_score') or colmap.get('score')
    icp_col = colmap.get('icp')
    tactics_col = colmap.get('growth tactics') or colmap.get('growth_tactics') or colmap.get('tactics')

    unknown = []
    required = []
    # Just warn if missing
    if not idea_col:
        required.append('idea')
    if not icp_col:
        required.append('icp')
    # Track headers
    headers = list(df.columns)

    results = {
        "rows_read": len(df),
        "rows_valid": 0,
        "rows_added": 0,
        "rows_skipped": 0,
        "rows_failed": 0,
        "errors_sample": [],
        "headers": headers,
        "unknown_columns": [],
        "missing_columns": required
    }

    existing_keys = set()
    if not dry_run:
        for k in db.query(SaaSIdea).all():
            key = compute_dedup_key(k.idea or "", k.icp or "")
            existing_keys.add(key)

    source_file = path.name
    for idx, row in df.iterrows():
        try:
            idea = str(row[idea_col]).strip() if idea_col and pd.notna(row[idea_col]) else ""
            if not idea or idea.lower() == 'idea':
                continue  # skip header-like rows
            icp = str(row[icp_col]).strip() if icp_col and pd.notna(row[icp_col]) else ""

            if not dry_run:
                dkey = compute_dedup_key(idea, icp)
                if dkey in existing_keys:
                    results["rows_skipped"] += 1
                    continue

            results["rows_valid"] += 1
            if dry_run:
                results["rows_added"] += 1  # would add
                continue

            tactics_val = row[tactics_col] if tactics_col and pd.notna(row[tactics_col]) else ""
            tactics = parse_growth_tactics(tactics_val)
            obj = SaaSIdea(
                idea=idea,
                monthly_revenue=clean_currency(row[rev_col]) if rev_col and pd.notna(row[rev_col]) else None,
                monthly_traffic=clean_bigint(row[traffic_col]) if traffic_col and pd.notna(row[traffic_col]) else None,
                revenue_per_visitor=clean_decimal(row[rpv_col]) if rpv_col and pd.notna(row[rpv_col]) else None,
                starting_costs=clean_currency(row[cost_col]) if cost_col and pd.notna(row[cost_col]) else None,
                solopreneur_score=clean_int(row[score_col]) if score_col and pd.notna(row[score_col]) else None,
                icp=icp,
                growth_tactics=json.dumps(tactics) if isinstance(tactics, list) else str(tactics),
                source_file=source_file,
            )
            db.add(obj)
            if not dry_run:
                existing_keys.add(dkey)
            results["rows_added"] += 1
        except Exception as e:
            results["rows_failed"] += 1
            if len(results["errors_sample"]) < 5:
                results["errors_sample"].append({"row": int(idx), "error": str(e)})
            continue

    if not dry_run:
        db.commit()
    return results
