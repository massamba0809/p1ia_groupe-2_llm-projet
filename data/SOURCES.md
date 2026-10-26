# Sources du corpus

## Document utilisé

| | |
|---|---|
| Titre | Code du travail, loi n° 97-17 du 1er décembre 1997 (République du Sénégal) |
| Éditeur de la version PDF | Bibliothèque juridique numérique JURISCONSULT / Ministère de la Justice |
| Téléchargé depuis | https://www.vie-publique.sn/documents/437/code-travail-senegal |
| Copie de référence | https://webapps.ilo.org/dyn/travail/docs/839/Code%20du%20travail.pdf (base NATLEX de l'OIT) |
| Fichier dans le dépôt | `data/code_travail_senegal.pdf` (78 pages) |
| Modifications intégrées | Loi n° 2015-04 du 12 février 2015 (articles L.49 et L.76bis) |

## Pourquoi ce corpus

- **Public** : texte de loi publié par l'État, sans donnée personnelle ni confidentielle.
- **En français**, avec des questions concrètes et vérifiables (durée du travail, congés, préavis, salaire...).
- **Bien structuré** : 289 articles numérotés (L.1 à L.288, plus L.76bis), regroupés en titres et chapitres, ce qui donne un découpage naturel et des citations précises.

## Comment citer

- Chaque chunk a un champ `source` : `Code du travail du Sénégal (loi n° 97-17), Article L.x`.
- Liste complète des articles citables : `python -m src.ingestion.ingest --sources`, ou `list_sources()` dans le code.
- Pour les sources d'une réponse : `list_sources(passages)`.

## Limites de la source

- **Version de 1997**, avec seulement la modification de 2015 visible dans le PDF. Un nouveau code du travail (projet de loi n° 15/2026) est en cours d'application : le texte en vigueur a pu changer. L'assistant répond sur la loi 97-17, pas sur le droit actuel.
- Le PDF n'est **pas une publication officielle** du Journal officiel. C'est une compilation de Jurisconsult. Il peut contenir des coquilles, par exemple « dipômé » dans L.76bis.
- Les **décrets d'application**, cités dans de nombreux articles (« fixées par décret »), ne font pas partie du corpus. L'assistant ne peut donc pas donner, par exemple, les montants fixés par décret.
- La page de garde (crédits Jurisconsult) n'est pas intégrée aux chunks.
