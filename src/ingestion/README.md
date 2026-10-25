# Module 2 : corpus et ingestion

Responsable : Abdou Karim (branche `feature/ingestion`).

Transforme le PDF du Code du travail du Sénégal en **chunks** `{id, text, source}`, utilisés par le module retrieval.
Le corpus et sa source sont décrits dans [`data/SOURCES.md`](../../data/SOURCES.md).

## Utilisation

```bash
# (re)construire les chunks et le rapport d'ingestion
python -m src.ingestion.build_chunks            # options : --max-chars 1200 --out fichier.json --check --no-report

# afficher un article, la liste des sources, ou un résumé
python -m src.ingestion.ingest L.135
python -m src.ingestion.ingest --sources
python -m src.ingestion.ingest

# comparer deux stratégies de découpage
python -m src.ingestion.compare_chunking        # options : --size 800 --overlap 150
```

Le fichier `data/code_travail_chunks.json` est versionné. Il n'est donc pas nécessaire de relancer `build_chunks` pour utiliser le projet.

## Fonctions exposées (`src/ingestion/ingest.py`)

| Fonction | Rôle |
|---|---|
| `ingest() -> list[Chunk]` | **Contrat commun** : tous les chunks du corpus |
| `chunks_by_id()` | Dictionnaire `id -> Chunk` |
| `get_article("L.115")` | Tous les morceaux d'un article (`L.115-1`, `L.115-2`) |
| `list_sources(chunks=None)` | Sources citables (une par article), pour tout le corpus ou pour des passages |
| `document_reference()` | Référence complète du document à citer |

## Étapes du pipeline

| Fichier | Étape |
|---|---|
| `extract.py` | PDF -> lignes de texte (pypdf) |
| `clean.py` | Normalisation Unicode, espaces, mots composés coupés, renvois `L 2` -> `L.2` |
| `parser.py` | Repère les articles, leur contexte (Titre > Chapitre > Section) et la loi modificative |
| `chunker.py` | Un chunk par article, coupé aux frontières de phrases au-delà de `MAX_CHARS` |
| `checks.py` | Contrôles qualité : numérotation, doublons, tailles, résidus d'extraction |
| `stats.py`, `report.py` | Chiffres du découpage et rapport `data/ingestion_report.md` |
| `config.py` | Chemins, nom du corpus, `MAX_CHARS`, référence de la source |

## Choix du découpage

**Un chunk = un article de loi.**
- Un article est l'unité de sens du texte juridique, et c'est aussi l'unité citée (« selon l'article L.135... »). Chaque passage retrouvé est donc citable tel quel.
- Chaque chunk commence par son contexte, `[TITRE IX : DU SALAIRE... > CHAPITRE II : ...]`. Un article court comme « Il est interdit à l'employeur d'infliger des amendes » (L.129) devient ainsi trouvable par le thème de son chapitre.
- Au-delà de `MAX_CHARS = 1200` caractères, l'article est coupé aux fins de phrases ou aux puces `a) b) c)`. Les morceaux s'appellent `L.115-1`, `L.115-2`... C'est le cas de 36 articles sur 289. On garde ainsi des vecteurs précis : un long article de 4 000 caractères noierait l'information.

### Chiffres (voir `data/ingestion_report.md`)

| Mesure | Valeur |
|---|---|
| Articles | 289 (L.1 à L.288 + L.76bis) |
| Chunks | 336 |
| Taille médiane / max | 647 / 1374 caractères (en-tête compris) |
| Contrôles bloquants | numérotation continue, aucun doublon, aucun résidu d'extraction |

### Comparaison avec un découpage à taille fixe

`python -m src.ingestion.compare_chunking` :

| Stratégie | Chunks | Taille médiane | Chunks mêlant plusieurs articles | Articles éparpillés sur plusieurs chunks |
|---|---|---|---|---|
| A : un chunk par article (retenue) | 336 | 647 | 0 % | 12 % |
| B : taille fixe 800, chevauchement 150 | 313 | 796 | 74 % | 85 % |
| B : taille fixe 1200, chevauchement 200 | 203 | 1195 | 87 % | 71 % |

Avec une taille fixe, 3 chunks sur 4 mélangent plusieurs articles. Un passage retrouvé ne correspond alors plus à un article précis, et le LLM risque d'attribuer une règle au mauvais article. Le découpage par article évite ce problème.

### Nettoyage appliqué, et pourquoi

| Problème constaté dans le PDF | Correction |
|---|---|
| `Article L 76 bis` écrit sans point : l'article était fusionné dans L.76 | Regex tolérante, numéro normalisé en `L.76bis` |
| Mention `(Loi 2015-04 du 12 Février 2015)` perdue | Conservée dans l'en-tête : `Article L.49 (rédaction issue de la Loi 2015-04...)` |
| Mots composés coupés en fin de ligne : `ci- dessus`, `procès- verbal` | Recollés : `ci-dessus` |
| Renvois écrits `L 2`, `L. 9`, `L7`, `L .273`, `L. «90»` | Uniformisés comme les ids : `L.2`, `L.9`... |
| Espaces doubles, espace avant la virgule, espaces insécables | Normalisés |
| Énumération `a) ... ; b) ...` de L.279 non coupée (1647 car.) | Coupure autorisée devant les puces |

## Limites connues

- **Articles très courts** (L.129, L.208, L.240, L.267 : moins de 80 caractères de texte). Ils sont signalés par les contrôles mais gardés tels quels : ce sont de vrais articles d'une phrase. Leur vecteur repose surtout sur l'en-tête de contexte.
- **Articles coupés** : une question peut porter sur la 2e partie d'un article (`L.115-2`). La réponse est alors retrouvée sans la phrase d'introduction de la 1re partie. `get_article()` permet de récupérer l'article entier.
- **Dépendance à pypdf** : deux versions de pypdf n'extraient pas exactement le même texte. La version est fixée dans `requirements.txt`, et le nettoyage rend le résultat stable.
- **Renvois** : la normalisation `L 2 -> L.2` suppose que tout « L » suivi d'un nombre est un renvoi d'article. C'est vrai dans ce corpus, mais pas forcément ailleurs.
- **Corpus daté** : loi de 1997 (voir `data/SOURCES.md`). Les décrets d'application ne sont pas inclus.

## Notes pour les autres modules

- **Retrieval** : après une mise à jour des chunks, supprimer le dossier `chroma_db/`. L'index n'est reconstruit automatiquement que si le *nombre* de chunks change, pas si leur texte change.
- **Évaluation** : les articles découpés n'ont pas d'id `L.115` mais `L.115-1`, `L.115-2`. Pour comparer un passage à un `chunk_attendu`, il faut utiliser le préfixe d'article : `checks.article_of("L.115-2") == "L.115"`.
- Les ids et le contrat `ingest() -> list[Chunk]` n'ont pas changé. Seuls changent L.76 (n'est plus coupé), le nouvel article L.76bis et le découpage de L.197 et L.279.
