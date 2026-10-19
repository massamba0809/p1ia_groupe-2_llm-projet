# Projet LLM & Écosystème : assistant RAG sur corpus public en français

Assistant qui répond à des questions sur un corpus de documents publics, avec indication des passages utilisés, puis mesure de la qualité de ses réponses.

> Corpus : **Code du travail du Sénégal** (loi n° 97-17, 288 articles), fichier `data/code_travail_senegal.pdf`.
> Découpage : un chunk par article (335 chunks), généré par `python -m src.ingestion.build_chunks` vers `data/code_travail_chunks.json`.
> Limite connue : version de 1997 ; un nouveau code du travail (projet de loi n°15/2026) est en cours d'application, le texte en vigueur a pu changer.

## Équipe et modules

| Membre | Module | Dossier | Branche |
|---|---|---|---|
| Massamba (tech lead) | Pipeline de génération, intégration | `src/pipeline/`, `main.py` | `feature/pipeline` |
| Abdou Karim | Corpus et ingestion | `data/`, `src/ingestion/` | `feature/ingestion` |
| Haroona | Embeddings et base vectorielle | `src/retrieval/` | `feature/retrieval` |
| Sine Ndoye | Évaluation | `eval/`, `reports/` | `feature/eval` |
| Mamadou | Function calling, garde-fous, observabilité | `src/tools/`, `src/guardrails/`, `src/observability/` | `feature/bonus` |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # puis renseigner la clé API
```

## Lancer

```bash
python main.py "Votre question ?"
```

(Pour l'instant, le projet tourne avec des bouchons : voir les `TODO` dans chaque module.)

## Interfaces communes (ne pas changer sans prévenir le tech lead)

```python
ingest() -> list[Chunk]                         # src/ingestion/ingest.py
retrieve(question, k) -> list[Passage]          # src/retrieval/retrieve.py
answer(question) -> {"reponse", "passages"}     # src/pipeline/answer.py
```

Les types `Chunk` et `Passage` sont dans `src/common/types.py`.

## Règles Git

- Une branche par membre, jamais de push direct sur `main`.
- Une Pull Request par module, relue par le tech lead avant fusion.
- Commits clairs et fréquents (`feat: ...`, `fix: ...`), faits avec son propre compte GitHub.

## Évaluation, limites, sources

À compléter dans `reports/rapport.md` (résultats, erreurs constatées, ce que nous changerions) et ci-dessous pour les sources.

## Sources et références

- République du Sénégal, Code du travail (loi n° 97-17), version PDF de la bibliothèque juridique Jurisconsult / Ministère de la Justice, téléchargée depuis https://www.vie-publique.sn/documents/437/code-travail-senegal (autre copie : https://webapps.ilo.org/dyn/travail/docs/839/Code%20du%20travail.pdf).
