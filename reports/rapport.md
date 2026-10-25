# Rapport d'évaluation : assistant RAG sur le Code du travail du Sénégal

> Module évaluation : Sine Ndoye. Les chiffres viennent de `eval/results/resume.md`,
> généré par `python -m eval.evaluate`. Les passages entre `[À COMPLÉTER]` sont à remplir
> après le lancement sur le pipeline complet.

## 1. Méthode

### Jeu de questions (`eval/sample_questions.json`)

21 questions, chacune avec une réponse de référence vérifiée dans le texte du Code et l'article attendu.
Elles sont classées par type, pour voir **sur quel genre de question** le système échoue :

| Type | Nombre | Ce qu'on teste |
|---|---|---|
| factuelle | 15 | Questions directes, vocabulaire proche du texte de loi |
| reformulee | 2 | Langage courant, sans les mots du Code (« payer avec des sacs de riz ») |
| hors_corpus | 1 | Sujet du domaine mais réponse absente du Code (montant du SMIG) : le système ne doit pas inventer |
| hors_sujet | 1 | Question sans rapport avec le droit du travail |
| injection | 1 | Tentative de détourner les instructions du modèle |
| donnees_perso | 1 | Question contenant un nom et un numéro de téléphone |

### Métriques

| Métrique | Ce qu'elle mesure | Comment |
|---|---|---|
| hit@1, hit@k | Le bon article est-il en 1re position / parmi les k passages ? | Comparaison avec `chunk_attendu` |
| MRR | À quel rang arrive le bon article (moyenne de 1/rang) | Idem |
| Fidélité | La réponse est-elle entièrement soutenue par les passages (pas d'invention) ? | LLM juge, note 0 / 0,5 / 1 |
| Exactitude | La réponse est-elle juste par rapport à la référence (ou le bon comportement pour les pièges) ? | LLM juge, note 0 / 0,5 / 1 |
| Citation | La réponse cite-t-elle au moins un article retrouvé ? | Règle simple (recherche de « L.xx ») |
| Latence | Temps de réponse de `answer()` | Chronomètre |

**Juge :** `openai/gpt-oss-120b` via Groq, température 0, sortie JSON imposée.
(`llama-3.3-70b-versatile`, souvent cité dans les tutoriels, a été retiré par Groq le 16/08/2026.)

## 2. Résultats

[À COMPLÉTER : coller ici le tableau de `eval/results/resume.md`]

Réglages : k = 4, modèle d'embedding `intfloat/multilingual-e5-small`, LLM de génération [À COMPLÉTER].

## 3. Erreurs constatées

[À COMPLÉTER à partir de la liste « Questions à analyser » de `resume.md` et du fichier `resultats.csv`.
Pour chaque échec : la question, ce qui s'est passé, la cause probable.]

| Question | Ce qui s'est passé | Cause probable |
|---|---|---|
| q02 congé de maternité | (constaté par le module retrieval) L.144 (allaitement) passe devant L.143 | Les deux articles parlent de la mère et de l'enfant : vocabulaire très proche |
| [À COMPLÉTER] | | |

## 4. Limites de l'évaluation (lucidité)

- **Petit jeu de questions** (21) : un seul échec fait varier un score de 5 à 7 points. Les tendances sont indicatives.
- **Le juge est lui-même un LLM** : il peut se tromper ou être indulgent. Nous avons relu à la main ses commentaires sur les échecs [À CONFIRMER après relecture].
- **Une seule « bonne » réponse par question** : si un autre article répond aussi correctement, le retrieval est compté en échec à tort.
- **Questions écrites par l'équipe** : elles ressemblent sans doute plus au texte de loi que les questions de vrais utilisateurs. Les 2 questions reformulées sont un début de test, pas une mesure solide.
- **Corpus de 1997** : une réponse fidèle au corpus peut être dépassée en droit (nouveau code en cours d'adoption).

## 5. Ce que nous changerions

[À COMPLÉTER selon les résultats. Pistes possibles à garder seulement si les résultats les justifient :]

- Plus de questions reformulées en langage courant, idéalement posées par de vraies personnes.
- Ajouter un reranker si le bon article est souvent retrouvé mais pas en 1re position.
- Ajouter le titre ou chapitre dans l'embedding si des articles voisins se confondent (cas q02).
- Faire noter une partie des réponses par un humain pour vérifier que le juge LLM est fiable.

## Sources

- Code du travail du Sénégal (loi n° 97-17), voir le README pour le lien.
- Documentation Groq, modèles et dépréciations : https://console.groq.com/docs/models et https://console.groq.com/docs/deprecations
