"""Compare deux stratégies de découpage du Code du travail.

Usage : python -m src.ingestion.compare_chunking [--size 800] [--overlap 150]

A : un chunk par article (stratégie retenue, voir chunker.py)
B : fenêtres de taille fixe avec chevauchement, sans tenir compte des articles

On mesure ce qui compte pour citer un passage : un chunk mélange-t-il plusieurs articles ?
un article est-il éparpillé dans plusieurs chunks ? (pas besoin d'embeddings pour cela)
"""
import argparse
import re
import statistics

from src.ingestion.chunker import to_chunks
from src.ingestion.clean import clean_lines, clean_paragraph
from src.ingestion.extract import read_lines
from src.ingestion.parser import parse


def fixed_size_chunks(articles: list[dict], size: int, overlap: int) -> list[dict]:
    """Texte continu découpé tous les (size - overlap) caractères, coupé sur un espace."""
    text, spans = "", []  # spans : (début, fin, numéro d'article) dans le texte continu
    for art in articles:
        body = f"Article {art['num']} " + " ".join(clean_paragraph(p) for p in art["paras"] if p)
        spans.append((len(text), len(text) + len(body), art["num"]))
        text += body + " "
    chunks, start = [], 0
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            end = text.rfind(" ", start, end) if " " in text[start:end] else end
        arts = [n for s, e, n in spans if s < end and e > start]
        chunks.append({"id": f"F.{len(chunks) + 1:04d}", "text": text[start:end].strip(), "articles": arts})
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def describe(name: str, chunks: list[dict], articles_of) -> dict:
    sizes = [len(c["text"]) for c in chunks]
    per_article: dict[str, int] = {}
    for c in chunks:
        for a in articles_of(c):
            per_article[a] = per_article.get(a, 0) + 1
    return {
        "stratégie": name,
        "chunks": len(chunks),
        "taille médiane": int(statistics.median(sizes)),
        "chunks multi-articles": f"{sum(len(articles_of(c)) > 1 for c in chunks) / len(chunks):.0%}",
        "articles éparpillés": f"{sum(n > 1 for n in per_article.values()) / len(per_article):.0%}",
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--size", type=int, default=800)
    ap.add_argument("--overlap", type=int, default=150)
    args = ap.parse_args()

    articles = parse(clean_lines(read_lines()))
    a = to_chunks(articles)
    b = fixed_size_chunks(articles, args.size, args.overlap)
    rows = [
        describe("A : un chunk par article", a, lambda c: [re.sub(r"-\d+$", "", c["id"])]),
        describe(f"B : taille fixe {args.size} / chevauchement {args.overlap}", b, lambda c: c["articles"]),
    ]
    cols = list(rows[0])
    print("| " + " | ".join(cols) + " |")
    print("|" + "---|" * len(cols))
    for r in rows:
        print("| " + " | ".join(str(r[c]) for c in cols) + " |")


if __name__ == "__main__":
    main()
