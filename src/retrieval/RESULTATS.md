# Retrieval : choix du modèle d'embedding et comparaison de 2 réglages

## Fonctionnement

- Chaque chunk (un article du Code du travail) est transformé en vecteur par un modèle d'embedding.
- Les vecteurs sont stockés dans une base **ChromaDB** sur disque (`chroma_db/`, non versionnée), avec la similarité cosinus.
- `retrieve(question, k)` transforme la question en vecteur et renvoie les `k` articles les plus proches avec leur score (1 = identique).
- L'index est construit automatiquement au premier appel, puis réutilisé. Il est reconstruit si le nombre de chunks change.

## Pourquoi ces outils

- **sentence-transformers** : modèles gratuits, utilisables hors ligne sur CPU, sans clé API.
- **ChromaDB** : base vectorielle simple à installer (`pip`), qui garde l'index sur disque.
- Des modèles **multilingues**, car le corpus et les questions sont en français.

## Les 2 réglages comparés

| Réglage | Modèle | Particularité |
|---|---|---|
| A | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Très léger, rapide |
| B | `intfloat/multilingual-e5-small` | Entraîné pour la recherche ; préfixes `query:` / `passage:` |

Relancer la comparaison : `python -m src.retrieval.compare`

## Résultats (k = 4, 6 questions de `eval/sample_questions.json` ayant un article attendu)

| Modèle | hit@1 | hit@4 | MRR |
|---|---|---|---|
| A : MiniLM | 0.33 | 0.83 | 0.58 |
| B : e5-small | **0.83** | **1.00** | **0.88** |

Rang du bon article pour chaque question :

| Question | Attendu | MiniLM | e5 |
|---|---|---|---|
| q01 durée légale du travail | L.135 | 2 | 1 |
| q02 congé de maternité | L.143 | 2 | 4 |
| q03 jours de congé par mois | L.148 | non trouvé | 1 |
| q04 durée max. de l'essai | L.38 | 1 | 1 |
| q05 rupture de l'essai | L.40 | 2 | 1 |
| q06 travail forcé | L.4 | 1 | 1 |

**Choix : e5-small** (modèle par défaut dans `retrieve.py`).

## Limites constatées

- **Seulement 6 questions** : l'écart est net, mais il faudra confirmer avec le jeu complet d'environ 20 questions. Le script le relira automatiquement.
- **Congé de maternité (q02)** : avec les deux modèles, l'article L.144 (repos pour allaitement) passe devant L.143, car les deux parlent de la mère et de l'enfant. Avec e5, L.143 n'arrive qu'au 4e rang : avec `k < 4`, il serait perdu.
- **Scores e5 très resserrés** (par exemple 0,86 à 0,88 entre les 4 premiers) : le score ne permet pas de fixer un seuil fiable pour détecter une question hors sujet.
- **Temps** : au premier lancement, e5 met environ 13 min (téléchargement du modèle et indexation sur CPU). Ensuite, chaque lancement prend environ 30 s, surtout pour charger PyTorch et le modèle.
- Un article long est découpé en plusieurs morceaux (`L.xx-1`, `L.xx-2`). Le script compte un morceau comme une bonne réponse.
