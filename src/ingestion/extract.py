"""Extraction du texte brut du PDF, ligne par ligne."""
from pathlib import Path

from pypdf import PdfReader

from src.ingestion.config import PDF_PATH


def read_lines(pdf_path: Path = PDF_PATH) -> list[str]:
    reader = PdfReader(str(pdf_path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return [ln.strip() for ln in text.splitlines()]
