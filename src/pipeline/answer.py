"""Module 1 - Pipeline de génération (tech lead).

Contrat : answer(question) -> {"reponse": str, "passages": list[dict]}
Pour l'instant : BOUCHON qui ne contacte aucun LLM.
"""
from src.retrieval.retrieve import retrieve


def answer(question: str, k: int = 4) -> dict:
    passages = retrieve(question, k)
    # TODO (tech lead) : construire le prompt avec les passages, appeler le LLM,
    # exiger que la réponse cite les passages utilisés.
    return {
        "reponse": "[BOUCHON] Réponse non générée : le LLM n'est pas encore branché.",
        "passages": [p.to_dict() for p in passages],
    }
