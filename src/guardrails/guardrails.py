"""Garde-fous : injection de prompt, données personnelles, hors sujet."""
import re

INJECTION_PATTERNS = [
    r"ignore[rz]?\s+(toutes?\s+)?(les\s+|tes\s+|vos\s+)?(instructions|consignes|r[èe]gles)",
    r"oublie[rz]?\s+(toutes?\s+)?(les\s+|tes\s+)?(instructions|consignes)",
    r"ignore\s+(all\s+|the\s+)?(previous|above)\s+instructions",
    r"(prompt|message)\s+syst[èe]me|system\s+prompt",
    r"tu\s+es\s+maintenant|you\s+are\s+now|fais\s+semblant\s+d['e]",
    r"jailbreak|DAN\s+mode",
]
PII_PATTERNS = {
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "telephone": r"(?:(?:\+|00)?221[\s\.-]?)?\b(?:7[05-8]|3[03])[\s\.-]?\d{3}[\s\.-]?\d{2}[\s\.-]?\d{2}\b",
    "numero_long": r"\b\d{13,}\b",   # CNI / NINEA / carte bancaire
}

REFUSAL_INJECTION = ("Je ne peux pas traiter cette demande : elle tente de modifier mes instructions. "
                     "Je réponds uniquement aux questions sur le Code du travail sénégalais.")
REFUSAL_OFFTOPIC = ("Cette question semble hors du périmètre du Code du travail sénégalais, "
                    "ou je n'ai pas trouvé de passage pertinent. Pouvez-vous la reformuler ?")


def check_input(question: str):
    """Retourne (question_nettoyée, flags)."""
    flags = {"injection": False, "pii": []}
    low = question.lower()
    if any(re.search(p, low) for p in INJECTION_PATTERNS):
        flags["injection"] = True
    clean = question
    for name, pat in PII_PATTERNS.items():
        if re.search(pat, clean):
            flags["pii"].append(name)
            clean = re.sub(pat, f"[{name.upper()}_MASQUÉ]", clean)
    return clean, flags
