"""Project paths shared across backend modules."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
MODELS_DIR = DATA_DIR / "models"
SAMPLES_DIR = ROOT / "samples"
DB_PATH = DATA_DIR / "cases.db"
GEO_CACHE_PATH = DATA_DIR / "geo_cache.json"
MODEL_PATH = MODELS_DIR / "phishing_tfidf.joblib"
TRAINING_CSV = DATA_DIR / "training_emails.csv"
