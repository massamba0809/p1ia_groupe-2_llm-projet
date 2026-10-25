"""Contrôles qualité sur les chunks produits.

Chaque contrôle renvoie une liste de problèmes (chaînes lisibles), vide si tout va bien.
Usage : run_checks(chunks) -> {"nom du contrôle": [problèmes...]}
"""
import re

from src.ingestion.config import MAX_CHARS

MIN_BODY_CHARS = 80  # en dessous, l'article tient en une phrase : peu de contexte pour la recherche

RE_ID = re.compile(r"^L\.(\d+)(bis|ter)?(?:-(\d+))?$")


def article_of(chunk_id: str) -> str:
    """'L.115-2' -> 'L.115'."""
    return re.sub(r"-\d+$", "", chunk_id)


def check_numbering(chunks: list[dict]) -> list[str]:
    """Les articles L.1 ... L.n doivent tous être présents, sans trou."""
    nums = set()
    issues = []
    for c in chunks:
        m = RE_ID.match(c["id"])
        if not m:
            issues.append(f"id inattendu : {c['id']}")
            continue
        nums.add(int(m.group(1)))
    if nums:
        missing = [n for n in range(1, max(nums) + 1) if n not in nums]
        issues += [f"article manquant : L.{n}" for n in missing]
    return issues


def check_duplicates(chunks: list[dict]) -> list[str]:
    """Deux chunks ne doivent jamais avoir le même id (la base vectorielle l'exige)."""
    seen, issues = set(), []
    for c in chunks:
        if c["id"] in seen:
            issues.append(f"id en double : {c['id']}")
        seen.add(c["id"])
    return issues


def body_of(chunk: dict) -> str:
    """Texte du chunk sans les 2 lignes d'en-tête ([contexte] et 'Article L.x')."""
    return chunk["text"].split("\n", 2)[-1]


def check_sizes(chunks: list[dict], min_chars: int = MIN_BODY_CHARS,
                max_chars: int = MAX_CHARS) -> list[str]:
    """Signale les chunks très courts et ceux qui dépassent max_chars (phrase trop longue pour être coupée)."""
    issues = []
    for c in chunks:
        n = len(body_of(c))
        if n < min_chars:
            issues.append(f"chunk court ({n} car.) : {c['id']}")
        elif n > max_chars:
            issues.append(f"chunk long ({n} car. > {max_chars}) : {c['id']}")
    return issues


RESIDUES = {
    "pied de page": re.compile(r"\bpage\s+\d+\s*/\s*\d+", re.I),
    "caractère illisible": re.compile("�"),
    "en-tête d'article dans le corps": re.compile(r"^Article\s+L", re.M),
    "crédits de l'éditeur": re.compile(r"JURISCONSULT", re.I),
    "espace double": re.compile(r"  "),
}


def check_residues(chunks: list[dict]) -> list[str]:
    """Repère ce que l'extraction PDF a pu laisser dans le texte."""
    issues = []
    for c in chunks:
        for label, pattern in RESIDUES.items():
            if pattern.search(body_of(c)):
                issues.append(f"{label} : {c['id']}")
    return issues


CHECKS = {
    "numérotation": check_numbering,
    "doublons": check_duplicates,
    "tailles": check_sizes,
    "résidus d'extraction": check_residues,
}


def run_checks(chunks: list[dict], max_chars: int = MAX_CHARS) -> dict[str, list[str]]:
    results = {name: check(chunks) for name, check in CHECKS.items()}
    results["tailles"] = check_sizes(chunks, max_chars=max_chars)
    return results
