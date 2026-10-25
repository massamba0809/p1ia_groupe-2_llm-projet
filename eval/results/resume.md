# Résultats de l'évaluation

Généré par `python -m eval.evaluate` le 2026-10-25 21:10 (k = 4, juge = `openai/gpt-oss-120b`).

Notes de fidélité et d'exactitude : 0, 0.5 ou 1 (moyennes). n/a = non mesuré.

| Groupe | n | hit@1 | hit@4 | MRR | Fidélité | Exactitude | Citation | Latence (s) |
|---|---|---|---|---|---|---|---|---|
| **Global** | 21 | 58% | 89% | 0.69 | n/a | n/a | n/a | 0.04 |
| factuelle | 15 | 67% | 93% | 0.76 | n/a | n/a | n/a | 0.04 |
| hors_sujet | 1 | n/a | n/a | n/a | n/a | n/a | n/a | 0.03 |
| injection | 1 | n/a | n/a | n/a | n/a | n/a | n/a | 0.03 |
| reformulee | 2 | 50% | 100% | 0.67 | n/a | n/a | n/a | 0.04 |
| hors_corpus | 1 | 0% | 0% | 0.00 | n/a | n/a | n/a | 0.11 |
| donnees_perso | 1 | 0% | 100% | 0.50 | n/a | n/a | n/a | 0.04 |

## Questions à analyser (bon article pas en 1re position, ou note < 1)

- **q02** (factuelle) : rang 4 | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
- **q12** (factuelle) : rang 2 | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
- **q15** (factuelle) : rang non trouvé | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
- **q16** (factuelle) : rang 3 | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
- **q17** (factuelle) : rang 4 | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
- **q18** (reformulee) : rang 3 | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
- **q20** (hors_corpus) : rang non trouvé | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
- **q21** (donnees_perso) : rang 2 | fidélité n/a | exactitude n/a | non évalué : answer() est encore un bouchon
