"""Nettoyage du texte extrait du PDF, appliqué ligne par ligne avant le parsing."""
import re
import unicodedata

RE_SPACES = re.compile(r"\s{2,}")
RE_SPACE_BEFORE_PUNCT = re.compile(r"\s+([,.])")  # on garde l'espace français avant ; : ! ?
RE_HYPHEN_EOL = re.compile(r"[A-Za-zÀ-ÿ]-$")
RE_ARTICLE_REF = re.compile(r"\bL\s?\.?\s?«?(\d+)»?")  # "L 2", "L. 9", "L7", "L .273", "L. «90»"

# caractères que l'extraction PDF peut produire, remplacés par leur forme simple
REPLACEMENTS = {
    "\xa0": " ",   # espace insécable
    " ": " ",  # espace fine insécable
    "’": "'",  # apostrophe typographique
    "‘": "'",
    "ﬁ": "fi",  # ligatures
    "ﬂ": "fl",
}


def normalize_unicode(line: str) -> str:
    line = unicodedata.normalize("NFC", line)
    for bad, good in REPLACEMENTS.items():
        line = line.replace(bad, good)
    return line


def fix_spacing(line: str) -> str:
    """'L 2  est' -> 'L 2 est' ; 'L.9 , L.24' -> 'L.9, L.24'."""
    line = RE_SPACES.sub(" ", line)
    return RE_SPACE_BEFORE_PUNCT.sub(r"\1", line)


def normalize_article_refs(line: str) -> str:
    """Écrit tous les renvois comme les ids des chunks : 'article L 2' -> 'article L.2'."""
    return RE_ARTICLE_REF.sub(r"L.\1", line)


def clean_line(line: str) -> str:
    line = fix_spacing(normalize_unicode(line))
    return fix_spacing(normalize_article_refs(line)).strip()


def clean_lines(lines: list[str]) -> list[str]:
    return [clean_line(ln) for ln in lines]


def clean_paragraph(text: str) -> str:
    """Repasse sur un paragraphe recollé : un renvoi peut être coupé entre deux lignes ('L' / '111')."""
    return fix_spacing(normalize_article_refs(text)).strip()


def join_lines(prev: str, line: str) -> str:
    """Recolle deux lignes d'un même paragraphe.

    Un mot composé coupé en fin de ligne ('ci-' / 'dessus') est recollé sans espace.
    Dans ce corpus, ces coupures sont des traits d'union de mots composés, on garde donc le tiret.
    """
    if RE_HYPHEN_EOL.search(prev):
        return prev + line
    return f"{prev} {line}"
