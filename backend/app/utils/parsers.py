import re
import json
from decimal import Decimal
from typing import Any, Optional

def normalize_text(s: Any) -> str:
    if s is None:
        return ""
    if isinstance(s, str):
        return re.sub(r'\s+', ' ', s.strip().lower())
    return str(s).strip().lower()

def clean_currency(val: Any) -> Optional[Decimal]:
    if val is None or val == "":
        return None
    if isinstance(val, bool):
        return Decimal(str(val))
    if isinstance(val, Decimal):
        return val
    if isinstance(val, (int, float)):
        return Decimal(str(val))
    s = str(val).strip()
    if not s or s in ("—", "-", "NA", "N/A", "n/a", "NULL", "null"):
        return None
    s = re.sub(r'[\$£€¥,]', '', s)
    m = re.search(r'([\d.]+)\s*(k|m|K|M)\b', s)
    if m:
        num = float(m.group(1))
        suffix = m.group(2).lower()
        if suffix == 'k':
            num *= 1000
        elif suffix == 'm':
            num *= 1000000
        try:
            return Decimal(str(int(round(num))) if num.is_integer() else str(num))
        except:
            return Decimal(str(num))
    m2 = re.search(r'[-\d.]+', s)
    if m2:
        try:
            return Decimal(m2.group(0))
        except:
            return None
    return None

def clean_int(val: Any) -> Optional[int]:
    if val is None or val == "":
        return None
    if isinstance(val, bool):
        return int(val)
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(round(val))
    s = str(val).strip()
    if not s or s in ("—", "-", "NA", "N/A", "n/a", "NULL", "null"):
        return None
    s = re.sub(r'[,]', '', s)
    m = re.search(r'([\d.]+)\s*(k|m|K|M)\b', s)
    if m:
        num = float(m.group(1))
        suffix = m.group(2).lower()
        if suffix == 'k':
            num *= 1000
        elif suffix == 'm':
            num *= 1000000
        return int(round(num))
    m2 = re.search(r'[-\d]+', s)
    if m2:
        try:
            return int(m2.group(0))
        except:
            return None
    return None

def clean_bigint(val: Any) -> Optional[int]:
    return clean_int(val)

def clean_float(val: Any) -> Optional[float]:
    if val is None or val == "":
        return None
    if isinstance(val, bool):
        return float(val)
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    if not s or s in ("—", "-", "NA", "N/A", "n/a", "NULL", "null"):
        return None
    s = re.sub(r'[\$£€¥,]', '', s)
    m = re.search(r'([\d.]+)\s*(k|m|K|M)\b', s)
    if m:
        num = float(m.group(1))
        suffix = m.group(2).lower()
        if suffix == 'k':
            num *= 1000
        elif suffix == 'm':
            num *= 1000000
        return num
    m2 = re.search(r'[-\d.]+', s)
    if m2:
        try:
            return float(m2.group(0))
        except:
            return None
    return None

def clean_decimal(val: Any) -> Optional[Decimal]:
    if val is None or val == "":
        return None
    if isinstance(val, bool):
        return Decimal(str(val))
    if isinstance(val, Decimal):
        return val
    if isinstance(val, (int, float)):
        return Decimal(str(val))
    s = str(val).strip()
    if not s or s in ("—", "-", "NA", "N/A", "n/a", "NULL", "null"):
        return None
    s = re.sub(r'[\$£€¥,]', '', s)
    m = re.search(r'([\d.]+)\s*(k|m|K|M)\b', s)
    if m:
        num = float(m.group(1))
        suffix = m.group(2).lower()
        if suffix == 'k':
            num *= 1000
        elif suffix == 'm':
            num *= 1000000
        return Decimal(str(int(round(num))) if num.is_integer() else str(num))
    m2 = re.search(r'[-\d.]+', s)
    if m2:
        try:
            return Decimal(m2.group(0))
        except:
            return None
    return None

def parse_growth_tactics(val: Any) -> Any:
    if val is None or val == "":
        return []
    if isinstance(val, list):
        return [str(x).strip() for x in val if str(x).strip()]
    s = str(val).strip()
    if not s or s in ("—", "-", "NA", "N/A", "n/a", "NULL", "null"):
        return []
    if s.startswith('['):
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed]
        except:
            pass
    parts = [p.strip() for p in s.split(',')]
    return [p for p in parts if p]
