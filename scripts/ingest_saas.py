#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.database import SessionLocal, engine
from app.models.saas import SaaSIdea
from app.utils.ingest import ingest_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    db = SessionLocal()
    try:
        res = ingest_file(db, args.file, dry_run=args.dry_run)
        print(res)
    finally:
        db.close()

if __name__ == '__main__':
    main()
