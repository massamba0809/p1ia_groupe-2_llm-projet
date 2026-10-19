"""Module 3 - Embeddings et base vectorielle (Haroona).

Contrat : retrieve(question, k) renvoie les k passages les plus pertinents.
Pour l'instant : BOUCHON qui renvoie les k premiers chunks d'exemple.
"""
from src.common.types import Passage
from src.ingestion.ingest import ingest


def retrieve(question: str, k: int = 4) -> list[Passage]:
    # TODO (Haroona) : embeddings + base vectorielle (Chroma/FAISS), recherche par similarité
    chunks = ingest()[:k]
    return [Passage(chunk_id=c.id, text=c.text, source=c.source, score=0.0) for c in chunks]
