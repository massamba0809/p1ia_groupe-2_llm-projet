"""Module 2 - Corpus et ingestion (Abdou Karim).

Contrat : ingest() renvoie la liste des chunks du corpus.
Corpus : Code du travail du Sénégal (loi n° 97-17), un chunk par article.

Les chunks sont générés une fois par : python -m src.ingestion.build_chunks
(le fichier data/code_travail_chunks.json est déjà fourni dans le dépôt).
"""
import json

from src.common.types import Chunk
from src.ingestion.checks import article_of
from src.ingestion.config import OUT_PATH as CHUNKS_PATH, SOURCE_DOC


def ingest() -> list[Chunk]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"{CHUNKS_PATH} introuvable : lancer d'abord `python -m src.ingestion.build_chunks`."
        )
    with open(CHUNKS_PATH, encoding="utf-8") as f:
        return [Chunk(**c) for c in json.load(f)]


def chunks_by_id() -> dict[str, Chunk]:
    return {c.id: c for c in ingest()}


def get_article(num: str) -> list[Chunk]:
    """Tous les chunks d'un article, dans l'ordre : get_article("L.115") -> [L.115-1, L.115-2, ...]."""
    return [c for c in ingest() if article_of(c.id) == num]


def list_sources(chunks: list[Chunk] | None = None) -> list[str]:
    """Liste des sources citables (une par article), dans l'ordre du code.

    Avec une liste de chunks (ex. les passages d'une réponse), ne renvoie que leurs sources.
    """
    chunks = ingest() if chunks is None else chunks
    return list(dict.fromkeys(c.source for c in chunks))


def document_reference() -> str:
    d = SOURCE_DOC
    return f"{d['titre']}, {d['editeur']}. {d['url']} (copie : {d['url_miroir']})"
