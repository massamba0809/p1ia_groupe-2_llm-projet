"""Découpe le Code du travail du Sénégal (PDF) en chunks : un chunk par article.

Usage : python -m src.ingestion.build_chunks
Entrée : data/code_travail_senegal.pdf
Sortie : data/code_travail_chunks.json  (liste de {id, text, source})

Étapes : extract (PDF -> lignes) -> parser (lignes -> articles) -> chunker (articles -> chunks).

Choix de découpage (à justifier dans le rapport) :
- un article de loi = une unité de sens, donc un chunk par article ;
- un article trop long (> MAX_CHARS) est coupé aux frontières de paragraphes ;
- chaque chunk commence par son contexte (Titre / Chapitre / Section) pour aider la recherche.
"""
import json

from src.ingestion.chunker import to_chunks
from src.ingestion.config import MAX_CHARS, OUT_PATH
from src.ingestion.extract import read_lines
from src.ingestion.parser import parse


def build(max_chars: int = MAX_CHARS) -> list[dict]:
    return to_chunks(parse(read_lines()), max_chars)


def main() -> None:
    chunks = build()
    OUT_PATH.write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    sizes = sorted(len(c["text"]) for c in chunks)
    n_articles = len({c["source"] for c in chunks})
    print(f"{n_articles} articles -> {len(chunks)} chunks ({OUT_PATH.name})")
    print(f"taille min/médiane/max : {sizes[0]} / {sizes[len(sizes)//2]} / {sizes[-1]} caractères")


if __name__ == "__main__":
    main()
