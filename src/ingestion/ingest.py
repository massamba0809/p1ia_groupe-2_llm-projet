"""Module 2 - Corpus et ingestion (Abdou Karim).

Contrat : ingest() renvoie la liste des chunks du corpus.
Corpus : Code du travail du Sénégal (loi n° 97-17), un chunk par article.

Les chunks sont générés une fois par : python -m src.ingestion.build_chunks
(le fichier data/code_travail_chunks.json est déjà fourni dans le dépôt).
"""
import json
from pathlib import Path

from src.common.types import Chunk

CHUNKS_PATH = Path(__file__).resolve().parents[2] / "data" / "code_travail_chunks.json"


def ingest() -> list[Chunk]:
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        return [Chunk(**c) for c in json.load(f)]
