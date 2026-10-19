"""Découpe le Code du travail du Sénégal (PDF) en chunks : un chunk par article.

Usage : python -m src.ingestion.build_chunks
Entrée : data/code_travail_senegal.pdf
Sortie : data/code_travail_chunks.json  (liste de {id, text, source})

Choix de découpage (à justifier dans le rapport) :
- un article de loi = une unité de sens, donc un chunk par article ;
- un article trop long (> MAX_CHARS) est coupé aux frontières de paragraphes ;
- chaque chunk commence par son contexte (Titre / Chapitre / Section) pour aider la recherche.
"""
import json
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = ROOT / "data" / "code_travail_senegal.pdf"
OUT_PATH = ROOT / "data" / "code_travail_chunks.json"

LAW = "Code du travail du Sénégal (loi n° 97-17)"
MAX_CHARS = 1200

# tolère une mention de modification après le numéro : "Article L.49. (Loi 2015-04 du 12 Février 2015)"
RE_ARTICLE = re.compile(r"^Article\s+(L\.\s?\d+(?:\s?(?:bis|ter))?)\.?\s*(?:\(.*\))?\s*$", re.I)
RE_SENTENCE = re.compile(r"(?<=[.;:!?»])\s+(?=[A-ZÀ-Ý«\-])")
RE_STRUCT = re.compile(r"^(TITRE|CHAPITRE|SECTION|PARAGRAPHE)\b", re.I)
RE_FOOTER = re.compile(r"^page\s+\d+\s*/\s*\d+$", re.I)


def read_lines() -> list[str]:
    reader = PdfReader(str(PDF_PATH))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return [ln.strip() for ln in text.splitlines()]


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
            current = {"num": re.sub(r"\s+", "", m.group(1)), "ctx": dict(ctx), "paras": [""]}
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
                current["paras"][-1] += " " + ln
    flush()
    return articles


def to_chunks(articles: list[dict]) -> list[dict]:
    chunks = []
    for art in articles:
        paras = []
        for p in art["paras"]:
            if p:  # coupe aussi aux phrases/puces, car l'extraction fusionne parfois les paragraphes
                paras.extend(RE_SENTENCE.split(p))
        header = " > ".join(v for v in art["ctx"].values() if v)
        source = f"{LAW}, Article {art['num']}"
        # regrouper les paragraphes sans dépasser MAX_CHARS
        parts, buf = [], ""
        for p in paras:
            if buf and len(buf) + len(p) + 1 > MAX_CHARS:
                parts.append(buf)
                buf = p
            else:
                buf = f"{buf} {p}".strip()
        if buf:
            parts.append(buf)
        for i, body in enumerate(parts, 1):
            cid = f"{art['num']}" if len(parts) == 1 else f"{art['num']}-{i}"
            text = f"[{header}]\nArticle {art['num']}\n{body}"
            chunks.append({"id": cid, "text": text, "source": source})
    return chunks


def main() -> None:
    articles = parse(read_lines())
    chunks = to_chunks(articles)
    OUT_PATH.write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    sizes = sorted(len(c["text"]) for c in chunks)
    print(f"{len(articles)} articles -> {len(chunks)} chunks ({OUT_PATH.name})")
    print(f"taille min/médiane/max : {sizes[0]} / {sizes[len(sizes)//2]} / {sizes[-1]} caractères")


if __name__ == "__main__":
    main()
