"""Écrit un rapport Markdown de l'ingestion (chiffres + contrôles), réutilisable dans le rapport final."""
from pathlib import Path

from src.ingestion.config import DATA_DIR, LAW, MAX_CHARS

REPORT_PATH = DATA_DIR / "ingestion_report.md"


def render_report(stats: dict, checks: dict[str, list[str]], max_chars: int = MAX_CHARS) -> str:
    lines = [
        "# Rapport d'ingestion",
        "",
        "Généré par `python -m src.ingestion.build_chunks` : ne pas modifier à la main.",
        "",
        f"- Corpus : {LAW}",
        f"- Découpage : un chunk par article, coupé au-delà de {max_chars} caractères",
        "",
        "## Chiffres",
        "",
        "| Mesure | Valeur |",
        "|---|---|",
        f"| Articles | {stats['articles']} |",
        f"| Chunks | {stats['chunks']} |",
        f"| Articles coupés en plusieurs chunks | {stats['articles_coupes']} (max {stats['max_morceaux']} morceaux) |",
        f"| Taille min / médiane / moyenne / max (car.) | {stats['taille_min']} / {stats['taille_mediane']} / "
        f"{stats['taille_moyenne']} / {stats['taille_max']} |",
        f"| Mots au total | {stats['mots_total']} |",
        "",
        "## Chunks par titre",
        "",
        "| Titre | Chunks |",
        "|---|---|",
    ]
    lines += [f"| {titre} | {n} |" for titre, n in stats["chunks_par_titre"].items()]
    lines += ["", "## Contrôles qualité", ""]
    for name, issues in checks.items():
        lines.append(f"- **{name}** : {'OK' if not issues else f'{len(issues)} signalement(s)'}")
        lines += [f"  - {issue}" for issue in issues]
    return "\n".join(lines) + "\n"


def write_report(stats: dict, checks: dict[str, list[str]], max_chars: int = MAX_CHARS,
                 path: Path = REPORT_PATH) -> Path:
    path.write_text(render_report(stats, checks, max_chars), encoding="utf-8")
    return path
