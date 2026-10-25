# Rapport d'ingestion

Généré par `python -m src.ingestion.build_chunks` : ne pas modifier à la main.

- Corpus : Code du travail du Sénégal (loi n° 97-17)
- Découpage : un chunk par article, coupé au-delà de 1200 caractères

## Chiffres

| Mesure | Valeur |
|---|---|
| Articles | 289 |
| Chunks | 336 |
| Articles coupés en plusieurs chunks | 36 (max 4 morceaux) |
| Taille min / médiane / moyenne / max (car.) | 156 / 647 / 699 / 1374 |
| Mots au total | 37025 |

## Chunks par titre

| Titre | Chunks |
|---|---|
| TITRE PREMIER : DISPOSITIONS GENERALES | 5 |
| TITRE II : DES SYNDICATS PROFESSIONNELS | 27 |
| TITRE III : DU CONTRAT DE TRAVAIL | 48 |
| TITRE IV : DE L'APPRENTISSAGE, DE LA FORMATION PROFESSIONNELLE ET DU STAGE | 5 |
| TITRE V : DU TACHERONNAT | 4 |
| TITRE VI : DE LA CONVENTION ET DES ACCORDS COLLECTIFS DE TRAVAIL | 25 |
| TITRE VII : DU REGLEMENT INTERIEUR | 1 |
| TITRE VIII : DU CAUTIONNEMENT | 4 |
| TITRE IX : DU SALAIRE ET DE SES ACCESSOIRES | 35 |
| TITRE X : DES CONDITIONS DU TRAVAIL | 35 |
| TITRE XI : HYGIENE ET SECURITE | 23 |
| TITRE XII : DES ORGANISMES ET DES MOYENS D'EXECUTION | 52 |
| TITRE XIII : DES DIFFERENDS DU TRAVAIL | 57 |
| TITRE XIV : PENALITES | 13 |
| TITRE XV : DISPOSITIONS TRANSITOIRES | 2 |

## Contrôles qualité

- **numérotation** : OK
- **doublons** : OK
- **tailles** : 4 signalement(s)
  - chunk court (53 car.) : L.129
  - chunk court (71 car.) : L.208
  - chunk court (58 car.) : L.240
  - chunk court (78 car.) : L.267
- **résidus d'extraction** : OK
