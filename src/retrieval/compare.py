"""Comparaison de deux réglages du retrieval : deux modèles d'embedding.

Usage : python -m src.retrieval.compare

Pour chaque question de eval/sample_questions.json qui a un article attendu, on regarde
à quel rang cet article ressort dans les résultats de retrieve().
Métriques :
- hit@1 : part des questions où le bon article est en 1re position ;
- hit@k : part des questions où le bon article est dans les k premiers ;
- MRR   : moyenne de 1/rang (1 = toujours premier, 0 = jamais trouvé).
"""
import json
import time
from pathlib import Path

from src.retrieval.retrieve import MODELS, get_collection, retrieve

QUESTIONS_PATH = Path(__file__).resolve().parents[2] / "eval" / "sample_questions.json"
K = 4


def rank_of(expected: str, passages) -> int:
    """Rang (1, 2, ...) du bon article, ou 0 s'il n'est pas retrouvé.
    Un article long est découpé en L.xx-1, L.xx-2... : chaque morceau compte."""
    for i, p in enumerate(passages, 1):
        if p.chunk_id == expected or p.chunk_id.startswith(expected + "-"):
            return i
    return 0


def evaluate(model: str, questions: list[dict]) -> dict:
    start = time.time()
    get_collection(model)  # charge le modèle (et indexe si besoin)
    load_time = time.time() - start

    ranks = []
    for q in questions:
        r = rank_of(q["chunk_attendu"], retrieve(q["question"], K, model=model))
        ranks.append(r)
        print(f"  [{model}] {q['id']} attendu {q['chunk_attendu']:6} -> rang {r or 'non trouvé'}")

    n = len(ranks)
    return {
        "modele": MODELS[model]["name"],
        "hit@1": sum(r == 1 for r in ranks) / n,
        f"hit@{K}": sum(r > 0 for r in ranks) / n,
        "MRR": sum(1 / r for r in ranks if r) / n,
        "chargement_s": load_time,
    }


def main() -> None:
    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        questions = [q for q in json.load(f) if q.get("chunk_attendu")]
    print(f"{len(questions)} questions avec article attendu, k = {K}\n")

    results = [evaluate(m, questions) for m in MODELS]

    print(f"\n| Modèle | hit@1 | hit@{K} | MRR | Chargement (s) |")
    print("|---|---|---|---|---|")
    for r in results:
        print(f"| {r['modele']} | {r['hit@1']:.2f} | {r[f'hit@{K}']:.2f} | {r['MRR']:.2f} | {r['chargement_s']:.1f} |")


if __name__ == "__main__":
    main()
