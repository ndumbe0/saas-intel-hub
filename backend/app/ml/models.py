import pickle
from pathlib import Path
from typing import Any

MODELS_DIR = Path(__file__).parent.parent.parent / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

def save_model(model: Any, name: str):
    path = MODELS_DIR / f"{name}.pkl"
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    return str(path)
