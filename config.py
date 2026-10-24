"""Configuration centrale du projet."""
from pathlib import Path

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
INDEX_DIR = ROOT / "index"
EVAL_DIR = ROOT / "eval"
LOG_FILE = ROOT / "logs" / "traces.jsonl"

CORPUS_PDF = DATA_DIR / "code_du_travail_senegal.pdf"

# Embeddings multilingues (bon en français, gère 512 tokens, tourne sur CPU)
EMBED_MODEL = "intfloat/multilingual-e5-small"

CHUNK_MAX_CHARS = 1500     # au-delà, un article est coupé en morceaux
CHUNK_OVERLAP = 200
TOP_K = 4

# Seuil de similarité cosinus sous lequel on considère la question hors sujet.
# À CALIBRER : lancer `python evaluate.py` et regarder les scores des questions
# hors sujet vs. dans le sujet (colonne top_score de eval/results.csv).
MIN_SCORE = 0.78
