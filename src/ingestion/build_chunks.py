"""Découpe le Code du travail du Sénégal (PDF) en chunks : un chunk par article.

Usage : python -m src.ingestion.build_chunks [--max-chars 1200] [--out chemin.json] [--check] [--no-report]
Entrée : data/code_travail_senegal.pdf
Sorties : data/code_travail_chunks.json  (liste de {id, text, source})
          data/ingestion_report.md      (chiffres et contrôles qualité)

Étapes : extract (PDF -> lignes) -> clean (nettoyage) -> parser (lignes -> articles)
-> chunker (articles -> chunks) -> checks (contrôles qualité).

Choix de découpage (à justifier dans le rapport) :
- un article de loi = une unité de sens, donc un chunk par article ;
- un article trop long (> MAX_CHARS) est coupé aux frontières de paragraphes ;
- chaque chunk commence par son contexte (Titre / Chapitre / Section) pour aider la recherche.
"""
import argparse
import json
import sys
from pathlib import Path

from src.ingestion.checks import run_checks
from src.ingestion.chunker import to_chunks
from src.ingestion.clean import clean_lines
from src.ingestion.config import MAX_CHARS, OUT_PATH
from src.ingestion.extract import read_lines
from src.ingestion.parser import parse
from src.ingestion.report import write_report
from src.ingestion.stats import compute_stats, format_stats

# contrôles qui font échouer --check ; les tailles ne sont que des avertissements
BLOCKING = {"numérotation", "doublons", "résidus d'extraction"}


def build(max_chars: int = MAX_CHARS) -> list[dict]:
    return to_chunks(parse(clean_lines(read_lines())), max_chars)


def print_checks(results: dict[str, list[str]]) -> int:
    """Affiche les contrôles et renvoie le nombre de problèmes bloquants."""
    blocking = 0
    for name, issues in results.items():
        status = "OK" if not issues else f"{len(issues)} problème(s)"
        print(f"[{name}] {status}")
        for issue in issues:
            print(f"  - {issue}")
        if name in BLOCKING:
            blocking += len(issues)
    return blocking


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Construit les chunks du Code du travail.")
    ap.add_argument("--max-chars", type=int, default=MAX_CHARS, help="taille max du corps d'un chunk")
    ap.add_argument("--out", type=Path, default=OUT_PATH, help="fichier JSON de sortie")
    ap.add_argument("--check", action="store_true", help="échoue si un contrôle bloquant trouve un problème")
    ap.add_argument("--no-report", action="store_true", help="ne pas réécrire data/ingestion_report.md")
    args = ap.parse_args(argv)

    chunks = build(args.max_chars)
    args.out.write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"-> {args.out.name}")
    stats = compute_stats(chunks)
    checks = run_checks(chunks, args.max_chars)
    print(format_stats(stats))
    blocking = print_checks(checks)
    if not args.no_report:
        print(f"-> {write_report(stats, checks, args.max_chars).name}")
    if args.check and blocking:
        sys.exit(1)


if __name__ == "__main__":
    main()
