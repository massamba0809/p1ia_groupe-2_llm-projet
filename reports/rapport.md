# Rapport d'évaluation : assistant RAG sur le Code du travail du Sénégal

> Module évaluation : Sine Ndoye. Les chiffres viennent de `eval/results/resume.md` et `eval/results/resultats.csv`,
> générés par `python -m eval.evaluate` (k = 4, modèle d'embedding `intfloat/multilingual-e5-small`).
> Les passages entre `[À COMPLÉTER]` dépendent de la génération (LLM), qui n'était pas branchée lors du premier lancement.

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

Les métriques de retrieval ne portent que sur les 19 questions qui ont un article attendu (q07 et q08 n'en ont pas).

**Juge :** `openai/gpt-oss-120b` via Groq, température 0, sortie JSON imposée.
(`llama-3.3-70b-versatile`, souvent cité dans les tutoriels, a été retiré par Groq le 16/08/2026.)

**Contrôle du script :** sur les 6 premières questions (q01 à q06), notre script donne les mêmes chiffres que
le module retrieval (`src/retrieval/RESULTATS.md`) : hit@1 = 5/6, hit@4 = 6/6, MRR = 0,88, avec L.143 au rang 4 pour q02.

## 2. Résultats

### 2.1 Retrieval (mesuré)

| Groupe | n | hit@1 | hit@4 | MRR |
|---|---|---|---|---|
| **Global** | 19 | 58 % (11/19) | 89 % (17/19) | 0,69 |
| Global sans q20 (voir limites) | 18 | 61 % (11/18) | 94 % (17/18) | 0,73 |
| factuelle | 15 | 67 % | 93 % | 0,76 |
| reformulee | 2 | 50 % | 100 % | 0,67 |
| hors_corpus (q20) | 1 | 0 % | 0 % | 0,00 |
| donnees_perso (q21) | 1 | 0 % | 100 % | 0,50 |

Onze questions ont le bon article en 1re position (q01, q03, q04, q05, q06, q09, q10, q11, q13, q14, q19).
Rang observé pour les huit autres :

| Question | Article attendu | Rang |
|---|---|---|
| q02 congé de maternité | L.143 | 4 |
| q12 nombre de CDD | L.42 | 2 |
| q15 délai pour réclamer un salaire | L.126 | non trouvé |
| q16 rupture sans préavis | L.54 | 3 |
| q17 égalité de salaire | L.105 | 4 |
| q18 salaire en sacs de riz | L.114 | 3 |
| q20 montant du SMIG | L.109 | non trouvé |
| q21 congés avec données personnelles | L.148 | 2 |

**Effet du nombre de passages k** (calculé à partir des rangs ci-dessus) : hit@4 = 89 %, hit@3 = 79 %, hit@2 = 68 %.
Réduire k à 3 ferait perdre q02 et q17.

### 2.2 Génération : fidélité et exactitude

[À COMPLÉTER : coller la ligne « Global » et les lignes par type de `eval/results/resume.md` après avoir relancé
`python -m eval.evaluate` avec le LLM branché. LLM de génération utilisé : [À COMPLÉTER].]

## 3. Erreurs constatées (retrieval)

Pour chaque échec, nous avons lu le texte des articles qui ont pris la place du bon (colonne `passages_retrouves` de `resultats.csv`).

| Question | Ce qui s'est passé | Cause constatée dans le texte du Code |
|---|---|---|
| q02 congé de maternité | L.143 au rang 4, derrière L.144, L.148, L.141 | Le mot « maternité » n'apparaît nulle part dans le Code : L.143 dit « accouchement » et « suspendre son travail ». Les articles voisins sur les mères (allaitement L.144, repos des femmes L.141, congé des mères de famille L.148) ressemblent davantage à la question. |
| q12 nombre de CDD | L.42 au rang 2, derrière L.41 | L.41 définit le CDD, L.42 pose la limite de deux contrats. Les deux contiennent « durée déterminée » : deux articles voisins presque interchangeables pour le modèle. |
| q15 délai pour réclamer un salaire | L.126 non trouvé (retrouvés : L.115-2, L.116-4, L.241-1, L.127) | La question dit « délai » et « réclamer » ; L.126 ne contient aucun de ces mots (il dit « action en paiement » et « se prescrivent par cinq ans »). L.116-4 contient « délai » (de paiement) et passe devant. L.127, de la même section « prescription », arrive 4e : bon sujet, mais l'article qui contient la réponse (« cinq ans ») est L.126. |
| q16 rupture sans préavis | L.54 au rang 3, derrière L.50 et L.53 | Quatre articles de la même section parlent du préavis ; L.53 contient « sans préavis » presque mot pour mot. L.54 est le seul à dire « faute lourde », terme absent de la question. |
| q17 égalité de salaire | L.105 au rang 4, derrière L.249, L.116-4, L.10 | La question dit « femme » et « homme » ; L.105 dit « sexe » et non « femme ». Deux articles sur la « femme mariée » (L.249 tribunal du travail, L.10 syndicats), sans rapport avec le salaire, passent devant : le modèle s'accroche au mot « femme ». |
| q18 salaire en sacs de riz | L.114 au rang 3, derrière L.116-4 et L.117 | Question en langage courant (« patron », « sacs de riz ») ; le Code parle de salaire « payé en nature ». Les articles sur le paiement du salaire en général passent devant. L.107 (« denrées alimentaires ») arrive 4e, attiré par « riz ». |
| q20 montant du SMIG | L.109 non trouvé | Voir limites : question piège, ce n'est pas un vrai échec de retrieval. Le sigle « SMIG » n'est pas dans le Code, L.109 dit « salaires minima interprofessionnels garantis ». |
| q21 congés avec données personnelles | L.148 au rang 2, derrière L.149-1 | La question contient un nom et un numéro de téléphone. La question équivalente sans données personnelles (q03) a L.148 au rang 1. Les deux formulations diffèrent aussi légèrement, l'effet des données personnelles n'est donc pas isolé. |

**Constat général :** sur les 7 questions où le bon article n'est pas en 1re position (hors q20), 4 viennent d'un **écart de vocabulaire** entre la question (« maternité », « réclamer », « femme », « riz ») et le texte de loi (« accouchement », « prescription », « sexe », « en nature ») : q02, q15, q17, q18. Deux viennent d'**articles voisins** quasi identiques : q12 et q16. La dernière, q21, concerne les données personnelles.

[À COMPLÉTER après relance avec le LLM : erreurs de génération (réponses infidèles, refus à tort, injection mal gérée, données personnelles répétées), à partir de la colonne `commentaire_juge`.]

## 4. Limites de l'évaluation

- **Petit jeu de questions** (21, dont 19 pour le retrieval) : un seul échec fait varier un score de 5 points. Les tendances sont indicatives.
- **Un seul article attendu par question** : c'est strict. En q12 et q16, les articles qui passent devant sont aussi pertinents ; en q15, L.127 traite du bon sujet. Le retrieval est parfois sous-estimé.
- **q20 (SMIG) mesure deux choses à la fois.** Nous avons attendu L.109 (« les décrets fixent les salaires minima »), mais le bon comportement du système est de dire que le Code ne donne pas de montant. Nous présentons donc les scores avec et sans q20.
- **q21 n'isole pas l'effet des données personnelles** : sa formulation diffère de q03. Un test propre utiliserait exactement la même question, avec et sans nom et téléphone.
- **Le juge est lui-même un LLM** : il peut se tromper ou être indulgent. [À CONFIRMER : relecture manuelle de ses commentaires sur les échecs.]
- **Questions écrites par l'équipe** : elles ressemblent sans doute plus au texte de loi que celles de vrais utilisateurs. Seules 2 questions sont en langage courant.
- **Corpus de 1997** : une réponse fidèle au corpus peut être dépassée en droit (nouveau code en cours d'adoption).

## 5. Ce que nous changerions

Ces pistes découlent des échecs observés ; **aucune n'a encore été testée**.

1. **Garder k = 4 au minimum** : avec k = 3, hit@k tombe à 79 % (calcul sur nos rangs).
2. **Reformuler la question avec le vocabulaire du Code avant la recherche** (par exemple « maternité » vers « accouchement », « réclamer un salaire » vers « prescription de l'action en paiement »). Cela viserait q02, q15, q17 et q18.
3. **Ajouter un reranker** pour départager les articles voisins (q12, q16).
4. **Masquer les données personnelles avant la recherche** (garde-fou du module bonus) et vérifier l'effet avec une paire de questions strictement identiques.
5. **Ne pas fixer de seuil sur le score pour détecter le hors-sujet** : les scores e5 sont très resserrés (voir `src/retrieval/RESULTATS.md`). Laisser le LLM refuser quand les passages ne répondent pas.
6. **Plus de questions en langage courant**, idéalement posées par de vraies personnes, et une partie des réponses notées par un humain pour valider le juge.

## Sources

- Code du travail du Sénégal (loi n° 97-17), voir le README pour le lien.
- Résultats du module retrieval : `src/retrieval/RESULTATS.md`.
- Documentation Groq, modèles et dépréciations : https://console.groq.com/docs/models et https://console.groq.com/docs/deprecations
