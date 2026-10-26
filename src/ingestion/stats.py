"""Statistiques descriptives du découpage, pour le rapport et la démo."""
import statistics
from collections import Counter

from src.ingestion.checks import article_of


def compute_stats(chunks: list[dict]) -> dict:
    sizes = sorted(len(c["text"]) for c in chunks)
    per_article = Counter(article_of(c["id"]) for c in chunks)
    titres = Counter(c["text"].split("\n", 1)[0].strip("[]").split(" > ")[0] for c in chunks)
    return {
        "articles": len(per_article),
        "chunks": len(chunks),
        "articles_coupes": sum(1 for n in per_article.values() if n > 1),
        "max_morceaux": max(per_article.values()),
        "taille_min": sizes[0],
        "taille_mediane": int(statistics.median(sizes)),
        "taille_moyenne": round(statistics.mean(sizes)),
        "taille_max": sizes[-1],
        "mots_total": sum(len(c["text"].split()) for c in chunks),
        "chunks_par_titre": dict(titres),
    }


def format_stats(s: dict) -> str:
    return (
        f"{s['articles']} articles -> {s['chunks']} chunks "
        f"({s['articles_coupes']} articles coupés, jusqu'à {s['max_morceaux']} morceaux)\n"
        f"taille min/médiane/moyenne/max : {s['taille_min']} / {s['taille_mediane']} / "
        f"{s['taille_moyenne']} / {s['taille_max']} caractères ; {s['mots_total']} mots au total"
    )
