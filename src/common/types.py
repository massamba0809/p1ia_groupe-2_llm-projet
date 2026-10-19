"""Types partagés entre les modules. NE PAS modifier sans prévenir le tech lead."""
from dataclasses import dataclass, asdict


@dataclass
class Chunk:
    id: str
    text: str
    source: str  # nom du document d'origine (à citer dans le rapport)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Passage:
    chunk_id: str
    text: str
    source: str
    score: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)
