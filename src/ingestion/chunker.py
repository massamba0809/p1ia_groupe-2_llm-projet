"""Transforme les articles en chunks {id, text, source}.

- un article = un chunk ;
- un article plus long que max_chars est coupé aux frontières de phrases (ids "L.115-1", "L.115-2"...) ;
- chaque chunk commence par son contexte [Titre > Chapitre > Section] puis "Article L.x".
"""
import re

from src.ingestion.clean import clean_paragraph
from src.ingestion.config import LAW, MAX_CHARS

RE_SENTENCE = re.compile(r"(?<=[.;:!?»])\s+(?=[A-ZÀ-Ý«\-])")


def to_chunks(articles: list[dict], max_chars: int = MAX_CHARS) -> list[dict]:
    chunks = []
    for art in articles:
        paras = []
        for p in art["paras"]:
            if p:  # coupe aussi aux phrases/puces, car l'extraction fusionne parfois les paragraphes
                paras.extend(RE_SENTENCE.split(clean_paragraph(p)))
        header = " > ".join(v for v in art["ctx"].values() if v)
        title = f"Article {art['num']}"
        if art.get("modif"):
            title += f" (rédaction issue de la {art['modif']})"
        source = f"{LAW}, Article {art['num']}"
        # regrouper les paragraphes sans dépasser max_chars
        parts, buf = [], ""
        for p in paras:
            if buf and len(buf) + len(p) + 1 > max_chars:
                parts.append(buf)
                buf = p
            else:
                buf = f"{buf} {p}".strip()
        if buf:
            parts.append(buf)
        for i, body in enumerate(parts, 1):
            cid = f"{art['num']}" if len(parts) == 1 else f"{art['num']}-{i}"
            text = f"[{header}]\n{title}\n{body}"
            chunks.append({"id": cid, "text": text, "source": source})
    return chunks
