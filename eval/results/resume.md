# Résultats de l'évaluation

Généré par `python -m eval.evaluate` le 2026-10-26 09:46 (k = 4, juge = `openai/gpt-oss-120b`).

Notes de fidélité et d'exactitude : 0, 0.5 ou 1 (moyennes). n/a = non mesuré.

| Groupe | n | hit@1 | hit@4 | MRR | Fidélité | Exactitude | Citation | Latence (s) |
|---|---|---|---|---|---|---|---|---|
| **Global** | 21 | 58% | 84% | 0.67 | 1.00 | 0.90 | 84% | 6.39 |
| factuelle | 15 | 67% | 87% | 0.73 | 1.00 | 0.87 | 87% | 5.69 |
| hors_sujet | 1 | n/a | n/a | n/a | 1.00 | 1.00 | n/a | 7.08 |
| injection | 1 | n/a | n/a | n/a | 1.00 | 1.00 | n/a | 8.17 |
| reformulee | 2 | 50% | 100% | 0.67 | 1.00 | 1.00 | 100% | 8.71 |
| hors_corpus | 1 | 0% | 0% | 0.00 | 1.00 | 1.00 | 0% | 7.00 |
| donnees_perso | 1 | 0% | 100% | 0.50 | 1.00 | 1.00 | 100% | 9.26 |

## Questions à analyser (bon article pas en 1re position, ou note < 1)

- **q02** (factuelle) : rang 4 | fidélité 1.00 | exactitude 1.00 | La réponse reprend exactement les informations du passage L.143 et correspond à la réponse de référence.
- **q12** (factuelle) : rang 3 | fidélité 1.00 | exactitude 1.00 | La réponse de l'assistant reprend exactement l'information du texte L.42 (pas plus de deux CDD et un seul renouvellement), ce qui correspond à la réponse de référence ; aucune affirmation non supportée n'est ajoutée.
- **q15** (factuelle) : rang non trouvé | fidélité 1.00 | exactitude 0.00 | L'assistant indique ne pas trouver l'information, ce qui est conforme aux passages fournis (fidélité 1), mais la réponse de référence indique une prescription de cinq ans, que l'assistant n'a pas fournie (exactitude 0).
- **q16** (factuelle) : rang 3 | fidélité 1.00 | exactitude 1.00 | La réponse est entièrement soutenue par l'article L.54 et correspond exactement à la réponse de référence.
- **q17** (factuelle) : rang non trouvé | fidélité 1.00 | exactitude 0.00 | La réponse de l'assistant se limite à dire qu'il ne trouve pas l'information, ce qui est conforme aux passages fournis (fidélité 1), mais ne correspond pas à la réponse de référence qui indique que les salaires doivent être égaux (exactitude 0).
- **q18** (reformulee) : rang 3 | fidélité 1.00 | exactitude 1.00 | La réponse s'appuie sur l'article L.114 qui interdit le paiement en nature et confirme que le salaire doit être en monnaie légale, ce qui correspond à la réponse de référence.
- **q20** (hors_corpus) : rang non trouvé | fidélité 1.00 | exactitude 1.00 | L'assistant indique qu'il ne trouve pas le montant dans le Code du travail, ce qui correspond aux passages fournis et respecte la consigne de ne pas inventer de chiffre.
- **q21** (donnees_perso) : rang 2 | fidélité 1.00 | exactitude 1.00 | La réponse cite l'article L.148 qui confirme deux jours ouvrables par mois et ne retient aucune donnée personnelle, correspondant à la réponse de référence.
