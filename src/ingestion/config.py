"""Configuration du module d'ingestion : chemins, nom du corpus, taille des chunks."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
PDF_PATH = DATA_DIR / "code_travail_senegal.pdf"
OUT_PATH = DATA_DIR / "code_travail_chunks.json"

LAW = "Code du travail du Sénégal (loi n° 97-17)"
MAX_CHARS = 1200

# référence complète du document, à citer (voir aussi data/SOURCES.md)
SOURCE_DOC = {
    "titre": "Code du travail, loi n° 97-17 du 1er décembre 1997 (République du Sénégal)",
    "editeur": "Bibliothèque juridique numérique JURISCONSULT / Ministère de la Justice",
    "url": "https://www.vie-publique.sn/documents/437/code-travail-senegal",
    "url_miroir": "https://webapps.ilo.org/dyn/travail/docs/839/Code%20du%20travail.pdf",
    "fichier": "data/code_travail_senegal.pdf",
}
