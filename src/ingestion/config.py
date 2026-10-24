"""Configuration du module d'ingestion : chemins, nom du corpus, taille des chunks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
PDF_PATH = DATA_DIR / "code_travail_senegal.pdf"
OUT_PATH = DATA_DIR / "code_travail_chunks.json"

LAW = "Code du travail du Sénégal (loi n° 97-17)"
MAX_CHARS = 1200
