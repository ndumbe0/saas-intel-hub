#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import yaml

backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

def main():
    parser = argparse.ArgumentParser(description="Fetch and ingest sources from sources.yaml")
    parser.add_argument("--sources", default=str(Path(__file__).parent.parent / "sources.yaml"))
    args = parser.parse_args()
    pass

if __name__ == "__main__":
    main()
