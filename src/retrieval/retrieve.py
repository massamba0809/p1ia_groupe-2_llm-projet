"""Module 3 - Embeddings et base vectorielle (Haroona).

Contrat : retrieve(question, k) renvoie les k passages les plus pertinents.

Fonctionnement :
- chaque chunk est transformé en vecteur par un modèle d'embedding multilingue ;
- les vecteurs sont stockés dans une base ChromaDB sur disque (dossier chroma_db/) ;
- la question est transformée en vecteur, puis on cherche les chunks les plus proches
  (similarité cosinus).
L'index est construit au premier appel (une à deux minutes), puis réutilisé.

Test rapide : python -m src.retrieval.retrieve "Combien dure le congé de maternité ?"
"""
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from src.common.types import Passage
from src.ingestion.ingest import ingest

DB_PATH = Path(__file__).resolve().parents[2] / "chroma_db"

# Les deux modèles comparés (voir compare.py). Les modèles e5 attendent un préfixe
# "query: " devant la question et "passage: " devant les documents.
MODELS = {
    "minilm": {
        "name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "query_prefix": "",
        "passage_prefix": "",
    },
    "e5": {
        "name": "intfloat/multilingual-e5-small",
        "query_prefix": "query: ",
        "passage_prefix": "passage: ",
    },
}
DEFAULT_MODEL = "minilm"

_models = {}       # modèles déjà chargés en mémoire
_collections = {}  # collections ChromaDB déjà ouvertes


def get_model(key: str) -> SentenceTransformer:
    if key not in _models:
        _models[key] = SentenceTransformer(MODELS[key]["name"])
    return _models[key]


def get_collection(key: str = DEFAULT_MODEL):
    """Ouvre la collection du modèle `key`, et l'indexe si elle est vide ou incomplète."""
    if key in _collections:
        return _collections[key]

    client = chromadb.PersistentClient(path=str(DB_PATH))
    collection = client.get_or_create_collection(
        name=f"code_travail_{key}", metadata={"hnsw:space": "cosine"}
    )
    chunks = ingest()
    if collection.count() != len(chunks):
        build_index(collection, chunks, key)

    _collections[key] = collection
    return collection


def build_index(collection, chunks, key: str) -> None:
    print(f"Indexation de {len(chunks)} chunks avec {MODELS[key]['name']}...", file=sys.stderr)
    if collection.count():
        collection.delete(ids=collection.get()["ids"])  # repartir d'un index propre

    prefix = MODELS[key]["passage_prefix"]
    embeddings = get_model(key).encode(
        [prefix + c.text for c in chunks], normalize_embeddings=True, show_progress_bar=True
    )
    collection.add(
        ids=[c.id for c in chunks],
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source} for c in chunks],
        embeddings=embeddings.tolist(),
    )


def retrieve(question: str, k: int = 4, model: str = DEFAULT_MODEL) -> list[Passage]:
    collection = get_collection(model)
    query = MODELS[model]["query_prefix"] + question
    embedding = get_model(model).encode(query, normalize_embeddings=True)

    res = collection.query(query_embeddings=[embedding.tolist()], n_results=k)
    return [
        # Chroma renvoie une distance cosinus : score = 1 - distance (1 = identique)
        Passage(chunk_id=cid, text=text, source=meta["source"], score=round(1 - dist, 4))
        for cid, text, meta, dist in zip(
            res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Combien de temps dure le congé de maternité ?"
    for p in retrieve(question):
        print(f"{p.score:.3f}  {p.chunk_id:8}  {p.text.splitlines()[-1][:100]}")
