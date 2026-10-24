"""Fonctions appelables par le modèle (function calling)."""
import json
from datetime import date

import config
from ingestion.ingest import normalize_label

_chunks = None


def _load():
    global _chunks
    if _chunks is None:
        _chunks = json.loads((config.INDEX_DIR / "code_travail_chunks.json").read_text(encoding="utf-8"))
    return _chunks


def recherche_article(numero: str) -> str:
    """Recherche structurée : renvoie le texte exact d'un article (ex. 'L.42')."""
    target = normalize_label(numero)
    parts = [c for c in _load() if c["article"] == target]
    if not parts:
        return f"Article {numero} introuvable dans le corpus."
    return "\n".join(c["text"] for c in sorted(parts, key=lambda c: c["part"]))


def calcul_anciennete(date_debut: str, date_fin: str) -> str:
    """Ancienneté entre deux dates ISO (AAAA-MM-JJ) : années, mois, jours."""
    try:
        d1, d2 = date.fromisoformat(date_debut), date.fromisoformat(date_fin)
    except ValueError:
        return "Format de date invalide, utiliser AAAA-MM-JJ."
    if d2 < d1:
        return "La date de fin précède la date de début."
    y, m, d = d2.year - d1.year, d2.month - d1.month, d2.day - d1.day
    if d < 0:
        m -= 1
        d += 30
    if m < 0:
        y -= 1
        m += 12
    return f"{y} an(s), {m} mois, {d} jour(s) ({(d2 - d1).days} jours au total)."


REGISTRE = {"get_article": recherche_article, "calcul_anciennete": calcul_anciennete}

SCHEMAS = [
    {"type": "function", "function": {
        "name": "get_article",
        "description": "Récupère le texte exact d'un article du Code du travail à partir de son numéro (ex: 'L.42').",
        "parameters": {"type": "object", "properties": {"numero": {"type": "string"}}, "required": ["numero"]}}},
    {"type": "function", "function": {
        "name": "calcul_anciennete",
        "description": "Calcule l'ancienneté d'un travailleur entre deux dates (format AAAA-MM-JJ).",
        "parameters": {"type": "object", "properties": {
            "date_debut": {"type": "string"}, "date_fin": {"type": "string"}},
            "required": ["date_debut", "date_fin"]}}},
]


def run(name: str, args: dict) -> str:
    fn = REGISTRE.get(name)
    if fn is None:
        return f"Outil inconnu : {name}"
    try:
        return fn(**args)
    except Exception as e:  
        return f"Erreur outil : {e}"
