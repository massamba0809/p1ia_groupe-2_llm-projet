"""Repère les articles et leur contexte (Titre / Chapitre / Section) dans les lignes du PDF.

Chaque article est un dict : {"num": "L.49", "modif": "Loi 2015-04 ...", "ctx": {...}, "paras": [...]}.
"modif" contient la loi modificative indiquée dans l'en-tête de l'article (vide sinon).
"""
import re

from src.ingestion.clean import join_lines

# tolère une mention de modification après le numéro : "Article L.49. (Loi 2015-04 du 12 Février 2015)"
# et l'absence de point après "L" : "Article L 76 bis (Loi 2015 -04 du 12 Février 2015)"
RE_ARTICLE = re.compile(r"^Article\s+(L\.?\s?\d+(?:\s?(?:bis|ter))?)\.?\s*(?:\((.*)\))?\s*$", re.I)
RE_NUM = re.compile(r"L\.?\s*(\d+)\s*(bis|ter)?", re.I)
RE_STRUCT = re.compile(r"^(TITRE|CHAPITRE|SECTION|PARAGRAPHE)\b", re.I)
RE_FOOTER = re.compile(r"^page\s+\d+\s*/\s*\d+$", re.I)


def normalize_num(raw: str) -> str:
    """'L 76 bis' -> 'L.76bis', 'L. 9' -> 'L.9'."""
    m = RE_NUM.match(raw)
    return f"L.{m.group(1)}{(m.group(2) or '').lower()}"


def normalize_modif(raw: str | None) -> str:
    """' Loi 2015 -04 du 12 Février 2015' -> 'Loi 2015-04 du 12 Février 2015'."""
    if not raw:
        return ""
    return re.sub(r"(\d)\s*-\s*(\d)", r"\1-\2", " ".join(raw.split()))


def parse(lines: list[str]) -> list[dict]:
    articles, ctx = [], {"TITRE": "", "CHAPITRE": "", "SECTION": ""}
    current = None
    struct_buffer = None  # titre/chapitre sur plusieurs lignes

    def flush():
        nonlocal current
        if current and current["paras"]:
            articles.append(current)
        current = None

    for ln in lines:
        if not ln or RE_FOOTER.match(ln):
            if current is not None:
                current["paras"].append("")  # séparateur de paragraphe
            continue
        m = RE_ARTICLE.match(ln)
        if m:
            flush()
            struct_buffer = None
            current = {
                "num": normalize_num(m.group(1)),
                "modif": normalize_modif(m.group(2)),
                "ctx": dict(ctx),
                "paras": [""],
            }
            continue
        s = RE_STRUCT.match(ln)
        if s and ln.upper() == ln:  # les intitulés de structure sont en majuscules
            flush()
            kind = s.group(1).upper()
            if kind == "TITRE":
                ctx.update({"TITRE": ln, "CHAPITRE": "", "SECTION": ""})
            elif kind == "CHAPITRE":
                ctx.update({"CHAPITRE": ln, "SECTION": ""})
            else:
                ctx["SECTION"] = ln
            struct_buffer = kind
            continue
        if struct_buffer and current is None and ln.upper() == ln:
            ctx[struct_buffer] += " " + ln  # suite d'un intitulé sur 2 lignes
            continue
        struct_buffer = None
        if current is not None:
            if current["paras"][-1] == "":
                current["paras"][-1] = ln
            else:
                current["paras"][-1] = join_lines(current["paras"][-1], ln)
    flush()
    return articles
