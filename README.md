# Projet LLM & Écosystème : assistant RAG sur le Code du travail du Sénégal

Assistant qui répond à des questions sur le Code du travail du Sénégal (loi n° 97-17) en citant les articles utilisés, puis mesure la qualité de ses réponses.

- **Corpus** : 289 articles (L.1 à L.288 + L.76bis), `data/code_travail_senegal.pdf`. Sources : `data/SOURCES.md`.
- **Découpage** : un chunk par article (336 chunks, les articles de plus de 1200 caractères sont scindés), dans `data/code_travail_chunks.json`.
- **Recherche** : embeddings `intfloat/multilingual-e5-small` + base vectorielle ChromaDB.
- **Génération** : Groq, modèle `openai/gpt-oss-120b`, température 0. Le prompt traite les articles et la question comme des données (défense contre l'injection de prompt).
- **Limite connue** : texte de 1997. Un nouveau code du travail est en cours d'application, le texte en vigueur a pu changer.

## Équipe et modules

| Membre | Module | Dossier | Branche |
|---|---|---|---|
| Massamba (tech lead) | Génération, intégration | `src/pipeline/`, `main.py` | `feature/pipeline` |
| Abdou Karim | Corpus et ingestion | `data/`, `src/ingestion/` | `feature/ingestion` |
| Haroona | Embeddings et base vectorielle | `src/retrieval/` | `feature/retrieval` |
| Sine Ndoye | Évaluation et rapport | `eval/`, `reports/` | `feature/eval` |
| Mamadou | Bonus (function calling, garde-fous, observabilité) | `src/tools/`, `src/guardrails/`, `src/observability/` | `feature/bonus` |

Le bonus n'a pas été intégré au rendu : les dossiers correspondants sont vides. Seule la défense de base contre l'injection de prompt est présente (règle 4 du prompt système, mesurée dans l'évaluation).

## Installation

Python 3.10 ou plus.

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # puis écrire sa clé : GROQ_API_KEY=...
```

Clé Groq gratuite : https://console.groq.com. Le fichier `.env` n'est jamais poussé sur GitHub.
Au premier lancement, le modèle d'embeddings est téléchargé et l'index `chroma_db/` est construit (quelques minutes). Les lancements suivants sont rapides.

## Utilisation

```bash
python main.py "Quelle est la durée du congé de maternité ?"
```

Affiche la réponse (avec les articles cités) et les passages retrouvés. Sans `GROQ_API_KEY`, seule la recherche est exécutée (réponse « [SANS LLM] »).

## Évaluation

```bash
python -m eval.evaluate              # complète (nécessite la clé Groq)
python -m eval.evaluate --sans-llm   # recherche seule, sans clé
python -m eval.evaluate --k 4
```

21 questions (`eval/sample_questions.json`) : factuelles, reformulées, hors sujet, hors corpus, injection, données personnelles. Mesures : hit@1, hit@k, MRR, fidélité et exactitude (juge LLM), respect de la règle de citation, latence.
Résultats : `eval/results/resume.md` et `eval/results/resultats.csv`. Analyse des erreurs : `reports/rapport.md`.

## Interfaces communes

```python
ingest() -> list[Chunk]                         # src/ingestion/ingest.py
retrieve(question, k) -> list[Passage]          # src/retrieval/retrieve.py
answer(question, k=4) -> {"reponse", "passages"}  # src/pipeline/answer.py
```

Types `Chunk` et `Passage` : `src/common/types.py`.

## Règles Git

Une branche par membre, aucun push direct sur `main`, une Pull Request par module relue par le tech lead, commits faits avec son propre compte GitHub.

## Documentation des modules

- Ingestion : `src/ingestion/README.md`, `data/ingestion_report.md`
- Recherche : `src/retrieval/RESULTATS.md`
- Évaluation : `eval/results/resume.md`, `reports/rapport.md`

## Sources

- République du Sénégal, Code du travail (loi n° 97-17), PDF de la bibliothèque juridique Jurisconsult / Ministère de la Justice : https://www.vie-publique.sn/documents/437/code-travail-senegal (autre copie : https://webapps.ilo.org/dyn/travail/docs/839/Code%20du%20travail.pdf).
- Modèle d'embeddings : intfloat/multilingual-e5-small. LLM : openai/gpt-oss-120b via Groq.
